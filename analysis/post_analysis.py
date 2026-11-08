# -*- coding: utf-8 -*-
"""Ablation, cluster-aware statistics, threshold study, operating points, error analysis.

REGIME=A|B python -I post_analysis.py     (run evaluate_all.py first)
Writes results_<REGIME>/post_analysis.json and results_<REGIME>/pr_curves.png
"""
import json
import os
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE  # noqa: E402
from exp_lib import (NEG_SLICE, REGIME, SEEDS, adaptive_thresholds, f1_of, load, metrics,  # noqa: E402
                     tune_threshold)
from stats_tools import (boot_p, cluster_bootstrap, cluster_counts, cluster_signflip, holm,  # noqa: E402
                         mcnemar_exact)

from exp_lib import TAG  # noqa: E402
RES = os.path.join(HERE, "results_" + TAG)
D = load()
va, te, ax = D["val"], D["test"], D["aux"]
yv, yt = va.label.values, te.label.values
R = np.load(os.path.join(RES, "scores.npz"))
P = np.load(os.path.join(RES, "preds.npz"))
clusters = te.group1.values
out = {"regime": REGIME}


def f1s(key):
    return np.array([f1_of(yt, p.astype(int)) for p in P[key]]) * 100


# ----------------------------------------------------------------- 1. ablation (problem-grouped)
ABL = [
    ("Single expert", "Semantic (CodeBERT) alone", "codebert|val"),
    ("Single expert", "Structural (AST) alone", "ast|val"),
    ("Single expert", "Syntactic (Token) alone", "token|val"),
    ("Leave-one-out", "without semantic expert", "gate_wo_sem|val"),
    ("Leave-one-out", "without structural expert", "gate_wo_str|val"),
    ("Leave-one-out", "without syntactic expert", "gate_wo_syn|val"),
    ("Fusion rule", "Equal weights (static averaging)", "static|val"),
    ("Fusion rule", "Random weights per pair", "random|val"),
    ("Input features", "without X5, X6 (retrained)", "gate_x4|val"),
    ("Decision rule", "Fixed threshold 0.50", "gate|fixed"),
    ("Decision rule", "Adaptive threshold (Eq. 12)", "gate|adaptive"),
    ("Capacity control", "Direct classifier (no routing)", "direct|val"),
    ("Capacity control", "Logistic regression", "logreg|val"),
]
for _nm, _k in (("JPlag", "jplag|val"), ("JPlag + token normalization", "tokennorm|val")):
    if _k in P.files:
        ABL.append(("External baseline", _nm, _k))


def pk(key, s):
    return P[key][min(s, len(P[key]) - 1)]


ref = f1s("gate|val")
out["gate_f1"] = [float(ref.mean()), float(ref.std(ddof=1))]
rows, pv = [], []
cnt_ref = np.stack([cluster_counts(yt, p.astype(int), clusters) for p in P["gate|val"]])
for grp, nm, key in ABL:
    f = f1s(key)
    ok_ref = [(pk("gate|val", s) == yt) for s in SEEDS]
    ok_cfg = [(pk(key, s) == yt) for s in SEEDS]
    ps_cluster, ps_mc = [], []
    for s in SEEDS:
        _, p_c, ncl = cluster_signflip(ok_ref[s], ok_cfg[s], clusters, n_perm=5000, seed=s)
        ps_cluster.append(p_c)
        ps_mc.append(mcnemar_exact(ok_ref[s], ok_cfg[s])[2])
    cnt = np.stack([cluster_counts(yt, p.astype(int), clusters) for p in P[key]])
    bs = cluster_bootstrap({"ref": cnt_ref, "cfg": cnt}, cnt_ref.shape[1], B=20000, seed=1)
    d = (bs["cfg"] - bs["ref"]) * 100
    rows.append(dict(group=grp, config=nm, key=key, f1=[float(f.mean()), float(f.std(ddof=1))],
                     delta=float(f.mean() - ref.mean()), ci=[float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],
                     p_pair_seed0=ps_mc[0], p_pair_median=float(np.median(ps_mc)),
                     p_cluster_median=float(np.median(ps_cluster)), p_cluster_max=float(np.max(ps_cluster)), p_boot=boot_p(d),
                     n_clusters=int(ncl)))
    pv.append(boot_p(d))
adj = holm(pv)
for r, a in zip(rows, adj):
    r["p_cluster_holm"] = float(a)
    r["p_boot_holm"] = float(a)
out["ablation"] = rows

