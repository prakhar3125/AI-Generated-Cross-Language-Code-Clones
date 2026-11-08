# -*- coding: utf-8 -*-
"""1) Check D_lang for label leakage.  2) 8-seed runs -> significance + CI."""
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score
from scipy import stats

X_COLS = ["S_CodeBERT", "S_AST", "S_Token", "D_lang",
          "S_CodeBERT_minus_S_AST", "one_minus_S_AST"]
S_COLS = ["S_CodeBERT", "S_AST", "S_Token"]


class Gate(nn.Module):
    def __init__(self, n_in=6, h=16, p=0.3):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(n_in, h), nn.ReLU(), nn.Dropout(p),
            nn.Linear(h, h // 2), nn.ReLU(), nn.Dropout(p),
            nn.Linear(h // 2, 3), nn.Softmax(dim=-1))

    def forward(self, x):
        return self.network(x)


df = pd.read_csv("gptclonebench_features.csv")
df["S_CodeBERT_minus_S_AST"] = np.abs(df["S_CodeBERT"] - df["S_AST"])
df["one_minus_S_AST"] = 1.0 - df["S_AST"]
X, S, y = df[X_COLS].values, df[S_COLS].values, df["label"].values

print("=" * 64)
print("1. D_lang leakage check")
print("=" * 64)
for v in (0.0, 1.0):
    m = df.D_lang == v
    print("  D_lang=%.0f : n=%5d  positives=%5d  P(label=1)=%.3f"
          % (v, m.sum(), df.label[m].sum(), df.label[m].mean()))
same = df[df.D_lang == 0.0]
print("\n  A rule of 'predict 0 whenever D_lang=0' is correct on %d/%d = %.1f%% of those rows."
      % ((same.label == 0).sum(), len(same), (same.label == 0).mean() * 100))
print("  D_lang is in the gate's input vector (X4 of Equation 8).")


def fit_eval(seed, n_ep=100):
    itr, itm = train_test_split(np.arange(len(df)), test_size=0.3,
                                random_state=42, stratify=y)
    iv, ite = train_test_split(itm, test_size=0.5, random_state=42, stratify=y[itm])
    torch.manual_seed(seed)
    g = Gate(6)
    opt = optim.AdamW(g.parameters(), lr=1e-3, weight_decay=1e-5)
    lf = nn.BCELoss()
    Xt = torch.tensor(X[itr], dtype=torch.float32)
    St = torch.tensor(S[itr], dtype=torch.float32)
    yt = torch.tensor(y[itr], dtype=torch.float32).unsqueeze(1)
    best, best_state = -1, None
    Xv = torch.tensor(X[iv], dtype=torch.float32)
    for ep in range(n_ep):
        g.train()
        perm = torch.randperm(len(Xt))
        for b in range(0, len(perm), 64):
            j = perm[b:b + 64]
            out = (g(Xt[j]) * St[j]).sum(1, keepdim=True).clamp(1e-6, 1 - 1e-6)
            loss = lf(out, yt[j])
            opt.zero_grad(); loss.backward(); opt.step()
        g.eval()
        with torch.no_grad():
            sv = (g(Xv).numpy() * S[iv]).sum(1)
        f = max(f1_score(y[iv], (sv >= t).astype(int), zero_division=0)
                for t in np.arange(0.05, 0.96, 0.05))
        if f > best:
            best, best_state = f, {k: v.clone() for k, v in g.state_dict().items()}
    g.load_state_dict(best_state)
    g.eval()
    with torch.no_grad():
        sv = (g(Xv).numpy() * S[iv]).sum(1)
        ste = (g(torch.tensor(X[ite], dtype=torch.float32)).numpy() * S[ite]).sum(1)
    bt = max(np.arange(0.02, 0.99, 0.01),
             key=lambda t: f1_score(y[iv], (sv >= t).astype(int), zero_division=0))
    pred = (ste >= bt).astype(int)
    return f1_score(y[ite], pred) * 100, accuracy_score(y[ite], pred) * 100, ste, y[ite], iv, ite


print("\n" + "=" * 64)
print("2. Eight seeds")
print("=" * 64)
moe_f1, moe_acc = [], []
last = None
for s in range(8):
    f1, acc, ste, yte, iv, ite = fit_eval(s)
    moe_f1.append(f1); moe_acc.append(acc); last = (ste, yte, iv, ite)
    print("  seed %d : F1 %.2f  Acc %.2f" % (s, f1, acc))
moe_f1 = np.array(moe_f1)
print("\n  MoE F1: %.2f +/- %.2f" % (moe_f1.mean(), moe_f1.std()))

ste, yte, iv, ite = last
base = {}
for i, nm in enumerate(["CodeBERT-only", "AST-only", "Token-only"]):
    bt = max(np.arange(0.02, 0.99, 0.01),
             key=lambda t: f1_score(y[iv], (S[iv][:, i] >= t).astype(int), zero_division=0))
    base[nm] = f1_score(yte, (S[ite][:, i] >= bt).astype(int)) * 100
bt = max(np.arange(0.02, 0.99, 0.01),
         key=lambda t: f1_score(y[iv], (S[iv].mean(1) >= t).astype(int), zero_division=0))
base["Equal-weights"] = f1_score(yte, (S[ite].mean(1) >= bt).astype(int)) * 100

print("\n  Deterministic baselines (same test split):")
for k, v in base.items():
    print("    %-16s F1 %.2f" % (k, v))

print("\n  One-sample t-test, MoE seeds vs each fixed baseline:")
for k, v in base.items():
    t, p = stats.ttest_1samp(moe_f1, v)
    print("    vs %-16s diff %+6.2f   p = %.2e" % (k, moe_f1.mean() - v, p))

rng = np.random.default_rng(0)
bt = max(np.arange(0.02, 0.99, 0.01),
         key=lambda t: f1_score(y[iv], ((S[iv] * 0 + 1) * 0 + 1).sum(1) * 0 + 1, zero_division=0)
         if False else f1_score(y[iv], (S[iv].mean(1) >= t).astype(int), zero_division=0))
boot = []
n = len(yte)
pred = (ste >= bt).astype(int)
for _ in range(10000):
    j = rng.integers(0, n, n)
    boot.append(f1_score(yte[j], pred[j], zero_division=0))
lo, hi = np.percentile(boot, [2.5, 97.5])
print("\n  Bootstrap 95%% CI for MoE F1 (10,000 resamples): [%.3f, %.3f]" % (lo, hi))
