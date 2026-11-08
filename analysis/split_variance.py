# -*- coding: utf-8 -*-
"""Sensitivity to the train/validation group assignment.

The test partition is fixed by construction (every eligible exact / renamed pair, the
held-out cross-language problems), so only the assignment of the remaining groups to
training vs validation can be re-drawn.  For each of 5 re-draws (draw 0 is the original),
groups of the train+validation pool are re-assigned to train / validation (18% validation);
a pair is kept only if all its groups fall in the same side (cross-side negatives are dropped).
Gate and direct classifier are retrained (3 seeds each, hyper-parameters as selected) and
evaluated on the fixed test partition with the validation-tuned threshold.

REGIME=A|B|C python -I split_variance.py
"""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE  # noqa: E402
from exp_lib import REGIME, SC, TAG, X6, load, metrics, score, train_model, tune_threshold  # noqa: E402

RES = os.path.join(HERE, "results_" + TAG)
D = load()
tr0, va0, te = D["train"], D["val"], D["test"]
pool = pd.concat([tr0, va0], ignore_index=True)
summ = json.load(open(os.path.join(RES, "training_summary.json")))
LR, BS = summ["selected"]["lr"], summ["selected"]["batch"]
arr = lambda df, c: df[c].values.astype(np.float64)


import pickle  # noqa: E402
from compute_pair_features import pair_features  # noqa: E402
from common import DATA  # noqa: E402

F = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))


def feat_row(k1, k2, l1, l2, g1, g2, label, sl):
    s_c, s_a, s_t = pair_features(F[k1], F[k2])
    return dict(label=label, slice=sl, lang1=l1, lang2=l2, key1=k1, key2=k2, group1=g1, group2=g2,
                S_CodeBERT=s_c, S_AST=s_a, S_Token=s_t, D_lang=float(l1 != l2), S_CodeBERT_minus_S_AST=abs(s_c - s_a),
                one_minus_S_AST=1.0 - s_a, cc1=F[k1]["cc"])


def regen_negatives(pos, rng):
    """Independent negatives inside one side (regime A), or nearest-neighbour ones (regime B)."""
    pool = {}
    grp = {}
    for r in pos.itertuples():
        pool.setdefault(r.lang1, {})[r.key1] = r.group1
        pool.setdefault(r.lang2, {})[r.key2] = r.group2
    pool = {l: sorted(d.items()) for l, d in pool.items()}
    cross = pos[pos.lang1 != pos.lang2]
    n = len(pos)
    n_cross = int(round(n * len(cross) / max(len(pos), 1)))
    cc = list(zip(cross.lang1, cross.lang2))
    sl = list(pos[pos.lang1 == pos.lang2].lang1)
    if REGIME == "B":
        emb = {l: np.vstack([F[k]["win"][0] for k, _ in v]).astype(np.float32) for l, v in pool.items()}
        for l in emb:
            emb[l] /= np.clip(np.linalg.norm(emb[l], axis=1, keepdims=True), 1e-9, None)
    rows, used = [], set()
    tries = 0
    while len(rows) < n and tries < n * 100:
        tries += 1
        cross_now = len(rows) < n_cross
        if cross_now:
            l1, l2 = cc[rng.randint(len(cc))]
        else:
            l1 = l2 = sl[rng.randint(len(sl))]
        k1, g1 = pool[l1][rng.randint(len(pool[l1]))]
        if REGIME == "B":
            q = emb[l1][[k for k, _ in pool[l1]].index(k1)] if False else F[k1]["win"][0].astype(np.float32)
            q = q / max(np.linalg.norm(q), 1e-9)
            sims = emb[l2] @ q
            order = np.argsort(-sims)[:40]
            cands = [pool[l2][i] for i in order if pool[l2][i][1] != g1 and pool[l2][i][0] != k1 and frozenset((k1, pool[l2][i][0])) not in used]
            if not cands:
                continue
            sc = sorted(((np.mean(pair_features(F[k1], F[k])), k, g) for k, g in cands), key=lambda t: -t[0])
            _, k2, g2 = sc[rng.randint(min(3, len(sc)))]
        else:
            k2, g2 = pool[l2][rng.randint(len(pool[l2]))]
            if g2 == g1 or k2 == k1 or frozenset((k1, k2)) in used:
                continue
        used.add(frozenset((k1, k2)))
        rows.append(feat_row(k1, k2, l1, l2, g1, g2, 0, "neg"))
    return pd.DataFrame(rows)


