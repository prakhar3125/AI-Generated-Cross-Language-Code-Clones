"""Why does the gate lose to the direct classifier / trees? Diagnostics on the corrected released scores (no retraining of the gate).
REGIME=B python -I diag_gate_loss.py"""
import json, os, sys
import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_curve, roc_auc_score
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE
from exp_lib import REGIME, SC, X6, load, tune_threshold

D = load(); tr, va, te = D["train"], D["val"], D["test"]
R = np.load(os.path.join(HERE, "results_" + REGIME, "scores.npz"))
y = te.label.values
g = R["test__gate"].mean(0); d = R["test__direct"].mean(0)
gb = np.mean([HistGradientBoostingClassifier(max_depth=3, learning_rate=0.1, max_iter=200, early_stopping=True, validation_fraction=0.2, random_state=s)
              .fit(tr[X6].values, tr.label.values).predict_proba(te[X6].values)[:, 1] for s in range(4)], 0)
tok = te.S_Token.values
print("regime", REGIME, "| test pairs", len(te), "| AUROC gate %.3f direct %.3f trees %.3f token %.3f" % tuple(roc_auc_score(y, s) for s in (g, d, gb, tok)))

def r_at(s, f):
    fpr, tpr, _ = roc_curve(y, s); return tpr[np.searchsorted(fpr, f, side="right") - 1]
print("recall@1%%FPR gate %.3f direct %.3f trees %.3f | @5%% gate %.3f direct %.3f trees %.3f" % (r_at(g, .01), r_at(d, .01), r_at(gb, .01), r_at(g, .05), r_at(d, .05), r_at(gb, .05)))

print("\n-- (1) saturation: how many distinct score values / ties in the top tail of the gate vs trees (test negatives)")
neg = y == 0
for nm, s in (("gate", g), ("direct", d), ("trees", gb)):
    sn = s[neg]; print("  %-7s negatives>=0.9: %4d  >=0.95: %4d  >=0.99: %4d | positives>=0.9: %4d  >=0.99: %4d" % (nm, (sn >= .9).sum(), (sn >= .95).sum(), (sn >= .99).sum(), (s[~neg] >= .9).sum(), (s[~neg] >= .99).sum()))

print("\n-- (2) the part of the input space where the trees win: at a matched 5% FPR threshold, positives caught by trees but missed by the gate")
def at_fpr(s, f=.05): return np.quantile(s[neg], 1 - f)
tg, tt = at_fpr(g), at_fpr(gb)
catch_t, catch_g = (gb >= tt) & ~neg, (g >= tg) & ~neg
only_t, only_g = catch_t & ~catch_g, catch_g & ~catch_t
print("  positives caught: trees %d, gate %d | only trees %d, only gate %d" % (catch_t.sum(), catch_g.sum(), only_t.sum(), only_g.sum()))
for nm, m in (("only trees", only_t), ("only gate", only_g), ("both", catch_t & catch_g), ("neither", ~neg & ~catch_t & ~catch_g)):
    x = te[m]
    print("  %-10s n=%4d  mean S_sem %.3f S_ast %.3f S_tok %.3f D_lang %.2f | slices %s" % (nm, m.sum(), x.S_CodeBERT.mean(), x.S_AST.mean(), x.S_Token.mean(), x.D_lang.mean(), x.slice.value_counts().to_dict()))
fa_t, fa_g = (gb >= tt) & neg, (g >= tg) & neg
print("  false alarms at that threshold: trees %d gate %d (by design equal) | overlap %d" % (fa_t.sum(), fa_g.sum(), (fa_t & fa_g).sum()))

print("\n-- (3) can a convex combination express what the trees do? Fit the BEST per-pair convex weights (oracle, 3-simplex grid) and see the ceiling")
grid = [(a / 20, b / 20, (20 - a - b) / 20) for a in range(21) for b in range(21 - a)]
S = te[SC].values
best = None
for w in grid:
    s = S @ np.array(w); auc = roc_auc_score(y, s)
    if best is None or auc > best[0]: best = (auc, w)
print("  best FIXED convex weights by test AUROC (oracle):", best[1], "AUROC %.3f   [gate %.3f, trees %.3f]" % (best[0], roc_auc_score(y, g), roc_auc_score(y, gb)))
# gate with an input-dependent weight but linear output: upper-bound check using a 2-bin oracle on D_lang
sc = np.zeros(len(te))
for dl in (0, 1):
    m = te.D_lang.values == dl; bb = None
    for w in grid:
        s = S[m] @ np.array(w); a = roc_auc_score(y[m], s) if len(set(y[m])) > 1 else 0
        if bb is None or a > bb[0]: bb = (a, w)
    sc[m] = S[m] @ np.array(bb[1]); print("  D_lang=%d: best convex weights" % dl, bb[1], "within-group AUROC %.3f" % bb[0])
print("  pooled score from the two per-relation convex rules: AUROC %.3f" % roc_auc_score(y, sc))

print("\n-- (4) output range: the fused score is a weighted mean of expert scores, so it is bounded by them")
print("  share of test positives whose max(S) < 0.5 (fused score cannot exceed 0.5): %.3f" % ((S.max(1) < .5) & ~neg).mean())
print("  gate score, positives: p10 %.3f p50 %.3f | negatives p50 %.3f p90 %.3f p99 %.3f" % (*np.quantile(g[~neg], [.1, .5]), *np.quantile(g[neg], [.5, .9, .99])))
print("  trees score, positives: p10 %.3f p50 %.3f | negatives p50 %.3f p90 %.3f p99 %.3f" % (*np.quantile(gb[~neg], [.1, .5]), *np.quantile(gb[neg], [.5, .9, .99])))
w = R["test__gate_w"].mean(0)
print("\n-- (5) what the gate's weights do: std of the weight vector across test pairs (sem,str,syn):", np.round(w.std(0), 3), "| mean", np.round(w.mean(0), 3))
print("  weight on token expert by slice:", {s: round(float(w[(te.slice == s).values, 2].mean()), 3) for s in te.slice.unique()})
