"""Rank of the derived pair and hit@k from the released cohort scores (no training), plus the per-student
false-flag burden of an honest cohort. Regime A. python -I cohort_rank_at_k.py"""
import json, os, pickle, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE
RES = os.path.join(HERE, "results_A")
P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv")); M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv"))
S = pd.read_csv(os.path.join(DATA, "cohort_subs.csv"))
C = pickle.load(open(os.path.join(RES, "cohort_scores.pkl"), "rb"))
J = pd.read_csv(os.path.join(DATA, "jplag_cohort.csv")); DOL = pd.read_csv(os.path.join(DATA, "dolos_cohort.csv"))
honest = {g: set(G[G.role == "honest"].id) for g, G in S.groupby("group")}
M["ds"] = np.where(M.group.str.startswith("Progpedia"), "PROGpedia", "IR-Plag")
idx = {}
for g, G in P.groupby("group"):
    h = honest[g]; hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
    for d in M[M.group == g].itertuples():
        dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
        nd = np.array([i for i in dm if i != d.derived_pair and not ((P.id1[i] == d.src) or (P.id2[i] == d.src))])
        idx[(g, d.derived)] = (int(P.index[P.pair_id == d.derived_pair][0]), np.concatenate([hh, nd]))
sysm = {"Gate, CodeBERT (plain)": C["scores"]["gate"]["plain"].mean(0), "Gate, CodeBERT (boilerplate removed)": C["scores"]["gate"]["filt"].mean(0),
        "Token k-gram (plain)": C["scores"]["token"]["plain"][0], "Token k-gram (boilerplate removed)": C["scores"]["token"]["filt"][0],
        "JPlag": J[J.cond == "plain"].set_index("pair_id").sim.reindex(P.pair_id).fillna(0).values,
        "Dolos default": DOL[DOL.cond == "default"].set_index("pair_id").sim.reindex(P.pair_id).fillna(0).values}
out = {}
print("cohorts:", M.ds.value_counts().to_dict(), " median non-derived pairs per cohort:", {ds: int(np.median([len(idx[(d.group, d.derived)][1]) for d in M[M.ds == ds].itertuples()])) for ds in M.ds.unique()})
for nm, sc in sysm.items():
    for ds in ("PROGpedia", "IR-Plag"):
        rk, fr = [], []
        for d in M[M.ds == ds].itertuples():
            dp, nd = idx[(d.group, d.derived)]
            r = 1 + (sc[nd] > sc[dp]).sum() + 0.5 * (sc[nd] == sc[dp]).sum()   # 1 = top, ties split
            rk.append(r); fr.append(r / (len(nd) + 1))
        rk = np.array(rk)
        out[(nm, ds)] = dict(n=len(rk), top1=float((rk <= 1).mean()), top5=float((rk <= 5).mean()), top10=float((rk <= 10).mean()),
                             med=float(np.median(rk)), medfrac=float(np.median(fr)))
        print("%-38s %-9s n=%3d  hit@1 %.3f hit@5 %.3f hit@10 %.3f | median rank %.1f (median fraction of cohort %.3f)" % ((nm, ds) + tuple(out[(nm, ds)][k] for k in ("n", "top1", "top5", "top10", "med", "medfrac"))))
# per-student burden at the label-free cohort rule (adaptive threshold) for the filtered gate
print("\nper-student false flags, honest pairs only, gate boilerplate-removed, adaptive cohort rule")
sc = C["scores"]["gate"]["filt"]
cc_med = {}
F = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
for g, G in S.groupby("group"):
    cc_med[g] = float(np.median([F[k]["cc"] for k in G[G.role == "honest"].key]))
for ds_name, pref in (("PROGpedia", "Progpedia"), ("IR-Plag", "IRPlag")):
    fr, flg, npairs, nst = [], [], 0, 0
    for g, G in P.groupby("group"):
        if not g.startswith(pref): continue
        h = honest[g]; hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
        x = sc.mean(0)[hh]; k = 1.8 if cc_med[g] <= 5 else 1.2
        # mean over seeds of per-seed rule, as in analyze_cohorts
        flagged = np.zeros(len(hh))
        for s in range(sc.shape[0]):
            xs = sc[s, hh]; t = float(np.clip(xs.mean() + k * xs.std(), 0.40, 0.80)); flagged += (xs >= t)
        flagged = flagged / sc.shape[0]
        ids = sorted(h); cnt = {i: 0.0 for i in ids}
        for j, pi in enumerate(hh):
            cnt[G.id1[pi]] += flagged[j]; cnt[G.id2[pi]] += flagged[j]
        v = np.array(list(cnt.values()))
        print("  %-9s group %-22s students %3d  flagged-pair share %.3f  students with >=1 flagged pair %.2f  mean flagged pairs/student %.2f" % (ds_name, g, len(ids), flagged.mean(), (v >= 0.5).mean(), v.mean()))
        fr.append(flagged.mean()); npairs += len(hh); nst += len(ids)
    print("  ", ds_name, "mean flagged-pair share across groups", np.mean(fr))
