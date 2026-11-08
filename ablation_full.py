# -*- coding: utf-8 -*-
"""R2-6 component ablation + R2-4 significance, on the released artifacts.

Every configuration R2-6 asks for:
  single-expert (3), leave-one-out (3), random / equal / trained gate,
  with and without X5,X6, fixed vs tuned threshold.

Masking rule: removed experts' logits are set to -inf BEFORE the softmax, so
the surviving weights renormalise to 1. Zeroing after the softmax would leave
them not summing to one and the scores would stop being comparable.

X5,X6 removal needs retraining, not masking -- the gate takes a 4-dim input.

Significance: McNemar over per-pair predictions on the shared test split, which
is the right instrument here. Only systems derivable from these columns can be
tested; JPlag and TokenNorm cannot (they are external tools, not functions of
S_CodeBERT / S_AST / S_Token).
"""
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score

X6 = ["S_CodeBERT", "S_AST", "S_Token", "D_lang",
      "S_CodeBERT_minus_S_AST", "one_minus_S_AST"]
X4 = ["S_CodeBERT", "S_AST", "S_Token", "D_lang"]
SC = ["S_CodeBERT", "S_AST", "S_Token"]
SEEDS = [0, 1, 2, 3, 4, 5, 6, 7]


def gate(nin=6):
    return nn.Sequential(nn.Linear(nin, 16), nn.ReLU(), nn.Dropout(0.3),
                         nn.Linear(16, 8), nn.ReLU(), nn.Dropout(0.3),
                         nn.Linear(8, 3))          # logits; softmax applied outside


df = pd.read_csv("gptclonebench_features.csv")
df["S_CodeBERT_minus_S_AST"] = np.abs(df["S_CodeBERT"] - df["S_AST"])
df["one_minus_S_AST"] = 1.0 - df["S_AST"]
S = df[SC].values
y = df["label"].values

idx = np.arange(len(df))
itr, itm = train_test_split(idx, test_size=0.3, random_state=42, stratify=y)
iv, ite = train_test_split(itm, test_size=0.5, random_state=42, stratify=y[itm])
print("train %d  val %d  test %d\n" % (len(itr), len(iv), len(ite)))


def train_gate(cols, seed, epochs=60):
    torch.manual_seed(seed)
    m = gate(len(cols))
    X = df[cols].values
    opt = optim.AdamW(m.parameters(), lr=1e-3, weight_decay=1e-5)
    lf = nn.BCELoss()
    Xt = torch.tensor(X[itr], dtype=torch.float32)
    St = torch.tensor(S[itr], dtype=torch.float32)
    yt = torch.tensor(y[itr], dtype=torch.float32).unsqueeze(1)
    for _ in range(epochs):
        m.train()
        perm = torch.randperm(len(Xt))
        for b in range(0, len(perm), 32):
            j = perm[b:b + 32]
            w = torch.softmax(m(Xt[j]), dim=-1)
            out = (w * St[j]).sum(1, keepdim=True).clamp(1e-6, 1 - 1e-6)
            loss = lf(out, yt[j])
            opt.zero_grad(); loss.backward(); opt.step()
    m.eval()
    return m, X


def weights_from(m, X, ix, mask=None):
    """mask: indices of experts to KEEP; others get -inf before softmax."""
    with torch.no_grad():
        lg = m(torch.tensor(X[ix], dtype=torch.float32))
        if mask is not None:
            neg = torch.full_like(lg, float("-inf"))
            keep = torch.zeros_like(lg, dtype=torch.bool)
            keep[:, mask] = True
            lg = torch.where(keep, lg, neg)
        return torch.softmax(lg, dim=-1).numpy()


def metrics(sv, st, fixed=None):
    thr = 0.50 if fixed else max(np.arange(0.02, 0.99, 0.005),
                                 key=lambda z: f1_score(y[iv], (sv >= z).astype(int),
                                                        zero_division=0))
    p = (st >= thr).astype(int)
    return (accuracy_score(y[ite], p) * 100, f1_score(y[ite], p) * 100, p)


def run(scorer, fixed=None):
    """scorer(seed) -> (val_scores, test_scores). Returns mean/sd and preds of seed 0."""
    A, F, P0 = [], [], None
    for s in SEEDS:
        sv, st = scorer(s)
        a, f, p = metrics(sv, st, fixed)
        A.append(a); F.append(f)
        if s == SEEDS[0]:
            P0 = p
    return np.mean(A), np.std(A), np.mean(F), np.std(F), P0


rows, preds = [], {}


