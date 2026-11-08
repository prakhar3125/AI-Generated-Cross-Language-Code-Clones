import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from scipy.stats import binomtest

X_COLS = ['S_CodeBERT', 'S_AST', 'S_Token', 'D_lang', 'S_CodeBERT_minus_S_AST', 'one_minus_S_AST']
S_COLS = ['S_CodeBERT', 'S_AST', 'S_Token']

df = pd.read_csv('leakage_safe_features.csv')
df = df[df['partition'] != 'drop'].reset_index(drop=True)
print('pairs after dropping cross-partition negatives:', len(df))
print(df['partition'].value_counts())
print(df.groupby('partition')['label'].value_counts())

X = df[X_COLS].values
S = df[S_COLS].values
y = df['label'].values
itr = df.index[df['partition'] == 'train'].to_numpy()
iv = df.index[df['partition'] == 'val'].to_numpy()
ite = df.index[df['partition'] == 'test'].to_numpy()
print('split sizes: train', len(itr), 'val', len(iv), 'test', len(ite))


def net(out, seed):
    torch.manual_seed(seed)
    return nn.Sequential(nn.Linear(6, 16), nn.ReLU(), nn.Dropout(0.3),
                         nn.Linear(16, 8), nn.ReLU(), nn.Dropout(0.3),
                         nn.Linear(8, out), nn.Softmax(dim=-1) if out == 3 else nn.Sigmoid())


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
            return (o.numpy() * S[ix]).sum(1) if routing else o.numpy().ravel()
        return sc(iv), sc(ite)


def evaluate(sv, st):
    thr = max(np.arange(0.02, 0.99, 0.005),
              key=lambda z: f1_score(y[iv], (sv >= z).astype(int), zero_division=0))
    p = (st >= thr).astype(int)
    return f1_score(y[ite], p) * 100, p


gate_f1, direct_f1, logreg_f1 = [], [], []
gate_p0 = direct_p0 = logreg_p0 = None
for s in range(5):
    f1g, pg = evaluate(*train(net(3, s), True))
    f1d, pd_ = evaluate(*train(net(1, s), False))
    lr = LogisticRegression(max_iter=2000).fit(X[itr], y[itr])
    f1l, pl = evaluate(lr.predict_proba(X[iv])[:, 1], lr.predict_proba(X[ite])[:, 1])
    gate_f1.append(f1g); direct_f1.append(f1d); logreg_f1.append(f1l)
    print('seed %d  gate=%.2f  direct=%.2f  logreg=%.2f' % (s, f1g, f1d, f1l))
    if s == 0:
        gate_p0, direct_p0, logreg_p0 = pg, pd_, pl

print()
print('gate      F1 mean=%.2f sd=%.2f' % (np.mean(gate_f1), np.std(gate_f1, ddof=1)))
print('direct    F1 mean=%.2f sd=%.2f' % (np.mean(direct_f1), np.std(direct_f1, ddof=1)))
print('logreg    F1 mean=%.2f sd=%.2f' % (np.mean(logreg_f1), np.std(logreg_f1, ddof=1)))
print('gate - direct = %.2f points' % (np.mean(gate_f1) - np.mean(direct_f1)))
print('gate - logreg = %.2f points' % (np.mean(gate_f1) - np.mean(logreg_f1)))

correctA = gate_p0 == y[ite]
correctB = direct_p0 == y[ite]
correctC = logreg_p0 == y[ite]
b1 = int((correctA & ~correctB).sum()); c1 = int((~correctA & correctB).sum())
p1 = binomtest(b1, b1 + c1, 0.5).pvalue if (b1 + c1) else 1.0
b2 = int((correctA & ~correctC).sum()); c2 = int((~correctA & correctC).sum())
p2 = binomtest(b2, b2 + c2, 0.5).pvalue if (b2 + c2) else 1.0
print()
print('McNemar gate vs direct: b=%d c=%d p=%.4g' % (b1, c1, p1))
print('McNemar gate vs logreg: b=%d c=%d p=%.4g' % (b2, c2, p2))