# ----------------------------------------------------------------- 2. realised thresholds + sensitivity
Rg_v, Rg_t = R["val__gate"], R["test__gate"]
T0 = adaptive_thresholds(Rg_v[0], yv, va.D_lang.values, va.cc1.values, te.D_lang.values, te.cc1.values)
simple = te.cc1.values <= 5
tinfo = {"n_pairs": int(len(T0)), "min": float(T0.min()), "median": float(np.median(T0)),
         "mean": float(T0.mean()), "max": float(T0.max()),
         "frac_at_lower_clamp": float((T0 <= 0.4 + 1e-9).mean()), "frac_at_upper_clamp": float((T0 >= 0.8 - 1e-9).mean()),
         "frac_simple": float(simple.mean()),
         "by_class": {}, "val_tuned_threshold_gate": [float(tune_threshold(Rg_v[s], yv)) for s in SEEDS]}
for nm, m in (("simple", simple), ("complex", ~simple), ("same_language", te.D_lang.values == 0),
              ("cross_language", te.D_lang.values == 1)):
    if m.sum():
        tinfo["by_class"][nm] = dict(n=int(m.sum()), median=float(np.median(T0[m])), min=float(T0[m].min()), max=float(T0[m].max()))
cc_all = te.cc1.values
tinfo["cc_quartiles_reference_snippet"] = [float(x) for x in np.percentile(cc_all, [25, 50, 75, 100])]
out["thresholds"] = tinfo
grid = []
for ks in (1.2, 1.5, 1.8, 2.1):
    for cut in (3, 5, 8, 10):
        for lo, hi in ((0.40, 0.80), (0.30, 0.90), (0.50, 0.70)):
            ms = []
            for s in SEEDS:
                T = adaptive_thresholds(Rg_v[s], yv, va.D_lang.values, va.cc1.values, te.D_lang.values,
                                        te.cc1.values, k_simple=ks, k_complex=ks - 0.6, cc_cut=cut, lo=lo, hi=hi)
                ms.append(metrics(yt, (Rg_t[s] >= T).astype(int)))
            grid.append(dict(k_simple=ks, k_complex=round(ks - 0.6, 2), cc_cut=cut, clamp=[lo, hi],
                             acc=float(np.mean([m["acc"] for m in ms])), f1=float(np.mean([m["f1"] for m in ms])),
                             recall=float(np.mean([m["recall"] for m in ms])), fpr=float(np.mean([m["fpr"] for m in ms]))))
out["sensitivity"] = grid
g = {k: np.array([x[k] for x in grid]) for k in ("acc", "f1", "recall", "fpr")}
out["sensitivity_range"] = {k: [float(v.min()), float(v.max())] for k, v in g.items()}

# ----------------------------------------------------------------- 3. operating points
ens = {nm: R["test__" + nm].mean(0) for nm in ("gate", "direct", "static", "codebert", "token", "ast")}
ens_v = {nm: R["val__" + nm].mean(0) for nm in ens}
ops = {}
for nm in ("gate", "direct", "token", "codebert", "static"):
    st, sv = ens[nm], ens_v[nm]
    rows_ = []
    for budget in (0.01, 0.05, 0.10):
        negs = np.sort(sv[yv == 0])[::-1]
        thr = negs[int(np.floor(budget * len(negs)))] + 1e-9 if int(np.floor(budget * len(negs))) < len(negs) else 1.0
        m = metrics(yt, (st >= thr).astype(int))
        rows_.append(dict(kind="fpr_budget_val", budget=budget, threshold=float(thr), recall=m["recall"],
                          precision=m["precision"], fpr=m["fpr"], f1=m["f1"]))
    for rec_t in (0.80, 0.90):
        pos = np.sort(sv[yv == 1])
        thr = pos[int(np.floor((1 - rec_t) * len(pos)))]
        m = metrics(yt, (st >= thr).astype(int))
        rows_.append(dict(kind="recall_target_val", budget=rec_t, threshold=float(thr), recall=m["recall"],
                          precision=m["precision"], fpr=m["fpr"], f1=m["f1"]))
    ops[nm] = rows_
