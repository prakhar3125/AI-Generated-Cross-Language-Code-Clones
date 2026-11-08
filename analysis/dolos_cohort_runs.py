# -*- coding: utf-8 -*-
"""Dolos 2.10.0 with one run PER COHORT (the honest submissions of the assignment plus the one derived submission), so that its frequency
filter (-M: fingerprints present in more than that fraction of the files are ignored) sees exactly the cohort an instructor would submit.
(dolos_cohort.py runs once per assignment over all derived files, which is correct for JPlag but not for a frequency filter.)

variants: default (-M 0.9, Dolos default)   m50 (-M 0.5)
python -I dolos_cohort_runs.py -> data/dolos_cohort_runs.json
"""
import csv
import json
import os
import pickle
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE, PROJECT  # noqa: E402

IMG = "ghcr.io/dodona-edu/dolos-cli@sha256:64ca9827208a4893975a9a2adcc22a8f16c53341f773f4139c1410cf948930af"  # v2.10.0
W = os.path.join(PROJECT, "tools", "dolos_work", "cohorts")
VARIANTS = {"default": [], "m50": ["-M", "0.5"]}
THR = json.load(open(os.path.join(HERE, "results_A", "main_eval.json")))["thresholds"]["dolos|val"][0]

S = pickle.load(open(os.path.join(DATA, "cohort_snippets.pkl"), "rb"))
subs = pd.read_csv(os.path.join(DATA, "cohort_subs.csv"))
M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv"))
code = {(r.group, r.id): S[r.key][1] for r in subs.itertuples()}
honest = {g: sorted(G[G.role == "honest"].id) for g, G in subs.groupby("group")}


def run(job):
    i, d = job
    g = d.group
    root = os.path.join(W, "c%04d" % i)
    inp = os.path.join(root, "in")
    if os.path.isdir(root):
        shutil.rmtree(root)
    os.makedirs(inp)
    ids = honest[g] + [d.derived]
    nm = {x: "f%03d.java" % k for k, x in enumerate(ids)}
    for x in ids:
        with open(os.path.join(inp, nm[x]), "w", encoding="utf-8", newline="\n") as f:
            f.write(code[(g, x)] + "\n")
    res = {}
    for var, extra in VARIANTS.items():
        out = os.path.join(root, "out_" + var)
        os.makedirs(out)
        cmd = ["docker", "run", "--rm", "-v", inp + ":/in:ro", "-v", out + ":/out", IMG, "run", "-l", "java", "-f", "csv", "-o", "/out/res"] + extra + ["/in/" + n for n in nm.values()]
        subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        p = os.path.join(out, "res", "pairs.csv")
        sims = {}
        if os.path.exists(p):
            with open(p, newline="", encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    a, b = os.path.basename(r["leftFilePath"]), os.path.basename(r["rightFilePath"])
                    sims[frozenset((a, b))] = float(r["similarity"])
        dp = sims.get(frozenset((nm[d.src], nm[d.derived])), 0.0)
        nd = [sims.get(frozenset((nm[a], nm[b])), 0.0) for k, a in enumerate(ids) for b in ids[k + 1:]
              if frozenset((a, b)) != frozenset((d.src, d.derived))]
        nd = np.array(nd)
        # non-derived pairs: all others among the cohort files
        res[var] = dict(auc=float((nd < dp).mean() + 0.5 * (nd == dp).mean()), det=float(dp >= THR), ff=float((nd >= THR).mean()))
    shutil.rmtree(root, ignore_errors=True)
    if i % 25 == 0:
        print(i, len(M), flush=True)
    return res


if __name__ == "__main__":
    jobs = list(enumerate(M.itertuples()))
    with ThreadPoolExecutor(4) as ex:
        out = list(ex.map(run, jobs))
    M["ds"] = np.where(M.group.str.startswith("Progpedia"), "PROGpedia", "IR-Plag")
    res = {"threshold": THR, "n": len(M)}
    for var in VARIANTS:
        res[var] = {}
        for ds in ("PROGpedia", "IR-Plag"):
            m = (M.ds == ds).values
            e = {}
            for k in ("auc", "det", "ff"):
                v = np.array([o[var][k] for o in out])
                e[k] = float(v[m].mean())
                e["by_kind_" + k] = {kd: float(v[m & (M.kind == kd).values].mean()) for kd in M[m].kind.unique()}
            # cluster bootstrap (sources) CI of mean AUROC
            v = np.array([o[var]["auc"] for o in out])[m]
            cl = (M.group + "|" + M.src).values[m]
            u, iv = np.unique(cl, return_inverse=True)
            cnt = np.bincount(iv, minlength=len(u))
            sums = np.bincount(iv, weights=v, minlength=len(u))
            rng = np.random.default_rng(0)
            bs = [sums[b].sum() / cnt[b].sum() for b in (rng.integers(0, len(u), len(u)) for _ in range(2000))]
            e["auc_ci"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
            res[var][ds] = e
    res["vec_auc"] = {var: [o[var]["auc"] for o in out] for var in VARIANTS}
    json.dump(res, open(os.path.join(DATA, "dolos_cohort_runs.json"), "w"), indent=1)
    for var in VARIANTS:
        print(var, {ds: (round(res[var][ds]["auc"], 3), [round(c, 3) for c in res[var][ds]["auc_ci"]], round(res[var][ds]["det"], 2), round(res[var][ds]["ff"], 2)) for ds in ("PROGpedia", "IR-Plag")})
        print("   ", {ds: {k: round(x, 3) for k, x in res[var][ds]["by_kind_auc"].items()} for ds in ("PROGpedia", "IR-Plag")})
