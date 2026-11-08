# -*- coding: utf-8 -*-
"""Two artifacts cited in the manuscript.

1. Fidelity of the rebuilt feature pipeline against the earlier one: the earlier 10,608-pair
   file is shuffled with DataFrame.sample(frac=1, random_state=42); inverting that permutation
   maps each positive row to (problem, language pair), whose recomputed features are compared.
2. Composition of a seeded random sample of 600 judge-rejected ("false semantic clone") pairs:
   exact / renamed / refactored by the token-normalisation bands of the dataset build.

python -I fidelity_check.py       -> results_fidelity.json
"""
import json
import os
import random
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, FSC, REPO, two_snippets, read  # noqa: E402
from tokenizer import band, tokens  # noqa: E402

out = {}
old = pd.read_csv(os.path.join(REPO, "gptclonebench_features.csv"))
perm = pd.DataFrame(index=np.arange(len(old))).sample(frac=1, random_state=42).index.values
inv = {g: j for j, g in enumerate(perm)}
new = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
x = new[(new.slice == "cross-language") & (new.split != "test")].copy()
x["row"] = x.problem_id.str.slice(3).astype(int)
L = ["java", "python", "c", "csharp"]
combos = [(a, b) for i, a in enumerate(L) for b in L[i + 1:]]
rows = []
for r in x.itertuples():
    g = 6 * r.row + combos.index((r.lang1, r.lang2))
    o = old.iloc[inv[g]]
    rows.append((o.S_CodeBERT, r.S_CodeBERT, o.S_AST, r.S_AST, o.S_Token, r.S_Token))
a = np.array(rows)
out["fidelity"] = {"n_pairs": int(len(a))}
for i, n in enumerate(["S_CodeBERT", "S_AST", "S_Token"]):
    d = a[:, 2 * i] - a[:, 2 * i + 1]
    out["fidelity"][n] = dict(corr=float(np.corrcoef(a[:, 2 * i], a[:, 2 * i + 1])[0, 1]), mean_abs_diff=float(np.abs(d).mean()),
                              max_abs_diff=float(np.abs(d).max()))

files = []
for dp, _, fs in os.walk(FSC):
    for f in fs:
        files.append(os.path.join(dp, f))
files.sort()
random.Random(1).shuffle(files)
cnt = {"exact": 0, "renamed": 0, "refactored": 0, "unparsed": 0}
LANG = {"java": "java", "py": "python", "c": "c", "cs": "csharp"}
for p in files[:600]:
    lang = LANG[os.path.relpath(p, FSC).replace("\\", "/").split("/")[0]]
    sn = two_snippets(read(p))
    if sn is None:
        cnt["unparsed"] += 1
        continue
    s1, s2 = sn
    cnt[band(tokens(s1, lang), tokens(s1, lang, True), tokens(s2, lang), tokens(s2, lang, True))] += 1
out["false_pair_sample_600"] = cnt
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_fidelity.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