out["operating_points"] = ops
plt.figure(figsize=(4.2, 3.4))
for nm, lab in (("gate", "Gating network"), ("direct", "Direct classifier"), ("token", "Token only"),
                ("codebert", "CodeBERT only"), ("static", "Static averaging")):
    st = ens[nm]
    ts = np.unique(np.quantile(st, np.linspace(0, 1, 400)))
    pr, rc = [], []
    for t in ts:
        m = metrics(yt, (st >= t).astype(int))
        pr.append(m["precision"] if (m["tp"] + m["fp"]) else 1.0)
        rc.append(m["recall"])
    plt.plot(rc, pr, label=lab, lw=1.4)
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.ylim(0.4, 1.01)
plt.grid(alpha=0.3)
plt.legend(fontsize=7, loc="lower left")
plt.tight_layout()
plt.savefig(os.path.join(RES, "pr_curves.png"), dpi=300)

# ----------------------------------------------------------------- 4. error analysis (gate, val rule, seed 0)
p0 = P["gate|val"][0].astype(bool)
fn = (yt == 1) & ~p0
fp = (yt == 0) & p0
ea = {"n_fn": int(fn.sum()), "n_fp": int(fp.sum()), "fn_by_slice": {}, "fp_by_dlang": {}, "fp_by_lang": {}}
for s in ("exact", "renamed", "refactored", "cross-language"):
    m = (te.slice == s).values
    ea["fn_by_slice"][s] = [int((fn & m).sum()), int(m.sum())]
for dl in (0, 1):
    m = (yt == 0) & (te.D_lang.values == dl)
    ea["fp_by_dlang"][str(dl)] = [int((fp & m).sum()), int(m.sum())]
for l in ("java", "python", "c", "csharp"):
    m = (yt == 0) & (te.lang1.values == l) & (te.lang2.values == l)
    ea["fp_by_lang"][l] = [int((fp & m).sum()), int(m.sum())]
ea["fn_median_S"] = {k: float(np.median(te.loc[fn, k])) for k in ("S_CodeBERT", "S_AST", "S_Token")}
ea["fp_median_S"] = {k: float(np.median(te.loc[fp, k])) for k in ("S_CodeBERT", "S_AST", "S_Token")}
ea["tp_median_S"] = {k: float(np.median(te.loc[(yt == 1) & p0, k])) for k in ("S_CodeBERT", "S_AST", "S_Token")}
ea["tn_median_S"] = {k: float(np.median(te.loc[(yt == 0) & ~p0, k])) for k in ("S_CodeBERT", "S_AST", "S_Token")}
ea["fn_median_ntok"] = float(np.median(te.loc[fn, ["ntok1", "ntok2"]].min(axis=1)))
ea["all_median_ntok"] = float(np.median(te[["ntok1", "ntok2"]].min(axis=1)))
out["error_analysis"] = ea
# mean routing weights by slice
W = R["test__gate_w"].mean(0)
out["mean_weights"] = {s: [float(x) for x in W[(te.slice == s).values].mean(0)]
                       for s in ["exact", "renamed", "refactored", "cross-language", NEG_SLICE]}
from sklearn.metrics import roc_auc_score  # noqa: E402
out["auc"] = {nm: float(roc_auc_score(yt, R["test__" + nm].mean(0))) for nm in ("gate", "direct", "static", "codebert", "ast", "token", "logreg")}
fpr_seed = {}
for dl, nmx in ((0, "same_language"), (1, "cross_language")):
    m_ = (yt == 0) & (te.D_lang.values == dl)
    v_ = [float(q[m_].mean()) for q in P["gate|val"]]
    fpr_seed[nmx] = dict(mean=float(np.mean(v_)), min=float(np.min(v_)), max=float(np.max(v_)))
out["gate_fpr_by_dlang_over_seeds"] = fpr_seed
out["effective_clusters_ablation"] = [r["n_clusters"] for r in rows]
out["n_clusters_test"] = int(len(set(clusters)))
out["aux_flag_gate"] = float((R["aux__gate"][0] >= tune_threshold(R["val__gate"][0], yv)).mean())
with open(os.path.join(RES, "post_analysis.json"), "w") as f:
    json.dump(out, f, indent=1)
print("regime", REGIME)
print("gate F1 %.1f +- %.1f" % tuple(out["gate_f1"]))
for r in rows:
    print("%-16s %-34s F1 %5.1f  d %+5.1f [%+.1f,%+.1f]  p_pair %.1e  p_cl %.1e holm %.1e" % (
        r["group"], r["config"], r["f1"][0], r["delta"], r["ci"][0], r["ci"][1], r["p_pair_median"],
        r["p_cluster_median"], r["p_cluster_holm"]))
print("thresholds", json.dumps({k: v for k, v in tinfo.items() if k != "by_class"}))
print("sensitivity range", out["sensitivity_range"])
