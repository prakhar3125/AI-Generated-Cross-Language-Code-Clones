# -*- coding: utf-8 -*-
"""Real student submissions (PROGpedia, Zenodo 10.5281/zenodo.7449056) as an external check.

Whole programs (Java, Python, C) submitted to 16 introductory assignments; directory names give
problem / verdict / submitter_attempt.  There are no plagiarism labels, so two kinds of pairs are built
inside each (problem, language) group:

  same-author   : two attempts by the same submitter on the same problem (derivation by the same
                  person: a natural, if easy, positive);
  cross-author  : attempts by two different submitters (independent work, plus an unknown amount of
                  real copying) -- a noisy negative, so flag rates on it bound the false-positive
                  burden from above.

No boilerplate is stripped: files are used as submitted.

python -I build_progpedia.py
"""
import collections
import os
import pickle
import random
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, PROJECT, skey  # noqa: E402

ROOT = os.path.join(PROJECT, "tools", "progpedia")
LANG = {"java": "java", "py": "python", "c": "c"}
rng = random.Random(42)
recs = []
for p in sorted(os.listdir(ROOT)):
    pp = os.path.join(ROOT, p)
    if not os.path.isdir(pp):
        continue
    for v in os.listdir(pp):
        vp = os.path.join(pp, v)
        if not os.path.isdir(vp):
            continue
        for sa in os.listdir(vp):
            d = os.path.join(vp, sa)
            for f in os.listdir(d):
                ext = f.rsplit(".", 1)[-1]
                if ext in LANG:
                    s, a = sa.split("_")
                    code = open(os.path.join(d, f), encoding="utf-8", errors="ignore").read().strip()
                    if 80 <= len(code) <= 12000:
                        recs.append(dict(problem=p, verdict=v, submitter=s, attempt=int(a), lang=LANG[ext], code=code))
df = pd.DataFrame(recs)
snips, pairs = {}, []
for (p, lang), g in df.groupby(["problem", "lang"]):
    by_sub = {s: sub.sort_values("attempt") for s, sub in g.groupby("submitter")}
    multi = [s for s, sub in by_sub.items() if len(sub) >= 2]
    single = [s for s, sub in by_sub.items() if len(sub) == 1]
    if len(multi) < 12:
        continue
    rng.shuffle(multi)
    rng.shuffle(single)
    chosen = multi[:30] + single[:20]
    files = []
    for s in chosen:
        for r in by_sub[s].itertuples():
            k = skey(lang, r.code)
            snips[k] = (lang, r.code)
            files.append((s, r.attempt, k))
    pos = []
    for s in chosen:
        ks = [k for (ss, a, k) in files if ss == s]
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                if ks[i] != ks[j]:
                    pos.append((ks[i], ks[j]))
    cross = [(a, b) for (s1, _, a) in files for (s2, _, b) in files if s1 < s2]
    rng.shuffle(cross)
    for a, b in pos:
        pairs.append(dict(problem=p, lang1=lang, lang2=lang, key1=a, key2=b, label=1, kind="same_author"))
    for a, b in cross[:600]:
        pairs.append(dict(problem=p, lang1=lang, lang2=lang, key1=a, key2=b, label=0, kind="cross_author"))
out = pd.DataFrame(pairs)
out.insert(0, "pair_id", ["R%06d" % i for i in range(len(out))])
out["D_lang"] = 0
out.to_csv(os.path.join(DATA, "progpedia_pairs.csv"), index=False)
pickle.dump(snips, open(os.path.join(DATA, "progpedia_snippets.pkl"), "wb"))
print(out.groupby(["lang1", "kind"]).size())
print("snippets", len(snips), "pairs", len(out))
