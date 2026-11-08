"""Recompute S_CodeBERT (and S_CodeBERT_minus_S_AST) of every pair of data/pair_features.csv with the corrected Eq. 2
(window centring only for programs with >=3 windows). The pair set, splits and every other column are unchanged.
python -I recompute_sem_feature.py"""
import os, pickle, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA
import compute_pair_features as cpf
pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
F = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
old = pf.S_CodeBERT.values.copy()
new = np.array([cpf.sem(F[a], F[b]) for a, b in zip(pf.key1, pf.key2)])
two = {k for k, v in F.items() if len(v["win"]) == 2}
touched = (pf.key1.isin(two) | pf.key2.isin(two)).values
print("pairs", len(pf), "touched", int(touched.sum()), "| max change on untouched pairs %.2e" % np.abs(new - old)[~touched].max(),
      "| mean change on touched %.3f" % (new - old)[touched].mean())
pf["S_CodeBERT"] = new
pf["S_CodeBERT_minus_S_AST"] = (pf.S_CodeBERT - pf.S_AST).abs()
pf.to_csv(os.path.join(DATA, "pair_features.csv"), index=False)
print("saved")
