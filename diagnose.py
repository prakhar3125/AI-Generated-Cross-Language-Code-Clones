# -*- coding: utf-8 -*-
"""Can any threshold or subset of the released data reproduce F1 = 0.900 / acc = 90.2%?"""
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score


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

model = GatingNetwork(6)
model.load_state_dict(torch.load("best_gating_model.pth", map_location="cpu",
                                 weights_only=False)["model_state_dict"])
model.eval()


def scores(frame):
    with torch.no_grad():
        w = model(torch.tensor(frame[X_COLS].values, dtype=torch.float32)).numpy()
    return (w * frame[S_COLS].values).sum(axis=1), frame["label"].values


def sweep(name, frame):
    s, y = scores(frame)
    best_f1 = best_acc = -1.0
    bt_f1 = bt_acc = None
    for th in np.arange(0.05, 0.96, 0.01):
        p = (s >= th).astype(int)
        f1 = f1_score(y, p, zero_division=0)
        ac = accuracy_score(y, p)
        if f1 > best_f1:
            best_f1, bt_f1 = f1, th
        if ac > best_acc:
            best_acc, bt_acc = ac, th
    print("%-34s n=%5d  pos=%5d  bestF1=%.4f @t=%.2f   bestAcc=%.4f @t=%.2f"
          % (name, len(y), int(y.sum()), best_f1, bt_f1, best_acc, bt_acc))
    return best_f1, best_acc


X, S, y = df[X_COLS].values, df[S_COLS].values, df["label"].values
idx = np.arange(len(df))
itr, itm = train_test_split(idx, test_size=0.3, random_state=42, stratify=y)
iv, ite = train_test_split(itm, test_size=0.5, random_state=42, stratify=y[itm])

print("Best achievable over ALL thresholds -- paper claims F1 0.900 / acc 0.902\n")
sweep("test partition (15%)", df.iloc[ite])
sweep("val partition (15%)", df.iloc[iv])
sweep("train partition (70%)", df.iloc[itr])
sweep("FULL dataset", df)
print("")
sweep("cross-language only (D_lang=1)", df[df.D_lang == 1.0])
sweep("same-language only (D_lang=0)", df[df.D_lang == 0.0])
print("")
sweep("test, cross-language only", df.iloc[ite][df.iloc[ite].D_lang == 1.0])

print("\n--- does any subset have 2,652 positives / 3,000 negatives? ---")
print("total positives in released file: %d  (2 x 2652 = %d)" % (int(y.sum()), 2 * 2652))
print("total negatives in released file: %d" % int((y == 0).sum()))
xl = df[df.D_lang == 1.0]
print("cross-language rows: %d  (pos %d / neg %d)"
      % (len(xl), int((xl.label == 1).sum()), int((xl.label == 0).sum())))
