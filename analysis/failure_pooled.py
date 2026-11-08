# -*- coding: utf-8 -*-
"""Failure analysis pooled over the eight seeds and per-language false-positive rates (regimes A and B).
REGIME=A|B python -I failure_pooled.py -> results_<R>/failure_pooled.json"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE  # noqa: E402
from exp_lib import REGIME, TAG, load  # noqa: E402

te = load()["test"]
P = np.load(os.path.join(HERE, "results_" + TAG, "preds.npz"))["gate|val"].astype(bool)
y = te.label.values
S, A, T = te.S_CodeBERT.values, te.S_AST.values, te.S_Token.values
rel = np.where(te.D_lang.values == 1, "cross", "same")
out = {"n_seeds": int(P.shape[0]), "per_seed": []}
slices = ["exact", "renamed", "refactored", "cross-language"]
fn_med, fp_med = [], []
for s in range(P.shape[0]):
    p = P[s]
    fn = (y == 1) & ~p
    fp = (y == 0) & p
    d = dict(seed=s, fn=int(fn.sum()), fp=int(fp.sum()),
             fn_by_slice={k: int((fn & (te.slice == k).values).sum()) for k in slices},
             fpr_cross=float(p[(y == 0) & (rel == "cross")].mean()), fpr_same=float(p[(y == 0) & (rel == "same")].mean()))
    for lg in ("java", "python", "c", "csharp"):
        m = (y == 0) & (rel == "same") & (te.lang1.values == lg)
        d["fpr_" + lg] = float(p[m].mean())
        d["n_neg_" + lg] = int(m.sum())
    out["per_seed"].append(d)
    fn_med.append((np.median(S[fn]), np.median(A[fn]), np.median(T[fn])))
    fp_med.append((np.median(S[fp]), np.median(T[fp])))
ps = out["per_seed"]
for k in ("fn", "fp", "fpr_cross", "fpr_same", "fpr_java", "fpr_python", "fpr_c", "fpr_csharp"):
    v = np.array([d[k] for d in ps], float)
    out[k] = dict(mean=float(v.mean()), min=float(v.min()), max=float(v.max()))
out["fn_by_slice_mean"] = {k: float(np.mean([d["fn_by_slice"][k] for d in ps])) for k in slices}
out["fn_median_scores_mean_over_seeds"] = dict(zip(("sem", "str", "tok"), [float(x) for x in np.mean(fn_med, 0)]))
out["fp_median_scores_mean_over_seeds"] = dict(zip(("sem", "tok"), [float(x) for x in np.mean(fp_med, 0)]))
neg_ok = (y == 0)
out["neg_median_token_correctly_rejected_seed0"] = float(np.median(T[neg_ok & ~P[0]]))
json.dump(out, open(os.path.join(HERE, "results_" + TAG, "failure_pooled.json"), "w"), indent=1)
print(REGIME, {k: out[k] for k in ("fn", "fp", "fpr_cross", "fpr_same", "fpr_java", "fpr_python", "fpr_c", "fpr_csharp")})
print(out["fn_by_slice_mean"], out["fn_median_scores_mean_over_seeds"], out["fp_median_scores_mean_over_seeds"])
