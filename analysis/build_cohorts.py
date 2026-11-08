# -*- coding: utf-8 -*-
"""Cohort screening sets with real derived submissions.

Sources (both downloaded, CC-BY / Apache-2.0):
  * Maisch et al. replication package (Zenodo 10.5281/zenodo.18089904): the two PROGpedia assignments
    Progpedia19 and Progpedia56 (Java); for each real submission an insertion-based variant (dead statements),
    an automatically refactored variant and, for five submissions, GPT-4 rewrites under 16 prompts.
  * IR-Plag (Karnalim et al. 2019): seven Java tasks, each with the lecturer's solution, independent student
    solutions and plagiarized versions of the solution at six levels (L1 comments/layout ... L6 program logic).

Cohort protocol (an instructor screening one assignment):
  honest set H : PROGpedia -> all real submissions;  IR-Plag -> lecturer solution + independent solutions
  one derived submission d (one cohort per derived file) with source s in H
  derived pair   = (s, d)
  non-derived    = all pairs inside H, and (d, h) for every h in H other than s
  cohort AUROC   = share of non-derived pairs scored below the derived pair (ties count 1/2)

python -I build_cohorts.py -> data/cohort_snippets.pkl, data/cohort_pairs.csv, data/cohort_meta.csv
"""
import os
import pickle
import re
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, PROJECT, skey  # noqa: E402

MAI = os.path.join(PROJECT, "tools", "maisch_dl", "x", "datasets")
IRP = os.path.join(PROJECT, "tools", "irplag_dl", "x", "IR-Plag-Dataset")


def rd(p):
    return open(p, encoding="utf-8", errors="ignore").read().strip()


def dir_code(d):
    fs = sorted(f for f in os.listdir(d) if f.endswith(".java"))
    return "\n\n".join(rd(os.path.join(d, f)) for f in fs)


subs = []  # dict(group, id, role, src, kind, code)
# ---- PROGpedia (Maisch package)
for a in ("Progpedia19", "Progpedia56"):
    root = os.path.join(MAI, a)
    hum = {}
    for d in sorted(os.listdir(os.path.join(root, "human"))):
        p = os.path.join(root, "human", d)
        if os.path.isdir(p) and any(f.endswith(".java") for f in os.listdir(p)):
            hum[d] = dir_code(p)
            subs.append(dict(group=a, id=d, role="honest", src="", kind="", code=hum[d]))
    for kind, pref in (("insert", r"plag-(subm\d+)"), ("refactor", r"plag-(subm\d+)"), ("gptobf", r"gpt(\d+)-(subm\d+)")):
        kp = os.path.join(root, kind)
        if not os.path.isdir(kp):
            continue
        for d in sorted(os.listdir(kp)):
            p = os.path.join(kp, d)
            m = re.fullmatch(pref, d)
            if not (os.path.isdir(p) and m):
                continue
            src = m.group(m.lastindex)
            if src not in hum or not any(f.endswith(".java") for f in os.listdir(p)):
                continue
            subs.append(dict(group=a, id=kind + ":" + d, role="derived", src=src, kind=kind, code=dir_code(p)))
# ---- IR-Plag
for c in sorted(os.listdir(IRP)):
    root = os.path.join(IRP, c)
    if not os.path.isdir(root) or not c.startswith("case-"):
        continue
    g = "IRPlag-" + c
    o = os.path.join(root, "original")
    orig_id = "orig"
    subs.append(dict(group=g, id=orig_id, role="honest", src="", kind="", code=dir_code(o)))
    npd = os.path.join(root, "non-plagiarized")
    for d in sorted(os.listdir(npd)):
        if d == "15":      # alike to submission 13 in several cases (dataset README); excluded
            continue
        subs.append(dict(group=g, id="np" + d, role="honest", src="", kind="", code=dir_code(os.path.join(npd, d))))
    for lv in sorted(os.listdir(os.path.join(root, "plagiarized"))):
        lp = os.path.join(root, "plagiarized", lv)
        for d in sorted(os.listdir(lp)):
            if os.path.isdir(os.path.join(lp, d)):
                subs.append(dict(group=g, id="%s:%s" % (lv, d), role="derived", src=orig_id, kind=lv, code=dir_code(os.path.join(lp, d))))
S = pd.DataFrame(subs)
S = S[S.code.str.len() >= 40].reset_index(drop=True)
S["key"] = [skey("java", c) for c in S.code]
snips = {k: ("java", c) for k, c in zip(S.key, S.code)}

pairs, meta = [], []
for g, G in S.groupby("group"):
    H = G[G.role == "honest"]
    D = G[G.role == "derived"]
    Hid = H.set_index("id").key.to_dict()
    ids = sorted(Hid)
    seen = {}

    def add(a, b, ia, ib):
        t = tuple(sorted((ia, ib)))
        if t not in seen:
            seen[t] = "P%06d" % len(pairs)
            pairs.append(dict(pair_id=seen[t], group=g, id1=ia, id2=ib, key1=a, key2=b))
        return seen[t]

    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            add(Hid[a], Hid[b], a, b)
    for r in D.itertuples():
        if r.src not in Hid:
            continue
        dp = add(Hid[r.src], r.key, r.src, r.id)
        for h in ids:
            add(Hid[h], r.key, h, r.id)
        meta.append(dict(group=g, derived=r.id, kind=r.kind, src=r.src, derived_pair=dp))
P = pd.DataFrame(pairs)
P["lang1"] = P["lang2"] = "java"
P["D_lang"] = 0
P["label"] = -1
M = pd.DataFrame(meta)
H = S[S.role == "honest"].groupby("group").size().rename("n_honest")
print(S.groupby(["group", "role"]).size().unstack())
print(M.groupby(["group", "kind"]).size().unstack(fill_value=0))
print("pairs", len(P), "cohorts", len(M), "snippets", len(snips))
pickle.dump(snips, open(os.path.join(DATA, "cohort_snippets.pkl"), "wb"))
P.to_csv(os.path.join(DATA, "cohort_pairs.csv"), index=False)
M.to_csv(os.path.join(DATA, "cohort_meta.csv"), index=False)
S[["group", "id", "role", "src", "kind", "key"]].to_csv(os.path.join(DATA, "cohort_subs.csv"), index=False)
