# -*- coding: utf-8 -*-
"""Decision rules, metrics, per-slice recalls and predictions for every system.

Reads results/scores.npz (learned / score-based systems) and data/jplag_scores.csv
(real JPlag and JPlag + token normalization), applies three decision rules

  val       global threshold maximising validation F1          (primary rule, all systems)
  fixed     threshold 0.50
  adaptive  per-pair T = clamp(mu + k sigma) of Eq. 12, calibrated on validation negatives

and writes results/preds.npz (boolean predictions, [seeds, test pairs]) and
results/main_eval.json.

python -I evaluate_all.py
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE  # noqa: E402
from exp_lib import (SEEDS, adaptive_thresholds, load, metrics, tune_threshold, wilson)  # noqa: E402

from exp_lib import NEG_SLICE, REGIME  # noqa: E402
from exp_lib import TAG  # noqa: E402
RES = os.path.join(HERE, "results_" + TAG)
D = load()
va, te, ax = D["val"], D["test"], D["aux"]
yv, yt = va.label.values, te.label.values
R = np.load(os.path.join(RES, "scores.npz"))
SLICES = ["exact", "renamed", "refactored", "cross-language"]
LEARNED = ["gate", "direct", "logreg", "static", "codebert", "ast", "token", "random",
           "gate_x4", "gate_wo_sem", "gate_wo_str", "gate_wo_syn"]


def jplag_arrays():
    f = os.path.join(DATA, "jplag_scores.csv")
    if not os.path.exists(f):
        return None
    j = pd.read_csv(f)
    for extra in ("jplag_scores_hard.csv", "jplag_scores_tfidf.csv"):
        fh = os.path.join(DATA, extra)
        if os.path.exists(fh):
            j = pd.concat([j, pd.read_csv(fh)], ignore_index=True)
    plain = j[j.cond == "plain"].set_index("pair_id").col2.astype(float)
    norm = j[j.cond == "norm"].set_index("pair_id").col2.astype(float)
    out = {}
    for nm, df in (("val", va), ("test", te), ("aux", ax)):
        jp = np.array([plain.get(p, 0.0) if d == 0 else 0.0 for p, d in zip(df.pair_id, df.D_lang)], float)
        jp = np.nan_to_num(jp, nan=0.0)
        tn = np.array([(norm.get(p, np.nan) if (p in norm.index) else plain.get(p, 0.0)) if d == 0 else 0.0
                       for p, d in zip(df.pair_id, df.D_lang)], float)
        tn = np.nan_to_num(tn, nan=0.0)
        out[nm] = {"jplag": jp, "tokennorm": tn}
    fd = os.path.join(DATA, "dolos_scores.csv")
    if os.path.exists(fd):
        dol = pd.read_csv(fd).drop_duplicates("pair_id").set_index("pair_id").sim.astype(float)
        for nm, df in (("val", va), ("test", te), ("aux", ax)):
            out[nm]["dolos"] = np.nan_to_num(np.array([dol.get(p, 0.0) if d == 0 else 0.0 for p, d in zip(df.pair_id, df.D_lang)], float), nan=0.0)
    return out


def rule_preds(sv, st, rule, seed_idx=None):
    if rule == "val":
        return st >= tune_threshold(sv, yv)
    if rule == "fixed":
        return st >= 0.5
    T = adaptive_thresholds(sv, yv, va.D_lang.values, va.cc1.values, te.D_lang.values, te.cc1.values)
    return st >= T


def summarise(P):
    """P: [seeds, n] boolean predictions on test -> dict of mean/sd metrics."""
    ms = [metrics(yt, p.astype(int)) for p in P]
    out = {}
    for k in ms[0]:
        v = np.array([m[k] for m in ms], float)
        out[k] = [float(v.mean()), float(v.std(ddof=1)) if len(v) > 1 else 0.0]
    sl = {}
    for s in SLICES:
        msk = (te.slice == s).values
        r = np.array([p[msk].mean() for p in P])
        sl[s] = [float(r.mean()), float(r.std(ddof=1)) if len(r) > 1 else 0.0, int(msk.sum())]
    msk = (te.slice == NEG_SLICE).values
    sp = np.array([(~p[msk]).mean() for p in P])
    sl["independent_specificity"] = [float(sp.mean()), float(sp.std(ddof=1)) if len(sp) > 1 else 0.0, int(msk.sum())]
    out["slices"] = sl
    return out


def main():
    preds, thr, summ = {}, {}, {}
    for sysn in LEARNED:
        for rule in ("val", "fixed", "adaptive"):
            P, th = [], []
            for i in range(len(SEEDS)):
                sv, st = R["val__" + sysn][i], R["test__" + sysn][i]
                P.append(rule_preds(sv, st, rule))
                th.append(tune_threshold(sv, yv) if rule == "val" else (0.5 if rule == "fixed" else float("nan")))
            preds["%s|%s" % (sysn, rule)] = np.array(P)
            thr["%s|%s" % (sysn, rule)] = th
            summ["%s|%s" % (sysn, rule)] = summarise(np.array(P))
    jp = jplag_arrays()
    if jp is not None:
        for nm in [n for n in ("jplag", "tokennorm", "dolos") if n in jp["val"]]:
            grid = np.arange(0.0, 1.0001, 0.005)
            from exp_lib import f1_of
            best, bt = -1, 0.0
            for t in grid:
                f = f1_of(yv, (jp["val"][nm] >= t).astype(int))
                if f > best + 1e-12:
                    best, bt = f, t
            bt = max(bt, 1e-9)       # a threshold of 0 would flag every pair
            P = np.array([jp["test"][nm] >= bt])
            preds["%s|val" % nm] = P
            thr["%s|val" % nm] = [float(bt)]
            summ["%s|val" % nm] = summarise(P)
            # judge-rejected diagnostic
            thr_aux = float((jp["aux"][nm] >= bt).mean())
            summ["%s|val" % nm]["aux_flag_rate"] = thr_aux
    # judge-rejected (Type-I/II) diagnostic for the score-based systems
    for sysn in LEARNED:
        t = [tune_threshold(R["val__" + sysn][i], yv) for i in range(len(SEEDS))]
        rate = [float((R["aux__" + sysn][i] >= t[i]).mean()) for i in range(len(SEEDS))]
        summ["%s|val" % sysn]["aux_flag_rate"] = float(np.mean(rate))
    np.savez_compressed(os.path.join(RES, "preds.npz"), **{k: v for k, v in preds.items()})
    with open(os.path.join(RES, "main_eval.json"), "w") as f:
        json.dump({"summary": summ, "thresholds": thr}, f, indent=1)
    show = ["gate|val", "gate|fixed", "gate|adaptive", "direct|val", "logreg|val", "static|val",
            "codebert|val", "ast|val", "token|val", "random|val"] + (["jplag|val", "tokennorm|val"] if jp else [])
    print("%-16s %6s %6s %6s %6s %6s %6s | %s" % ("system|rule", "acc", "prec", "rec", "spec", "F1", "FPR",
                                                  "exact renamed refact xlang"))
    for k in show:
        m = summ[k]
        print("%-16s %6.1f %6.1f %6.1f %6.1f %6.1f %6.1f | %s" % (
            k, 100 * m["acc"][0], 100 * m["precision"][0], 100 * m["recall"][0], 100 * m["specificity"][0],
            100 * m["f1"][0], 100 * m["fpr"][0], " ".join("%.3f" % m["slices"][s][0] for s in SLICES)))


if __name__ == "__main__":
    main()
