# -*- coding: utf-8 -*-
"""Real JPlag 6.3.0 (plain and --normalize) on the cohort pairs: one run per assignment over all its submissions.
python -I jplag_cohort.py -> data/jplag_cohort.csv"""
import os
import pickle
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA  # noqa: E402
from jplag_external import run_group  # noqa: E402

P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv"))
S = pickle.load(open(os.path.join(DATA, "cohort_snippets.pkl"), "rb"))
subs = pd.read_csv(os.path.join(DATA, "cohort_subs.csv"))
rows = []
for g, G in subs.groupby("group"):
    nm = {r.id: "s%04d" % i for i, r in enumerate(G.itertuples())}
    files = {nm[r.id]: S[r.key][1] for r in G.itertuples()}
    for cond in ("plain", "norm"):
        sims = run_group(files, "java", cond == "norm", "co_%s_%s" % (g, cond))
        for r in P[P.group == g].itertuples():
            rows.append((r.pair_id, cond, sims.get((nm[r.id1], nm[r.id2]))))
        print(g, cond, len(files), len(sims), flush=True)
pd.DataFrame(rows, columns=["pair_id", "cond", "sim"]).to_csv(os.path.join(DATA, "jplag_cohort.csv"), index=False)
print("done")
