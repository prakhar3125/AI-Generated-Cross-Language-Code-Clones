# -*- coding: utf-8 -*-
"""Frozen models (trained on the benchmark train split) on two external pair sets.

  progpedia    real student programs: same-author attempts (derived by the same person) vs cross-author pairs
               (independent work + unknown copying); full files, no boilerplate stripping
  convergence  same-name algorithmic functions by different authors inside the benchmark
               (independent convergence: same task, no derivation)

REGIME=A|B python -I eval_external.py -> results_<R>/external.json
"""
import json
import os
import pickle
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE  # noqa: E402
from compute_pair_features import pair_features  # noqa: E402
from exp_lib import REGIME, SC, SEEDS, SEM, TAG, X6, load, score, train_model, tune_threshold  # noqa: E402

RES = os.path.join(HERE, "results_" + TAG)
D = load()
tr, va = D["train"], D["val"]
summ = json.load(open(os.path.join(RES, "training_summary.json")))
LR, BS = summ["selected"]["lr"], summ["selected"]["batch"]
arr = lambda df, c: df[c].values.astype(np.float64)


def ux_override(f, emb_file):
    U = np.load(os.path.join(DATA, emb_file))
    keys, emb = U["keys"], U["emb"]
    emb = emb / np.clip(np.linalg.norm(emb, axis=1, keepdims=True), 1e-9, None)
    idx = {k: i for i, k in enumerate(keys)}
    a = emb[[idx[k] for k in f.key1]]
    b = emb[[idx[k] for k in f.key2]]
    f["S_CodeBERT"] = np.clip((a * b).sum(1), 0.0, 1.0)
    f["S_CodeBERT_minus_S_AST"] = (f["S_CodeBERT"] - f["S_AST"]).abs()
    return f


def featurize(pairs, F):
    rows = []
    for r in pairs.itertuples():
        a, b = F[r.key1], F[r.key2]
        s = pair_features(a, b)
        rows.append((s[0], s[1], s[2], 0.0, abs(s[0] - s[1]), 1 - s[1], a["cc"]))
    f = pd.DataFrame(rows, columns=["S_CodeBERT", "S_AST", "S_Token", "D_lang", "S_CodeBERT_minus_S_AST", "one_minus_S_AST", "cc1"])
    return pd.concat([pairs.reset_index(drop=True).drop(columns=["D_lang"], errors="ignore"), f], axis=1)


def job(a):
    kind, seed, sets = a
    routing = kind == "gate"
    m, _, _ = train_model(arr(tr, X6), arr(tr, SC), tr.label.values, arr(va, X6), arr(va, SC), va.label.values, seed, routing, LR, BS)
    sv = score(m, arr(va, X6), arr(va, SC), routing)[0]
    return kind, seed, sv, {k: score(m, arr(d, X6), arr(d, SC), routing)[0] for k, d in sets.items()}


