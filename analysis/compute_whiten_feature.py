# -*- coding: utf-8 -*-
"""Semantic expert with a whitened CodeBERT embedding space: ZCA whitening (eps = 1e-3 x mean eigenvalue) fitted on the window embeddings of the snippets of the
TRAINING split only (union over the three negative regimes), then the symmetric top-3 window cosine of the paper's expert.  One value per pair of pair_features.csv.
python -I compute_whiten_feature.py -> data/sem_whiten.csv"""
import os
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA  # noqa: E402

pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
F = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
tk = sorted(set(pf[pf.split == "train"].key1) | set(pf[pf.split == "train"].key2))
X = np.vstack([F[k]["win"] for k in tk]).astype(np.float64)
mu = X.mean(0)
w, V = np.linalg.eigh(np.cov((X - mu).T))
Wm = V @ np.diag(1.0 / np.sqrt(np.maximum(w, 0) + 1e-3 * w.mean())) @ V.T
cache = {}


def get(k):
    if k not in cache:
        Z = (F[k]["win"].astype(np.float64) - mu) @ Wm
        cache[k] = Z / np.clip(np.linalg.norm(Z, axis=1, keepdims=True), 1e-9, None)
    return cache[k]


def top3(a, b):
    sim = np.clip(a @ b.T, -1, 1)
    k = max(1, min(3, sim.shape[0], sim.shape[1]))
    return 0.5 * (np.mean(np.mean(np.partition(sim, -k, axis=1)[:, -k:], axis=1)) + np.mean(np.mean(np.partition(sim, -k, axis=0)[-k:, :], axis=0)))


vals = [top3(get(a), get(b)) for a, b in zip(pf.key1, pf.key2)]
pd.DataFrame({"pair_id": pf.pair_id, "S_sem_w": vals}).to_csv(os.path.join(DATA, "sem_whiten.csv"), index=False)
print("saved", len(vals), "mean", float(np.mean(vals)))
