# -*- coding: utf-8 -*-
"""Learned and zero-shot embedding baselines on the same problem-grouped splits.

  unixcoder_cos        zero-shot cosine of UniXcoder embeddings, validation-tuned threshold
  codebert_siamese     MLP head over [|e1-e2|, e1*e2] of frozen CodeBERT embeddings (mean of window embeddings),
                       trained on the training split (no encoder fine-tuning)
  unixcoder_siamese    same head over frozen UniXcoder embeddings

REGIME=A|B|C python -I eval_embedding_baselines.py -> results_<R>/embedding_baselines.json
"""
import json
import os
import pickle
import sys

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE  # noqa: E402
from exp_lib import REGIME, SEEDS, load, metrics, tune_threshold  # noqa: E402

RES = os.path.join(HERE, "results_" + REGIME)
D = load()
tr, va, te = D["train"], D["val"], D["test"]
F = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
U = np.load(os.path.join(DATA, "unixcoder_emb.npz"))
UK, UE = U["keys"], U["emb"]
uidx = {k: i for i, k in enumerate(UK)}
EMB = {
    "codebert": lambda k: F[k]["win"].mean(0),
    "unixcoder": lambda k: UE[uidx[k]],
}


def pair_mat(df, name):
    f = EMB[name]
    a = np.vstack([f(k) for k in df.key1]).astype(np.float32)
    b = np.vstack([f(k) for k in df.key2]).astype(np.float32)
    a /= np.clip(np.linalg.norm(a, axis=1, keepdims=True), 1e-9, None)
    b /= np.clip(np.linalg.norm(b, axis=1, keepdims=True), 1e-9, None)
    return a, b


def head_features(a, b):
    return np.hstack([np.abs(a - b), a * b])


def train_head(Xtr, ytr, Xva, yva, seed):
    torch.manual_seed(seed)
    m = nn.Sequential(nn.Linear(Xtr.shape[1], 64), nn.ReLU(), nn.Dropout(0.3), nn.Linear(64, 1))
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3, weight_decay=1e-5)
    lf = nn.BCEWithLogitsLoss()
    Xt, yt = torch.tensor(Xtr), torch.tensor(ytr, dtype=torch.float32).unsqueeze(1)
    Xv, yv = torch.tensor(Xva), torch.tensor(yva, dtype=torch.float32).unsqueeze(1)
    best, state, bad = 1e9, None, 0
    for ep in range(100):
        m.train()
        perm = torch.randperm(len(Xt))
        for i in range(0, len(perm), 32):
            j = perm[i:i + 32]
            loss = lf(m(Xt[j]), yt[j])
            opt.zero_grad(); loss.backward(); opt.step()
        m.eval()
        with torch.no_grad():
            vl = lf(m(Xv), yv).item()
        if vl < best - 1e-5:
            best, bad, state = vl, 0, {k: v.clone() for k, v in m.state_dict().items()}
        else:
            bad += 1
            if bad >= 10:
                break
    m.load_state_dict(state)
    m.eval()
    return m


def slices(p, df):
    out = {}
    for s in ("exact", "renamed", "refactored", "cross-language"):
        msk = (df.slice == s).values
        out[s] = float(p[msk].mean())
    return out


out = {}
ytr, yva, yte = tr.label.values, va.label.values, te.label.values
for name in ("codebert", "unixcoder"):
    atr, btr = pair_mat(tr, name)
    ava, bva = pair_mat(va, name)
    ate, bte = pair_mat(te, name)
    if name == "unixcoder":
        sv, st = (ava * bva).sum(1), (ate * bte).sum(1)
        thr = tune_threshold(np.clip((sv + 1) / 2, 0, 1), yva)
        p = ((st + 1) / 2 >= thr).astype(int)
        m = metrics(yte, p)
        m["slices"] = slices(p, te)
        out["unixcoder_cos"] = {k: [v, 0.0] if not isinstance(v, dict) else v for k, v in m.items()}
    Xtr, Xva, Xte = head_features(atr, btr), head_features(ava, bva), head_features(ate, bte)
    runs = []
    for s in SEEDS:
        h = train_head(Xtr, ytr, Xva, yva, s)
        with torch.no_grad():
            pv = torch.sigmoid(h(torch.tensor(Xva))).numpy().ravel()
            pt = torch.sigmoid(h(torch.tensor(Xte))).numpy().ravel()
        p = (pt >= tune_threshold(pv, yva)).astype(int)
        m = metrics(yte, p)
        m["slices"] = slices(p, te)
        runs.append(m)
    agg = {}
    for k in runs[0]:
        if k == "slices":
            agg[k] = {s: float(np.mean([r[k][s] for r in runs])) for s in runs[0][k]}
        else:
            v = np.array([r[k] for r in runs], float)
            agg[k] = [float(v.mean()), float(v.std(ddof=1))]
    out[name + "_siamese"] = agg
json.dump(out, open(os.path.join(RES, "embedding_baselines.json"), "w"), indent=1)
for k, v in out.items():
    print(REGIME, k, {a: round(v[a][0] * 100, 1) for a in ("acc", "precision", "recall", "specificity", "f1")})
