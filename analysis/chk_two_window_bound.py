"""Bound the benchmark impact of the two-window degeneracy on the released regime A/B/C test predictions
(no retraining): F1 on all test pairs, on the untouched pairs only, and worst-case flipping of every touched pair.
REGIME=A|B|C python -I chk_two_window_bound.py"""
import os, pickle, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE
from exp_lib import load, TAG
D = load(); te = D["test"]
B = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
two = {k for k, v in B.items() if len(v["win"]) == 2}
m = (te.key1.isin(two) | te.key2.isin(two)).values
y = te.label.values
P = np.load(os.path.join(HERE, "results_" + TAG, "preds.npz"))
def f1(p, y):
    tp = ((p == 1) & (y == 1)).sum(); fp = ((p == 1) & (y == 0)).sum(); fn = ((p == 0) & (y == 1)).sum()
    return 2 * tp / max(1, 2 * tp + fp + fn)
def fpr(p, y): return ((p == 1) & (y == 0)).sum() / max(1, (y == 0).sum())
print("regime", TAG, "test pairs", len(te), "touched", int(m.sum()), "(pos %d, neg %d)" % ((y[m] == 1).sum(), (y[m] == 0).sum()))
for k in ("gate|val", "direct|val", "token|val", "codebert|val"):
    p = P[k]
    full = np.mean([f1(p[s], y) for s in range(p.shape[0])])
    unt = np.mean([f1(p[s][~m], y[~m]) for s in range(p.shape[0])])
    t_acc = np.mean([(p[s][m] == y[m]).mean() for s in range(p.shape[0])])
    worst = []
    best = []
    for s in range(p.shape[0]):
        w = p[s].copy(); w[m] = 1 - y[m]; worst.append(f1(w, y))
        b = p[s].copy(); b[m] = y[m]; best.append(f1(b, y))
    print("%-13s F1 all %.4f | untouched only %.4f | touched-pair acc %.3f | bounds if every touched pair were wrong %.4f / right %.4f" % (
        k, full, unt, t_acc, np.mean(worst), np.mean(best)))
