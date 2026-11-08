# -*- coding: utf-8 -*-
"""E2: ablation by RETRAINING without an expert (its score and every feature derived from it removed from the input), gate and direct classifier.

  wo_sem : inputs [S_AST, S_Token, D_lang, 1-S_AST]            experts (AST, Token)       (X5 = |S_sem - S_AST| removed)
  wo_str : inputs [S_sem, S_Token, D_lang]                      experts (sem, Token)       (X5, X6 removed)
  wo_syn : inputs [S_sem, S_AST, D_lang, X5, X6]                experts (sem, AST)

Same protocol as the main run (AdamW, BCE on the fused score, early stopping on validation loss, hyper-parameters of the regime's grid selection, 8 seeds,
validation-tuned threshold).  The old masked-logit rows stay in Table ablation as 'output masking'.

REGIME=A|B|C [SEM=ux] python -I e2_retrained_ablation.py -> results_<TAG>/e2_retrained.json
"""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE  # noqa: E402
import exp_lib  # noqa: E402
from exp_lib import FUSION, SC, SEEDS, TAG, X6, load, metrics, trunk, tune_threshold  # noqa: E402
from stats_tools import boot_p, cluster_bootstrap, cluster_counts, holm  # noqa: E402

RES = os.path.join(HERE, "results_" + TAG)
D = load()
tr, va, te = D["train"], D["val"], D["test"]
summ = json.load(open(os.path.join(RES, "training_summary.json")))
LR, BS = summ["selected"]["lr"], summ["selected"]["batch"]
VARIANTS = {
    "wo_sem": (["S_AST", "S_Token", "D_lang", "one_minus_S_AST"], ["S_AST", "S_Token"]),
    "wo_str": (["S_CodeBERT", "S_Token", "D_lang"], ["S_CodeBERT", "S_Token"]),
    "wo_syn": (["S_CodeBERT", "S_AST", "D_lang", "S_CodeBERT_minus_S_AST", "one_minus_S_AST"], ["S_CodeBERT", "S_AST"]),
}
arr = lambda df, c: df[c].values.astype(np.float32)


def train(seed, routing, xin, sc):
    torch.manual_seed(seed)
    np.random.seed(seed)
    nexp = len(sc)
    m = trunk(len(xin), nexp if routing else 1)
    opt = torch.optim.AdamW(m.parameters(), lr=LR, weight_decay=1e-5)
    lf = nn.BCELoss()
    Xt, St = torch.tensor(arr(tr, xin)), torch.tensor(arr(tr, sc))
    yt = torch.tensor(tr.label.values, dtype=torch.float32).unsqueeze(1)
    Xv, Sv = torch.tensor(arr(va, xin)), torch.tensor(arr(va, sc))
    yv = torch.tensor(va.label.values, dtype=torch.float32).unsqueeze(1)

    def fwd(x, s):
        z = m(x)
        if not routing:
            return torch.sigmoid(z)
        w = torch.softmax(z, -1)
        return exp_lib._logit_fuse(m, w, s) if FUSION == "logit" else (w * s).sum(1, keepdim=True)
    best, bad, state = 1e9, 0, None
    g = torch.Generator().manual_seed(seed)
    for ep in range(100):
        m.train()
        perm = torch.randperm(len(Xt), generator=g)
        for b in range(0, len(perm), BS):
            j = perm[b:b + BS]
            loss = lf(fwd(Xt[j], St[j]).clamp(1e-6, 1 - 1e-6), yt[j])
            opt.zero_grad()
            loss.backward()
            opt.step()
        m.eval()
        with torch.no_grad():
            vl = lf(fwd(Xv, Sv).clamp(1e-6, 1 - 1e-6), yv).item()
        if vl < best - 1e-5:
            best, bad, state = vl, 0, {k: v.clone() for k, v in m.state_dict().items()}
        else:
            bad += 1
            if bad >= 10:
                break
    m.load_state_dict(state)
    m.eval()
    with torch.no_grad():
        sv = fwd(Xv, Sv).numpy().ravel()
        st = fwd(torch.tensor(arr(te, xin)), torch.tensor(arr(te, sc))).numpy().ravel()
    return sv, st


def job(a):
    var, kind, seed = a
    xin, sc = VARIANTS[var]
    sv, st = train(seed, kind == "gate", xin, sc)
    return var, kind, seed, sv, st


if __name__ == "__main__":
    torch.set_num_threads(1)
    with Pool(8) as p:
        res = p.map(job, [(v, k, s) for v in VARIANTS for k in ("gate", "direct") for s in SEEDS])
    yv, yt = va.label.values, te.label.values
    cl = te.group1.values
    ref = np.load(os.path.join(RES, "preds.npz"))
    out = {}
    SL = ["exact", "renamed", "refactored", "cross-language"]
    cnt_ref = {k: np.stack([cluster_counts(yt, p.astype(int), cl) for p in ref[k + "|val"]]) for k in ("gate", "direct")}
    rows = []
    for var in VARIANTS:
        for kind in ("gate", "direct"):
            rs = sorted([r for r in res if r[0] == var and r[1] == kind], key=lambda r: r[2])
            P = np.array([r[4] >= tune_threshold(r[3], yv) for r in rs])
            ms = [metrics(yt, p.astype(int)) for p in P]
            e = {k: [float(np.mean([m[k] for m in ms])), float(np.std([m[k] for m in ms], ddof=1))] for k in ("f1", "recall", "specificity", "fpr")}
            e["slices"] = {s: float(np.mean([p[(te.slice == s).values].mean() for p in P])) for s in SL}
            cnt = np.stack([cluster_counts(yt, p.astype(int), cl) for p in P])
            bs = cluster_bootstrap({"ref": cnt_ref[kind], "cfg": cnt}, cnt.shape[1], B=5000, seed=5)
            d = (bs["cfg"] - bs["ref"]) * 100
            e["delta_f1_vs_full"] = float(d.mean())
            e["ci"] = [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))]
            e["p_boot"] = boot_p(d)
            out["%s|%s" % (kind, var)] = e
            rows.append("%s|%s" % (kind, var))
    adj = holm([out[k]["p_boot"] for k in rows])
    for k, a in zip(rows, adj):
        out[k]["p_holm"] = float(a)
    # reference rows of the full model (same seeds, from the main run)
    for kind in ("gate", "direct"):
        ms = [metrics(yt, p.astype(int)) for p in ref[kind + "|val"]]
        out[kind + "|full"] = {"f1": [float(np.mean([m["f1"] for m in ms])), float(np.std([m["f1"] for m in ms], ddof=1))],
                               "slices": {s: float(np.mean([p[(te.slice == s).values].mean() for p in ref[kind + "|val"]])) for s in SL}}
    json.dump(out, open(os.path.join(RES, "e2_retrained.json"), "w"), indent=1)
    for k, v in out.items():
        print(TAG, k.ljust(16), "F1 %.1f" % (100 * v["f1"][0]), ("d %+.1f [%+.1f,%+.1f] pH %.3f" % (v["delta_f1_vs_full"], v["ci"][0], v["ci"][1], v["p_holm"]) if "ci" in v else ""),
              {s: round(100 * x, 1) for s, x in v["slices"].items()})
