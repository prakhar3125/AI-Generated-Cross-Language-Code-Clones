# -*- coding: utf-8 -*-
"""E6: (a) per-assignment / per-task cohort AUROC tables from the saved per-cohort vectors; (b) mean gate weights on derived versus honest pairs per dataset,
plain and boilerplate-removed inputs (diagnosis of the below-chance IR-Plag AUROC).
REGIME=A python -I e6_weights_and_tasks.py -> results_A/e6_cohort_detail.json"""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_cohorts as ec  # noqa: E402  (module level: loads the benchmark split and training summary)
from common import DATA, HERE  # noqa: E402
from exp_lib import SC, SEEDS, X6, score, train_model  # noqa: E402

RES = os.path.join(HERE, "results_A")
P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv"))
M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv"))
S = pd.read_csv(os.path.join(DATA, "cohort_subs.csv"))
M["ds"] = np.where(M.group.str.startswith("Progpedia"), "PROGpedia", "IR-Plag")
arr = ec.arr


def wjob(a):
    seed, sets = a
    m, _, _ = train_model(arr(ec.tr, X6), arr(ec.tr, SC), ec.tr.label.values, arr(ec.va, X6), arr(ec.va, SC), ec.va.label.values, seed, True, ec.LR, ec.BS)
    return {k: score(m, arr(d, X6), arr(d, SC), True)[1] for k, d in sets.items()}


if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    # (a) per-group AUROC from the saved vectors
    V = np.load(os.path.join(RES, "cohort_auc_vectors.npz"), allow_pickle=True)
    dol = json.load(open(os.path.join(DATA, "dolos_cohort_runs.json")))
    systems = {"Gate (CodeBERT)": V["gate__plain"], "Gate, boilerplate removed": V["gate__filt"], "Token only": V["token__plain"], "Token, boilerplate removed": V["token__filt"],
               "JPlag": V["jplag__plain"], "Dolos default": np.array(dol["vec_auc"]["default"]), "Dolos -M 0.5": np.array(dol["vec_auc"]["m50"])}
    detail = {"per_group": {}}
    for g in sorted(M.group.unique()):
        m = (M.group == g).values
        detail["per_group"][g] = {k: float(v[m].mean()) for k, v in systems.items()}
        detail["per_group"][g]["n_cohorts"] = int(m.sum())
    # (b) gate weights
    honest = {g: set(G[G.role == "honest"].id) for g, G in S.groupby("group")}
    idx = {}
    for g, G in P.groupby("group"):
        h = honest[g]
        hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
        for d in M[M.group == g].itertuples():
            dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
            nd = [i for i in dm if i != d.derived_pair and d.src not in (P.id1[i], P.id2[i])]
            idx[(g, d.derived)] = (int(P.index[P.pair_id == d.derived_pair][0]), np.concatenate([hh, np.array(nd, int)]))
    F = ec.pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
    UXe = ec.ux_emb()
    sets = {v: ec.featurize(P, F, S, v, UXe) for v in ("plain", "filt")}
    with Pool(8) as p:
        res = p.map(wjob, [(s, sets) for s in SEEDS])
    detail["weights"] = {}
    for v in ("plain", "filt"):
        Wm = np.mean([r[v] for r in res], axis=0)          # [pairs, 3] seed-averaged weights
        for ds in ("PROGpedia", "IR-Plag"):
            dw, hw = [], []
            for i, d in enumerate(M.itertuples()):
                if M.ds[i] != ds:
                    continue
                dp, nd = idx[(d.group, d.derived)]
                dw.append(Wm[dp])
                hw.append(Wm[nd].mean(0))
            detail["weights"]["%s|%s" % (v, ds)] = {"derived": [float(x) for x in np.mean(dw, 0)], "honest": [float(x) for x in np.mean(hw, 0)]}
    json.dump(detail, open(os.path.join(RES, "e6_cohort_detail.json"), "w"), indent=1)
    for g, d in detail["per_group"].items():
        print(g, {k: round(x, 3) for k, x in d.items()})
    for k, v in detail["weights"].items():
        print(k, {a: [round(x, 2) for x in b] for a, b in v.items()})
