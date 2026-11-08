# -*- coding: utf-8 -*-
"""Build the problem-grouped train / validation / test protocol.

Why this exists
---------------
The earlier 10,608-pair development sample used all 884 cross-language
problems, so no problem-disjoint evaluation was possible. This script
re-draws every split at the level of *problem groups*:

  * A group is a connected component of the graph whose nodes are normalised
    snippet hashes and whose edges link the two snippets of every GPTCloneBench
    pair (true or false) and all four language versions of every
    code_clones.csv problem. Two pairs that share any snippet therefore always
    land in the same group, and a group is assigned to exactly one split.
  * The test side is fixed first: it contains every group touched by the
    corrected evaluation dataset (eval_dataset/eval_pairs.csv) for the exact,
    renamed, refactored slices, plus enough code_clones.csv problems to supply
    the 928-pair cross-language slice.
  * Training and validation are drawn only from groups that touch none of
    the test snippets.
  * Negatives are independent-program pairs (snippets from two different
    groups of the same split). The judge-rejected "false semantic clone"
    pairs are Type-I/II copies and are kept only as a separate diagnostic.

python -I build_protocol.py
"""
import collections
import json
import os
import pickle
import random
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (CANON, DATA, EVAL_DIR, FSC, LANGS, PROJECT, RELEASE, REPO, SEED, TSC,
                    UnionFind, read, skey, two_snippets)
from tokenizer import band, tokens  # noqa: E402  (from the dataset build folder)

rng = random.Random(SEED)
CACHE = os.path.join(DATA, "release_cache.pkl")

# --------------------------------------------------------------------------
# A. parse the GPTCloneBench release (cached)
# --------------------------------------------------------------------------
if os.path.exists(CACHE):
    with open(CACHE, "rb") as f:
        release = pickle.load(f)
    print("loaded release cache:", len(release), "pairs")
else:
    release = []
    for kind, base, tiers in (("true", TSC, ("MT3", "T4")), ("false", FSC, (None,))):
        for dcode in ("java", "py", "c", "cs"):
            lang = CANON[dcode]
            for prompt in (("prompt_1", "prompt_2") if kind == "true" else (None,)):
                for tier in tiers:
                    d = os.path.join(base, dcode)
                    if kind == "true":
                        d = os.path.join(d, prompt, tier)
                    if not os.path.isdir(d):
                        continue
                    for fn in sorted(os.listdir(d)):
                        sn = two_snippets(read(os.path.join(d, fn)))
                        if sn is None:
                            continue
                        s1, s2 = sn
                        b = None
                        if kind == "true":
                            b = band(tokens(s1, lang), tokens(s1, lang, True),
                                     tokens(s2, lang), tokens(s2, lang, True))
                        release.append(dict(kind=kind, lang=lang, prompt=prompt, tier=tier,
                                            band=b, s1=s1, s2=s2,
                                            k1=skey(lang, s1), k2=skey(lang, s2),
                                            rel=os.path.relpath(os.path.join(d, fn), RELEASE).replace("\\", "/")))
        print("parsed", kind, len(release))
    with open(CACHE, "wb") as f:
        pickle.dump(release, f)

snips = {}                      # key -> (lang, code)
for r in release:
    snips[r["k1"]] = (r["lang"], r["s1"])
    snips[r["k2"]] = (r["lang"], r["s2"])

# --------------------------------------------------------------------------
# B. cross-language problems from code_clones.csv
# --------------------------------------------------------------------------
cc = pd.read_csv(os.path.join(REPO, "code_clones.csv"))
xl_keys = {}                    # row -> {lang: key}
for i, row in cc.iterrows():
    d = {}
    for lang in LANGS:
        v = row[lang]
        if isinstance(v, str) and v.strip():
            k = skey(lang, v)
            snips[k] = (lang, v.strip())
            d[lang] = k
    xl_keys[i] = d
print("code_clones rows:", len(xl_keys),
      "with all 4 languages:", sum(len(v) == 4 for v in xl_keys.values()))

# --------------------------------------------------------------------------
# C. corrected evaluation dataset (test-side anchor)
# --------------------------------------------------------------------------
ev = pd.read_csv(os.path.join(EVAL_DIR, "eval_pairs.csv"))
ev_nonxl = ev[ev["slice"] != "cross-language"].copy()


