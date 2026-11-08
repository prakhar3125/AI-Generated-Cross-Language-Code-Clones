# -*- coding: utf-8 -*-
"""Training and scoring code shared by every experiment on the problem-grouped protocol."""
import os
import sys

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.linear_model import LogisticRegression

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA  # noqa: E402

X6 = ["S_CodeBERT", "S_AST", "S_Token", "D_lang", "S_CodeBERT_minus_S_AST", "one_minus_S_AST"]
X4 = ["S_CodeBERT", "S_AST", "S_Token", "D_lang"]
SC = ["S_CodeBERT", "S_AST", "S_Token"]
SEEDS = list(range(8))
THR_GRID = np.arange(0.02, 0.99, 0.005)


REGIME = os.environ.get("REGIME", "A")          # A: random independent negatives, B: hard negatives
NEG_SLICE = {"A": "independent", "B": "hard_independent", "C": "tfidf_independent"}[REGIME]


SEM = os.environ.get("SEM", "cb")                 # cb: frozen CodeBERT semantic expert; ux: UniXcoder cosine
FUSION = os.environ.get("FUSION", "mean")         # mean: weighted mean of the scores (first submission); logit: weighted mean of logits + learned scale/bias
TAG = REGIME + {"ux": "ux", "wh": "wh"}.get(SEM, "") + ("lo" if FUSION == "logit" else "")
EPS_LOGIT = 0.01


def load():
    df = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
    if SEM == "ux":
        U = np.load(os.path.join(DATA, "unixcoder_emb.npz"))
        keys, emb = U["keys"], U["emb"]
        emb = emb / np.clip(np.linalg.norm(emb, axis=1, keepdims=True), 1e-9, None)
        idx = {k: i for i, k in enumerate(keys)}
        a = emb[[idx[k] for k in df.key1]]
        b = emb[[idx[k] for k in df.key2]]
        df["S_CodeBERT"] = np.clip((a * b).sum(1), 0.0, 1.0)
        df["S_CodeBERT_minus_S_AST"] = (df["S_CodeBERT"] - df["S_AST"]).abs()
    if SEM == "wh":
        w = pd.read_csv(os.path.join(DATA, "sem_whiten.csv")).drop_duplicates("pair_id").set_index("pair_id").S_sem_w
        df["S_CodeBERT"] = df.pair_id.map(w).fillna(0.0).clip(0.0, 1.0).values
        df["S_CodeBERT_minus_S_AST"] = (df["S_CodeBERT"] - df["S_AST"]).abs()
    df = df[~df.slice.isin({"independent", "hard_independent", "tfidf_independent"} - {NEG_SLICE})]
    return {sp: df[df.split == sp].reset_index(drop=True) for sp in ("train", "val", "test", "aux")}


# --------------------------------------------------------------------------- models
class _Trunk(nn.Sequential):
    """The 6-16-8-k MLP; with FUSION=logit it also carries the two scalars of the log-odds fusion (tau = softplus(rho), b)."""
    def __init__(self, nin, nout, drop=0.3):
        super().__init__(nn.Linear(nin, 16), nn.ReLU(), nn.Dropout(drop), nn.Linear(16, 8), nn.ReLU(), nn.Dropout(drop), nn.Linear(8, nout))
        self.raw_tau = nn.Parameter(torch.tensor(0.5413))      # softplus(0.5413) = 1.0
        self.b = nn.Parameter(torch.tensor(0.0))


def trunk(nin, nout, drop=0.3):
    return _Trunk(nin, nout, drop)


def _logit_fuse(model, w, s):
    sc = s.clamp(EPS_LOGIT, 1 - EPS_LOGIT)
    z = (w * torch.log(sc / (1 - sc))).sum(1, keepdim=True)
    return torch.sigmoid(nn.functional.softplus(model.raw_tau) * z + model.b)


def fused(model, x, s, routing, mask=None):
    z = model(x)
    if routing:
        if mask is not None:
            keep = torch.zeros_like(z, dtype=torch.bool)
            keep[:, mask] = True
            z = torch.where(keep, z, torch.full_like(z, float("-inf")))
        w = torch.softmax(z, dim=-1)
        if FUSION == "logit":
            return _logit_fuse(model, w, s), w
        return (w * s).sum(1, keepdim=True), w
    return torch.sigmoid(z), None


