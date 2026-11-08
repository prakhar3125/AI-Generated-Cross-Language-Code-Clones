# -*- coding: utf-8 -*-
"""Real per-system confusion counts on the released artifacts.

Every threshold is tuned on the validation split and applied to the held-out
test split. These are measurements, not reconstructions.
"""
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

X_COLS = ["S_CodeBERT", "S_AST", "S_Token", "D_lang",
          "S_CodeBERT_minus_S_AST", "one_minus_S_AST"]
S_COLS = ["S_CodeBERT", "S_AST", "S_Token"]


class Gate(nn.Module):
    def __init__(self, n=6, h=16, p=0.3):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(n, h), nn.ReLU(), nn.Dropout(p),
            nn.Linear(h, h // 2), nn.ReLU(), nn.Dropout(p),
            nn.Linear(h // 2, 3), nn.Softmax(dim=-1))

    def forward(self, x):
        return self.network(x)


df = pd.read_csv("gptclonebench_features.csv")
df["S_CodeBERT_minus_S_AST"] = np.abs(df["S_CodeBERT"] - df["S_AST"])
df["one_minus_S_AST"] = 1.0 - df["S_AST"]
S, y = df[S_COLS].values, df["label"].values

idx = np.arange(len(df))
itr, itm = train_test_split(idx, test_size=0.3, random_state=42, stratify=y)
iv, ite = train_test_split(itm, test_size=0.5, random_state=42, stratify=y[itm])

g = Gate()
g.load_state_dict(torch.load("best_gating_model.pth", map_location="cpu",
                             weights_only=False)["model_state_dict"])
g.eval()
with torch.no_grad():
    w_v = g(torch.tensor(df[X_COLS].values[iv], dtype=torch.float32)).numpy()
    w_t = g(torch.tensor(df[X_COLS].values[ite], dtype=torch.float32)).numpy()

systems = {
    "MoE (trained gate)": ((w_v * S[iv]).sum(1), (w_t * S[ite]).sum(1)),
    "Static Avg (equal w)": (S[iv].mean(1), S[ite].mean(1)),
    "CodeBERT only": (S[iv][:, 0], S[ite][:, 0]),
    "AST only": (S[iv][:, 1], S[ite][:, 1]),
    "Token only": (S[iv][:, 2], S[ite][:, 2]),
}

P = int((y[ite] == 1).sum())
N = int((y[ite] == 0).sum())
print("Test split: %d pairs (%d positive, %d negative)\n" % (len(ite), P, N))
print("%-22s %6s %6s %6s %6s | %6s %6s %6s %6s %6s" %
      ("system", "TP", "FN", "TN", "FP", "Acc", "Prec", "Rec", "Spec", "F1"))
print("-" * 92)
for name, (sv, st) in systems.items():
    thr = max(np.arange(0.02, 0.99, 0.005),
              key=lambda z: f1_score(y[iv], (sv >= z).astype(int), zero_division=0))
    p = (st >= thr).astype(int)
    tp = int(((y[ite] == 1) & (p == 1)).sum())
    fn = int(((y[ite] == 1) & (p == 0)).sum())
    tn = int(((y[ite] == 0) & (p == 0)).sum())
    fp = int(((y[ite] == 0) & (p == 1)).sum())
    acc = (tp + tn) / len(ite) * 100
    prec = tp / (tp + fp) * 100 if tp + fp else 0.0
    rec = tp / P * 100
    spec = tn / N * 100
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    print("%-22s %6d %6d %6d %6d | %6.1f %6.1f %6.1f %6.1f %6.1f"
          % (name, tp, fn, tn, fp, acc, prec, rec, spec, f1))

print("\nNot obtainable from these artifacts: JPlag, TokenNorm.")
print("They are external tools; the released data contains only the three expert")
print("scores, so no confusion matrix for them can be produced here.")
