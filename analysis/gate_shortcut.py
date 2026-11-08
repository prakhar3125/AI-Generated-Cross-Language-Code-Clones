"""Shortcut check and cohort vectors for the gate variants.
 (1) length-only baseline: AUROC of a classifier that sees ONLY the evidence-quality inputs (min length, length ratio, complexity);
     if it is high, those inputs can separate classes without comparing the programs.
 (2) length-matched test set: test pairs are binned on the length ratio |log(1+n1) - log(1+n2)| and positives/negatives subsampled to
     equal counts per bin (seeded), then AUROC and F1 of every variant are recomputed on that subset.
 (3) per-cohort AUROC vectors of every variant (ensemble over seeds) saved for paired cluster-bootstrap tests.
Kinds: logit, logit_len (min length + complexity, no ratio), logit_feat, direct, direct_feat, direct_len, base.
REGIME=A|B|C python -I gate_shortcut.py -> results_<R>/gate_shortcut.json, results_<R>/gate_cohort_vectors.npz"""
import json, os, sys
from multiprocessing import Pool
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate_variants as gv
from common import DATA
from exp_lib import SEEDS, TAG

KINDS = ["base", "logit", "logit_len", "logit_feat", "direct", "direct_len", "direct_feat"]

def job(a):
    kind, seed = a
    k, s, thr, st, sc, wt, wc = gv.job((kind, seed))
    return kind, seed, thr, st, sc

def cohort_vectors(sc, P, M, S):
    hon = {g: set(G[G.role == "honest"].id) for g, G in S.groupby("group")}
    out = []
    for g, G in P.groupby("group"):
        h = hon[g]; hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
        for d in M[M.group == g].itertuples():
            dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
            nd = np.concatenate([hh, np.array([i for i in dm if i != d.derived_pair and not ((P.id1[i] == d.src) or (P.id2[i] == d.src))])])
            dp = int(P.index[P.pair_id == d.derived_pair][0]); x = sc[nd]
            out.append((g + "|" + d.src, g, (x < sc[dp]).mean() + .5 * (x == sc[dp]).mean()))
    return out

def f1(y, p):
    tp = ((p == 1) & (y == 1)).sum(); return float(2 * tp / max(2 * tp + ((p == 1) & (y == 0)).sum() + ((p == 0) & (y == 1)).sum(), 1))

if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    te, tr = gv.te, gv.tr; y = te.label.values
    # (1) length-only baseline
    Ftr = gv.extras(tr.cc1, tr.cc2, tr.ntok1, tr.ntok2); Fte = gv.extras(te.cc1, te.cc2, te.ntok1, te.ntok2)
    lr = LogisticRegression(max_iter=1000).fit((Ftr - Ftr.mean(0)) / (Ftr.std(0) + 1e-9), tr.label.values)
    p_len = lr.predict_proba((Fte - Ftr.mean(0)) / (Ftr.std(0) + 1e-9))[:, 1]
    out = {"length_only_auc": float(roc_auc_score(y, p_len)),
           "length_ratio_only_auc": float(roc_auc_score(y, LogisticRegression(max_iter=1000).fit(Ftr[:, [1]], tr.label.values).predict_proba(Fte[:, [1]])[:, 1]))}
    print(TAG, "length-only AUROC %.3f | ratio-only AUROC %.3f" % (out["length_only_auc"], out["length_ratio_only_auc"]), flush=True)
    # (2) length-matched subset
    ratio = Fte[:, 1]; edges = np.quantile(ratio, np.linspace(0, 1, 11)[1:-1]); b = np.digitize(ratio, edges)
    rng = np.random.default_rng(0); keep = []
    for k in range(10):
        pi = np.where((b == k) & (y == 1))[0]; ni = np.where((b == k) & (y == 0))[0]; n = min(len(pi), len(ni))
        if n: keep += list(rng.choice(pi, n, replace=False)) + list(rng.choice(ni, n, replace=False))
    keep = np.array(sorted(keep)); out["matched_n"] = int(len(keep)); out["matched_pos_share"] = float(y[keep].mean())
    with Pool(5) as pool:
        res = pool.map(job, [(k, s) for k in KINDS for s in SEEDS])
    P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv")); M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv")); S = pd.read_csv(os.path.join(DATA, "cohort_subs.csv"))
    vec = {}
    for k in KINDS:
        r = sorted([x for x in res if x[0] == k], key=lambda z: z[1])
        full = [f1(y, (x[3] >= x[2]).astype(int)) for x in r]
        mf = [f1(y[keep], (x[3][keep] >= x[2]).astype(int)) for x in r]
        mauc = [roc_auc_score(y[keep], x[3][keep]) for x in r]; auc = [roc_auc_score(y, x[3]) for x in r]
        cv = cohort_vectors(np.mean([x[4] for x in r], 0), P, M, S)
        vec[k] = np.array([c[2] for c in cv]); vec["_clusters"] = np.array([c[0] for c in cv]); vec["_group"] = np.array([c[1] for c in cv])
        out[k] = dict(f1_full=float(np.mean(full)), auc_full=float(np.mean(auc)), f1_matched=float(np.mean(mf)), auc_matched=float(np.mean(mauc)),
                      cohort_prog=float(vec[k][[g.startswith("Progpedia") for g in vec["_group"]]].mean()), cohort_irplag=float(vec[k][[not g.startswith("Progpedia") for g in vec["_group"]]].mean()))
        print(TAG, "%-12s full F1 %.1f AUC %.3f | length-matched F1 %.1f AUC %.3f | cohorts %.3f/%.3f" % (
            k, 100 * out[k]["f1_full"], out[k]["auc_full"], 100 * out[k]["f1_matched"], out[k]["auc_matched"], out[k]["cohort_prog"], out[k]["cohort_irplag"]), flush=True)
    json.dump(out, open(os.path.join(gv.RES, "gate_shortcut.json"), "w"), indent=1)
    np.savez(os.path.join(gv.RES, "gate_cohort_vectors.npz"), **vec)
