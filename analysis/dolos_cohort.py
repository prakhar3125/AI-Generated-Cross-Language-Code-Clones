# -*- coding: utf-8 -*-
"""Dolos 2.10.0 (official container ghcr.io/dodona-edu/dolos-cli) on the cohort pairs: one run per assignment over all submissions.

variants: default  (Dolos defaults: k=23, w=17, fingerprints in more than 90% of the files ignored)
          m50      (-M 0.5: fingerprints in more than half of the files ignored; the boilerplate setting)
          m20      (-M 0.2, sensitivity)
python -I dolos_cohort.py -> data/dolos_cohort.csv
"""
import csv
import os
import pickle
import shutil
import subprocess
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, PROJECT  # noqa: E402

IMG = "ghcr.io/dodona-edu/dolos-cli@sha256:64ca9827208a4893975a9a2adcc22a8f16c53341f773f4139c1410cf948930af"  # v2.10.0
W = os.path.join(PROJECT, "tools", "dolos_work")
VARIANTS = {"default": [], "m50": ["-M", "0.5"], "m20": ["-M", "0.2"]}

P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv"))
S = pickle.load(open(os.path.join(DATA, "cohort_snippets.pkl"), "rb"))
subs = pd.read_csv(os.path.join(DATA, "cohort_subs.csv"))
rows = []
for g, G in subs.groupby("group"):
    inp = os.path.join(W, g, "in")
    if os.path.isdir(inp):
        shutil.rmtree(inp)
    os.makedirs(inp)
    nm = {}
    for i, r in enumerate(G.itertuples()):
        nm[r.id] = "s%04d.java" % i
        with open(os.path.join(inp, nm[r.id]), "w", encoding="utf-8", newline="\n") as f:
            f.write(S[r.key][1] + "\n")
    for var, extra in VARIANTS.items():
        out = os.path.join(W, g, "out_" + var)
        if os.path.isdir(out):
            shutil.rmtree(out)
        os.makedirs(out)
        cmd = ["docker", "run", "--rm", "-v", inp + ":/in:ro", "-v", out + ":/out", IMG, "run", "-l", "java", "-f", "csv", "-o", "/out/res"] + extra + \
              ["/in/" + n for n in nm.values()]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        out = os.path.join(out, "res")
        csvs = [f for f in os.listdir(out) if f.endswith(".csv")] if os.path.isdir(out) else []
        sims = {}
        if csvs:
            with open(os.path.join(out, "pairs.csv" if "pairs.csv" in csvs else csvs[0]), newline="", encoding="utf-8") as f:
                rd = csv.DictReader(f)
                for r in rd:
                    a = os.path.basename(r["leftFilePath"])
                    b = os.path.basename(r["rightFilePath"])
                    sims[(a, b)] = sims[(b, a)] = float(r["similarity"])
        else:
            print("no csv", g, var, res.stderr[-300:], res.stdout[-300:], flush=True)
        for r in P[P.group == g].itertuples():
            rows.append((r.pair_id, var, sims.get((nm[r.id1], nm[r.id2]), 0.0)))
        print(g, var, len(sims) // 2, flush=True)
pd.DataFrame(rows, columns=["pair_id", "cond", "sim"]).to_csv(os.path.join(DATA, "dolos_cohort.csv"), index=False)
print("done")
