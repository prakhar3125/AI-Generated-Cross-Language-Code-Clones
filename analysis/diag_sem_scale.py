"""Is S_sem (Eq. 2) on one scale? Distribution by window-count class, benchmark vs cohorts, by label.
python -I diag_sem_scale.py"""
import os, pickle, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA
B = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
C = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv")); M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv"))
import compute_pair_features as cpf
def cls(n): return "1" if n == 1 else ("2" if n == 2 else "3+")
def q(x): return "n=%5d  p10 %.3f  p50 %.3f  p90 %.3f" % (len(x), *np.quantile(x, [.1, .5, .9])) if len(x) else "n=0"
print("== benchmark, train split, by (window class of the pair = max of the two) and label")
tr = pf[(pf.split == "train") & pf.slice.isin(["exact", "renamed", "refactored", "cross-language", "same-language", "independent"])].copy()
tr["w"] = [max(len(B[a]["win"]), len(B[b]["win"])) for a, b in zip(tr.key1, tr.key2)]
tr["wc"] = tr.w.map(lambda n: "both<=1" if n == 1 else ("max=2" if n == 2 else "max>=3"))
for wc in ("both<=1", "max=2", "max>=3"):
    for lab in (1, 0):
        print(" %-8s label %d  %s" % (wc, lab, q(tr[(tr.wc == wc) & (tr.label == lab)].S_CodeBERT.values)))
print("== cohorts (PROGpedia+IR-Plag), by window class and derived/non-derived")
s = np.array([cpf.sem(C[r.key1], C[r.key2]) for r in P.itertuples()])
w = np.array([max(len(C[r.key1]["win"]), len(C[r.key2]["win"])) for r in P.itertuples()])
der = P.pair_id.isin(M.derived_pair).values
for name, m in (("both<=1", w == 1), ("max=2", w == 2), ("max>=3", w >= 3)):
    print(" %-8s derived     %s" % (name, q(s[m & der])))
    print(" %-8s non-derived %s" % (name, q(s[m & ~der])))
print("window-class shares: benchmark train pairs", tr.wc.value_counts(normalize=True).round(3).to_dict(),
      "| cohort pairs", {"both<=1": round(float((w == 1).mean()), 3), "max=2": round(float((w == 2).mean()), 3), "max>=3": round(float((w >= 3).mean()), 3)})
