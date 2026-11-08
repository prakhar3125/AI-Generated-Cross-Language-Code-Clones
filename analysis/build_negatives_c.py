# -*- coding: utf-8 -*-
"""Regime C: hard negatives mined with a criterion independent of every expert score.

Regime B mined its negatives with the same expert scores that the gate consumes
(CodeBERT cosine, then the mean of the three experts), so the gate's decisive behavior could
be partly an artifact of the mining.  Regime C ranks candidate partners only by the TF-IDF
cosine of their *identifier vocabularies* (lower-cased identifier tokens, no CodeBERT, no AST
statistics, no token k-gram Jaccard), inside the same split and language, excluding the
same problem group.  Exact expert scores are computed only for the chosen pair.

python -I build_negatives_c.py
"""
import os
import pickle
import re
import sys

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, SEED  # noqa: E402
from compute_pair_features import pair_features  # noqa: E402

rng = np.random.RandomState(SEED + 3)
pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
pr = pd.read_csv(os.path.join(DATA, "pairs.csv"))
F = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
S = pickle.load(open(os.path.join(DATA, "snippets.pkl"), "rb"))
grp = {}
for r in pr.itertuples():
    grp[r.key1] = r.group1
    grp[r.key2] = r.group2
ID = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def doc(code):
    return " ".join(w.lower() for w in ID.findall(code))


rows, used = [], set()
for sp in ("train", "val", "test"):
    sub = pf[pf.split == sp]
    keys = {}
    for r in sub[sub.label == 1].itertuples():
        keys[r.key1] = r.lang1
        keys[r.key2] = r.lang2
    allk = sorted(keys)
    vec = TfidfVectorizer(token_pattern=r"\S+", min_df=1, sublinear_tf=True)
    M = vec.fit_transform([doc(S[k][1]) for k in allk])
    idx = {k: i for i, k in enumerate(allk)}
    by_lang = {}
    for k in allk:
        by_lang.setdefault(keys[k], []).append(idx[k])
    for r in sub[sub.slice == "independent"].itertuples():
        cand = np.array(by_lang[r.lang2])
        sims = (M[idx[r.key1]] @ M[cand].T).toarray().ravel()
        order = cand[np.argsort(-sims)[:60]]
        c = [allk[i] for i in order if grp[allk[i]] != grp[r.key1] and allk[i] != r.key1
             and frozenset((r.key1, allk[i])) not in used][:3]
        if not c:
            continue
        k2 = c[rng.randint(len(c))]
        used.add(frozenset((r.key1, k2)))
        s_c, s_a, s_t = pair_features(F[r.key1], F[k2])
        rows.append(dict(split=sp, slice="tfidf_independent", label=0, lang1=r.lang1, lang2=r.lang2, key1=r.key1,
                         key2=k2, group1=grp[r.key1], group2=grp[k2], problem_id="G-%s-%s" % (grp[r.key1][:10], grp[k2][:10]),
                         band="tfidf_independent", tier=None, source="", D_lang=int(r.lang1 != r.lang2), S_CodeBERT=s_c,
                         S_AST=s_a, S_Token=s_t, S_CodeBERT_minus_S_AST=abs(s_c - s_a), one_minus_S_AST=1.0 - s_a,
                         cc1=F[r.key1]["cc"], cc2=F[k2]["cc"], ntok1=F[r.key1]["ntok"], ntok2=F[k2]["ntok"]))
    print(sp, sum(1 for x in rows if x["split"] == sp))
new = pd.DataFrame(rows)
new.insert(0, "pair_id", ["G%06d" % (i + 1) for i in range(len(new))])
pf = pf[pf.slice != "tfidf_independent"]
pr = pr[pr.slice != "tfidf_independent"]
pf = pd.concat([pf, new], ignore_index=True)
pr = pd.concat([pr, new[[c for c in pr.columns if c in new.columns]]], ignore_index=True)
pf.to_csv(os.path.join(DATA, "pair_features.csv"), index=False)
pr.to_csv(os.path.join(DATA, "pairs.csv"), index=False)
print(new.groupby("split")[["S_CodeBERT", "S_AST", "S_Token"]].mean().round(3))
