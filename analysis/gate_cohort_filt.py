"""Cohort screening of the mean-fusion gate, the log-odds gate and the direct classifier with and without label-free boilerplate removal
(same featurization as eval_cohorts.py: token 5-grams in more than half of a cohort's honest submissions dropped, cohort mean embedding
subtracted), plus the flag rates at the benchmark validation-tuned threshold. Per-cohort AUROC vectors are saved for paired tests.
REGIME=A|B|C python -I gate_cohort_filt.py -> results_<R>/gate_cohort_filt.json, gate_cohort_filt_vectors.npz"""
import json, os, pickle, sys
from multiprocessing import Pool
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_cohorts as ec
import gate_variants as gv
from common import DATA
from exp_lib import SC, SEEDS, TAG, tune_threshold

KINDS = ["base", "logit", "direct"]
P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv")); M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv"))
S = pd.read_csv(os.path.join(DATA, "cohort_subs.csv")); F = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
UX = ec.ux_emb()
SETS = {v: ec.featurize(P, F, S, v, UX) for v in ("plain", "filt")}

def job(a):
    kind, seed = a
    m = gv.train(kind, gv.design(gv.tr, kind, gv.EX), gv.tr[SC].values, gv.tr.label.values, gv.design(gv.va, kind, gv.EX), gv.va[SC].values, gv.va.label.values, seed, gv.LR, gv.BS)
    sv, _ = gv.predict(m, gv.design(gv.va, kind, gv.EX), gv.va[SC].values)
    thr = tune_threshold(sv, gv.va.label.values)
    return kind, seed, thr, {v: gv.predict(m, gv.design(d, kind, gv.EX), d[SC].values)[0] for v, d in SETS.items()}

def indices():
    hon = {g: set(G[G.role == "honest"].id) for g, G in S.groupby("group")}; idx = {}
    for g, G in P.groupby("group"):
        h = hon[g]; hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
        for d in M[M.group == g].itertuples():
            dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
            nd = np.concatenate([hh, np.array([i for i in dm if i != d.derived_pair and not ((P.id1[i] == d.src) or (P.id2[i] == d.src))])])
            idx[(g, d.derived)] = (int(P.index[P.pair_id == d.derived_pair][0]), nd, d.src)
    return idx

if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    idx = indices()
    def vec(sc):
        return np.array([((sc[nd] < sc[dp]).mean() + .5 * (sc[nd] == sc[dp]).mean()) for (g, dv), (dp, nd, src) in idx.items()])
    keys = list(idx); ds = np.array(["PROGpedia" if g.startswith("Progpedia") else "IR-Plag" for g, _ in keys]); cl = np.array([g + "|" + idx[(g, d)][2] for g, d in keys])
    with Pool(5) as pool:
        res = pool.map(job, [(k, s) for k in KINDS for s in SEEDS])
    out, vecs = {}, {"_ds": ds, "_cl": cl}
    for k in KINDS:
        r = sorted([x for x in res if x[0] == k], key=lambda z: z[1]); out[k] = {}
        for v in ("plain", "filt"):
            ens = np.mean([x[3][v] for x in r], 0); a = vec(ens); vecs["%s|%s" % (k, v)] = a
            flags = {"PROGpedia": [], "IR-Plag": []}
            for x in r:
                sc = x[3][v]
                for d_ in flags:
                    flags[d_].append(float(np.mean([(sc[nd] >= x[2]).mean() for i, ((g, dv), (dp, nd, src)) in enumerate(idx.items()) if ds[i] == d_])))
            out[k][v] = dict(prog=float(a[ds == "PROGpedia"].mean()), irplag=float(a[ds == "IR-Plag"].mean()),
                             false_flag_at_val_thr_prog=float(np.mean(flags["PROGpedia"])), false_flag_at_val_thr_irplag=float(np.mean(flags["IR-Plag"])))
        print(TAG, k, {v: (round(out[k][v]["prog"], 3), round(out[k][v]["irplag"], 3)) for v in ("plain", "filt")}, flush=True)
    for v in ("plain", "filt"):
        for nm, col in (("token", "S_Token"), ("ast", "S_AST")):
            a = vec(SETS[v][col].values); vecs["%s|%s" % (nm, v)] = a
            out.setdefault(nm, {})[v] = dict(prog=float(a[ds == "PROGpedia"].mean()), irplag=float(a[ds == "IR-Plag"].mean()))
    json.dump(out, open(os.path.join(gv.RES, "gate_cohort_filt.json"), "w"), indent=1)
    np.savez(os.path.join(gv.RES, "gate_cohort_filt_vectors.npz"), **vecs)
