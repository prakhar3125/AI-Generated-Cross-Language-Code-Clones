# -*- coding: utf-8 -*-
"""Sensitivity of the boilerplate filter: token expert cohort AUROC when 5-grams present in more than a fraction q of a cohort's
honest submissions are dropped (q = none, 0.9 ... 0.2), and when the filter is estimated from only n randomly chosen honest submissions.
python -I sens_filter.py -> results_A/sens_filter.json
"""
import collections
import json
import os
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE  # noqa: E402

P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv"))
M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv"))
S = pd.read_csv(os.path.join(DATA, "cohort_subs.csv"))
F = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
M["ds"] = np.where(M.group.str.startswith("Progpedia"), "PROGpedia", "IR-Plag")
honest = {g: G[G.role == "honest"] for g, G in S.groupby("group")}
hid = {g: set(G.id) for g, G in honest.items()}
idx = {}
for g, G in P.groupby("group"):
    h = hid[g]
    hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
    for d in M[M.group == g].itertuples():
        dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
        nd = [i for i in dm if i != d.derived_pair and d.src not in (P.id1[i], P.id2[i])]
        idx[(g, d.derived)] = (int(P.index[P.pair_id == d.derived_pair][0]), np.concatenate([hh, np.array(nd, int)]))


def run(q, n_est, rng):
    boiler = {}
    for g, H in honest.items():
        ks = list(H.key)
        if n_est and n_est < len(ks):
            ks = list(rng.choice(ks, n_est, replace=False))
        cnt = collections.Counter()
        for k in ks:
            cnt.update(F[k]["grams"])
        boiler[g] = {x for x, c in cnt.items() if c > q * len(ks)} if q is not None else set()
    sc = np.zeros(len(P))
    for i, r in enumerate(P.itertuples()):
        a = F[r.key1]["grams"] - boiler[r.group]
        b = F[r.key2]["grams"] - boiler[r.group]
        sc[i] = len(a & b) / len(a | b) if (a and b) else 0.0
    out = {}
    for ds in ("PROGpedia", "IR-Plag"):
        v = []
        for d in M[M.ds == ds].itertuples():
            dp, nd = idx[(d.group, d.derived)]
            x = sc[nd]
            v.append((x < sc[dp]).mean() + 0.5 * (x == sc[dp]).mean())
        out[ds] = float(np.mean(v))
    return out


rng = np.random.default_rng(0)
res = {"fraction": {}, "n_est": {}}
for q in (None, 0.9, 0.7, 0.5, 0.3, 0.2):
    res["fraction"]["none" if q is None else str(q)] = run(q, 0, rng)
    print("q", q, res["fraction"]["none" if q is None else str(q)], flush=True)
for n in (5, 8, 12):
    rr = [run(0.5, n, np.random.default_rng(s)) for s in range(5)]
    res["n_est"][str(n)] = {ds: [float(np.mean([r[ds] for r in rr])), float(np.std([r[ds] for r in rr], ddof=1))] for ds in ("PROGpedia", "IR-Plag")}
    print("n", n, res["n_est"][str(n)], flush=True)
json.dump(res, open(os.path.join(HERE, "results_A", "sens_filter.json"), "w"), indent=1)
