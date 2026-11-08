"""Diagnostic: is the post-fix collapse of the gate's PROGpedia cohort AUROC due to the selected batch size?
Retrains the regime-A gate (8 seeds) at lr=1e-3 and batch 16/32/64 on the corrected features and scores the plain cohort
pairs; also the direct classifier at the same settings. REGIME=A python -I diag_cohort_gate_bs.py"""
import json, os, pickle, sys
from multiprocessing import Pool
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE
import eval_cohorts as ec
from exp_lib import SC, SEEDS, X6

arr = ec.arr
P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv")); M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv"))
S = pd.read_csv(os.path.join(DATA, "cohort_subs.csv")); F = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
plain = ec.featurize(P, F, S, "plain", {})
hon = {g: set(G[G.role == "honest"].id) for g, G in S.groupby("group")}
idx = {}
for g, G in P.groupby("group"):
    h = hon[g]; hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
    for d in M[M.group == g].itertuples():
        dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
        nd = np.array([i for i in dm if i != d.derived_pair and not ((P.id1[i] == d.src) or (P.id2[i] == d.src))])
        idx[(g, d.derived)] = (int(P.index[P.pair_id == d.derived_pair][0]), np.concatenate([hh, nd]))
M["ds"] = np.where(M.group.str.startswith("Progpedia"), "PROGpedia", "IR-Plag")

def auc(sc, ds):
    v = []
    for d in M[M.ds == ds].itertuples():
        dp, nd = idx[(d.group, d.derived)]; x = sc[nd]; v.append((x < sc[dp]).mean() + .5 * (x == sc[dp]).mean())
    return float(np.mean(v))

def job(a):
    kind, bs, seed = a
    routing = kind == "gate"
    from exp_lib import train_model, score
    m, _, _ = train_model(arr(ec.tr, X6), arr(ec.tr, SC), ec.tr.label.values, arr(ec.va, X6), arr(ec.va, SC), ec.va.label.values, seed, routing, 1e-3, bs)
    return kind, bs, seed, score(m, arr(plain, X6), arr(plain, SC), routing)[0]

if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    with Pool(8) as p:
        res = p.map(job, [(k, bs, s) for k in ("gate", "direct") for bs in (16, 32, 64) for s in SEEDS])
    out = {}
    for kind in ("gate", "direct"):
        for bs in (16, 32, 64):
            r = [x for x in res if x[0] == kind and x[1] == bs]
            per = [auc(x[3], "PROGpedia") for x in sorted(r, key=lambda z: z[2])]
            ens = auc(np.mean([x[3] for x in r], 0), "PROGpedia")
            ir = auc(np.mean([x[3] for x in r], 0), "IR-Plag")
            out["%s|bs%d" % (kind, bs)] = dict(per_seed=[round(v, 3) for v in per], mean=round(float(np.mean(per)), 3), ensemble_prog=round(ens, 3), ensemble_irplag=round(ir, 3))
            print(kind, bs, out["%s|bs%d" % (kind, bs)], flush=True)
    json.dump(out, open(os.path.join(HERE, "results_A", "diag_cohort_gate_bs.json"), "w"), indent=1)