def draw(seed):
    if seed == 0:
        return tr0, va0
    rng = np.random.RandomState(1000 + seed)
    pos = pool[pool.label == 1].reset_index(drop=True)
    groups = sorted(set(pos.group1) | set(pos.group2))
    val = set(g for g in groups if rng.rand() < 0.18)
    in_val = pos.group1.isin(val) & pos.group2.isin(val)
    in_tr = ~pos.group1.isin(val) & ~pos.group2.isin(val)
    out = []
    for side in (pos[in_tr].reset_index(drop=True), pos[in_val].reset_index(drop=True)):
        neg = regen_negatives(side, rng)
        keep = ["label", "slice", "lang1", "lang2", "key1", "key2", "group1", "group2", "S_CodeBERT", "S_AST", "S_Token",
                "D_lang", "S_CodeBERT_minus_S_AST", "one_minus_S_AST", "cc1"]
        out.append(pd.concat([side[keep], neg[keep]], ignore_index=True))
    return out[0], out[1]


def job(a):
    dseed, kind, tseed, tr, va = a
    routing = kind == "gate"
    m, _, _ = train_model(arr(tr, X6), arr(tr, SC), tr.label.values, arr(va, X6), arr(va, SC), va.label.values,
                          tseed, routing, LR, BS)
    sv = score(m, arr(va, X6), arr(va, SC), routing)[0]
    st = score(m, arr(te, X6), arr(te, SC), routing)[0]
    p = (st >= tune_threshold(sv, va.label.values)).astype(int)
    mm = metrics(te.label.values, p)
    xl = (te.slice == "cross-language").values
    return dict(draw=dseed, kind=kind, tseed=tseed, f1=mm["f1"], fpr=mm["fpr"], recall=mm["recall"],
                xl_recall=float(p[xl].mean()), n_train=len(tr), n_val=len(va))


if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    draws = {d: draw(d) for d in range(5)}
    jobs = [(d, k, s, draws[d][0], draws[d][1]) for d in range(5) for k in ("gate", "direct") for s in range(3)]
    with Pool(8) as pool_:
        res = pool_.map(job, jobs)
    df = pd.DataFrame(res)
    out = {"regime": REGIME, "per_draw": {}}
    for d in range(5):
        g = df[(df.draw == d) & (df.kind == "gate")]
        di = df[(df.draw == d) & (df.kind == "direct")]
        out["per_draw"][d] = dict(gate_f1=float(g.f1.mean() * 100), direct_f1=float(di.f1.mean() * 100),
                                  delta_direct_minus_gate=float((di.f1.mean() - g.f1.mean()) * 100),
                                  gate_xl_recall=float(g.xl_recall.mean() * 100), gate_fpr=float(g.fpr.mean() * 100),
                                  n_train=int(g.n_train.iloc[0]), n_val=int(g.n_val.iloc[0]))
    vals = out["per_draw"]
    for k in ("gate_f1", "delta_direct_minus_gate", "gate_xl_recall", "gate_fpr"):
        v = np.array([vals[d][k] for d in range(5)])
        out[k + "_over_draws"] = dict(mean=float(v.mean()), sd=float(v.std(ddof=1)), min=float(v.min()), max=float(v.max()))
    json.dump(out, open(os.path.join(RES, "split_variance.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "per_draw"}, indent=1))
    print({d: {k: round(x, 2) for k, x in v.items()} for d, v in vals.items()})
