# -*- coding: utf-8 -*-
"""E1: fixed-weight and non-routing baselines, and operating-point metrics (AUROC, recall at 1% / 5% FPR) for every score-based system.

Baselines (all use only the three expert scores and D_lang; weights / thresholds chosen on the validation partition):
  best_convex       best convex weights on the 3-simplex (step 0.05, 231 points) over the raw scores, validation-tuned threshold
  best_convex_logit same, weights over logit(S)
  best_convex_z     same, weights over z-scored S (mean/std from the training split)
  hand_rule         same-language -> S_token, cross-language -> S_sem, one validation-tuned threshold per language relation
  gbt               histogram gradient-boosted trees on the six gate features (8 seeds)
Recall at FPR: from the ROC curve of the test scores (threshold chosen on the test negatives, i.e. an oracle operating point).

REGIME=A|B|C [SEM=ux] python -I e1_baselines.py -> results_<TAG>/e1_baselines.json
"""
import itertools
import json
import os
import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, roc_curve

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE  # noqa: E402
from exp_lib import SC, SEEDS, TAG, X6, load, metrics, tune_threshold  # noqa: E402

RES = os.path.join(HERE, "results_" + TAG)
D = load()
tr, va, te = D["train"], D["val"], D["test"]
ytr, yva, yte = tr.label.values, va.label.values, te.label.values


def f1(y, p):
    tp = ((p == 1) & (y == 1)).sum()
    return 2 * tp / max(2 * tp + ((p == 1) & (y == 0)).sum() + ((p == 0) & (y == 1)).sum(), 1)


def tune(sv, yv):
    if sv.min() >= 0 and sv.max() <= 1:
        t = tune_threshold(sv, yv)
        return t, f1(yv, (sv >= t).astype(int))
    cand = np.unique(np.quantile(sv, np.linspace(0.01, 0.99, 197)))
    best, bt = -1.0, cand[0]
    for t in cand:
        f = f1(yv, (sv >= t).astype(int))
        if f > best + 1e-12:
            best, bt = f, t
    return bt, best


def recall_at(y, s, fpr):
    f, t, _ = roc_curve(y, s)
    return float(t[np.searchsorted(f, fpr, side="right") - 1]) if False else float(np.interp(fpr, f, t))


def report(sv, st):
    thr, _ = tune(sv, yva)
    m = metrics(yte, (st >= thr).astype(int))
    fpr, tpr, _ = roc_curve(yte, st)
    return dict(f1=m["f1"], precision=m["precision"], recall=m["recall"], specificity=m["specificity"], auc=float(roc_auc_score(yte, st)),
                r1=float(tpr[np.searchsorted(fpr, 0.01, side="right") - 1]), r5=float(tpr[np.searchsorted(fpr, 0.05, side="right") - 1]))


S = {k: d[SC].values.astype(float) for k, d in (("tr", tr), ("va", va), ("te", te))}
logit = lambda x: np.log(np.clip(x, 1e-3, 1 - 1e-3) / (1 - np.clip(x, 1e-3, 1 - 1e-3)))
mu, sd = S["tr"].mean(0), S["tr"].std(0) + 1e-9
W = [np.array([a, b, round(1 - a - b, 2)]) for a, b in itertools.product(np.arange(0, 1.0001, 0.05), repeat=2) if a + b <= 1.0001]
W = [w for w in W if abs(w.sum() - 1) < 1e-9]
out = {"n_grid": len(W)}
for name, tf in (("best_convex", lambda x: x), ("best_convex_logit", logit), ("best_convex_z", lambda x: (x - mu) / sd)):
    Zv, Zt = tf(S["va"]), tf(S["te"])
    best = (-1, None, None)
    for w in W:
        thr, f = tune(Zv @ w, yva)
        if f > best[0]:
            best = (f, w, thr)
    f, w, thr = best
    r = report(Zv @ w, Zt @ w)
    r["weights"] = [float(x) for x in w]
    out[name] = r
# hand-coded rule: same-language -> token expert, cross-language -> semantic expert; threshold per language relation
dv, dt = va.D_lang.values, te.D_lang.values
sv = np.where(dv == 0, S["va"][:, 2], S["va"][:, 0])
st = np.where(dt == 0, S["te"][:, 2], S["te"][:, 0])
thr = {}
pred = np.zeros(len(te), int)
for rel in (0, 1):
    thr[rel], _ = tune(sv[dv == rel], yva[dv == rel])
    pred[dt == rel] = (st[dt == rel] >= thr[rel]).astype(int)
m = metrics(yte, pred)
# oracle-free ranking score for AUROC / recall@FPR: rank-normalise inside each relation by its validation threshold
sc = np.where(dt == 0, st - thr[0], st - thr[1])
fpr, tpr, _ = roc_curve(yte, sc)
out["hand_rule"] = dict(f1=m["f1"], precision=m["precision"], recall=m["recall"], specificity=m["specificity"], auc=float(roc_auc_score(yte, sc)),
                        r1=float(tpr[np.searchsorted(fpr, 0.01, side="right") - 1]), r5=float(tpr[np.searchsorted(fpr, 0.05, side="right") - 1]), thr=[float(thr[0]), float(thr[1])])
# gradient-boosted trees on the six features, 8 seeds
runs = []
for s in SEEDS:
    g = HistGradientBoostingClassifier(max_depth=3, learning_rate=0.1, max_iter=200, early_stopping=True, validation_fraction=0.2, random_state=s)
    g.fit(tr[X6].values, ytr)
    runs.append(report(g.predict_proba(va[X6].values)[:, 1], g.predict_proba(te[X6].values)[:, 1]))
out["gbt"] = {k: [float(np.mean([r[k] for r in runs])), float(np.std([r[k] for r in runs], ddof=1))] for k in runs[0]}
# existing systems: operating-point metrics from the saved ensemble-mean scores
Z = np.load(os.path.join(RES, "scores.npz"))
for k in ("gate", "direct", "logreg", "static", "codebert", "ast", "token"):
    out[k] = report(Z["val__" + k].mean(0), Z["test__" + k].mean(0))
    me = os.path.join(RES, "main_eval.json")
    if os.path.exists(me):
        sm = json.load(open(me))["summary"].get(k + "|val")
        if sm:
            out[k]["f1"] = sm["f1"]   # seed-averaged F1 as in the main tables
json.dump(out, open(os.path.join(RES, "e1_baselines.json"), "w"), indent=1)
for k, v in out.items():
    if isinstance(v, dict) and "f1" in v:
        f = lambda x: x[0] if isinstance(x, list) else x
        print(TAG, k.ljust(18), "F1 %.1f AUC %.3f R@1 %.1f R@5 %.1f" % (100 * f(v["f1"]), f(v["auc"]), 100 * f(v["r1"]), 100 * f(v["r5"])), v.get("weights", ""))