def ev_snips(r):
    out = []
    for rel, lang in ((r.snippet1_relpath, r.lang1), (r.snippet2_relpath, r.lang2)):
        code = read(os.path.join(EVAL_DIR, rel)).strip()
        k = skey(lang, code)
        snips[k] = (lang, code)
        out.append(k)
    return out


ev_nonxl["k1"], ev_nonxl["k2"] = zip(*[ev_snips(r) for r in ev_nonxl.itertuples()])
aux_ids = set(ev[ev["slice"] == "negative"].sample(n=1000, random_state=SEED).pair_id)
ev_nonxl = ev_nonxl[(ev_nonxl["slice"] != "negative") | ev_nonxl.pair_id.isin(aux_ids)].copy()

# --------------------------------------------------------------------------
# D. groups = connected components over snippet keys
# --------------------------------------------------------------------------
uf = UnionFind()
for r in release:
    uf.union(r["k1"], r["k2"])
for i, d in xl_keys.items():
    ks = list(d.values())
    for k in ks[1:]:
        uf.union(ks[0], k)
for r in ev_nonxl.itertuples():
    uf.union(r.k1, r.k2)

comp_size = collections.Counter(uf.find(k) for k in snips)
big = comp_size.most_common(3)
print("snippets:", len(snips), "groups:", len(comp_size), "largest groups:", big)

