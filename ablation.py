# -*- coding: utf-8 -*-
"""Real ablation on the released artifacts.

Every configuration tunes its decision threshold on the validation split and is
then scored on the test split, so no row benefits from seeing test data.
"""
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

torch.manual_seed(0)
np.random.seed(0)

X_COLS = ["S_CodeBERT", "S_AST", "S_Token", "D_lang",
          "S_CodeBERT_minus_S_AST", "one_minus_S_AST"]
S_COLS = ["S_CodeBERT", "S_AST", "S_Token"]


class Gate(nn.Module):
    def __init__(self, n_in=6, h=16, p=0.3):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(n_in, h), nn.ReLU(), nn.Dropout(p),
            nn.Linear(h, h // 2), nn.ReLU(), nn.Dropout(p),
            nn.Linear(h // 2, 3), nn.Softmax(dim=-1),
        )

    def forward(self, x):
        return self.network(x)


def logits_of(model, x):
    """Run every layer except the final softmax."""
    h = x
    for layer in list(model.network)[:-1]:
        h = layer(h)
    return h


df = pd.read_csv("gptclonebench_features.csv")
df["S_CodeBERT_minus_S_AST"] = np.abs(df["S_CodeBERT"] - df["S_AST"])
df["one_minus_S_AST"] = 1.0 - df["S_AST"]

X, S, y = df[X_COLS].values, df[S_COLS].values, df["label"].values
idx = np.arange(len(df))
itr, itm = train_test_split(idx, test_size=0.3, random_state=42, stratify=y)
iv, ite = train_test_split(itm, test_size=0.5, random_state=42, stratify=y[itm])

gate = Gate(6)
gate.load_state_dict(torch.load("best_gating_model.pth", map_location="cpu",
                                weights_only=False)["model_state_dict"])
gate.eval()


def metrics(name, sv, yv, ste, yte):
    """Tune threshold on val, report on test."""
    best_t, best_f = 0.5, -1.0
    for t in np.arange(0.02, 0.99, 0.01):
        f = f1_score(yv, (sv >= t).astype(int), zero_division=0)
        if f > best_f:
            best_f, best_t = f, t
    p = (ste >= best_t).astype(int)
    return (name,
            accuracy_score(yte, p) * 100,
            precision_score(yte, p, zero_division=0) * 100,
            recall_score(yte, p, zero_division=0) * 100,
            f1_score(yte, p, zero_division=0) * 100)


def gated(model, keep, rows, n_in=6, cols=None):
    """Fused score with only `keep` experts, logits zeroed BEFORE softmax."""
    cols = cols or X_COLS
    with torch.no_grad():
        lg = logits_of(model, torch.tensor(df[cols].values[rows], dtype=torch.float32))
        mask = torch.full((3,), float("-inf"))
        for k in keep:
            mask[k] = 0.0
        w = torch.softmax(lg + mask, dim=-1).numpy()
    return (w * S[rows]).sum(axis=1)


results = []
ALL = [0, 1, 2]

# --- single expert: the raw score itself -------------------------------------
for i, nm in enumerate(["CodeBERT only", "AST only", "Token only"]):
    results.append(metrics(nm, S[iv][:, i], y[iv], S[ite][:, i], y[ite]))

# --- leave-one-out -----------------------------------------------------------
for keep, nm in [([0, 1], "CodeBERT + AST (no Token)"),
                 ([0, 2], "CodeBERT + Token (no AST)"),
                 ([1, 2], "AST + Token (no CodeBERT)")]:
    results.append(metrics(nm, gated(gate, keep, iv), y[iv],
                           gated(gate, keep, ite), y[ite]))

# --- gating mechanism --------------------------------------------------------
rng = np.random.default_rng(0)
wv = rng.dirichlet(np.ones(3), len(iv))
wt = rng.dirichlet(np.ones(3), len(ite))
results.append(metrics("Random (untrained) gate",
                       (wv * S[iv]).sum(1), y[iv], (wt * S[ite]).sum(1), y[ite]))
results.append(metrics("Fixed equal weights",
                       S[iv].mean(1), y[iv], S[ite].mean(1), y[ite]))
results.append(metrics("Trained gate (full model)",
                       gated(gate, ALL, iv), y[iv], gated(gate, ALL, ite), y[ite]))

# --- gate input: retrain without X5, X6 --------------------------------------
C4 = ["S_CodeBERT", "S_AST", "S_Token", "D_lang"]
g4 = Gate(4)
opt = optim.AdamW(g4.parameters(), lr=1e-3, weight_decay=1e-5)
lossf = nn.BCELoss()
Xtr4 = torch.tensor(df[C4].values[itr], dtype=torch.float32)
Str = torch.tensor(S[itr], dtype=torch.float32)
ytr = torch.tensor(y[itr], dtype=torch.float32).unsqueeze(1)
for ep in range(100):
    g4.train()
    perm = torch.randperm(len(Xtr4))
    for b in range(0, len(perm), 64):
        j = perm[b:b + 64]
        out = (g4(Xtr4[j]) * Str[j]).sum(1, keepdim=True)
        loss = lossf(out.clamp(1e-6, 1 - 1e-6), ytr[j])
        opt.zero_grad(); loss.backward(); opt.step()
g4.eval()
results.append(metrics("Without X5, X6",
                       gated(g4, ALL, iv, cols=C4), y[iv],
                       gated(g4, ALL, ite, cols=C4), y[ite]))
results.append(metrics("Full 6-dimensional input",
                       gated(gate, ALL, iv), y[iv], gated(gate, ALL, ite), y[ite]))

# --- decision rule -----------------------------------------------------------
ste = gated(gate, ALL, ite)
p50 = (ste >= 0.50).astype(int)
results.append(("Fixed threshold T=0.50",
                accuracy_score(y[ite], p50) * 100,
                precision_score(y[ite], p50, zero_division=0) * 100,
                recall_score(y[ite], p50, zero_division=0) * 100,
                f1_score(y[ite], p50, zero_division=0) * 100))
results.append(metrics("Tuned threshold", gated(gate, ALL, iv), y[iv], ste, y[ite]))

print("\nMEASURED on released artifacts (n_test=%d)\n" % len(ite))
print("%-30s %7s %7s %7s %7s" % ("Configuration", "Acc", "Prec", "Rec", "F1"))
print("-" * 62)
for r in results:
    print("%-30s %7.1f %7.1f %7.1f %7.1f" % r)
