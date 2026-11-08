# -*- coding: utf-8 -*-
"""Zero-shot cross-generator probe: GPT-4 translations of held-out problems.

cross_language_part_2.zip (part of the GPTCloneBench release) holds GPT-4 translations
(file prefix Gpt4D_) of the Java seed fragments whose GPT-3 translations make up
cross_language.zip (prefix Gpt3D_). For every code_clones.csv problem that sits in the
*test* side of the problem-grouped protocol, and whose Java seed also occurs in part 2,
we build

  positives : (Java seed, GPT-4 Python / C / C# translation)     -- unseen generator
  controls  : (Java seed, GPT-3 translation of the same problem) -- the training generator
  negatives : (Java seed of problem i, GPT-4 translation of problem j != i), language
              mix matched to the positives.

The gate and every threshold are frozen on the GPT-3 train / validation splits.

python -I build_probe.py
"""
import os
import pickle
import re
import sys
import zipfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, REPO, SEED, skey  # noqa: E402

rng = np.random.RandomState(SEED)
HDR = re.compile(r"^\s*(?://\s*)?(?:#\s*)?\**(Python|C#|Csharp|C)\**\s*(?:[Ii]mplementation)?\s*:?\s*\**\s*$", re.M)


def strip_fence(t):
    m = re.search(r"```[A-Za-z#+]*\n(.*?)```", t, re.S)
    t = m.group(1) if m else re.sub(r"```[A-Za-z#+]*", "", t)
    return t.strip()


def parse_part2(text):
    m = re.search(r"#input\s*(.*?)\s*#=+", text, re.S)
    if not m:
        return None
    java = m.group(1).strip()
    o = re.search(r"#gpt output=+\s*(.*)", text, re.S)
    if not o:
        return None
    out = o.group(1)
    hs = list(HDR.finditer(out))
    got = {}
    for i, h in enumerate(hs):
        lang = {"Python": "python", "C": "c", "C#": "csharp", "Csharp": "csharp"}[h.group(1)]
        end = hs[i + 1].start() if i + 1 < len(hs) else len(out)
        code = strip_fence(out[h.end():end])
        if len(code) > 20 and lang not in got:
            got[lang] = code
    return java, got


def main():
    cc = pd.read_csv(os.path.join(REPO, "code_clones.csv"))
    man = pd.read_csv(os.path.join(DATA, "cross_language_problem_manifest.csv"))
    test_rows = set(man[man.split == "test"].code_clones_row)
    jkey_to_row = {}
    for i, v in cc.java.items():
        if isinstance(v, str):
            jkey_to_row.setdefault(skey("java", v), i)
    z = zipfile.ZipFile(os.path.join(REPO, "cross_language_part_2.zip"))
    by_row = {}
    n_files = n_ok = 0
    for n in sorted(z.namelist()):
        if n.startswith("cross_java_to_other/Gpt4D") and n.endswith(".java"):
            n_files += 1
            r = parse_part2(z.read(n).decode("utf8", "ignore"))
            if r is None:
                continue
            java, got = r
            row = jkey_to_row.get(skey("java", java))
            if row is None or row not in test_rows or len(got) < 3 or row in by_row:
                continue
            by_row[row] = (java, got)
            n_ok += 1
    print("part-2 java files:", n_files, " usable test-side problems with 3 GPT-4 translations:", n_ok)
    snips, pairs = {}, []

    def reg(lang, code):
        k = skey(lang, code)
        snips[k] = (lang, code)
        return k

    rows = sorted(by_row)
    for r in rows:
        java, got = by_row[r]
        kj = reg("java", java)
        for lang in ("python", "c", "csharp"):
            k4 = reg(lang, got[lang])
            pairs.append(dict(gen="gpt4", kind="positive", label=1, row=r, lang2=lang, key1=kj, key2=k4))
            v3 = cc.loc[r, lang]
            if isinstance(v3, str) and v3.strip():
                k3 = reg(lang, v3)
                pairs.append(dict(gen="gpt3", kind="positive", label=1, row=r, lang2=lang, key1=kj, key2=k3))
    pos = [p for p in pairs if p["gen"] == "gpt4"]
    lang_counts = pd.Series([p["lang2"] for p in pos]).value_counts()
    seen = set()
    for gen in ("gpt4", "gpt3"):
        for _ in range(len(pos)):
            for tries in range(100):
                r1, r2 = rng.choice(rows, 2, replace=False)
                lang = rng.choice(lang_counts.index, p=(lang_counts / lang_counts.sum()).values)
                j1 = reg("java", by_row[r1][0])
                if gen == "gpt4":
                    k2 = reg(lang, by_row[r2][1][lang])
                else:
                    v3 = cc.loc[r2, lang]
                    if not isinstance(v3, str):
                        continue
                    k2 = reg(lang, v3)
                if (j1, k2) in seen:
                    continue
                seen.add((j1, k2))
                pairs.append(dict(gen=gen, kind="negative", label=0, row=r1, lang2=lang, key1=j1, key2=k2))
                break
    df = pd.DataFrame(pairs)
    df.insert(0, "pair_id", ["B%05d" % i for i in range(len(df))])
    df["lang1"] = "java"
    df["D_lang"] = 1
    df.to_csv(os.path.join(DATA, "probe_pairs.csv"), index=False)
    with open(os.path.join(DATA, "probe_snippets.pkl"), "wb") as f:
        pickle.dump(snips, f)
    print(df.groupby(["gen", "kind"]).size())
    print("snippets:", len(snips))


if __name__ == "__main__":
    main()
