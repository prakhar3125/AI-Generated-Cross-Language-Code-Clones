# -*- coding: utf-8 -*-
"""Stacked precision-recall curves on the benchmark test partition (regimes A, B, C), including JPlag and Dolos (continuous similarities;
cross-language pairs score 0 for both) and the UniXcoder cosine.
python -I make_pr_figure.py -> tables/fig_pr_stacked.pdf
"""
import os

import matplotlib
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, precision_recall_curve

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LO = os.environ.get("LOGIT_TABLES") == "1"        # 1: the gate curve is the log-odds gate (results_<R>lo/), written to tables_lo/
SUF = "lo" if LO else ""
DATA = os.path.join(HERE, "data")
POS = ["exact", "renamed", "refactored", "cross-language"]
NEG = {"A": "independent", "B": "hard_independent", "C": "tfidf_independent"}
pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
jp = pd.concat([pd.read_csv(os.path.join(DATA, f)) for f in ("jplag_scores.csv", "jplag_scores_hard.csv", "jplag_scores_tfidf.csv")], ignore_index=True)
jp = jp[jp.cond == "plain"].drop_duplicates("pair_id").set_index("pair_id").col2.astype(float)
dol = pd.read_csv(os.path.join(DATA, "dolos_scores.csv")).drop_duplicates("pair_id").set_index("pair_id").sim.astype(float)

plt.rcParams.update({"font.size": 8, "font.family": "serif", "axes.linewidth": 0.6})
STY = [("Gating network", "gate", "#0072B2", "-", 1.6), ("Direct classifier", "direct", "#E69F00", "-", 1.2), ("Token $k$-gram only", "token", "#009E73", "-", 1.2),
       ("UniXcoder cosine", "ux", "#CC79A7", "-", 1.2), ("CodeBERT cosine", "codebert", "#D55E00", "-", 1.2), ("Static averaging", "static", "#7F7F7F", "-", 1.0),
       ("Dolos 2.10.0", "dolos", "#000000", "--", 1.4), ("JPlag 6.3.0", "jplag", "#56B4E9", "--", 1.4)]
fig, axes = plt.subplots(3, 1, figsize=(3.45, 5.4), sharex=True)
for ax, r in zip(axes, "ABC"):
    te = pf[(pf.split == "test") & (pf.slice.isin(POS + [NEG[r]]))].reset_index(drop=True)
    y = te.label.values
    S = np.load(os.path.join(HERE, "results_%s%s" % (r, SUF), "scores.npz"))
    SU = np.load(os.path.join(HERE, "results_%sux" % r, "scores.npz"))
    sc = {k: S["test__" + k].mean(0) for k in ("gate", "direct", "token", "codebert", "static")}
    sc["ux"] = SU["test__codebert"].mean(0)
    same = te.D_lang.values == 0
    sc["jplag"] = np.where(same, te.pair_id.map(jp).fillna(0).values, 0.0)
    sc["dolos"] = np.where(same, te.pair_id.map(dol).fillna(0).values, 0.0)
    for lab, k, c, ls, lw in STY:
        p, rc, _ = precision_recall_curve(y, sc[k])
        ap = average_precision_score(y, sc[k])
        ax.plot(rc, p, color=c, ls=ls, lw=lw, label="%s (AP %.2f)" % (lab, ap) if r == "A" else None)
    ax.set_ylim(0.38, 1.02)
    ax.set_xlim(0, 1.0)
    ax.set_ylabel("Precision")
    ax.set_title({"A": "(a) Regime A: random independent negatives", "B": "(b) Regime B: hard negatives (expert-score mining)", "C": "(c) Regime C: hard negatives (identifier mining)"}[r], fontsize=8, loc="left")
    ax.grid(alpha=0.3, lw=0.4)
    ax.axhline(y.mean(), color="0.6", lw=0.7, ls=":")
axes[-1].set_xlabel("Recall")
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, [x.split(" (AP")[0] for x in l], loc="lower center", ncol=3, frameon=False, fontsize=7, bbox_to_anchor=(0.5, 0.0))
fig.tight_layout(rect=(0, 0.13, 1, 1), h_pad=1.0)
os.makedirs(os.path.join(HERE, "tables_lo" if LO else "tables"), exist_ok=True)
fig.savefig(os.path.join(HERE, "tables_lo" if LO else "tables", "fig_pr_stacked.pdf"))
print("ok")
