# -*- coding: utf-8 -*-
"""E8 (part): operating-point metrics (F1 at the validation-tuned threshold, AUROC, recall at 1% / 5% FPR) for JPlag, JPlag+TokenNorm and Dolos from their
continuous similarities (cross-language pairs score 0), regimes A, B, C.
python -I e8_tool_metrics.py -> results_<R>/e8_tools.json"""
import json
import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
POS = ["exact", "renamed", "refactored", "cross-language"]
NEG = {"A": "independent", "B": "hard_independent", "C": "tfidf_independent"}
pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
jp = pd.concat([pd.read_csv(os.path.join(DATA, f)) for f in ("jplag_scores.csv", "jplag_scores_hard.csv", "jplag_scores_tfidf.csv")], ignore_index=True)
plain = jp[jp.cond == "plain"].drop_duplicates("pair_id").set_index("pair_id").col2.astype(float)
norm = jp[jp.cond == "norm"].drop_duplicates("pair_id").set_index("pair_id").col2.astype(float)
dol = pd.read_csv(os.path.join(DATA, "dolos_scores.csv")).drop_duplicates("pair_id").set_index("pair_id").sim.astype(float)


def f1(y, p):
    tp = ((p == 1) & (y == 1)).sum()
    return 2 * tp / max(2 * tp + ((p == 1) & (y == 0)).sum() + ((p == 0) & (y == 1)).sum(), 1)


def score_of(df, which):
    same = df.D_lang.values == 0
    if which == "jplag":
        v = df.pair_id.map(plain)
    elif which == "tokennorm":
        v = df.pair_id.map(norm).fillna(df.pair_id.map(plain))
    else:
        v = df.pair_id.map(dol)
    return np.where(same, v.fillna(0).values, 0.0)


for r in "ABC":
    sel = ~pf.slice.isin({"independent", "hard_independent", "tfidf_independent"} - {NEG[r]})
    va, te = pf[sel & (pf.split == "val")], pf[sel & (pf.split == "test")]
    yv, yt = va.label.values, te.label.values
    out = {}
    for w in ("jplag", "tokennorm", "dolos"):
        sv, st = score_of(va, w), score_of(te, w)
        grid = np.arange(0.0, 1.0001, 0.005)
        best, bt = -1, 1e-9
        for t in grid:
            f = f1(yv, (sv >= t).astype(int))
            if f > best + 1e-12:
                best, bt = f, max(t, 1e-9)
        p = (st >= bt).astype(int)
        fpr, tpr, _ = roc_curve(yt, st)
        out[w] = dict(f1=float(f1(yt, p)), recall=float(p[yt == 1].mean()), specificity=float(1 - p[yt == 0].mean()), auc=float(roc_auc_score(yt, st)),
                      r1=float(tpr[np.searchsorted(fpr, 0.01, side="right") - 1]), r5=float(tpr[np.searchsorted(fpr, 0.05, side="right") - 1]), thr=float(bt))
        print(r, w, {k: round(v, 3) for k, v in out[w].items()})
    json.dump(out, open(os.path.join(HERE, "results_%s" % r, "e8_tools.json"), "w"), indent=1)
