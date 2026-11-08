# -*- coding: utf-8 -*-
"""Cohort metrics from saved scores.

per cohort (one derived submission + the honest set of its assignment):
  AUROC     share of the cohort's non-derived pairs scored below the derived pair (ties 1/2)
  detection derived pair flagged;  false flags = share of non-derived pairs flagged
  thresholds: (i) validation threshold transferred from the benchmark, (ii) the label-free adaptive rule
              T = clamp(mu + k sigma, 0.40, 0.80), mu / sigma over all pairs of the cohort, k = 1.8 if the median
              cyclomatic complexity of the honest submissions is <= 5 else 1.2   (fused-score systems only)

REGIME=A|B|C [SEM=ux] python -I analyze_cohorts.py -> results_<TAG>/cohort_eval.json
"""
import json
import os
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE  # noqa: E402
from exp_lib import TAG  # noqa: E402

RES = os.path.join(HERE, "results_" + TAG)
P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv"))
M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv"))
S = pd.read_csv(os.path.join(DATA, "cohort_subs.csv"))
F = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
C = pickle.load(open(os.path.join(RES, "cohort_scores.pkl"), "rb"))
J = pd.read_csv(os.path.join(DATA, "jplag_cohort.csv"))
ev = json.load(open(os.path.join(RES, "main_eval.json")))
assert (C["pair_id"] == P.pair_id.values).all()

honest = {g: set(G[G.role == "honest"].id) for g, G in S.groupby("group")}
cc_med = {g: float(np.median([F[k]["cc"] for k in G[G.role == "honest"].key])) for g, G in S.groupby("group")}
# cohort index sets
idx = {}
for g, G in P.groupby("group"):
    h = honest[g]
    hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
    for d in M[M.group == g].itertuples():
        dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
        nd_d = np.array([i for i in dm if i != d.derived_pair and not ((P.id1[i] == d.src) or (P.id2[i] == d.src))])
        idx[(g, d.derived)] = (int(P.index[P.pair_id == d.derived_pair][0]), np.concatenate([hh, nd_d]), np.concatenate([hh, dm]))
M["cluster"] = M.group + "|" + M.src
M["ds"] = np.where(M.group.str.startswith("Progpedia"), "PROGpedia", "IR-Plag")

systems = {}   # name -> (scores [S,n], thresholds [S], adaptive?)
for k in ("gate", "direct"):
    for v in ("plain", "filt"):
        systems["%s|%s" % (k, v)] = (C["scores"][k][v], C["thr"][k], True)
for k in ("token", "static", "codebert", "ast"):
    for v in ("plain", "filt"):
        systems["%s|%s" % (k, v)] = (C["scores"][k][v], C["thr"][k], False)
for cond, nm in (("plain", "jplag"), ("norm", "tokennorm")):
    sim = J[J.cond == cond].set_index("pair_id").sim.reindex(P.pair_id).fillna(0).values[None]
    systems[nm + "|plain"] = (sim, np.array([ev["thresholds"]["%s|val" % nm][0]]), False)
DOL = pd.read_csv(os.path.join(DATA, "dolos_cohort.csv"))
for cond in ("default", "m50", "m20"):
    sim = DOL[DOL.cond == cond].set_index("pair_id").sim.reindex(P.pair_id).fillna(0).values[None]
    systems["dolos_" + cond + "|plain"] = (sim, np.array([ev["thresholds"]["dolos|val"][0]]), False)


def auroc_vec(sc):
    out = np.zeros(len(M))
    for i, d in enumerate(M.itertuples()):
        dp, nd, _ = idx[(d.group, d.derived)]
        x = sc[nd]
        out[i] = (x < sc[dp]).mean() + 0.5 * (x == sc[dp]).mean()
    return out


def rates(sc, thr, adaptive):
    """sc [S,n]; returns det, ff (per cohort, averaged over seeds)"""
    det = np.zeros((sc.shape[0], len(M)))
    ff = np.zeros_like(det)
    for s in range(sc.shape[0]):
        for i, d in enumerate(M.itertuples()):
            dp, nd, allp = idx[(d.group, d.derived)]
            if adaptive:
                x = sc[s, allp]
                k = 1.8 if cc_med[d.group] <= 5 else 1.2
                t = float(np.clip(x.mean() + k * x.std(), 0.40, 0.80))
            else:
                t = thr[min(s, len(thr) - 1)]
            det[s, i] = sc[s, dp] >= t
            ff[s, i] = (sc[s, nd] >= t).mean()
    return det.mean(0), ff.mean(0)


