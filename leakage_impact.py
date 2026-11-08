# -*- coding: utf-8 -*-
"""How much of the gate's performance depends on the D_lang confound?

Three conditions, 5 seeds each:
  A  full 6-dim input, scored on the whole test split      (as published)
  B  D_lang removed from the input, whole test split
  C  full input, scored only on cross-language rows, where D_lang carries
     no information because every row has D_lang = 1
"""
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

X6 = ["S_CodeBERT", "S_AST", "S_Token", "D_lang",
      "S_CodeBERT_minus_S_AST", "one_minus_S_AST"]
X5 = ["S_CodeBERT", "S_AST", "S_Token",
      "S_CodeBERT_minus_S_AST", "one_minus_S_AST"]
S_COLS = ["S_CodeBERT", "S_AST", "S_Token"]


class Gate(nn.Module):
    def __init__(self, n_in, h=16, p=0.3):
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
S, y = df[S_COLS].values, df["label"].values

itr, itm = train_test_split(np.arange(len(df)), test_size=0.3, random_state=42, stratify=y)
iv, ite = train_test_split(itm, test_size=0.5, random_state=42, stratify=y[itm])
xl_te = ite[df.D_lang.values[ite] == 1.0]


def run(cols, seed):
    Xa = df[cols].values
    torch.manual_seed(seed)
    g = Gate(len(cols))
    opt = optim.AdamW(g.parameters(), lr=1e-3, weight_decay=1e-5)
    lf = nn.BCELoss()
    Xt = torch.tensor(Xa[itr], dtype=torch.float32)
    St = torch.tensor(S[itr], dtype=torch.float32)
    yt = torch.tensor(y[itr], dtype=torch.float32).unsqueeze(1)
    for _ in range(60):
        g.train()
        perm = torch.randperm(len(Xt))
        for b in range(0, len(perm), 64):
            j = perm[b:b + 64]
            out = (g(Xt[j]) * St[j]).sum(1, keepdim=True).clamp(1e-6, 1 - 1e-6)
            loss = lf(out, yt[j])
            opt.zero_grad(); loss.backward(); opt.step()
    g.eval()
    with torch.no_grad():
        sc = lambda ix: (g(torch.tensor(Xa[ix], dtype=torch.float32)).numpy() * S[ix]).sum(1)
        sv, ste, sxl = sc(iv), sc(ite), sc(xl_te)
    t = max(np.arange(0.02, 0.99, 0.01),
            key=lambda th: f1_score(y[iv], (sv >= th).astype(int), zero_division=0))
    return (f1_score(y[ite], (ste >= t).astype(int)) * 100,
            f1_score(y[xl_te], (sxl >= t).astype(int)) * 100)


res = {"A full / all rows": [], "B no D_lang / all rows": [], "C full / cross-lang only": []}
for s in range(5):
    a, c = run(X6, s)
    b, _ = run(X5, s)
    res["A full / all rows"].append(a)
    res["B no D_lang / all rows"].append(b)
    res["C full / cross-lang only"].append(c)

print("\nTest split: %d rows total, %d of them cross-language" % (len(ite), len(xl_te)))
print("Same-language rows in test: %d, of which positive: %d\n"
      % (len(ite) - len(xl_te), int(y[ite][df.D_lang.values[ite] == 0.0].sum())))
print("%-30s %8s %7s" % ("Condition", "F1 mean", "sd"))
print("-" * 48)
for k, v in res.items():
    v = np.array(v)
    print("%-30s %8.2f %7.2f" % (k, v.mean(), v.std()))

a = np.array(res["A full / all rows"]).mean()
b = np.array(res["B no D_lang / all rows"]).mean()
c = np.array(res["C full / cross-lang only"]).mean()
print("\n  dropping D_lang            : %+.2f F1" % (b - a))
print("  restricting to cross-lang  : %+.2f F1" % (c - a))
