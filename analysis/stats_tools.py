# -*- coding: utf-8 -*-
"""Cluster-aware inference helpers (pairs that share a base problem are not independent)."""
import numpy as np
from scipy.stats import binomtest


def mcnemar_exact(a_ok, b_ok):
    """Classical exact McNemar over pairs (treats pairs as independent)."""
    a_ok, b_ok = np.asarray(a_ok, bool), np.asarray(b_ok, bool)
    b = int((a_ok & ~b_ok).sum())
    c = int((~a_ok & b_ok).sum())
    p = binomtest(b, b + c, 0.5).pvalue if b + c else 1.0
    return b, c, float(p)


def cluster_signflip(a_ok, b_ok, clusters, n_perm=100000, seed=0):
    """Paired sign-flip permutation test with one unit per cluster.

    d_g = (#correct for A) - (#correct for B) summed inside cluster g.  Under the null
    of exchangeability of the two systems every cluster's d_g is symmetric about 0, so
    signs are flipped cluster-wise.  Returns (observed mean difference per pair, p, n_effective_clusters).
    """
    a_ok, b_ok = np.asarray(a_ok, int), np.asarray(b_ok, int)
    _, inv = np.unique(np.asarray(clusters), return_inverse=True)
    d = np.bincount(inv, weights=(a_ok - b_ok).astype(float))
    d = d[d != 0]
    if len(d) == 0:
        return 0.0, 1.0, 0
    obs = abs(d.sum())
    rng = np.random.default_rng(seed)
    cnt, done = 0, 0
    while done < n_perm:
        m = min(4000, n_perm - done)
        sgn = rng.integers(0, 2, size=(m, len(d)), dtype=np.int8) * 2 - 1
        cnt += int((np.abs(sgn @ d) >= obs - 1e-9).sum())
        done += m
    return float((a_ok - b_ok).mean()), (1 + cnt) / (1 + n_perm), int(len(d))


def holm(pvals):
    """Holm-Bonferroni adjusted p-values (same order as input)."""
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * p[i])
        adj[i] = min(1.0, run)
    return adj


def cluster_counts(y, pred, clusters):
    """Per-cluster (tp, fp, fn, tn) table, clusters in sorted-unique order."""
    _, inv = np.unique(np.asarray(clusters), return_inverse=True)
    k = inv.max() + 1
    y, pred = np.asarray(y), np.asarray(pred)
    out = np.zeros((k, 4))
    out[:, 0] = np.bincount(inv, weights=((y == 1) & (pred == 1)), minlength=k)
    out[:, 1] = np.bincount(inv, weights=((y == 0) & (pred == 1)), minlength=k)
    out[:, 2] = np.bincount(inv, weights=((y == 1) & (pred == 0)), minlength=k)
    out[:, 3] = np.bincount(inv, weights=((y == 0) & (pred == 0)), minlength=k)
    return out


def f1_from(c):
    tp, fp, fn = c[..., 0], c[..., 1], c[..., 2]
    return 2 * tp / np.maximum(2 * tp + fp + fn, 1e-12)


def cluster_bootstrap(counts_by_system, clusters_n, metric=f1_from, B=2000, seed=0, chunk=500):
    """Bootstrap over clusters (vectorised).

    counts_by_system: dict name -> array [n_seed_or_1, n_clusters, 4]
    returns dict name -> array [B] of the metric averaged over the seed axis.
    """
    rng = np.random.default_rng(seed)
    out = {k: np.empty(B) for k in counts_by_system}
    done = 0
    while done < B:
        m = min(chunk, B - done)
        W = rng.multinomial(clusters_n, np.full(clusters_n, 1.0 / clusters_n), size=m).astype(float)   # [m, K]
        for k, c in counts_by_system.items():
            tot = np.einsum("mc,sck->msk", W, c)
            out[k][done:done + m] = metric(tot).mean(axis=1)
        done += m
    return out


def boot_p(d):
    """Two-sided bootstrap p value for a difference sample d (0 not in the interval)."""
    B = len(d)
    lo = (1 + np.sum(d <= 0)) / (B + 1)
    hi = (1 + np.sum(d >= 0)) / (B + 1)
    return float(min(1.0, 2 * min(lo, hi)))
