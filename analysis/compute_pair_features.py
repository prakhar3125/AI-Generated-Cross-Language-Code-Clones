# -*- coding: utf-8 -*-
"""Turn cached snippet features into the six-dimensional gate input per pair.

Definitions are those of repo/extract_features.py:
  S_CodeBERT : window embeddings -> de-anisotropy (mean-centre if >1 window)
               -> L2 -> cosine matrix -> symmetric top-3 aggregation
  S_AST      : min( exp(-2 d), max(0, cosine) ) over the 8-d AST ratio vector
  S_Token    : Jaccard of the 5-gram sets of tree-sitter leaf tokens
  D_lang     : 1 if the languages differ, else 0
  X5 = |S_CodeBERT - S_AST|,  X6 = 1 - S_AST

python -I compute_pair_features.py
"""
import os
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA  # noqa: E402


def _normalize(X):
    X = X.astype(np.float32, copy=False)
    # Mean-centre across windows only when there are at least three: centring two windows gives two opposite
    # rows (+u, -u), which makes S_sem 0 for two 2-window programs and halves it for one (Eq. 2 degeneracy).
    if X.shape[0] >= 3:
        X = X - X.mean(axis=0, keepdims=True)
    d = np.clip(np.linalg.norm(X, axis=1, keepdims=True), 1e-12, None)
    return X / d


def _topk(sim, k=3):
    k = max(1, min(k, sim.shape[0], sim.shape[1]))
    row = np.mean(np.mean(np.partition(sim, -k, axis=1)[:, -k:], axis=1))
    col = np.mean(np.mean(np.partition(sim, -k, axis=0)[-k:, :], axis=0))
    return float(0.5 * (row + col))


def sem(a, b):
    A, B = _normalize(a["win"]), _normalize(b["win"])
    return _topk(np.clip(A @ B.T, -1.0, 1.0), 3)


def ast_sim(a, b):
    v1, v2 = a["ast"], b["ast"]
    e = np.exp(-2.0 * np.linalg.norm(v1 - v2))
    n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
    c = 0.0
    if n1 > 1e-9 and n2 > 1e-9:
        c = max(0.0, float(np.dot(v1, v2) / (n1 * n2)))
    return float(np.clip(min(e, c), 0.0, 1.0))


def tok_sim(a, b):
    ga, gb = a["grams"], b["grams"]
    if not ga or not gb:
        return 0.0
    return len(ga & gb) / len(ga | gb)


def pair_features(a, b):
    s_c, s_a, s_t = sem(a, b), ast_sim(a, b), tok_sim(a, b)
    return s_c, s_a, s_t


def main():
    pairs = pd.read_csv(os.path.join(DATA, "pairs.csv"))
    with open(os.path.join(DATA, "snippet_feats.pkl"), "rb") as f:
        F = pickle.load(f)
    rows = []
    for r in pairs.itertuples():
        a, b = F[r.key1], F[r.key2]
        s_c, s_a, s_t = pair_features(a, b)
        rows.append((r.pair_id, s_c, s_a, s_t, float(r.D_lang), abs(s_c - s_a), 1.0 - s_a,
                     a["cc"], b["cc"], a["ntok"], b["ntok"]))
    out = pd.DataFrame(rows, columns=["pair_id", "S_CodeBERT", "S_AST", "S_Token", "D_lang",
                                      "S_CodeBERT_minus_S_AST", "one_minus_S_AST",
                                      "cc1", "cc2", "ntok1", "ntok2"])
    full = pairs.drop(columns=["D_lang"]).merge(out, on="pair_id")
    full.to_csv(os.path.join(DATA, "pair_features.csv"), index=False)
    print(full.groupby(["split", "slice"])[["S_CodeBERT", "S_AST", "S_Token"]].mean().round(3))
    print("saved", len(full))


if __name__ == "__main__":
    main()