def add(name, scorer, fixed=None):
    a, asd, f, fsd, p = run(scorer, fixed)
    rows.append((name, a, asd, f, fsd))
    preds[name] = p
    print("  %-40s acc %5.1f +-%4.2f   F1 %5.1f +-%4.2f" % (name, a, asd, f, fsd))


# ---- trained gate, full input -----------------------------------------------
print("Trained gate (retrained, 8 seeds):")
_cache = {}


def trained(seed):
    if seed not in _cache:
        _cache[seed] = train_gate(X6, seed)
    m, X = _cache[seed]
    return ((weights_from(m, X, iv) * S[iv]).sum(1),
            (weights_from(m, X, ite) * S[ite]).sum(1))


add("Trained gate (full model)", trained)


# ---- single expert: keep exactly one logit ----------------------------------
print("\nSingle expert (gate masked to one expert):")
for i, nm in enumerate(["CodeBERT only", "AST only", "Token only"]):
    add(nm, (lambda i: (lambda s: (S[iv][:, i], S[ite][:, i])))(i))

# ---- leave-one-out ----------------------------------------------------------
print("\nLeave-one-out (remaining experts renormalised):")
for i, nm in enumerate(["without CodeBERT", "without AST", "without Token"]):
    keep = [j for j in range(3) if j != i]

    def loo(s, keep=keep):
        m, X = _cache[s] if s in _cache else train_gate(X6, s)
        _cache[s] = (m, X)
        return ((weights_from(m, X, iv, keep) * S[iv]).sum(1),
                (weights_from(m, X, ite, keep) * S[ite]).sum(1))
    add(nm, loo)

# ---- fusion rules -----------------------------------------------------------
print("\nFusion rule:")
add("Equal weights (static averaging)", lambda s: (S[iv].mean(1), S[ite].mean(1)))


def rnd(s):
    rs = np.random.RandomState(s)
    wv = rs.dirichlet(np.ones(3), len(iv))
    wt = rs.dirichlet(np.ones(3), len(ite))
    return ((wv * S[iv]).sum(1), (wt * S[ite]).sum(1))


add("Random weights per pair", rnd)

# ---- input ablation ---------------------------------------------------------
print("\nInput features:")
_c4 = {}


def no56(seed):
    if seed not in _c4:
        _c4[seed] = train_gate(X4, seed)
    m, X = _c4[seed]
    return ((weights_from(m, X, iv) * S[iv]).sum(1),
            (weights_from(m, X, ite) * S[ite]).sum(1))


add("Trained gate without X5, X6 (retrained)", no56)

# ---- threshold rule ---------------------------------------------------------
print("\nDecision rule:")
add("Trained gate, fixed threshold 0.50", trained, fixed=True)

# ---- released checkpoint ----------------------------------------------------
print("\nReleased checkpoint:")
ck = torch.load("best_gating_model.pth", map_location="cpu", weights_only=False)
mck = nn.Sequential(nn.Linear(6, 16), nn.ReLU(), nn.Dropout(0.3),
                    nn.Linear(16, 8), nn.ReLU(), nn.Dropout(0.3),
                    nn.Linear(8, 3))
sd = {k.replace("network.", ""): v for k, v in ck["model_state_dict"].items()}
mck.load_state_dict(sd)
mck.eval()
Xall = df[X6].values
a, f, p = metrics((weights_from(mck, Xall, iv) * S[iv]).sum(1),
                  (weights_from(mck, Xall, ite) * S[ite]).sum(1))
print("  %-40s acc %5.1f            F1 %5.1f" % ("released best_gating_model.pth", a, f))
preds["released checkpoint"] = p

# ---- McNemar ----------------------------------------------------------------
print("\n" + "=" * 74)
print("McNemar, trained gate vs each derivable baseline (test n=%d)" % len(ite))
print("=" * 74)
from scipy.stats import binomtest
base = preds["Trained gate (full model)"]
correct_base = (base == y[ite])
print("%-40s %6s %6s %10s" % ("baseline", "b", "c", "p (exact)"))
print("-" * 66)
for nm in ["Equal weights (static averaging)", "CodeBERT only", "AST only",
           "Token only", "without CodeBERT", "without AST", "without Token",
           "Trained gate without X5, X6 (retrained)", "Random weights per pair"]:
    co = (preds[nm] == y[ite])
    b = int((correct_base & ~co).sum())     # gate right, baseline wrong
    c = int((~correct_base & co).sum())     # gate wrong, baseline right
    pv = binomtest(b, b + c, 0.5).pvalue if b + c else 1.0
    print("%-40s %6d %6d %10.3g" % (nm, b, c, pv))

print("\nNot testable from these files: JPlag, TokenNorm.")
print("They are external tools; the CSV holds only the three expert scores,")
print("so no per-pair prediction for them can be reconstructed here.")