if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    pg = pd.read_csv(os.path.join(DATA, "progpedia_pairs.csv"))
    cv = pd.read_csv(os.path.join(DATA, "convergence_pairs.csv"))
    Fp = pickle.load(open(os.path.join(DATA, "progpedia_feats.pkl"), "rb"))
    Fb = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
    sets = {"progpedia": featurize(pg, Fp), "convergence": featurize(cv, Fb)}
    if SEM == "ux":
        sets["progpedia"] = ux_override(sets["progpedia"], "unixcoder_emb_progpedia.npz")
        sets["convergence"] = ux_override(sets["convergence"], "unixcoder_emb.npz")
    with Pool(8) as p:
        res = p.map(job, [(k, s, sets) for k in ("gate", "direct") for s in SEEDS])
    yv = va.label.values
    scores = {}
    for kind in ("gate", "direct"):
        rs = [r for r in res if r[0] == kind]
        scores[kind] = (np.vstack([r[2] for r in rs]), {k: np.vstack([r[3][k] for r in rs]) for k in sets})
    for nm, c in (("token", 2), ("static", None), ("codebert", 0), ("ast", 1)):
        def raw(df):
            S = arr(df, SC)
            return S.mean(1) if c is None else S[:, c]
        scores[nm] = (np.tile(raw(va), (8, 1)), {k: np.tile(raw(d), (8, 1)) for k, d in sets.items()})
    # JPlag flags at the validation-tuned threshold of the main evaluation
    ev = json.load(open(os.path.join(RES, "main_eval.json")))
    thr_j = {c: ev["thresholds"]["%s|val" % c][0] for c in ("jplag", "tokennorm")}
    out = {"regime": REGIME}
    jp = {}
    jsim = {}
    for ds, f in (("progpedia", "jplag_progpedia.csv"), ("convergence", "jplag_convergence.csv")):
        pth = os.path.join(DATA, f)
        if os.path.exists(pth):
            j = pd.read_csv(pth)
            for cond, nm in (("plain", "jplag"), ("norm", "tokennorm")):
                sub = j[j.cond == cond].set_index("pair_id").sim
                plain = j[j.cond == "plain"].set_index("pair_id").sim
                d = sets[ds]
                simv = np.array([(sub.get(p, np.nan) if p in sub.index else plain.get(p, np.nan)) for p in d.pair_id], float)
                jp[(ds, nm)] = np.nan_to_num(simv, nan=0.0) >= thr_j[nm]
                jsim[(ds, nm)] = np.nan_to_num(simv, nan=0.0)
    for nm, (sv, sd) in scores.items():
        out[nm] = {}
        for ds, d in sets.items():
            flags = np.vstack([sd[ds][s] >= tune_threshold(sv[s], yv) for s in range(8)])
            out[nm][ds] = summarise = None
            if ds == "progpedia":
                lab = d.label.values
                lang = d.lang1.values
                r = {}
                for lg in ("all", "java", "python", "c"):
                    m = np.ones(len(d), bool) if lg == "all" else (lang == lg)
                    rec = flags[:, m & (lab == 1)].mean(1)
                    fr = flags[:, m & (lab == 0)].mean(1)
                    r[lg] = dict(recall_same_author=[float(rec.mean()), float(rec.std(ddof=1))],
                                 flag_rate_cross_author=[float(fr.mean()), float(fr.std(ddof=1))],
                                 n_pos=int((m & (lab == 1)).sum()), n_neg=int((m & (lab == 0)).sum()))
                out[nm][ds] = r
            else:
                fr = flags.mean(1)
                out[nm][ds] = dict(flag_rate=[float(fr.mean()), float(fr.std(ddof=1))], n=int(len(d)))
    for (ds, nm), fl in jp.items():
        d = sets[ds]
        if ds == "progpedia":
            lab = d.label.values
            r = {}
            for lg in ("all", "java", "python", "c"):
                m = np.ones(len(d), bool) if lg == "all" else (d.lang1.values == lg)
                r[lg] = dict(recall_same_author=[float(fl[m & (lab == 1)].mean()), 0.0], flag_rate_cross_author=[float(fl[m & (lab == 0)].mean()), 0.0],
                             n_pos=int((m & (lab == 1)).sum()), n_neg=int((m & (lab == 0)).sum()))
            out.setdefault(nm, {})[ds] = r
        else:
            out.setdefault(nm, {})[ds] = dict(flag_rate=[float(fl.mean()), 0.0], n=int(len(d)))
    from sklearn.metrics import roc_auc_score
    d = sets["progpedia"]
    lab = d.label.values
    out["auc_progpedia"] = {}
    for nm, (sv, sd) in scores.items():
        ens = sd["progpedia"].mean(0)
        out["auc_progpedia"][nm] = {lg: float(roc_auc_score(lab[m], ens[m])) for lg in ("all", "java", "python", "c")
                                    for m in [np.ones(len(d), bool) if lg == "all" else (d.lang1.values == lg)]}
    for (ds, nm), v in jsim.items():
        if ds == "progpedia":
            out["auc_progpedia"][nm] = {lg: float(roc_auc_score(lab[m], v[m])) for lg in ("all", "java", "python", "c")
                                        for m in [np.ones(len(d), bool) if lg == "all" else (d.lang1.values == lg)]}
    json.dump(out, open(os.path.join(RES, "external.json"), "w"), indent=1)
    for nm in ("gate", "direct", "token", "static", "jplag", "tokennorm"):
        if nm in out:
            print(REGIME, nm, "PG all", {k: round(v[0] * 100, 1) for k, v in out[nm]["progpedia"]["all"].items() if k in ("recall_same_author", "flag_rate_cross_author")},
                  "CV", round(out[nm]["convergence"]["flag_rate"][0] * 100, 1))
