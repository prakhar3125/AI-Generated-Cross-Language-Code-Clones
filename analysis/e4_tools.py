# -*- coding: utf-8 -*-
"""E4 (tools): JPlag (+ TokenNorm) and Dolos similarities of the original and the attacked (A1) pairs.
python -I e4_tools.py -> data/e4_tool_scores.csv (pair_id, variant orig|attacked, system, sim)"""
import os
import pickle
import sys
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA  # noqa: E402
from dolos_benchmark import run as dolos_run  # noqa: E402
from run_jplag import NORMALIZABLE, run_batch  # noqa: E402

pairs = pd.read_csv(os.path.join(DATA, "e4_pairs.csv"))
S = pickle.load(open(os.path.join(DATA, "snippets.pkl"), "rb"))
SA = pickle.load(open(os.path.join(DATA, "e4_snippets.pkl"), "rb"))
rows = []
for variant in ("orig", "attacked"):
    for lang, g in pairs.groupby("lang1"):
        recs = [("%s%s" % (r.pair_id, variant[0]), S[r.key1][1], (S[r.key2][1] if variant == "orig" else SA[r.akey2][1])) for r in g.itertuples()]
        for bi in range(0, len(recs), 100):
            batch = recs[bi:bi + 100]
            for cond in ("plain", "norm"):
                if cond == "norm" and lang not in NORMALIZABLE:
                    continue
                r = run_batch(batch, lang, cond == "norm", "e4_%s_%s_%s_%d" % (variant, lang, cond, bi))
                if not r:
                    continue
                m, _ = r
                for pid, _, _ in batch:
                    row = m.get(("%s_a" % pid, "%s_b" % pid)) or m.get(("%s_b" % pid, "%s_a" % pid))
                    rows.append((pid[:-1], variant, "jplag" if cond == "plain" else "tokennorm", float(row[2]) if row else 0.0))
            for pid, lg, sim in dolos_run((lang, bi + 100000 * (variant == "attacked"), batch)):
                rows.append((pid[:-1], variant, "dolos", sim))
        print(variant, lang, flush=True)
pd.DataFrame(rows, columns=["pair_id", "variant", "system", "sim"]).to_csv(os.path.join(DATA, "e4_tool_scores.csv"), index=False)
print("saved", len(rows))
