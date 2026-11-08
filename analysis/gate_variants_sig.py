"""Significance of the gate variants against the direct classifier and gradient-boosted trees, with cluster-aware inference.
Retrains only the variants named below (same code, lr/batch and seeds as gate_variants.py), keeps the per-seed test scores and
validation thresholds, and compares F1 with a paired cluster bootstrap over problem groups (group1) as in e2_retrained_ablation.py.
Trees: HistGradientBoosting on X6 (8 seeds), validation-tuned threshold, as in e1_baselines.py.
REGIME=A|B|C python -I gate_variants_sig.py -> results_<R>/gate_variants_sig.json"""
import json, os, sys
from multiprocessing import Pool
import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_curve

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate_variants as gv
from exp_lib import SEEDS, TAG, X6, tune_threshold
from stats_tools import boot_p, cluster_bootstrap, cluster_counts, holm

KINDS = ["base", "logit", "resid", "logit_feat", "direct"]

def job(a):
    kind, seed = a
    k, s, thr, st, sc, wt, wc = gv.job((kind, seed))
    return kind, seed, thr, st

def trees(seed):
    g = HistGradientBoostingClassifier(max_depth=3, learning_rate=0.1, max_iter=200, early_stopping=True, validation_fraction=0.2, random_state=seed)
    g.fit(gv.tr[X6].values, gv.tr.label.values)
    sv = g.predict_proba(gv.va[X6].values)[:, 1]; st = g.predict_proba(gv.te[X6].values)[:, 1]
    return tune_threshold(sv, gv.va.label.values), st

if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    te = gv.te; y = te.label.values; cl = te.group1.values
    with Pool(5) as pool:
        res = pool.map(job, [(k, s) for k in KINDS for s in SEEDS])
    preds = {k: np.stack([(x[3] >= x[2]).astype(int) for x in sorted([r for r in res if r[0] == k], key=lambda z: z[1])]) for k in KINDS}
    scores = {k: np.stack([x[3] for x in sorted([r for r in res if r[0] == k], key=lambda z: z[1])]) for k in KINDS}
    tr_ = [trees(s) for s in SEEDS]
    preds["trees"] = np.stack([(s >= t).astype(int) for t, s in tr_]); scores["trees"] = np.stack([s for _, s in tr_])
    cnt = {k: np.stack([cluster_counts(y, p, cl) for p in preds[k]]) for k in preds}
    K = next(iter(cnt.values())).shape[1]
    bs = cluster_bootstrap(cnt, K, B=5000, seed=5)
    def r1(s):
        fpr, tpr, _ = roc_curve(y, s); return float(tpr[np.searchsorted(fpr, .01, side="right") - 1])
    out = {"n_clusters": int(K), "f1": {}, "r1": {}, "vs": {}}
    for k in preds:
        f = [2 * ((y == 1) & (p == 1)).sum() / max(2 * ((y == 1) & (p == 1)).sum() + ((y == 0) & (p == 1)).sum() + ((y == 1) & (p == 0)).sum(), 1) for p in preds[k]]
        out["f1"][k] = [float(np.mean(f)), float(np.std(f, ddof=1))]
        out["r1"][k] = float(np.mean([r1(s) for s in scores[k]]))
    for ref in ("direct", "trees"):
        names = [k for k in preds if k != ref]; ps = []
        for k in names:
            d = bs[k] - bs[ref]; ps.append(boot_p(d))
            out["vs"][k + "|" + ref] = dict(delta=float(out["f1"][k][0] - out["f1"][ref][0]), ci=[float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))])
        for k, p in zip(names, holm(ps)):
            out["vs"][k + "|" + ref]["p_holm"] = float(p)
    for k, v in out["vs"].items():
        print(TAG, "%-18s dF1 %+.4f  CI [%+.4f, %+.4f]  p_holm %.3f" % (k, v["delta"], *v["ci"], v["p_holm"]))
    print(TAG, "recall@1%FPR:", {k: round(v, 3) for k, v in out["r1"].items()})
    json.dump(out, open(os.path.join(gv.RES, "gate_variants_sig.json"), "w"), indent=1)
