# -*- coding: utf-8 -*-
"""Second negative regime: nearest-neighbour independent pairs ("hard" negatives).

Random independent pairs share almost no tokens, so on them a lexical detector is already
near-perfect. For every independent negative we therefore build a partner pair in which
the second snippet is the most similar snippet (language and split fixed) that belongs to a
*different problem group*:

  1. shortlist the 40 candidates with the highest cosine between first-window CodeBERT
     embeddings;
  2. compute the exact (S_CodeBERT, S_AST, S_Token) of each shortlisted pair;
  3. take the candidate with the highest mean of the three (random choice among the
     top three, seeded, to avoid always reusing the same snippet).

Anchors and candidates come from the same split, so the split guarantees (no shared group
across splits) are preserved.  Pairs of different groups can still, rarely, implement the
same task; the manuscript reports a manual audit of a random sample.

python -I build_hard_negatives.py
"""
import os
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, SEED  # noqa: E402
from compute_pair_features import pair_features  # noqa: E402

rng = np.random.RandomState(SEED)
pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
pr = pd.read_csv(os.path.join(DATA, "pairs.csv"))
with open(os.path.join(DATA, "snippet_feats.pkl"), "rb") as f:
    F = pickle.load(f)
grp = {}
for r in pr.itertuples():
    grp[r.key1] = r.group1
    grp[r.key2] = r.group2

new_rows = []
used = set()
for sp in ("train", "val", "test"):
    sub = pf[pf.split == sp]
    pool = {}
    for r in sub[sub.label == 1].itertuples():
        pool.setdefault(r.lang1, set()).add(r.key1)
        pool.setdefault(r.lang2, set()).add(r.key2)
    pool = {l: sorted(v) for l, v in pool.items()}
    emb = {}
    for l, keys in pool.items():
        M = np.vstack([F[k]["win"][0] for k in keys]).astype(np.float32)
        M /= np.clip(np.linalg.norm(M, axis=1, keepdims=True), 1e-9, None)
        emb[l] = M
    index = {l: {k: i for i, k in enumerate(v)} for l, v in pool.items()}
    negs = sub[sub.slice == "independent"]
    for r in negs.itertuples():
        l2 = r.lang2
        qa = F[r.key1]["win"][0].astype(np.float32)
        qa = qa / max(np.linalg.norm(qa), 1e-9)
        sims = emb[l2] @ qa
        order = np.argsort(-sims)[:80]
        cands = [pool[l2][i] for i in order if grp[pool[l2][i]] != grp[r.key1] and pool[l2][i] != r.key1][:40]
        scored = []
        for k in cands:
            if frozenset((r.key1, k)) in used:
                continue
            s = pair_features(F[r.key1], F[k])
            scored.append((np.mean(s), k, s))
        if not scored:
            continue
        scored.sort(key=lambda t: -t[0])
        _, k2, (s_c, s_a, s_t) = scored[rng.randint(0, min(3, len(scored)))]
        used.add(frozenset((r.key1, k2)))
        new_rows.append(dict(
            split=sp, slice="hard_independent", label=0, lang1=r.lang1, lang2=l2, key1=r.key1, key2=k2,
            group1=grp[r.key1], group2=grp[k2], problem_id="H-%s-%s" % (grp[r.key1][:10], grp[k2][:10]),
            band="hard_independent", tier=None, source="", D_lang=int(r.lang1 != l2),
            S_CodeBERT=s_c, S_AST=s_a, S_Token=s_t, S_CodeBERT_minus_S_AST=abs(s_c - s_a),
            one_minus_S_AST=1.0 - s_a, cc1=F[r.key1]["cc"], cc2=F[k2]["cc"],
            ntok1=F[r.key1]["ntok"], ntok2=F[k2]["ntok"]))
    print(sp, "hard negatives:", sum(1 for x in new_rows if x["split"] == sp))

hard = pd.DataFrame(new_rows)
hard.insert(0, "pair_id", ["H%06d" % (i + 1) for i in range(len(hard))])
pf = pf[pf.slice != "hard_independent"]
pr = pr[pr.slice != "hard_independent"]
pf = pd.concat([pf, hard], ignore_index=True)
pr = pd.concat([pr, hard[[c for c in pr.columns if c in hard.columns]]], ignore_index=True)
pf.to_csv(os.path.join(DATA, "pair_features.csv"), index=False)
pr.to_csv(os.path.join(DATA, "pairs.csv"), index=False)
print(hard.groupby("split")[["S_CodeBERT", "S_AST", "S_Token"]].mean().round(3))
ind = pf[pf.slice == "independent"].groupby("split")[["S_CodeBERT", "S_AST", "S_Token"]].mean().round(3)
print("independent (for comparison):\n", ind)
