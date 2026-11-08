# -*- coding: utf-8 -*-
"""The decisive control: is the gain from ROUTING, or just from having a small
classifier on these six features?

  A) MoE gate      6->16->8->3 softmax, score = sum(w * expert_scores)
  B) Direct MLP    6->16->8->1 sigmoid, score = P(clone)   <-- same capacity, no routing
  C) Logistic reg  linear on the same six features

5 seeds each, threshold tuned on validation, scored on held-out test.
"""
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score

X_COLS = ["S_CodeBERT", "S_AST", "S_Token", "D_lang",
          "S_CodeBERT_minus_S_AST", "one_minus_S_AST"]
S_COLS = ["S_CodeBERT", "S_AST", "S_Token"]

df = pd.read_csv("gptclonebench_features.csv")
df["S_CodeBERT_minus_S_AST"] = np.abs(df["S_CodeBERT"] - df["S_AST"])
df["one_minus_S_AST"] = 1.0 - df["S_AST"]
X, S, y = df[X_COLS].values, df[S_COLS].values, df["label"].values

itr, itm = train_test_split(np.arange(len(df)), test_size=0.3, random_state=42, stratify=y)
iv, ite = train_test_split(itm, test_size=0.5, random_state=42, stratify=y[itm])


def net(out, seed):
    torch.manual_seed(seed)
    return nn.Sequential(nn.Linear(6, 16), nn.ReLU(), nn.Dropout(0.3),
                         nn.Linear(16, 8), nn.ReLU(), nn.Dropout(0.3),
                         nn.Linear(8, out),
                         nn.Softmax(dim=-1) if out == 3 else nn.Sigmoid())


def train(model, routing, epochs=60):
    opt = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-5)
    lf = nn.BCELoss()
    Xt = torch.tensor(X[itr], dtype=torch.float32)
    St = torch.tensor(S[itr], dtype=torch.float32)
    yt = torch.tensor(y[itr], dtype=torch.float32).unsqueeze(1)
    for _ in range(epochs):
        model.train()
        perm = torch.randperm(len(Xt))
        for b in range(0, len(perm), 64):
            j = perm[b:b + 64]
            o = model(Xt[j])
            out = (o * St[j]).sum(1, keepdim=True) if routing else o
            loss = lf(out.clamp(1e-6, 1 - 1e-6), yt[j])
            opt.zero_grad(); loss.backward(); opt.step()
    model.eval()
    with torch.no_grad():
        def sc(ix):
            o = model(torch.tensor(X[ix], dtype=torch.float32))
            return ((o.numpy() * S[ix]).sum(1) if routing else o.numpy().ravel())
        return sc(iv), sc(ite)


def evaluate(sv, st):
    thr = max(np.arange(0.02, 0.99, 0.005),
              key=lambda z: f1_score(y[iv], (sv >= z).astype(int), zero_division=0))
    p = (st >= thr).astype(int)
    return f1_score(y[ite], p) * 100, accuracy_score(y[ite], p) * 100


res = {"A) MoE gate (routing)": [], "B) Direct MLP (no routing)": [], "C) Logistic regression": []}
for s in range(5):
    res["A) MoE gate (routing)"].append(evaluate(*train(net(3, s), True)))
    res["B) Direct MLP (no routing)"].append(evaluate(*train(net(1, s), False)))
    lr = LogisticRegression(max_iter=2000).fit(X[itr], y[itr])
    res["C) Logistic regression"].append(
        evaluate(lr.predict_proba(X[iv])[:, 1], lr.predict_proba(X[ite])[:, 1]))

print("\nSame six features, same split, 5 seeds (test n=%d)\n" % len(ite))
print("%-30s %14s %14s" % ("model", "F1 mean±sd", "Acc mean±sd"))
print("-" * 60)
for k, v in res.items():
    f = np.array([a for a, _ in v]); a = np.array([b for _, b in v])
    print("%-30s %7.1f ±%4.1f %8.1f ±%4.1f" % (k, f.mean(), f.std(), a.mean(), a.std()))

fa = np.array([x for x, _ in res["A) MoE gate (routing)"]]).mean()
fb = np.array([x for x, _ in res["B) Direct MLP (no routing)"]]).mean()
fc = np.array([x for x, _ in res["C) Logistic regression"]]).mean()
print("\nrouting minus direct MLP : %+.1f F1" % (fa - fb))
print("routing minus logistic   : %+.1f F1" % (fa - fc))
print()
if fb >= fa - 0.5:
    print(">>> The direct classifier MATCHES the gate. On this data the gain comes")
    print("    from the six features plus a small classifier, NOT from routing")
    print("    among experts. The paper's central attribution does not hold here.")
else:
    print(">>> Routing beats an equal-capacity classifier on the same features,")
    print("    which is the control the attribution claim requires.")