# --------------------------------------------------------------------------
# E. fix the test side
# --------------------------------------------------------------------------
test_comp = {uf.find(k) for k in list(ev_nonxl.k1) + list(ev_nonxl.k2)}
row_comp = {i: uf.find(next(iter(d.values()))) for i, d in xl_keys.items()}
M = sorted(i for i, c in row_comp.items() if c in test_comp)
print("code_clones rows pulled to the test side by non-cross-language evaluation pairs:", len(M))
M_PULLED = len(M)
N_XL_PAIRS = 928
need_rows = -(-N_XL_PAIRS // 3)           # 3 java->X pairs per row
H = list(M)
if len(H) < need_rows:
    cand = [i for i in sorted(xl_keys) if i not in set(H) and len(xl_keys[i]) == 4]
    rng.shuffle(cand)
    H += cand[: need_rows - len(H)]
H = sorted(H)
for i in H:
    test_comp.add(row_comp[i])
print("cross-language problems held out for test:", len(H))
H_set = set(H)

# --------------------------------------------------------------------------
# F. assign remaining groups to train / validation
# --------------------------------------------------------------------------
VAL_FRAC = 0.18
comp_pairs = collections.defaultdict(list)          # standalone true pairs by group
for idx, r in enumerate(release):
    if r["kind"] == "true":
        comp_pairs[uf.find(r["k1"])].append(idx)
free_rows = [i for i in sorted(xl_keys) if row_comp[i] not in test_comp and len(xl_keys[i]) == 4]
free_comps = sorted((set(comp_pairs) | {row_comp[i] for i in free_rows}) - test_comp)
rng.shuffle(free_comps)
nv = int(round(VAL_FRAC * len(free_comps)))
split_of_comp = {c: ("val" if j < nv else "train") for j, c in enumerate(free_comps)}
sa_comps = [c for c in free_comps if c in comp_pairs]
split_of_row = {i: split_of_comp[row_comp[i]] for i in free_rows}
for i in H:
    split_of_row[i] = "test"
print("free groups: train %d, val %d" % (len(free_comps) - nv, nv))
print("free cross-language problems: train %d, val %d" %
      (sum(v == "train" for v in split_of_row.values()),
       sum(v == "val" for v in split_of_row.values())))

# --------------------------------------------------------------------------
# G. positives
# --------------------------------------------------------------------------
pairs = []


def add(split, sl, label, l1, l2, k1, k2, prob, band_=None, tier=None, src=""):
    pairs.append(dict(split=split, slice=sl, label=label, lang1=l1, lang2=l2, key1=k1, key2=k2,
                      group1=uf.find(k1), group2=uf.find(k2), problem_id=prob, band=band_,
                      tier=tier, source=src))


# test: same-language positives and judge-rejected diagnostics, exactly as in eval_pairs.csv
for r in ev_nonxl.itertuples():
    if r.slice == "negative":
        continue
    add("test", r.slice, 1, r.lang1, r.lang2, r.k1, r.k2, r.problem_id, r.slice,
        None, r.source_file)

# test: cross-language slice, java original -> translation, from held-out problems
xl_all = [(i, l2) for i in H for l2 in ("python", "c", "csharp") if l2 in xl_keys[i]]
rng.shuffle(xl_all)
xl_cands, seen_rows = [], set()
for c in xl_all:                      # one pair per problem first ...
    if len(xl_cands) < N_XL_PAIRS and c[0] not in seen_rows:
        seen_rows.add(c[0])
        xl_cands.append(c)
for c in xl_all:                      # ... then fill the remainder
    if len(xl_cands) < N_XL_PAIRS and c not in xl_cands:
        xl_cands.append(c)
for i, l2 in xl_cands:
    add("test", "cross-language", 1, "java", l2, xl_keys[i]["java"], xl_keys[i][l2],
        "XL-%d" % i, "cross-language", None, "code_clones.csv#row %d" % i)

# train / validation: all 6 language combinations per cross-language problem
combos = [(a, b) for ai, a in enumerate(LANGS) for b in LANGS[ai + 1:]]
for i, sp in sorted(split_of_row.items()):
    if sp == "test":
        continue
    for a, b in combos:
        add(sp, "cross-language", 1, a, b, xl_keys[i][a], xl_keys[i][b], "XL-%d" % i,
            "cross-language", None, "code_clones.csv#row %d" % i)

n_xl = {sp: sum(1 for p in pairs if p["split"] == sp and p["slice"] == "cross-language")
        for sp in ("train", "val")}
# same-language positives: keep the cross-language share near the evaluation set's 35%
share = 928 / 2652.0
quota = {sp: int(round(n_xl[sp] * (1 - share) / share)) for sp in n_xl}
for sp in ("train", "val"):
    comps = [c for c in sa_comps if split_of_comp[c] == sp]
    cand = []
    for c in comps:
        idxs = comp_pairs[c][:]
        rng.shuffle(idxs)
        cand += idxs[:4]                       # at most four pairs per group
    rng.shuffle(cand)
    take = cand[: quota[sp]]
    for idx in take:
        r = release[idx]
        add(sp, "same-language", 1, r["lang"], r["lang"], r["k1"], r["k2"],
            "T-%s" % uf.find(r["k1"])[:14], r["band"], r["tier"], r["rel"])
    print("%s: cross-language positives %d, same-language positives %d (available %d, groups %d)"
          % (sp, n_xl[sp], len(take), len(cand), len(comps)))

# --------------------------------------------------------------------------
# H. negatives = independent-program pairs inside each split
# --------------------------------------------------------------------------
used_pairs = set()


def make_negatives(sp, n_total):
    pos = [p for p in pairs if p["split"] == sp and p["label"] == 1]
    xl = [p for p in pos if p["lang1"] != p["lang2"]]
    sl = [p for p in pos if p["lang1"] == p["lang2"]]
    n_cross = int(round(n_total * len(xl) / len(pos)))
    pool = collections.defaultdict(dict)       # lang -> key -> group
    for p in pos:
        pool[p["lang1"]][p["key1"]] = p["group1"]
        pool[p["lang2"]][p["key2"]] = p["group2"]
    pool = {l: list(d.items()) for l, d in pool.items()}
    cross_combo = collections.Counter((p["lang1"], p["lang2"]) for p in xl)
    same_lang = collections.Counter(p["lang1"] for p in sl)

    def draw(combo_counter, n, cross):
        combos_, w = zip(*combo_counter.items())
        out, tries = [], 0
        while len(out) < n and tries < n * 200:
            tries += 1
            c = rng.choices(combos_, weights=w)[0]
            l1, l2 = c if cross else (c, c)
            (ka, ga), (kb, gb) = rng.choice(pool[l1]), rng.choice(pool[l2])
            if ga == gb or ka == kb:
                continue
            key = frozenset((ka, kb))
            if key in used_pairs:
                continue
            used_pairs.add(key)
            out.append((l1, l2, ka, kb))
        return out

    negs = draw(cross_combo, n_cross, True) + draw(same_lang, n_total - n_cross, False)
    for l1, l2, ka, kb in negs:
        add(sp, "independent", 0, l1, l2, ka, kb, "I-%s-%s" % (uf.find(ka)[:10], uf.find(kb)[:10]),
            "independent", None, "")
    print("%s: independent negatives %d (cross-language %d)" % (sp, len(negs), n_cross))


for sp in ("train", "val"):
    make_negatives(sp, sum(1 for p in pairs if p["split"] == sp and p["label"] == 1))
make_negatives("test", 3000)

# --------------------------------------------------------------------------
# I. diagnostic: judge-rejected Type-I/II "false semantic clone" pairs (never used as negatives)
# --------------------------------------------------------------------------
neg_ev = ev[ev["pair_id"].isin(aux_ids)].copy()
for r in neg_ev.itertuples():
    ks = ev_snips(r)
    add("aux", "judge_rejected", 0, r.lang1, r.lang2, ks[0], ks[1], r.problem_id,
        "judge_rejected", None, r.source_file)
    uf.union(ks[0], ks[1])

df = pd.DataFrame(pairs)
df.insert(0, "pair_id", ["Q%06d" % (i + 1) for i in range(len(df))])
df["D_lang"] = (df.lang1 != df.lang2).astype(int)

# ---- disjointness checks -------------------------------------------------
grp_split = collections.defaultdict(set)
for r in df.itertuples():
    if r.split == "aux":
        continue
    grp_split[r.group1].add(r.split)
    grp_split[r.group2].add(r.split)
viol = {g: s for g, s in grp_split.items() if len(s) > 1}
print("groups appearing in more than one split (must be 0):", len(viol))
sn_split = collections.defaultdict(set)
for r in df.itertuples():
    sn_split[r.key1].add(r.split)
    sn_split[r.key2].add(r.split)
aux_overlap = sum(1 for k, s in sn_split.items() if "aux" in s and (s & {"train", "val"}))
print("diagnostic-pair snippets shared with train/val (must be 0):", aux_overlap)
snip_viol = sum(1 for k, s in sn_split.items() if len(s - {"aux"}) > 1)
for k, s_ in list(sn_split.items()):
    if len(s_ - {"aux"}) > 1:
        print("  VIOLATION", k, s_, df[(df.key1 == k) | (df.key2 == k)][["split", "slice", "label"]].drop_duplicates().values.tolist())
print("snippets used in more than one of train/val/test (must be 0):", snip_viol)

df.to_csv(os.path.join(DATA, "pairs.csv"), index=False)
with open(os.path.join(DATA, "snippets.pkl"), "wb") as f:
    pickle.dump({k: snips[k] for k in set(df.key1) | set(df.key2)}, f)

summ = (df.groupby(["split", "slice", "label"]).size().rename("pairs").reset_index())
print(summ.to_string(index=False))
stats = {
    "seed": SEED,
    "groups_total": len(comp_size),
    "largest_group_sizes": [c for _, c in big],
    "heldout_cross_language_problems": len(H),
    "cross_language_rows_pulled_by_shared_snippets": M_PULLED,
    "cross_language_problems_by_split": dict(collections.Counter(split_of_row.values())),
    "pairs_by_split_slice_label": {"%s|%s|%d" % k: int(v) for k, v in
                                   df.groupby(["split", "slice", "label"]).size().items()},
    "distinct_groups_by_split": {sp: int(len(set(df[df.split == sp].group1) | set(df[df.split == sp].group2)))
                                 for sp in ("train", "val", "test", "aux")},
    "distinct_snippets": len(set(df.key1) | set(df.key2)),
    "violations": {"groups": len(viol), "snippets": snip_viol, "aux_vs_trainval": aux_overlap},
}
with open(os.path.join(DATA, "protocol_stats.json"), "w") as f:
    json.dump(stats, f, indent=2)

# problem-ID manifest released with the code
seen = {}
for sp in ("train", "val", "test", "aux"):
    sub = df[df.split == sp]
    for g in sorted(set(sub.group1) | set(sub.group2)):
        seen.setdefault(g, set()).add(sp)
man = []
for g, sps in seen.items():
    main_sp = [x for x in ("train", "val", "test") if x in sps]
    man.append((g, main_sp[0] if main_sp else "aux", int("aux" in sps and bool(main_sp))))
pd.DataFrame(man, columns=["group_id", "split", "also_in_aux"]).to_csv(os.path.join(DATA, "problem_group_manifest.csv"), index=False)
mrows = [(i, split_of_row[i], ";".join(xl_keys[i].values())) for i in sorted(split_of_row)]
pd.DataFrame(mrows, columns=["code_clones_row", "split", "snippet_keys"]).to_csv(
    os.path.join(DATA, "cross_language_problem_manifest.csv"), index=False)
print(json.dumps(stats, indent=2))
