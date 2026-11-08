# -*- coding: utf-8 -*-
"""Independent-convergence pairs from the benchmark itself.

SemanticCloneBench seeds are crowd-sourced Stack Overflow snippets, so different problem groups
sometimes hold *independently written* implementations of the same function (e.g. two different
authors' isPrime).  We pair test-side snippets of the same language that belong to different problem
groups and define the same, non-generic function name.  These pairs implement the same task by
independent authors: exactly the case the framework cannot and should not separate from copying.

python -I build_convergence.py     -> data/convergence_pairs.csv
"""
import collections
import os
import pickle
import random
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA  # noqa: E402
import feature_pipeline as fp  # noqa: E402

ALGO = {"isanagram","reverse","isbalanced","tohexstring","ispalindrome","isprime","is_prime","removeduplicates","binary_search","collatz","factorial","flatten","int_to_roman","intersect","is_sorted","isperfectsquare","median","merge","merge_sort","same_structure","shufflearray","unique","cumulative_sum","rotateimage","zerofront","ispermutation","maxblock","countlines","compressbad","singlenumber","almostincreasingsequence","deep_reverse","searchwordlist","roundrobin","sublist","reverseparentheses","shuffle","find_nth"}
GENERIC = {"main", "run", "get", "set", "test", "init", "execute", "start", "stop", "update", "tick", "solution", "func",
           "foo", "bar", "doget", "dopost", "onclick", "oncreate", "tostring", "equals", "hashcode", "compare", "apply", "call"}
pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
S = pickle.load(open(os.path.join(DATA, "snippets.pkl"), "rb"))
grp = {}
for r in pf.itertuples():
    grp[r.key1] = r.group1
    grp[r.key2] = r.group2
test_keys = set(pf[pf.split == "test"].key1) | set(pf[pf.split == "test"].key2)


def first_name(code, lang):
    tree = fp.PARSERS[lang].parse(bytes(code, "utf8"))
    stack = [tree.root_node]
    while stack:
        n = stack.pop(0)
        if n.type in ("method_declaration", "function_definition", "local_function_statement"):
            nm = n.child_by_field_name("name")
            if nm is None:
                d = n.child_by_field_name("declarator")
                while d is not None and d.child_by_field_name("declarator") is not None:
                    d = d.child_by_field_name("declarator")
                nm = d
            if nm is not None:
                t = nm.text.decode("utf8", "ignore")
                return t.split("(")[0].strip().lower()
        stack.extend(n.children)
    return None


by = collections.defaultdict(list)
for k in sorted(test_keys):
    lang, code = S[k]
    if len(code.splitlines()) < 4:
        continue
    nm = first_name(code, lang)
    if nm and nm in ALGO:
        by[(lang, nm)].append(k)
rng = random.Random(42)
pairs = []
for (lang, nm), ks in sorted(by.items()):
    cand = [(a, b) for i, a in enumerate(ks) for b in ks[i + 1:] if grp[a] != grp[b]]
    rng.shuffle(cand)
    for a, b in cand[:4]:
        pairs.append(dict(lang1=lang, lang2=lang, key1=a, key2=b, name=nm, label=0, kind="convergence", D_lang=0))
df = pd.DataFrame(pairs)
df.insert(0, "pair_id", ["V%05d" % i for i in range(len(df))])
df.to_csv(os.path.join(DATA, "convergence_pairs.csv"), index=False)
print(len(df), df.groupby("lang1").size().to_dict(), df.name.nunique())
print(df.name.value_counts().head(12).to_dict())
