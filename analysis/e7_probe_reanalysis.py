# -*- coding: utf-8 -*-
"""E7: generator-probe re-analysis that does not depend on a single operating point.

Per generator and kind (translate / refactor): AUROC of derived vs independent pairs, recall at 1% and 5% FPR (thresholds taken from the probe's own negatives),
recall and FPR at the frozen validation threshold, with 95% cluster-bootstrap intervals that resample SEED PROBLEMS (the 'row' of a pair; positives and negatives
that share a seed problem stay together), and the paired AUROC difference between the benchmark's own translations and each current generator.
Systems: gate, direct classifier, token expert, first expert alone (CodeBERT cosine, or UniXcoder cosine with SEM=ux).

REGIME=A|B [SEM=ux] python -I e7_probe_reanalysis.py -> results_<TAG>/e7_probe.json
"""
import json
import os
import pickle
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE  # noqa: E402
from compute_pair_features import pair_features  # noqa: E402
from exp_lib import SC, SEEDS, SEM, TAG, X6, load, score, train_model, tune_threshold  # noqa: E402

RES = os.path.join(HERE, "results_" + TAG)
D = load()
tr, va = D["train"], D["val"]
summ = json.load(open(os.path.join(RES, "training_summary.json")))
LR, BS = summ["selected"]["lr"], summ["selected"]["batch"]
pp = pd.read_csv(os.path.join(DATA, "probe2_pairs.csv"))
F = pickle.load(open(os.path.join(DATA, "probe2_feats.pkl"), "rb"))
pp[["S_CodeBERT", "S_AST", "S_Token"]] = np.array([pair_features(F[r.key1], F[r.key2]) for r in pp.itertuples()])
if SEM == "ux":
    U = np.load(os.path.join(DATA, "unixcoder_emb_probe2.npz"))
    e = U["emb"] / np.clip(np.linalg.norm(U["emb"], axis=1, keepdims=True), 1e-9, None)
    ix = {k: i for i, k in enumerate(U["keys"])}
    pp["S_CodeBERT"] = np.clip([float(e[ix[a]] @ e[ix[b]]) for a, b in zip(pp.key1, pp.key2)], 0.0, 1.0)
pp["S_CodeBERT_minus_S_AST"] = (pp.S_CodeBERT - pp.S_AST).abs()
pp["one_minus_S_AST"] = 1 - pp.S_AST
arr = lambda df, c: df[c].values.astype(np.float64)


def job(a):
    kind, seed = a
    routing = kind == "gate"
    m, _, _ = train_model(arr(tr, X6), arr(tr, SC), tr.label.values, arr(va, X6), arr(va, SC), va.label.values, seed, routing, LR, BS)
    return kind, seed, score(m, arr(va, X6), arr(va, SC), routing)[0], score(m, arr(pp, X6), arr(pp, SC), routing)[0]


def rec_at(y, s, fpr):
    f, t, _ = roc_curve(y, s)
    return float(t[np.searchsorted(f, fpr, side="right") - 1])


def stats(y, s):
    return roc_auc_score(y, s), rec_at(y, s, 0.01), rec_at(y, s, 0.05)


if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    with Pool(8) as p:
        res = p.map(job, [(k, s) for k in ("gate", "direct") for s in SEEDS])
    yv = va.label.values
    sysv, syst = {}, {}
    for kind in ("gate", "direct"):
        rs = sorted([r for r in res if r[0] == kind], key=lambda r: r[1])
        sysv[kind] = np.vstack([r[2] for r in rs])
        syst[kind] = np.vstack([r[3] for r in rs])
    S, Sv = arr(pp, SC), arr(va, SC)
    for nm, i in (("first_expert", 0), ("token", 2)):
        sysv[nm] = np.tile(Sv[:, i], (8, 1))
        syst[nm] = np.tile(S[:, i], (8, 1))
    y = pp.label.values
    rows = np.where(pp.row.values >= 0, pp.row.values, 100000 + pd.factorize(pp.key1)[0])   # refactor pairs carry no problem id: cluster by the seed snippet
    gens = list(dict.fromkeys(pp.gen))
    rng = np.random.default_rng(0)
    out = {}
    uniq = np.unique(rows)
    boots = [rng.choice(uniq, len(uniq)) for _ in range(1000)]
    byrow = {r_: np.where(rows == r_)[0] for r_ in uniq}
    for nm in sysv:
        ens = syst[nm].mean(0)
        thr = [tune_threshold(sysv[nm][s], yv) for s in range(8)]
        for gen in gens:
            for kind in ("translate", "refactor"):
                m = ((pp.gen == gen) & (pp.kind == kind)).values
                if m.sum() == 0:
                    continue
                idx = np.where(m)[0]
                au, r1, r5 = stats(y[idx], ens[idx])
                rec = float(np.mean([(syst[nm][s][idx][y[idx] == 1] >= thr[s]).mean() for s in range(8)]))
                fpr = float(np.mean([(syst[nm][s][idx][y[idx] == 0] >= thr[s]).mean() for s in range(8)]))
                bs = []
                for b in boots:
                    ii = np.concatenate([byrow[r_][m[byrow[r_]]] for r_ in b])
                    if len(np.unique(y[ii])) == 2:
                        bs.append(stats(y[ii], ens[ii]))
                bs = np.array(bs)
                out["%s|%s|%s" % (nm, gen, kind)] = dict(auc=au, r1=r1, r5=r5, recall_frozen=rec, fpr_frozen=fpr, n=int(m.sum()),
                                                         auc_ci=[float(np.percentile(bs[:, 0], 2.5)), float(np.percentile(bs[:, 0], 97.5))],
                                                         r5_ci=[float(np.percentile(bs[:, 2], 2.5)), float(np.percentile(bs[:, 2], 97.5))])
        # paired AUROC difference benchmark translations - each current generator (resampling seed problems jointly)
        base = ((pp.gen == "gpt3") & (pp.kind == "translate")).values
        for gen in gens:
            if gen == "gpt3":
                continue
            m = ((pp.gen == gen) & (pp.kind == "translate")).values
            d = []
            for b in boots:
                ib = np.concatenate([byrow[r_][base[byrow[r_]]] for r_ in b])
                im = np.concatenate([byrow[r_][m[byrow[r_]]] for r_ in b])
                if len(np.unique(y[ib])) == 2 and len(np.unique(y[im])) == 2:
                    d.append(roc_auc_score(y[ib], ens[ib]) - roc_auc_score(y[im], ens[im]))
            d = np.array(d)
            out["%s|diff|%s" % (nm, gen)] = dict(delta=float(roc_auc_score(y[base], ens[base]) - roc_auc_score(y[m], ens[m])), ci=[float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))])
    json.dump(out, open(os.path.join(RES, "e7_probe.json"), "w"), indent=1)
    for nm in ("gate", "token", "first_expert"):
        print(TAG, nm, {k.split("|", 1)[1]: (round(v["auc"], 3), round(v["r5"], 3)) for k, v in out.items() if k.startswith(nm + "|") and "diff" not in k})
