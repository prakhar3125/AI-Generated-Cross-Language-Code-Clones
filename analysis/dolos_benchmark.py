# -*- coding: utf-8 -*-
"""Dolos 2.10.0 (official container) on the benchmark's same-language pairs (validation, test, judge-rejected), in batches.

Every pair contributes two one-file submissions; a batch is compared all-against-all and only the intended pair's similarity is read back
(as for JPlag in run_jplag.py).  Fragments are wrapped in a class for Java and C# exactly as for JPlag.  Cross-language pairs cannot be scored (similarity 0).
python -I dolos_benchmark.py -> data/dolos_scores.csv
"""
import csv
import os
import pickle
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, PROJECT  # noqa: E402

IMG = "ghcr.io/dodona-edu/dolos-cli@sha256:64ca9827208a4893975a9a2adcc22a8f16c53341f773f4139c1410cf948930af"  # v2.10.0
W = os.path.join(PROJECT, "tools", "dolos_work", "bench")
LANG = {"java": "java", "python": "python", "c": "c", "csharp": "c-sharp"}
EXT = {"java": "java", "python": "py", "c": "c", "csharp": "cs"}
BATCH = 100


def wrap(code, lang):
    return "public class W {\n%s\n}\n" % code if lang in ("java", "csharp") else code + "\n"


def run(job):
    lang, bi, recs = job
    root = os.path.join(W, "%s_%d" % (lang, bi))
    if os.path.isdir(root):
        shutil.rmtree(root)
    inp = os.path.join(root, "in")
    os.makedirs(inp)
    os.makedirs(os.path.join(root, "out"))
    names = []
    for pid, a, b in recs:
        for side, code in (("a", a), ("b", b)):
            fn = "%s_%s.%s" % (pid, side, EXT[lang])
            with open(os.path.join(inp, fn), "w", encoding="utf-8", newline="\n") as f:
                f.write(wrap(code, lang))
            names.append(fn)
    cmd = ["docker", "run", "--rm", "-v", inp + ":/in:ro", "-v", os.path.join(root, "out") + ":/out", IMG, "run", "-l", LANG[lang], "-f", "csv", "-o", "/out/res"] + \
          ["/in/" + n for n in names]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    res = os.path.join(root, "out", "res")
    csvs = [f for f in os.listdir(res) if f.endswith(".csv")] if os.path.isdir(res) else []
    sims = {}
    if csvs:
        with open(os.path.join(res, "pairs.csv" if "pairs.csv" in csvs else csvs[0]), newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                a = os.path.basename(row["leftFilePath"])
                b = os.path.basename(row["rightFilePath"])
                sims[(a, b)] = sims[(b, a)] = float(row["similarity"])
    else:
        print("no csv", lang, bi, (r.stdout + r.stderr)[-300:], flush=True)
    out = []
    for pid, a, b in recs:
        k = ("%s_a.%s" % (pid, EXT[lang]), "%s_b.%s" % (pid, EXT[lang]))
        out.append((pid, lang, sims.get(k, 0.0)))
    shutil.rmtree(root, ignore_errors=True)
    print(lang, bi, len(out), flush=True)
    return out


def main():
    d = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
    d = d[d.split.isin(["val", "test", "aux"]) & (d.lang1 == d.lang2)].drop_duplicates("pair_id")
    S = pickle.load(open(os.path.join(DATA, "snippets.pkl"), "rb"))
    jobs = []
    for lang, g in d.groupby("lang1"):
        recs = [(r.pair_id, S[r.key1][1], S[r.key2][1]) for r in g.itertuples()]
        for bi in range(0, len(recs), BATCH):
            jobs.append((lang, bi, recs[bi:bi + BATCH]))
    with ThreadPoolExecutor(3) as ex:
        res = list(ex.map(run, jobs))
    rows = [r for part in res for r in part]
    pd.DataFrame(rows, columns=["pair_id", "lang", "sim"]).to_csv(os.path.join(DATA, "dolos_scores.csv"), index=False)
    print("saved", len(rows))


if __name__ == "__main__":
    main()
