"""Mean gate weights of the UniXcoder-expert gate (mean fusion, trained on regime A, SEM=ux) on the real-code cohorts, derived versus honest pairs,
plain and boilerplate-removed inputs: is the trained "Gate, UniXcoder expert" row of tab:cohort a collapse onto the raw UniXcoder cosine?
Same pipeline as e6_weights_and_tasks.py (the CodeBERT gate). REGIME=A SEM=ux python -I ux_cohort_weights.py -> data/ux_cohort_weights_A.json"""
import json, os, sys
from multiprocessing import Pool
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_cohorts as ec
from common import DATA, HERE
from exp_lib import SC, SEEDS, SEM, X6, score, train_model

assert SEM == "ux", "run with SEM=ux"
P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv")); M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv")); S = pd.read_csv(os.path.join(DATA, "cohort_subs.csv"))
M["ds"] = np.where(M.group.str.startswith("Progpedia"), "PROGpedia", "IR-Plag")
arr = ec.arr

def wjob(a):
    seed, sets = a
    m, _, _ = train_model(arr(ec.tr, X6), arr(ec.tr, SC), ec.tr.label.values, arr(ec.va, X6), arr(ec.va, SC), ec.va.label.values, seed, True, ec.LR, ec.BS)
    return {k: score(m, arr(d, X6), arr(d, SC), True)[1] for k, d in sets.items()}

if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    honest = {g: set(G[G.role == "honest"].id) for g, G in S.groupby("group")}
    idx = {}
    for g, G in P.groupby("group"):
        h = honest[g]; hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
        for d in M[M.group == g].itertuples():
            dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
            nd = [i for i in dm if i != d.derived_pair and d.src not in (P.id1[i], P.id2[i])]
            idx[(g, d.derived)] = (int(P.index[P.pair_id == d.derived_pair][0]), np.concatenate([hh, np.array(nd, int)]))
    F = ec.pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb")); UXe = ec.ux_emb()
    sets = {v: ec.featurize(P, F, S, v, UXe) for v in ("plain", "filt")}
    with Pool(8) as p:
        res = p.map(wjob, [(s, sets) for s in SEEDS])
    out = {}
    for v in ("plain", "filt"):
        Wm = np.mean([r[v] for r in res], axis=0)
        for ds in ("PROGpedia", "IR-Plag"):
            dw, hw = [], []
            for i, d in enumerate(M.itertuples()):
                if M.ds[i] != ds: continue
                dp, nd = idx[(d.group, d.derived)]; dw.append(Wm[dp]); hw.append(Wm[nd].mean(0))
            out["%s|%s" % (v, ds)] = {"derived": [round(float(x), 3) for x in np.mean(dw, 0)], "honest": [round(float(x), 3) for x in np.mean(hw, 0)]}
            print(v, ds, out["%s|%s" % (v, ds)], flush=True)
    json.dump(out, open(os.path.join(DATA, "ux_cohort_weights_A.json"), "w"), indent=1)
