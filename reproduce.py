# -*- coding: utf-8 -*-
"""Reproduce the paper's reported test F1 from the released checkpoint."""
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score


class GatingNetwork(nn.Module):
    def __init__(self, input_size=6, hidden_size=16, dropout=0.3):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden_size, hidden_size // 2), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, 3), nn.Softmax(dim=-1),
        )

    def forward(self, x):
        return self.network(x)


X_COLS = ["S_CodeBERT", "S_AST", "S_Token", "D_lang",
          "S_CodeBERT_minus_S_AST", "one_minus_S_AST"]
S_COLS = ["S_CodeBERT", "S_AST", "S_Token"]

df = pd.read_csv("gptclonebench_features.csv")
df["S_CodeBERT_minus_S_AST"] = np.abs(df["S_CodeBERT"] - df["S_AST"])
df["one_minus_S_AST"] = 1.0 - df["S_AST"]

X, S, y = df[X_COLS].values, df[S_COLS].values, df["label"].values
Xtr, Xtm, Str, Stm, ytr, ytm = train_test_split(X, S, y, test_size=0.3, random_state=42, stratify=y)
Xv, Xte, Sv, Ste, yv, yte = train_test_split(Xtm, Stm, ytm, test_size=0.5, random_state=42, stratify=ytm)
print("split sizes -> train %d | val %d | test %d" % (len(Xtr), len(Xv), len(Xte)))

model = GatingNetwork(input_size=6)
ck = torch.load("best_gating_model.pth", map_location="cpu", weights_only=False)
model.load_state_dict(ck["model_state_dict"])
model.eval()
print("checkpoint: saved val_f1 = %.4f at epoch %s" % (ck.get("val_f1", float("nan")), ck.get("epoch")))
n_params = sum(p.numel() for p in model.parameters())
print("trainable parameters in gate: %d" % n_params)
print("layer shapes:", [tuple(p.shape) for p in model.parameters()])

with torch.no_grad():
    w = model(torch.tensor(Xte, dtype=torch.float32)).numpy()
score = (w * Ste).sum(axis=1)
pred = (score >= 0.5).astype(int)

print("\n--- test partition (n=%d), threshold 0.50 ---" % len(yte))
print("  accuracy  %.4f" % accuracy_score(yte, pred))
print("  precision %.4f" % precision_score(yte, pred, zero_division=0))
print("  recall    %.4f" % recall_score(yte, pred, zero_division=0))
print("  F1        %.4f" % f1_score(yte, pred, zero_division=0))
print("\nmean gate weights on test: CodeBERT %.3f | AST %.3f | Token %.3f" % tuple(w.mean(axis=0)))
