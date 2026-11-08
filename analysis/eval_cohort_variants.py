# -*- coding: utf-8 -*-
"""How the gate reacts to different ways of removing assignment boilerplate (robustness of the filter result).

variants of the gate's inputs (no retraining):
  plain      as in the main evaluation
  filt       token 5-grams in > half of the honest submissions dropped AND honest mean window embedding subtracted
  tok_only   token filter only, semantic score unchanged
  emb_only   embedding mean removal only, token score unchanged
  pooled     semantic score = cosine of the programs' window-mean embeddings after subtracting the honest mean (no top-3 window rule), token filtered

REGIME=A python -I eval_cohort_variants.py -> results_A/cohort_variants.json
"""
import collections
import json
import os
import pickle
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE  # noqa: E402
from compute_pair_features import ast_sim, sem, tok_sim  # noqa: E402
from exp_lib import REGIME, SC, SEEDS, TAG, X6, load, score, train_model, tune_threshold  # noqa: E402

assert TAG == "A"
RES = os.path.join(HERE, "results_" + TAG)
D = load()
tr, va = D["train"], D["val"]
summ = json.load(open(os.path.join(RES, "training_summary.json")))
LR, BS = summ["selected"]["lr"], summ["selected"]["batch"]
arr = lambda df, c: df[c].values.astype(np.float64)


def feats(P, F, subs):
    honest = {g: G[G.role == "honest"].key.tolist() for g, G in subs.groupby("group")}
    prep = {}
    for g, ks in honest.items():
        cnt = collections.Counter()
        for k in ks:
            cnt.update(F[k]["grams"])
        prep[g] = ({x for x, c in cnt.items() if c > 0.5 * len(ks)}, np.mean([F[k]["win"].mean(0) for k in ks], axis=0))
    rows = []
    for r in P.itertuples():
        boiler, mw = prep[r.group]
        a, b = F[r.key1], F[r.key2]
        af = dict(a, grams=a["grams"] - boiler, win=a["win"] - mw)
        bf = dict(b, grams=b["grams"] - boiler, win=b["win"] - mw)
        pa = a["win"].mean(0) - mw
        pb = b["win"].mean(0) - mw
        pooled = float(np.clip(pa @ pb / max(np.linalg.norm(pa) * np.linalg.norm(pb), 1e-9), 0, 1))
        rows.append(dict(sem_plain=sem(a, b), sem_filt=sem(af, bf), sem_pool=pooled, ast=ast_sim(a, b), tok_plain=tok_sim(a, b), tok_filt=tok_sim(af, bf), cc1=a["cc"]))
    return pd.DataFrame(rows)


def build(f, s, t):
    df = pd.DataFrame({"S_CodeBERT": f[s], "S_AST": f.ast, "S_Token": f[t], "D_lang": 0.0, "cc1": f.cc1})
    df["S_CodeBERT_minus_S_AST"] = (df.S_CodeBERT - df.S_AST).abs()
    df["one_minus_S_AST"] = 1 - df.S_AST
    return df


def job(a):
    kind, seed, sets = a
    routing = kind == "gate"
    m, _, _ = train_model(arr(tr, X6), arr(tr, SC), tr.label.values, arr(va, X6), arr(va, SC), va.label.values, seed, routing, LR, BS)
    sv = score(m, arr(va, X6), arr(va, SC), routing)[0]
    return kind, seed, sv, {k: score(m, arr(d, X6), arr(d, SC), routing)[0] for k, d in sets.items()}


if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv"))
    M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv"))
    subs = pd.read_csv(os.path.join(DATA, "cohort_subs.csv"))
    F = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
    f = feats(P, F, subs)
    sets = {"plain": build(f, "sem_plain", "tok_plain"), "filt": build(f, "sem_filt", "tok_filt"), "tok_only": build(f, "sem_plain", "tok_filt"),
            "emb_only": build(f, "sem_filt", "tok_plain"), "pooled": build(f, "sem_pool", "tok_filt")}
    with Pool(8) as p:
        res = p.map(job, [(k, s, sets) for k in ("gate", "direct") for s in SEEDS])
    # cohort AUROC
    honest = {g: set(G[G.role == "honest"].id) for g, G in subs.groupby("group")}
    M["ds"] = np.where(M.group.str.startswith("Progpedia"), "PROGpedia", "IR-Plag")
    idx = {}
    for g, G in P.groupby("group"):
        h = honest[g]
        hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
        for d in M[M.group == g].itertuples():
            dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
            nd = [i for i in dm if i != d.derived_pair and d.src not in (P.id1[i], P.id2[i])]
            idx[(g, d.derived)] = (int(P.index[P.pair_id == d.derived_pair][0]), np.concatenate([hh, np.array(nd, int)]))
    out = {}
    for kind in ("gate", "direct"):
        rs = [r for r in res if r[0] == kind]
        for v in sets:
            ens = np.vstack([r[3][v] for r in rs]).mean(0)
            au = []
            for d in M.itertuples():
                dp, nd = idx[(d.group, d.derived)]
                x = ens[nd]
                au.append((x < ens[dp]).mean() + 0.5 * (x == ens[dp]).mean())
            au = np.array(au)
            out["%s|%s" % (kind, v)] = {ds: float(au[(M.ds == ds).values].mean()) for ds in ("PROGpedia", "IR-Plag")}
    for v in ("plain", "tok_only", "emb_only", "pooled", "filt"):
        x = sets[v]
        for nm, c in (("token", "S_Token"), ("sem", "S_CodeBERT")):
            au = []
            for d in M.itertuples():
                dp, nd = idx[(d.group, d.derived)]
                s = x[c].values[nd]
                au.append((s < x[c].values[dp]).mean() + 0.5 * (s == x[c].values[dp]).mean())
            au = np.array(au)
            out["%s|%s" % (nm, v)] = {ds: float(au[(M.ds == ds).values].mean()) for ds in ("PROGpedia", "IR-Plag")}
    json.dump(out, open(os.path.join(RES, "cohort_variants.json"), "w"), indent=1)
    for k, v in out.items():
        print(k.ljust(18), {a: round(b, 3) for a, b in v.items()})
