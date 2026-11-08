# -*- coding: utf-8 -*-
"""Score same-language pairs with the real JPlag (v6.3.0) and JPlag + token normalization.

JPlag compares many submissions per run, so pairs are processed in batches: every
pair contributes two one-file submissions, the whole batch is compared pairwise,
and only the similarity of each intended pair is read back.

  * Fragments are wrapped in a class (Java, C#) so that the front end can parse them;
    both members of a pair receive the identical wrapper.
  * JPlag compares one language per run, so cross-language pairs cannot be scored
    by it. They are assigned similarity 0 (the tool is "not applicable"), which is
    what a deployed instance would report.
  * Token normalization (--normalize, the implementation of Saglam et al.'s token
    sequence normalization shipped in JPlag) exists for the Java and C++ front ends
    only. For Python and C# the normalized score is the plain JPlag score.
  * C is run through the C++ front end in both conditions.

python -I run_jplag.py [--splits val test aux] [--batch 120]
"""
import argparse
import csv
import os
import pickle
import shutil
import subprocess
import sys
import time

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, PROJECT  # noqa: E402

TOOLS = os.path.join(PROJECT, "tools")
JAVA = [os.path.join(TOOLS, "jdk25", d, "bin", "java.exe") for d in os.listdir(os.path.join(TOOLS, "jdk25"))][0]
JAR = os.path.join(TOOLS, "jplag.jar")
WORK = os.path.join(TOOLS, "work")

LANG_ARG = {"java": "java", "python": "python3", "c": "cpp", "csharp": "csharp"}
EXT = {"java": ".java", "python": ".py", "c": ".c", "csharp": ".cs"}
NORMALIZABLE = {"java", "c"}


def wrap(code, lang):
    if lang in ("java", "csharp"):
        return "public class W {\n%s\n}\n" % code
    return code + "\n"


def run_batch(batch, lang, normalize, tag):
    root = os.path.join(WORK, tag)
    if os.path.isdir(root):
        shutil.rmtree(root)
    os.makedirs(root)
    sub = os.path.join(root, "subs")
    os.makedirs(sub)
    for pid, a, b in batch:
        for side, code in (("a", a), ("b", b)):
            d = os.path.join(sub, "%s_%s" % (pid, side))
            os.makedirs(d)
            with open(os.path.join(d, "Main" + EXT[lang]), "w", encoding="utf-8", newline="\n") as f:
                f.write(wrap(code, lang))
    res = os.path.join(root, "res")
    cmd = [JAVA, "--enable-native-access=ALL-UNNAMED", "-jar", JAR, sub, "-l", LANG_ARG[lang], "-r", res, "-n", "-1",
           "--csv-export", "--cluster-skip", "--overwrite", "-M", "RUN"]
    if normalize:
        cmd.append("--normalize")
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    out = {}
    csv_path = os.path.join(res, "results.csv")
    if not os.path.exists(csv_path):
        csv_path = None
    if csv_path is None:
        print("no csv for batch", tag, p.stdout[-800:], p.stderr[-800:])
        return None
    with open(csv_path, newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        head = next(rd)
        for row in rd:
            out[(row[0], row[1])] = row
    return out, head


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", nargs="+", default=["val", "test", "aux"])
    ap.add_argument("--batch", type=int, default=120)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--slices", nargs="+", default=None)
    ap.add_argument("--out", default="jplag_scores.csv")
    a = ap.parse_args()
    pairs = pd.read_csv(os.path.join(DATA, "pairs.csv"))
    with open(os.path.join(DATA, "snippets.pkl"), "rb") as f:
        snips = pickle.load(f)
    res_path = os.path.join(DATA, a.out)
    done = {}
    rows = []
    t0 = time.time()
    for lang in ("java", "python", "c", "csharp"):
        sub = pairs[(pairs.split.isin(a.splits)) & (pairs.lang1 == lang) & (pairs.lang2 == lang)]
        if a.slices:
            sub = sub[sub.slice.isin(a.slices)]
        if a.limit:
            sub = sub.head(a.limit)
        recs = [(r.pair_id, snips[r.key1][1], snips[r.key2][1]) for r in sub.itertuples()]
        for cond in ("plain", "norm"):
            if cond == "norm" and lang not in NORMALIZABLE:
                continue
            for bi in range(0, len(recs), a.batch):
                batch = recs[bi:bi + a.batch]
                r = run_batch(batch, lang, cond == "norm", "%s_%s_%d" % (lang, cond, bi))
                if not r:
                    continue
                m, head = r
                if bi == 0 and cond == "plain":
                    print("csv header:", head)
                for pid, _, _ in batch:
                    row = m.get(("%s_a" % pid, "%s_b" % pid)) or m.get(("%s_b" % pid, "%s_a" % pid))
                    rows.append((pid, lang, cond, row[2] if row else None, row[3] if row and len(row) > 3 else None))
                print(lang, cond, bi, len(recs), "%.0fs" % (time.time() - t0), flush=True)
    pd.DataFrame(rows, columns=["pair_id", "lang", "cond", "col2", "col3"]).to_csv(res_path, index=False)
    print("saved", res_path)


if __name__ == "__main__":
    main()