def train_model(Xtr, Str, ytr, Xva, Sva, yva, seed, routing=True, lr=1e-3, bs=32,
                max_epochs=100, patience=10, nin=6):
    """AdamW(weight decay 1e-5), BCE on the fused score, early stopping on validation BCE."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    model = trunk(nin, 3 if routing else 1)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-5)
    lf = nn.BCELoss()
    Xt, St = torch.tensor(Xtr, dtype=torch.float32), torch.tensor(Str, dtype=torch.float32)
    yt = torch.tensor(ytr, dtype=torch.float32).unsqueeze(1)
    Xv, Sv = torch.tensor(Xva, dtype=torch.float32), torch.tensor(Sva, dtype=torch.float32)
    yv = torch.tensor(yva, dtype=torch.float32).unsqueeze(1)
    best, best_state, bad = float("inf"), None, 0
    g = torch.Generator().manual_seed(seed)
    for ep in range(max_epochs):
        model.train()
        perm = torch.randperm(len(Xt), generator=g)
        for b in range(0, len(perm), bs):
            j = perm[b:b + bs]
            out, _ = fused(model, Xt[j], St[j], routing)
            loss = lf(out.clamp(1e-6, 1 - 1e-6), yt[j])
            opt.zero_grad()
            loss.backward()
            opt.step()
        model.eval()
        with torch.no_grad():
            ov, _ = fused(model, Xv, Sv, routing)
            vl = lf(ov.clamp(1e-6, 1 - 1e-6), yv).item()
        if vl < best - 1e-5:
            best, bad = vl, 0
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
        else:
            bad += 1
            if bad >= patience:
                break
    model.load_state_dict(best_state)
    model.eval()
    return model, best, ep + 1


@torch.no_grad()
def score(model, X, S, routing=True, mask=None):
    out, w = fused(model, torch.tensor(X, dtype=torch.float32), torch.tensor(S, dtype=torch.float32),
                   routing, mask)
    return out.numpy().ravel(), (w.numpy() if w is not None else None)


# --------------------------------------------------------------------------- decision rules
def f1_of(y, p):
    tp = int(((y == 1) & (p == 1)).sum())
    fp = int(((y == 0) & (p == 1)).sum())
    fn = int(((y == 1) & (p == 0)).sum())
    return 2 * tp / max(2 * tp + fp + fn, 1)


def tune_threshold(sv, yv):
    """Threshold maximising validation F1 (ties -> the lowest)."""
    best, bt = -1.0, 0.5
    for t in THR_GRID:
        f = f1_of(yv, (sv >= t).astype(int))
        if f > best + 1e-12:
            best, bt = f, t
    return float(bt)


def adaptive_thresholds(sv, yv, dlv, ccv, dlt, cct, k_simple=1.8, k_complex=1.2, cc_cut=5,
                        lo=0.40, hi=0.80, min_n=30):
    """Per-pair adaptive threshold  T = clamp(mu + k * sigma, lo, hi)  (Eq. 12 of the paper).

    mu / sigma are the mean / standard deviation of the fused scores of the
    *validation-partition independent pairs* -- the benchmark's stand-in for the
    "original submissions" of an assignment -- inside the pair's stratum (language
    relation D_lang x complexity class).  A stratum with fewer than `min_n` validation
    negatives falls back to all validation negatives.  k = k_simple when the
    reference snippet has cyclomatic complexity <= cc_cut, else k_complex.
    No test label or test score is used.
    """
    neg = yv == 0
    allm, alls = sv[neg].mean(), sv[neg].std(ddof=1)
    stats = {}
    for dl in (0, 1):
        for simple in (True, False):
            sel = neg & (dlv == dl) & ((ccv <= cc_cut) == simple)
            stats[(dl, simple)] = (sv[sel].mean(), sv[sel].std(ddof=1)) if sel.sum() >= min_n else (allm, alls)
    T = np.empty(len(dlt))
    for i in range(len(dlt)):
        simple = bool(cct[i] <= cc_cut)
        mu, sd = stats[(int(dlt[i]), simple)]
        T[i] = min(hi, max(lo, mu + (k_simple if simple else k_complex) * sd))
    return T


def metrics(y, p):
    y, p = np.asarray(y), np.asarray(p)
    tp = int(((y == 1) & (p == 1)).sum())
    fp = int(((y == 0) & (p == 1)).sum())
    fn = int(((y == 1) & (p == 0)).sum())
    tn = int(((y == 0) & (p == 0)).sum())
    n = len(y)
    prec = tp / max(tp + fp, 1)
    rec = tp / max(tp + fn, 1)
    spec = tn / max(tn + fp, 1)
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, acc=(tp + tn) / n, precision=prec, recall=rec,
                specificity=spec, fpr=1 - spec, f1=2 * prec * rec / max(prec + rec, 1e-12))


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))
