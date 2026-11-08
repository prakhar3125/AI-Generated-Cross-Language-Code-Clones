# -*- coding: utf-8 -*-
"""Build the current-generation generator probe from gen/out/{sonnet,opus}_chunk*.json.

Seeds are held-out (test-side) problems; the models were prompted for (a) behavior-preserving
translations of Java seeds into Python / C / C# and (b) same-language functionally equivalent
but structurally different rewrites.  No NiCad filter and no human validation were applied.
Control pairs use the benchmark's own GPT-3 translations of the same Java seeds.
Negatives pair a seed with the output for a different seed (same language relation).
"""
import glob
import json
import os
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, REPO, SEED, skey  # noqa: E402
from tokenizer import band, tokens  # noqa: E402
import feature_pipeline as fp  # noqa: E402 (tree-sitter parsers)


def bad(lang, code):
    return fp.PARSERS[lang].parse(bytes(code, 'utf8')).root_node.has_error

rng = np.random.RandomState(SEED)
HERE = os.path.dirname(os.path.abspath(__file__))
cc = pd.read_csv(os.path.join(REPO, "code_clones.csv"))
snips, pairs = {}, []


def reg(lang, code):
    k = skey(lang, code)
    snips[k] = (lang, code.strip())
    return k


def clean(c):
    c = c.strip()
    if c.startswith("```"):
        c = "\n".join(l for l in c.splitlines() if not l.strip().startswith("```"))
    return c.strip()


stats = {}
LABELS = ["claude-sonnet-5-5", "claude-sonnet-4-6", "gpt-6-sol", "gpt-5.4-mini"]
for model in LABELS:
    seeds, outs = {}, {}
    for f in sorted(glob.glob(os.path.join(HERE, "gen", "seeds", "chunk*.json"))):
        for it in json.load(open(f, encoding="utf8")):
            seeds[it["id"]] = it
    for f in sorted(glob.glob(os.path.join(HERE, "gen", "out", model + "_chunk*.json"))):
        for it in json.load(open(f, encoding="utf8")):
            outs[it["id"]] = it
    tr_pos, rf_pos = [], []
    for i, o in outs.items():
        s = seeds.get(i)
        if s is None:
            continue
        if s["task"] == "translate":
            got = {l: clean(o["outputs"].get(l, "")) for l in ("python", "c", "csharp")}
            if all(len(v) > 20 and not bad(l, v) for l, v in got.items()):
                tr_pos.append((s, got))
        else:
            out = clean(o.get("output", ""))
            if len(out) > 20 and not bad(s["lang"], out):
                rf_pos.append((s, out))
    stats[model] = dict(translate_problems=len(tr_pos), refactor_seeds=len(rf_pos))
    for s, got in tr_pos:
        kj = reg("java", s["code"])
        for l, code in got.items():
            pairs.append(dict(gen=model, kind="translate", label=1, row=s["row"], lang1="java", lang2=l, key1=kj, key2=reg(l, code)))
            v3 = cc.loc[s["row"], l]
            if isinstance(v3, str) and v3.strip() and model == LABELS[0]:       # GPT-3 control once
                pairs.append(dict(gen="gpt3", kind="translate", label=1, row=s["row"], lang1="java", lang2=l, key1=kj, key2=reg(l, v3)))
    for s, out in rf_pos:
        k1, k2 = reg(s["lang"], s["code"]), reg(s["lang"], out)
        b = band(tokens(s["code"], s["lang"]), tokens(s["code"], s["lang"], True), tokens(out, s["lang"]), tokens(out, s["lang"], True))
        pairs.append(dict(gen=model, kind="refactor", label=1, row=-1, lang1=s["lang"], lang2=s["lang"], key1=k1, key2=k2, band=b))
    # negatives
    pos_tr = [p for p in pairs if p["gen"] == model and p["kind"] == "translate"]
    pos_rf = [p for p in pairs if p["gen"] == model and p["kind"] == "refactor"]
    for grp, kind in ((pos_tr, "translate"), (pos_rf, "refactor")):
        used = set()
        for p in grp:
            for _ in range(200):
                q = grp[rng.randint(len(grp))]
                if q["key1"] == p["key1"] or q["lang2"] != p["lang2"] or (p["key1"], q["key2"]) in used:
                    continue
                used.add((p["key1"], q["key2"]))
                pairs.append(dict(gen=model, kind=kind, label=0, row=p["row"], lang1=p["lang1"], lang2=p["lang2"], key1=p["key1"], key2=q["key2"]))
                break
# GPT-3 negatives matched to the control positives
g3 = [p for p in pairs if p["gen"] == "gpt3" and p["label"] == 1]
used = set()
for p in g3:
    for _ in range(200):
        q = g3[rng.randint(len(g3))]
        if q["key1"] == p["key1"] or q["lang2"] != p["lang2"] or (p["key1"], q["key2"]) in used:
            continue
        used.add((p["key1"], q["key2"]))
        pairs.append(dict(gen="gpt3", kind="translate", label=0, row=p["row"], lang1="java", lang2=p["lang2"], key1=p["key1"], key2=q["key2"]))
        break
df = pd.DataFrame(pairs)
df.insert(0, "pair_id", ["C%05d" % i for i in range(len(df))])
df["D_lang"] = (df.lang1 != df.lang2).astype(int)
df.to_csv(os.path.join(DATA, "probe2_pairs.csv"), index=False)
pickle.dump(snips, open(os.path.join(DATA, "probe2_snippets.pkl"), "wb"))
print(json.dumps(stats))
print(df.groupby(["gen", "kind", "label"]).size())
print(df[(df.kind == "refactor") & (df.label == 1)].groupby(["gen", "band"]).size())
print("snippets", len(snips))
