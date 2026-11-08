# -*- coding: utf-8 -*-
"""Cluster-bootstrap comparison of Dolos with the gate and with JPlag on the benchmark test partition (seed-averaged F1, own Holm family of two).
REGIME=A|B|C [SEM=ux] python -I dolos_bench_stats.py -> results_<TAG>/dolos_stats.json"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE  # noqa: E402
from exp_lib import TAG, load  # noqa: E402
from stats_tools import boot_p, cluster_bootstrap, cluster_counts, holm  # noqa: E402

RES = os.path.join(HERE, "results_" + TAG)
te = load()["test"]
yt = te.label.values
P = np.load(os.path.join(RES, "preds.npz"))
cl = te.group1.values
cnt = {k: np.stack([cluster_counts(yt, p.astype(int), cl) for p in P[k]]) for k in ("gate|val", "dolos|val", "jplag|val", "token|val")}
K = cnt["gate|val"].shape[1]
bs = cluster_bootstrap(cnt, K, B=20000, seed=3)
out = {}
rows = []
for a, b in (("gate|val", "dolos|val"), ("dolos|val", "jplag|val"), ("token|val", "dolos|val")):
    d = (bs[a] - bs[b]) * 100
    rows.append((a, b, float(d.mean()), [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))], boot_p(d)))
adj = holm([r[4] for r in rows])
for r, ap in zip(rows, adj):
    out["%s - %s" % (r[0], r[1])] = dict(delta=r[2], ci=r[3], p=r[4], p_holm=float(ap))
json.dump(out, open(os.path.join(RES, "dolos_stats.json"), "w"), indent=1)
print(TAG, {k: (round(v["delta"], 1), [round(c, 1) for c in v["ci"]], round(v["p_holm"], 4)) for k, v in out.items()})
