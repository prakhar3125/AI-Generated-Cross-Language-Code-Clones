# -*- coding: utf-8 -*-
"""Real JPlag 6.3.0 on the external pair sets.

PROGpedia: one JPlag run per (problem, language) group with all of the group's files as submissions;
only the needed pairs are read back.  Convergence pairs: batches as in run_jplag.py.
python -I jplag_external.py
"""
import csv
import os
import pickle
import shutil
import subprocess
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA  # noqa: E402
from run_jplag import EXT, JAR, JAVA, LANG_ARG, WORK  # noqa: E402

LANG_NORM = {"java", "c"}


def run_group(files, lang, normalize, tag):
    """files: {name: code}. returns {(a,b): sim}"""
    root = os.path.join(WORK, tag)
    if os.path.isdir(root):
        shutil.rmtree(root)
    sub = os.path.join(root, "subs")
    os.makedirs(sub)
    for nm, code in files.items():
        d = os.path.join(sub, nm)
        os.makedirs(d)
        with open(os.path.join(d, "Main" + EXT[lang]), "w", encoding="utf-8", newline="\n") as f:
            f.write(code + "\n")
    res = os.path.join(root, "res")
    cmd = [JAVA, "--enable-native-access=ALL-UNNAMED", "-jar", JAR, sub, "-l", LANG_ARG[lang], "-r", res, "-n", "-1",
           "--csv-export", "--cluster-skip", "--overwrite", "-M", "RUN"] + (["--normalize"] if normalize else [])
    subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    out = {}
    p = os.path.join(res, "results.csv")
    if os.path.exists(p):
        with open(p, newline="", encoding="utf-8") as f:
            rd = csv.reader(f)
            next(rd)
            for r in rd:
                out[(r[0], r[1])] = float(r[2])
                out[(r[1], r[0])] = float(r[2])
    return out


def main():
    rows = []
    # ---- PROGpedia
    pp = pd.read_csv(os.path.join(DATA, "progpedia_pairs.csv"))
    S = pickle.load(open(os.path.join(DATA, "progpedia_snippets.pkl"), "rb"))
    for (prob, lang), g in pp.groupby(["problem", "lang1"]):
        keys = sorted(set(g.key1) | set(g.key2))
        names = {k: "s%04d" % i for i, k in enumerate(keys)}
        files = {names[k]: S[k][1] for k in keys}
        for cond in ("plain", "norm"):
            if cond == "norm" and lang not in LANG_NORM:
                continue
            sims = run_group(files, lang, cond == "norm", "pg_%s_%s_%s" % (prob, lang, cond))
            for r in g.itertuples():
                rows.append((r.pair_id, cond, sims.get((names[r.key1], names[r.key2]))))
            print(prob, lang, cond, len(files), flush=True)
    pd.DataFrame(rows, columns=["pair_id", "cond", "sim"]).to_csv(os.path.join(DATA, "jplag_progpedia.csv"), index=False)
    # ---- convergence pairs (same-language, benchmark snippets; fragments wrapped as in run_jplag.py)
    from run_jplag import wrap
    cv = pd.read_csv(os.path.join(DATA, "convergence_pairs.csv"))
    SB = pickle.load(open(os.path.join(DATA, "snippets.pkl"), "rb"))
    rows = []
    for lang, g in cv.groupby("lang1"):
        for cond in ("plain", "norm"):
            if cond == "norm" and lang not in LANG_NORM:
                continue
            files = {}
            for r in g.itertuples():
                files[r.pair_id + "_a"] = wrap(SB[r.key1][1], lang)
                files[r.pair_id + "_b"] = wrap(SB[r.key2][1], lang)
            sims = run_group(files, lang, cond == "norm", "cv_%s_%s" % (lang, cond))
            for r in g.itertuples():
                rows.append((r.pair_id, cond, sims.get((r.pair_id + "_a", r.pair_id + "_b"))))
    pd.DataFrame(rows, columns=["pair_id", "cond", "sim"]).to_csv(os.path.join(DATA, "jplag_convergence.csv"), index=False)
    print("done")


if __name__ == "__main__":
    main()