rng = np.random.default_rng(0)
cl = M.cluster.values
ucl, inv = np.unique(cl, return_inverse=True)
boot = [rng.integers(0, len(ucl), len(ucl)) for _ in range(2000)]


def cboot(v):
    """cluster-bootstrap mean CI of a per-cohort vector (clusters = source submissions)"""
    sums = np.bincount(inv, weights=v, minlength=len(ucl))
    cnt = np.bincount(inv, minlength=len(ucl))
    m = np.array([sums[b].sum() / cnt[b].sum() for b in boot])
    return [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))], m


out = {"systems": {}, "n_cohorts": {ds: int((M.ds == ds).sum()) for ds in M.ds.unique()}}
V = {}
for nm, (sc, thr, ad) in systems.items():
    ens = sc.mean(0)
    V[nm] = auroc_vec(ens)
    det_t, ff_t = rates(sc, thr, False)
    r = {"auc": V[nm], "det_t": det_t, "ff_t": ff_t}
    if ad:
        r["det_a"], r["ff_a"] = rates(sc, thr, True)
    out["systems"][nm] = {}
    for ds in ("PROGpedia", "IR-Plag"):
        m = (M.ds == ds).values
        e = {}
        for key, vec in r.items():
            e[key] = float(vec[m].mean())
        kinds = {}
        for kd in M[m].kind.unique():
            mk = m & (M.kind == kd).values
            kinds[kd] = {key: float(vec[mk].mean()) for key, vec in r.items()}
        e["by_kind"] = kinds
        ci, _ = cboot(np.where(m, V[nm], np.nan)[m] if False else V[nm][m]) if False else (None, None)
        out["systems"][nm][ds] = e
# bootstrap CIs per dataset (clusters restricted to the dataset)
for ds in ("PROGpedia", "IR-Plag"):
    m = (M.ds == ds).values
    cl_d = M.cluster.values[m]
    u, iv = np.unique(cl_d, return_inverse=True)
    bs = [rng.integers(0, len(u), len(u)) for _ in range(2000)]
    cnt = np.bincount(iv, minlength=len(u))

    def stat(vec):
        sums = np.bincount(iv, weights=vec[m], minlength=len(u))
        return np.array([sums[b].sum() / cnt[b].sum() for b in bs])
    base = {nm: stat(V[nm]) for nm in V}
    for nm in V:
        out["systems"][nm][ds]["auc_ci"] = [float(np.percentile(base[nm], 2.5)), float(np.percentile(base[nm], 97.5))]
        for ref in ("jplag|plain", "token|plain", "token|filt"):
            dlt = base[nm] - base[ref]
            pv = 2 * min((dlt <= 0).mean(), (dlt >= 0).mean())
            out["systems"][nm][ds]["vs_" + ref.replace("|plain", "").replace("|", "")] = dict(delta=float(V[nm][m].mean() - V[ref][m].mean()),
                                                                     ci=[float(np.percentile(dlt, 2.5)), float(np.percentile(dlt, 97.5))], p=float(max(pv, 1 / 2000)))
np.savez(os.path.join(RES, "cohort_auc_vectors.npz"), clusters=(M.group + "|" + M.src).values, ds=M.ds.values,
         **{k.replace("|", "__"): v for k, v in V.items()})
json.dump(out, open(os.path.join(RES, "cohort_eval.json"), "w"), indent=1)
for nm in ("gate|plain", "gate|filt", "direct|plain", "token|plain", "token|filt", "codebert|plain", "codebert|filt", "static|plain", "ast|plain", "jplag|plain", "tokennorm|plain"):
    print(TAG, nm.ljust(16), {ds: round(out["systems"][nm][ds]["auc"], 3) for ds in ("PROGpedia", "IR-Plag")},
          {ds: (round(out["systems"][nm][ds]["det_t"], 2), round(out["systems"][nm][ds]["ff_t"], 3)) for ds in ("PROGpedia", "IR-Plag")})
