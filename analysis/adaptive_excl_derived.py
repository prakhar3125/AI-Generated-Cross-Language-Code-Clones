"""N1 check: the cohort adaptive threshold of analyze_cohorts.py computes mu, sigma over the honest pairs AND all pairs of the derived submission
(allp = hh + dm), so the judged derived pair contributes to its own threshold. Recompute detection / false-flag share (mean-fusion gate, regime A,
the setting of tab:cohort-thr) with mu, sigma over the honest pairs only, and over the honest pairs plus the derived submission's non-derived pairs
(no derived pair). Reads saved scores only; no training. python -I adaptive_excl_derived.py"""
import os, pickle, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE

P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv")); M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv"))
S = pd.read_csv(os.path.join(DATA, "cohort_subs.csv")); F = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
C = pickle.load(open(os.path.join(HERE, "results_A", "cohort_scores.pkl"), "rb"))
honest = {g: set(G[G.role == "honest"].id) for g, G in S.groupby("group")}
cc_med = {g: float(np.median([F[k]["cc"] for k in G[G.role == "honest"].key])) for g, G in S.groupby("group")}
M["ds"] = np.where(M.group.str.startswith("Progpedia"), "PROGpedia", "IR-Plag")
idx = {}
for g, G in P.groupby("group"):
    h = honest[g]; hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
    for d in M[M.group == g].itertuples():
        dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
        nd = np.array([i for i in dm if i != d.derived_pair and not ((P.id1[i] == d.src) or (P.id2[i] == d.src))])
        dp = int(P.index[P.pair_id == d.derived_pair][0])
        idx[(d.group, d.derived)] = (dp, np.concatenate([hh, nd]), hh, np.concatenate([hh, dm]), np.concatenate([hh, np.array([i for i in dm if i != dp])]))
for label, key in (("gate|plain", "plain"), ("gate|filt", "filt")):
    sc = C["scores"]["gate"][key]
    print("== mean-fusion gate, regime A,", key)
    for calib, pos in (("all pairs incl. derived (as in tab:cohort-thr)", 3), ("honest + derived submission's other pairs", 4), ("honest pairs only", 2)):
        res = {"PROGpedia": [[], []], "IR-Plag": [[], []]}
        for i, d in enumerate(M.itertuples()):
            dp, nd, hh, allp, ex = idx[(d.group, d.derived)]
            cal = {2: hh, 3: allp, 4: ex}[pos]
            k = 1.8 if cc_med[d.group] <= 5 else 1.2
            det, ff = [], []
            for s in range(sc.shape[0]):
                x = sc[s, cal]; t = float(np.clip(x.mean() + k * x.std(), 0.40, 0.80))
                det.append(float(sc[s, dp] >= t)); ff.append(float((sc[s, nd] >= t).mean()))
            res[d.ds][0].append(np.mean(det)); res[d.ds][1].append(np.mean(ff))
        print("  %-48s PROGpedia det %.3f false %.3f | IR-Plag det %.3f false %.3f" % (calib, np.mean(res["PROGpedia"][0]), np.mean(res["PROGpedia"][1]), np.mean(res["IR-Plag"][0]), np.mean(res["IR-Plag"][1])))
