# -*- coding: utf-8 -*-
"""E3: encoder control. Is the UniXcoder advantage an encoder effect or a pooling / normalisation effect?

Zero-shot cosine (validation-tuned threshold) and a frozen-embedding siamese head, for
  encoders / pooling : cb_first   CodeBERT, mean-pooled first 512-token window
                       cb_top3    CodeBERT, all windows, symmetric top-3 window cosine (the paper's expert)
                       ux_first   UniXcoder, mean-pooled first 512 tokens
  normalisation      : none      raw embeddings (cb_top3 'paper' = additionally centred per snippet across its windows, as in the expert)
                       center    subtract the mean embedding of the training-split snippets
                       whiten    centre + ZCA whitening fitted on the training-split snippets
Reported: F1 / AUROC on the test partition of the regime, and the mean cosine of random independent test pairs (anisotropy).
UniXcoder was embedded only over the first 512 tokens, so a windowed UniXcoder variant is not part of the design.

REGIME=A|B|C python -I e3_encoder_control.py -> results_<R>/e3_encoder.json
"""
import json
import os
import pickle
import sys

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import roc_auc_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE  # noqa: E402
from exp_lib import REGIME, TAG, load, metrics  # noqa: E402

assert TAG == REGIME
RES = os.path.join(HERE, "results_" + REGIME)
D = load()
tr, va, te = D["train"], D["val"], D["test"]
F = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
U = np.load(os.path.join(DATA, "unixcoder_emb.npz"))
_E, _K = U["emb"], U["keys"]
UX = {k: _E[i] for i, k in enumerate(_K)}
train_keys = sorted(set(tr.key1) | set(tr.key2))


def f1_of(y, p):
    tp = ((p == 1) & (y == 1)).sum()
    return 2 * tp / max(2 * tp + ((p == 1) & (y == 0)).sum() + ((p == 0) & (y == 1)).sum(), 1)


def tune(s, y):
    cand = np.unique(np.quantile(s, np.linspace(0.01, 0.99, 197)))
    best, bt = -1, cand[0]
    for t in cand:
        f = f1_of(y, (s >= t).astype(int))
        if f > best + 1e-12:
            best, bt = f, t
    return bt


def transform_fit(X, kind):
    mu = X.mean(0)
    if kind == "none":
        return lambda Z: Z
    if kind == "center":
        return lambda Z: Z - mu
    C = np.cov((X - mu).T)
    w, V = np.linalg.eigh(C)
    eps = 1e-3 * w.mean()
    Wm = V @ np.diag(1.0 / np.sqrt(np.maximum(w, 0) + eps)) @ V.T
    return lambda Z: (Z - mu) @ Wm


def l2(Z):
    return Z / np.clip(np.linalg.norm(Z, axis=-1, keepdims=True), 1e-9, None)


def top3(a, b):
    sim = np.clip(a @ b.T, -1, 1)
    k = max(1, min(3, sim.shape[0], sim.shape[1]))
    row = np.mean(np.mean(np.partition(sim, -k, axis=1)[:, -k:], axis=1))
    col = np.mean(np.mean(np.partition(sim, -k, axis=0)[-k:, :], axis=0))
    return 0.5 * (row + col)


def head(Xtr, ytr, Xva, yva, seed):
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
            opt.zero_grad()
            loss.backward()
            opt.step()
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


def embed(enc, keys):
    if enc == "ux_first":
        return {k: UX[k] for k in keys}
    return {k: F[k]["win"][0] for k in keys}


yv, yt = va.label.values, te.label.values
neg_test = te[(te.label == 0)]
rand_neg = neg_test[neg_test.slice == "independent"] if (neg_test.slice == "independent").any() else neg_test
out = {}
torch.set_num_threads(4)
for enc in ("cb_first", "cb_top3", "ux_first"):
    for norm in (("none", "paper", "center", "whiten") if enc == "cb_top3" else ("none", "center", "whiten")):
        r = {}
        if enc == "cb_top3":
            if norm == "paper":
                from compute_pair_features import sem
                cos = lambda df: np.array([sem(F[a], F[b]) for a, b in zip(df.key1, df.key2)])
            else:
                allw = np.vstack([F[k]["win"] for k in train_keys])
                T = transform_fit(allw, "none" if norm == "none" else norm)
                cache = {}

                def getw(k):
                    if k not in cache:
                        cache[k] = l2(T(F[k]["win"]))
                    return cache[k]
                cos = lambda df: np.array([top3(getw(a), getw(b)) for a, b in zip(df.key1, df.key2)])
            sv, st = cos(va), cos(te)
            r["rand_cos"] = float(cos(rand_neg).mean())
        else:
            keys = sorted(set(tr.key1) | set(tr.key2) | set(va.key1) | set(va.key2) | set(te.key1) | set(te.key2))
            E = embed(enc, keys)
            T = transform_fit(np.vstack([E[k] for k in train_keys]), norm)
            En = {k: l2(T(E[k][None]))[0] for k in keys}
            cos = lambda df: np.array([float(En[a] @ En[b]) for a, b in zip(df.key1, df.key2)])
            sv, st = cos(va), cos(te)
            r["rand_cos"] = float(cos(rand_neg).mean())
            # siamese head on the normalised frozen embeddings
            hf = lambda df: np.hstack([np.abs(np.vstack([En[k] for k in df.key1]) - np.vstack([En[k] for k in df.key2])),
                                       np.vstack([En[k] for k in df.key1]) * np.vstack([En[k] for k in df.key2])]).astype(np.float32)
            Xtr_, Xva_, Xte_ = hf(tr), hf(va), hf(te)
            runs = []
            for s in range(3):
                h = head(Xtr_, tr.label.values, Xva_, yv, s)
                with torch.no_grad():
                    pv = torch.sigmoid(h(torch.tensor(Xva_))).numpy().ravel()
                    pt = torch.sigmoid(h(torch.tensor(Xte_))).numpy().ravel()
                thr = tune(pv, yv)
                runs.append((f1_of(yt, (pt >= thr).astype(int)), float(roc_auc_score(yt, pt))))
            r["siamese_f1"] = float(np.mean([x[0] for x in runs]))
            r["siamese_auc"] = float(np.mean([x[1] for x in runs]))
        thr = tune(sv, yv)
        r["cos_f1"] = float(f1_of(yt, (st >= thr).astype(int)))
        r["cos_auc"] = float(roc_auc_score(yt, st))
        out["%s|%s" % (enc, norm)] = r
        print(REGIME, enc, norm, {k: round(v, 3) for k, v in r.items()}, flush=True)
json.dump(out, open(os.path.join(RES, "e3_encoder.json"), "w"), indent=1)
