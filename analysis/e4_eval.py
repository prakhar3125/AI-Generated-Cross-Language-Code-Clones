# -*- coding: utf-8 -*-
"""E4 (evaluate): frozen gate / direct classifier / experts on the original and A1-attacked same-language pairs.

For regime R the negatives are the sampled regime-A (REGIME=A) or regime-B (REGIME=B) same-language negatives; recall and FPR are at the frozen validation threshold,
AUROC and recall at 5% FPR use the pair set itself.  Gate weights are averaged over seeds and pairs, per class and variant.
REGIME=A|B [SEM=ux] python -I e4_eval.py -> results_<TAG>/e4_attack.json
"""
import json
import os
import pickle
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE  # noqa: E402
from compute_pair_features import pair_features  # noqa: E402
from exp_lib import REGIME, SC, SEEDS, SEM, TAG, X6, load, score, train_model, tune_threshold  # noqa: E402

RES = os.path.join(HERE, "results_" + TAG)
D = load()
tr, va = D["train"], D["val"]
summ = json.load(open(os.path.join(RES, "training_summary.json")))
LR, BS = summ["selected"]["lr"], summ["selected"]["batch"]
pairs = pd.read_csv(os.path.join(DATA, "e4_pairs.csv"))
pairs = pairs[pairs.kind.isin(["pos", "neg" + REGIME])].reset_index(drop=True)
F = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
FA = pickle.load(open(os.path.join(DATA, "e4_feats.pkl"), "rb"))
if SEM == "ux":
    U = np.load(os.path.join(DATA, "unixcoder_emb.npz"))
    UA = np.load(os.path.join(DATA, "unixcoder_emb_e4.npz"))
    e1, k1 = U["emb"], U["keys"]
    e2, k2 = UA["emb"], UA["keys"]
    UX = {k: e1[i] / max(np.linalg.norm(e1[i]), 1e-9) for i, k in enumerate(k1)}
    UX.update({k: e2[i] / max(np.linalg.norm(e2[i]), 1e-9) for i, k in enumerate(k2)})


def feats(variant):
    rows = []
    for r in pairs.itertuples():
        b = FA[r.akey2] if variant == "attacked" else F[r.key2]
        a = F[r.key1]
        s = list(pair_features(a, b))
        if SEM == "ux":
            s[0] = float(np.clip(UX[r.key1] @ UX[r.akey2 if variant == "attacked" else r.key2], 0, 1))
        rows.append(s + [0.0, abs(s[0] - s[1]), 1 - s[1]])
    df = pd.DataFrame(rows, columns=["S_CodeBERT", "S_AST", "S_Token", "D_lang", "S_CodeBERT_minus_S_AST", "one_minus_S_AST"])
    return df


arr = lambda df, c: df[c].values.astype(np.float64)


def job(a):
    kind, seed, sets = a
    routing = kind == "gate"
    m, _, _ = train_model(arr(tr, X6), arr(tr, SC), tr.label.values, arr(va, X6), arr(va, SC), va.label.values, seed, routing, LR, BS)
    sv = score(m, arr(va, X6), arr(va, SC), routing)[0]
    out = {}
    for k, d in sets.items():
        sc, w = score(m, arr(d, X6), arr(d, SC), routing)
        out[k] = (sc, w)
    return kind, seed, sv, out


if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    sets = {v: feats(v) for v in ("orig", "attacked")}
    with Pool(8) as p:
        res = p.map(job, [(k, s, sets) for k in ("gate", "direct") for s in SEEDS])
    yv = va.label.values
    y = pairs.label.values
    out = {"n_pos": int((y == 1).sum()), "n_neg": int((y == 0).sum())}
    systems = {}
    for kind in ("gate", "direct"):
        rs = sorted([r for r in res if r[0] == kind], key=lambda r: r[1])
        thr = [tune_threshold(r[2], yv) for r in rs]
        systems[kind] = {v: (np.vstack([r[3][v][0] for r in rs]), thr) for v in sets}
    Sv = arr(va, SC)
    for nm, i in (("first_expert", 0), ("token", 2)):
        t = tune_threshold(Sv[:, i], yv)
        systems[nm] = {v: (np.tile(arr(sets[v], SC)[:, i], (8, 1)), [t] * 8) for v in sets}
    for nm, d in systems.items():
        out[nm] = {}
        for v, (S, thr) in d.items():
            ens = S.mean(0)
            rec = float(np.mean([(S[s][y == 1] >= thr[s]).mean() for s in range(8)]))
            fpr = float(np.mean([(S[s][y == 0] >= thr[s]).mean() for s in range(8)]))
            f, t, _ = roc_curve(y, ens)
            out[nm][v] = dict(recall=rec, fpr=fpr, auc=float(roc_auc_score(y, ens)), r5=float(t[np.searchsorted(f, 0.05, side="right") - 1]))
    gw = [np.mean([r[3][v][1] for r in res if r[0] == "gate"], axis=0) for v in ("orig", "attacked")]
    out["gate_weights"] = {v: {"pos": [float(x) for x in w[y == 1].mean(0)], "neg": [float(x) for x in w[y == 0].mean(0)]} for v, w in zip(("orig", "attacked"), gw)}
    json.dump(out, open(os.path.join(RES, "e4_attack.json"), "w"), indent=1)
    for nm in ("gate", "direct", "first_expert", "token"):
        print(TAG, nm, {v: {k: round(x, 3) for k, x in o.items()} for v, o in out[nm].items()})
    print(out["gate_weights"])
