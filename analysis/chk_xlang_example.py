"""Measured values for the Section III worked example: median expert scores of the cross-language positives of the
test partition and the regime-A gate's mean weights on them; plus the same-/cross-language gate FPR (regimes A, B).
python -I chk_xlang_example.py"""
import json, os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE
pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
x = pf[(pf.split == "test") & (pf.label == 1) & (pf.D_lang == 1)]
med = x[["S_CodeBERT", "S_AST", "S_Token"]].median()
print("cross-language test positives:", len(x))
print("median S_sem %.4f  S_str %.4f  S_syn %.4f ; mean S_syn %.4f" % (med.S_CodeBERT, med.S_AST, med.S_Token, x.S_Token.mean()))
w = np.array(json.load(open(os.path.join(HERE, "results_A", "post_analysis.json")))["mean_weights"]["cross-language"])
print("regime-A mean gate weights (sem,str,syn) on cross-language positives:", np.round(w, 4), "sum", round(w.sum(), 4))
v = np.array([med.S_CodeBERT, med.S_AST, med.S_Token])
print("fused (unrounded) %.4f | equal weights %.4f | token only %.4f" % (w @ v, v.mean(), v[2]))
r = np.round(w, 2); rv = np.round(v, 2)
print("fused (rounded inputs) %.4f | equal %.4f" % (r @ rv, rv.mean()))
for reg in "ABC":
    d = json.load(open(os.path.join(HERE, "results_%s" % reg, "post_analysis.json")))["gate_fpr_by_dlang_over_seeds"]
    print(reg, "gate FPR same-language %.4f cross-language %.4f" % (d["same_language"]["mean"], d["cross_language"]["mean"]))
