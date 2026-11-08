# -*- coding: utf-8 -*-
"""Frozen models (trained on the benchmark train split) scored on every pair of the cohort sets.

Feature variants of every pair:  plain  (as in the main evaluation)
                                 filt   (assignment boilerplate removed per cohort, no retraining: token 5-grams present in
                                         more than half of the honest submissions are dropped; the honest mean embedding is
                                         subtracted before the cosine)

REGIME=A|B|C [SEM=ux] python -I eval_cohorts.py -> results_<TAG>/cohort_scores.pkl
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
from exp_lib import REGIME, SC, SEEDS, SEM, TAG, X6, load, score, train_model, tune_threshold  # noqa: E402

RES = os.path.join(HERE, "results_" + TAG)
D = load()
tr, va = D["train"], D["val"]
summ = json.load(open(os.path.join(RES, "training_summary.json")))
LR, BS = summ["selected"]["lr"], summ["selected"]["batch"]
arr = lambda df, c: df[c].values.astype(np.float64)


def ux_emb():
    U = np.load(os.path.join(DATA, "unixcoder_emb_cohort.npz"))
    e = U["emb"] / np.clip(np.linalg.norm(U["emb"], axis=1, keepdims=True), 1e-9, None)
    return {k: e[i] for i, k in enumerate(U["keys"])}


def featurize(P, F, subs, variant, UX):
    honest = {g: G[G.role == "honest"].key.tolist() for g, G in subs.groupby("group")}
    prep = {}
    for g, ks in honest.items():
        cnt = collections.Counter()
        for k in ks:
            cnt.update(F[k]["grams"])
        boiler = {x for x, c in cnt.items() if c > 0.5 * len(ks)} if variant == "filt" else set()
        mw = np.mean([F[k]["win"].mean(0) for k in ks], axis=0) if variant == "filt" else None
        mu = np.mean([UX[k] for k in ks], axis=0) if variant == "filt" else None
        prep[g] = (boiler, mw, mu)
    rows = []
    for r in P.itertuples():
        boiler, mw, mu = prep[r.group]
        a, b = F[r.key1], F[r.key2]
        if variant == "filt":
            a = dict(a, grams=a["grams"] - boiler, win=a["win"] - mw)
            b = dict(b, grams=b["grams"] - boiler, win=b["win"] - mw)
        s_c, s_a, s_t = sem(a, b), ast_sim(a, b), tok_sim(a, b)
        if SEM == "ux":
            ua, ub = UX[r.key1], UX[r.key2]
            if variant == "filt":
                ua, ub = ua - mu, ub - mu
                ua = ua / max(np.linalg.norm(ua), 1e-9)
                ub = ub / max(np.linalg.norm(ub), 1e-9)
            s_c = float(np.clip(ua @ ub, 0.0, 1.0))
        rows.append((s_c, s_a, s_t, 0.0, abs(s_c - s_a), 1 - s_a, F[r.key1]["cc"]))
    f = pd.DataFrame(rows, columns=["S_CodeBERT", "S_AST", "S_Token", "D_lang", "S_CodeBERT_minus_S_AST", "one_minus_S_AST", "cc1"])
    return pd.concat([P.reset_index(drop=True).drop(columns=["D_lang"], errors="ignore"), f], axis=1)


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
    subs = pd.read_csv(os.path.join(DATA, "cohort_subs.csv"))
    F = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
    UX = ux_emb()
    sets = {v: featurize(P, F, subs, v, UX) for v in ("plain", "filt")}
    with Pool(8) as p:
        res = p.map(job, [(k, s, sets) for k in ("gate", "direct") for s in SEEDS])
    yv = va.label.values
    out = {"pair_id": P.pair_id.values, "scores": {}, "thr": {}, "cc": sets["plain"].cc1.values}
    for kind in ("gate", "direct"):
        rs = [r for r in res if r[0] == kind]
        out["thr"][kind] = np.array([tune_threshold(r[2], yv) for r in rs])
        out["scores"][kind] = {v: np.vstack([r[3][v] for r in rs]) for v in sets}
    for nm, c in (("token", 2), ("static", None), ("codebert", 0), ("ast", 1)):
        out["thr"][nm] = np.array([tune_threshold((arr(va, SC).mean(1) if c is None else arr(va, SC)[:, c]), yv)])
        out["scores"][nm] = {v: np.tile((arr(sets[v], SC).mean(1) if c is None else arr(sets[v], SC)[:, c]), (1, 1)) for v in sets}
    pickle.dump(out, open(os.path.join(RES, "cohort_scores.pkl"), "wb"))
    print(TAG, "saved", {k: v["plain"].shape for k, v in out["scores"].items()})
