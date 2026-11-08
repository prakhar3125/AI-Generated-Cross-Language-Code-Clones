# -*- coding: utf-8 -*-
"""Frozen-model zero-shot probe on GPT-4 translations (see build_probe.py).

Retrains the gate / direct classifier exactly as run_experiments.py does (same seeds,
hyper-parameters read from training_summary.json; the retrained validation scores are
checked against the stored ones), freezes the validation-tuned threshold, and scores the
probe pairs.  REGIME=A|B python -I eval_probe.py
"""
import json, os, pickle, sys
from multiprocessing import Pool
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE
from compute_pair_features import pair_features
from exp_lib import REGIME, SC, SEEDS, SEM, TAG, X4, X6, load, metrics, score, train_model, tune_threshold, wilson

RES = os.path.join(HERE, "results_" + TAG)
D = load(); tr, va = D["train"], D["val"]
summ = json.load(open(os.path.join(RES, "training_summary.json")))
LR, BS = summ["selected"]["lr"], summ["selected"]["batch"]
pp = pd.read_csv(os.path.join(DATA, "probe2_pairs.csv"))
F = pickle.load(open(os.path.join(DATA, "probe2_feats.pkl"), "rb"))
feat = []
for r in pp.itertuples():
    s = pair_features(F[r.key1], F[r.key2]); feat.append(s)
pp[["S_CodeBERT", "S_AST", "S_Token"]] = np.array(feat)
if SEM == "ux":
    U = np.load(os.path.join(DATA, "unixcoder_emb_probe2.npz"))
    e = U["emb"] / np.clip(np.linalg.norm(U["emb"], axis=1, keepdims=True), 1e-9, None)
    ix = {k: i for i, k in enumerate(U["keys"])}
    pp["S_CodeBERT"] = np.clip([float(e[ix[a]] @ e[ix[b]]) for a, b in zip(pp.key1, pp.key2)], 0.0, 1.0)
pp["S_CodeBERT_minus_S_AST"] = (pp.S_CodeBERT - pp.S_AST).abs(); pp["one_minus_S_AST"] = 1 - pp.S_AST
pp["cc1"] = [F[k]["cc"] for k in pp.key1]
arr = lambda df, c: df[c].values.astype(np.float64)

def job(a):
    kind, seed = a
    routing = kind == "gate"
    m, _, _ = train_model(arr(tr, X6), arr(tr, SC), tr.label.values, arr(va, X6), arr(va, SC), va.label.values, seed, routing, LR, BS)
    return kind, seed, score(m, arr(va, X6), arr(va, SC), routing)[0], score(m, arr(pp, X6), arr(pp, SC), routing)[0]

if __name__ == "__main__":
    import torch; torch.set_num_threads(1)
    with Pool(8) as p:
        res = p.map(job, [(k, s) for k in ("gate", "direct") for s in SEEDS])
    stored = np.load(os.path.join(RES, "scores.npz"))
    out = {"retrain_check_max_abs_diff_val": {}}
    yv = va.label.values
    sysscores = {}
    for kind in ("gate", "direct"):
        rs = [r for r in res if r[0] == kind]
        v = np.vstack([r[2] for r in rs]); t = np.vstack([r[3] for r in rs])
        out["retrain_check_max_abs_diff_val"][kind] = float(np.abs(v - stored["val__" + kind]).max())
        sysscores[kind] = (v, t)
    S = arr(pp, SC); Sv = arr(va, SC)
    for nm, i in (("codebert", 0), ("ast", 1), ("token", 2)):
        sysscores[nm] = (np.tile(Sv[:, i], (8, 1)), np.tile(S[:, i], (8, 1)))
    sysscores["static"] = (np.tile(Sv.mean(1), (8, 1)), np.tile(S.mean(1), (8, 1)))
    y = pp.label.values
    gens = list(dict.fromkeys(pp.gen))
    for nm, (v, t) in sysscores.items():
        out[nm] = {}
        for gen in gens:
            for kind in ("translate", "refactor"):
                m = ((pp.gen == gen) & (pp.kind == kind)).values
                if m.sum() == 0:
                    continue
                rec, fpr = [], []
                for s_ in range(8):
                    thr = tune_threshold(v[s_], yv)
                    p_ = t[s_][m] >= thr
                    rec.append(p_[y[m] == 1].mean()); fpr.append(p_[y[m] == 0].mean())
                npos = int((y[m] == 1).sum()); nneg = int((y[m] == 0).sum())
                out[nm]["%s|%s" % (gen, kind)] = dict(recall=[float(np.mean(rec)), float(np.std(rec, ddof=1))], fpr=[float(np.mean(fpr)), float(np.std(fpr, ddof=1))],
                                                      n_pos=npos, n_neg=nneg, recall_wilson=wilson(int(round(np.mean(rec) * npos)), npos))
    out["n_pairs"] = {g: int((pp.gen == g).sum()) for g in gens}
    out["unixcoder_cosine"] = out.pop("codebert")      # the first expert is the UniXcoder cosine in these runs
    json.dump(out, open(os.path.join(RES, "probe2.json"), "w"), indent=1)
    print(json.dumps(out["retrain_check_max_abs_diff_val"]))
    for nm in ("gate", "direct", "static", "unixcoder_cosine", "token"):
        print(nm, {k: (round(v["recall"][0], 3), round(v["fpr"][0], 3)) for k, v in out[nm].items()})
