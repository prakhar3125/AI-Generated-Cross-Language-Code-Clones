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
from exp_lib import REGIME, SC, SEEDS, X4, X6, load, metrics, score, train_model, tune_threshold, wilson

RES = os.path.join(HERE, "results_" + REGIME)
D = load(); tr, va = D["train"], D["val"]
summ = json.load(open(os.path.join(RES, "training_summary.json")))
LR, BS = summ["selected"]["lr"], summ["selected"]["batch"]
pp = pd.read_csv(os.path.join(DATA, "probe_pairs.csv"))
F = pickle.load(open(os.path.join(DATA, "probe_feats.pkl"), "rb"))
feat = []
for r in pp.itertuples():
    s = pair_features(F[r.key1], F[r.key2]); feat.append(s)
pp[["S_CodeBERT", "S_AST", "S_Token"]] = np.array(feat)
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
    for nm, (v, t) in sysscores.items():
        out[nm] = {}
        for gen in ("gpt3", "gpt4"):
            m = (pp.gen == gen).values
            rec, fpr = [], []
            for s in range(8):
                thr = tune_threshold(v[s], yv)
                p_ = t[s][m] >= thr
                rec.append(p_[y[m] == 1].mean()); fpr.append(p_[y[m] == 0].mean())
            npos = int((y[m] == 1).sum()); nneg = int((y[m] == 0).sum())
            out[nm][gen] = dict(recall=[float(np.mean(rec)), float(np.std(rec, ddof=1))], fpr=[float(np.mean(fpr)), float(np.std(fpr, ddof=1))],
                                n_pos=npos, n_neg=nneg, recall_wilson=wilson(int(round(np.mean(rec) * npos)), npos))
        # paired GPT-3 vs GPT-4 on identical problems: detection-rate difference
    g3 = pp[(pp.gen == "gpt3") & (pp.label == 1)].set_index(["row", "lang2"]); g4 = pp[(pp.gen == "gpt4") & (pp.label == 1)].set_index(["row", "lang2"])
    out["mean_scores_pos"] = {gen: {c: float(pp[(pp.gen == gen) & (pp.label == 1)][c].mean()) for c in SC} for gen in ("gpt3", "gpt4")}
    out["mean_scores_neg"] = {gen: {c: float(pp[(pp.gen == gen) & (pp.label == 0)][c].mean()) for c in SC} for gen in ("gpt3", "gpt4")}
    out["n_problems"] = int(pp.row.nunique())
    json.dump(out, open(os.path.join(RES, "probe.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("retrain_check_max_abs_diff_val", "n_problems")}))
    for nm in ("gate", "direct", "static", "codebert", "token"):
        print(nm, {g: (round(out[nm][g]["recall"][0], 3), round(out[nm][g]["fpr"][0], 3)) for g in ("gpt3", "gpt4")})
