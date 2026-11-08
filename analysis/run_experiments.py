# -*- coding: utf-8 -*-
"""Train every learned system on the problem-grouped train split and score val / test / aux.

Systems saved (scores in [0,1], one row per seed, columns = pairs of the split):
  gate            trained routing gate, 6-d input (the proposed model)
  gate_x4         routing gate retrained on the 4-d input (ablation: without X5, X6)
  direct          equal-capacity direct classifier (no routing)
  logreg          logistic regression on the 6 features
  static          equal weights over the three experts      (deterministic)
  codebert/ast/token  single experts                         (deterministic)
  random          random Dirichlet weights per pair          (seeded)
  gate_wo_sem / gate_wo_str / gate_wo_syn   leave-one-out: trained gate with the
                  expert's logit set to -inf BEFORE the softmax (weights renormalise)

Hyper-parameters (learning rate, batch size) are selected by a real grid search
over {1e-2, 1e-3, 1e-4} x {16, 32, 64} on mean validation loss over seeds 0-2.

python -I run_experiments.py
"""
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np
from sklearn.linear_model import LogisticRegression

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE  # noqa: E402
from exp_lib import SC, SEEDS, X4, X6, load, score, train_model  # noqa: E402

from exp_lib import TAG  # noqa: E402
RES = os.path.join(HERE, "results_" + TAG)
os.makedirs(RES, exist_ok=True)
D = load()
tr, va, te, ax = D["train"], D["val"], D["test"], D["aux"]


def arrays(df, cols):
    return df[cols].values.astype(np.float64)


def job_grid(a):
    lr, bs, seed = a
    m, vl, ep = train_model(arrays(tr, X6), arrays(tr, SC), tr.label.values,
                            arrays(va, X6), arrays(va, SC), va.label.values,
                            seed, True, lr, bs)
    return (lr, bs, seed, vl, ep)


def job_model(a):
    kind, seed, lr, bs = a
    routing = kind != "direct"
    cols = X4 if kind == "gate_x4" else X6
    m, vl, ep = train_model(arrays(tr, cols), arrays(tr, SC), tr.label.values,
                            arrays(va, cols), arrays(va, SC), va.label.values,
                            seed, routing, lr, bs, nin=len(cols))
    out = {"kind": kind, "seed": seed, "val_loss": vl, "epochs": ep}
    for nm, df in (("val", va), ("test", te), ("aux", ax), ("train", tr)):
        s, w = score(m, arrays(df, cols), arrays(df, SC), routing)
        out[nm] = s
        if w is not None and nm in ("test", "val", "aux"):
            out[nm + "_w"] = w
        if kind == "gate":
            for tag, keep in (("gate_wo_sem", [1, 2]), ("gate_wo_str", [0, 2]), ("gate_wo_syn", [0, 1])):
                out[tag + "_" + nm], _ = score(m, arrays(df, cols), arrays(df, SC), True, keep)
    return out


if __name__ == "__main__":
    t0 = time.time()
    torch_threads = 1
    import torch
    torch.set_num_threads(1)
    with Pool(10) as pool:
        grid = [(lr, bs, s) for lr in (1e-2, 1e-3, 1e-4) for bs in (16, 32, 64) for s in (0, 1, 2)]
        gres = pool.map(job_grid, grid)
        agg = {}
        for lr, bs, s, vl, ep in gres:
            agg.setdefault((lr, bs), []).append(vl)
        table = {"%g|%d" % k: float(np.mean(v)) for k, v in agg.items()}
        (lr_best, bs_best) = min(agg, key=lambda k: np.mean(agg[k]))
        print("grid (mean val BCE):", json.dumps(table, indent=1))
        print("selected lr=%g batch=%d  (%.0fs)" % (lr_best, bs_best, time.time() - t0), flush=True)
        jobs = [(k, s, lr_best, bs_best) for k in ("gate", "gate_x4", "direct") for s in SEEDS]
        mres = pool.map(job_model, jobs)
    print("trained %d models (%.0fs)" % (len(mres), time.time() - t0), flush=True)

    out = {}
    epochs = {}
    for r in mres:
        epochs.setdefault(r["kind"], []).append(r["epochs"])
    for split in ("val", "test", "aux", "train"):
        d = {}
        for kind in ("gate", "gate_x4", "direct"):
            d[kind] = np.vstack([next(r for r in mres if r["kind"] == kind and r["seed"] == s)[split]
                                 for s in SEEDS])
        for tag in ("gate_wo_sem", "gate_wo_str", "gate_wo_syn"):
            d[tag] = np.vstack([next(r for r in mres if r["kind"] == "gate" and r["seed"] == s)[tag + "_" + split]
                                for s in SEEDS])
        df = {"val": va, "test": te, "aux": ax, "train": tr}[split]
        S = arrays(df, SC)
        d["static"] = np.tile(S.mean(1), (len(SEEDS), 1))
        d["codebert"] = np.tile(S[:, 0], (len(SEEDS), 1))
        d["ast"] = np.tile(S[:, 1], (len(SEEDS), 1))
        d["token"] = np.tile(S[:, 2], (len(SEEDS), 1))
        d["random"] = np.vstack([(np.random.RandomState(s + 1000 * (split == "test") + 7).dirichlet(np.ones(3), len(df)) * S).sum(1)
                                 for s in SEEDS])
        lr_models = [LogisticRegression(max_iter=3000).fit(arrays(tr, X6), tr.label.values) for _ in (0,)]
        d["logreg"] = np.tile(lr_models[0].predict_proba(arrays(df, X6))[:, 1], (len(SEEDS), 1))
        for k, v in d.items():
            out["%s__%s" % (split, k)] = v
    # mean gate weights by split for the routing figure / table
    for split in ("test", "val", "aux"):
        out["%s__gate_w" % split] = np.stack([next(r for r in mres if r["kind"] == "gate" and r["seed"] == s)[split + "_w"]
                                              for s in SEEDS])
    np.savez_compressed(os.path.join(RES, "scores.npz"), **out)
    with open(os.path.join(RES, "training_summary.json"), "w") as f:
        json.dump({"grid_mean_val_bce": table, "selected": {"lr": lr_best, "batch": bs_best},
                   "epochs_run": {k: [int(x) for x in v] for k, v in epochs.items()},
                   "n_train": len(tr), "n_val": len(va), "n_test": len(te), "n_aux": len(ax),
                   "seeds": SEEDS}, f, indent=2)
    print("saved scores.npz (%.0fs)" % (time.time() - t0))
