"""Headline analyses of the paper rerun for the LOG-ODDS gate (and its mean-fusion twin, for the paired comparison), same seeds,
lr/batch of the regime, validation-tuned thresholds. Produces
  - overall metrics at the validation-tuned threshold (acc/precision/recall/specificity/F1/FPR) and recall by slice,
  - operating points chosen on validation (FPR budgets 1/5/10%, recall targets 80/90%) and applied to test,
  - the zero-shot generator probe (probe2): recall / FPR per generator and kind at the frozen threshold,
  - gate weights by slice (inspectability).
REGIME=A|B|C python -I logit_headline.py -> results_<R>/logit_headline.json"""
import json, os, pickle, sys
from multiprocessing import Pool
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate_variants as gv
from common import DATA
from compute_pair_features import pair_features
from exp_lib import SC, SEEDS, TAG, X6, metrics, tune_threshold, wilson

KINDS = ["base", "logit"]
tr, va, te = gv.tr, gv.va, gv.te
pp = pickle.load(open(os.path.join(DATA, "_logit_probe_cache.pkl"), "rb")) if os.path.exists(os.path.join(DATA, "_logit_probe_cache.pkl")) else None

def probe_table():
    P = pd.read_csv(os.path.join(DATA, "probe2_pairs.csv")); F = pickle.load(open(os.path.join(DATA, "probe2_feats.pkl"), "rb"))
    P[["S_CodeBERT", "S_AST", "S_Token"]] = np.array([pair_features(F[r.key1], F[r.key2]) for r in P.itertuples()])
    P["S_CodeBERT_minus_S_AST"] = (P.S_CodeBERT - P.S_AST).abs(); P["one_minus_S_AST"] = 1 - P.S_AST
    P["D_lang"] = P.D_lang.astype(float)
    P["cc1"] = [F[k]["cc"] for k in P.key1]; P["cc2"] = [F[k]["cc"] for k in P.key2]
    P["ntok1"] = [F[k]["ntok"] for k in P.key1]; P["ntok2"] = [F[k]["ntok"] for k in P.key2]
    return P

def job(a):
    kind, seed = a
    global pp
    if pp is None:
        pp = probe_table() if TAG in ("A", "B") else None
    m = gv.train(kind, gv.design(tr, kind, gv.EX), tr[SC].values, tr.label.values, gv.design(va, kind, gv.EX), va[SC].values, va.label.values, seed, gv.LR, gv.BS)
    sv, _ = gv.predict(m, gv.design(va, kind, gv.EX), va[SC].values)
    st, wt = gv.predict(m, gv.design(te, kind, gv.EX), te[SC].values)
    sp = None
    if pp is not None:
        sp, _ = gv.predict(m, gv.design(pp, kind, gv.EX), pp[SC].values)
    return kind, seed, sv, st, wt, sp

if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    pp = probe_table() if TAG in ("A", "B") else None
    with Pool(5) as pool:
        res = pool.map(job, [(k, s) for k in KINDS for s in SEEDS])
    yv, yt = va.label.values, te.label.values; out = {}
    for k in KINDS:
        r = sorted([x for x in res if x[0] == k], key=lambda z: z[1])
        ms = []
        for x in r:
            thr = tune_threshold(x[2], yv); ms.append(metrics(yt, (x[3] >= thr).astype(int)))
        agg = {key: [float(np.mean([m[key] for m in ms])), float(np.std([m[key] for m in ms], ddof=1))] for key in ("acc", "precision", "recall", "specificity", "f1", "fpr")}
        slices = {}
        for sl in ("exact", "renamed", "refactored", "cross-language"):
            msk = (te.slice == sl).values
            slices[sl] = float(np.mean([(x[3][msk] >= tune_threshold(x[2], yv)).mean() for x in r]))
        ens_t, ens_v = np.mean([x[3] for x in r], 0), np.mean([x[2] for x in r], 0)
        ops = []
        for budget in (0.01, 0.05, 0.10):
            negs = np.sort(ens_v[yv == 0])[::-1]; i = int(np.floor(budget * len(negs)))
            thr = negs[i] + 1e-9 if i < len(negs) else 1.0
            mm = metrics(yt, (ens_t >= thr).astype(int)); ops.append(dict(kind="fpr_budget_val", budget=budget, threshold=float(thr), recall=mm["recall"], precision=mm["precision"], fpr=mm["fpr"], f1=mm["f1"]))
        for rt in (0.80, 0.90):
            pos = np.sort(ens_v[yv == 1]); thr = pos[int(np.floor((1 - rt) * len(pos)))]
            mm = metrics(yt, (ens_t >= thr).astype(int)); ops.append(dict(kind="recall_target_val", budget=rt, threshold=float(thr), recall=mm["recall"], precision=mm["precision"], fpr=mm["fpr"], f1=mm["f1"]))
        W = np.mean([x[4] for x in r], 0)
        wsl = {sl: [float(v) for v in W[(te.slice == sl).values].mean(0)] for sl in te.slice.unique()}
        probe = None
        if pp is not None:
            probe = {}
            y = pp.label.values
            for gen in dict.fromkeys(pp.gen):
                for kind in ("translate", "refactor"):
                    msk = ((pp.gen == gen) & (pp.kind == kind)).values
                    if msk.sum() == 0: continue
                    rec, fpr = [], []
                    for x in r:
                        thr = tune_threshold(x[2], yv); p_ = x[5][msk] >= thr
                        rec.append(p_[y[msk] == 1].mean()); fpr.append(p_[y[msk] == 0].mean())
                    npos = int((y[msk] == 1).sum())
                    probe["%s|%s" % (gen, kind)] = dict(recall=[float(np.mean(rec)), float(np.std(rec, ddof=1))], fpr=[float(np.mean(fpr)), float(np.std(fpr, ddof=1))], n_pos=npos, n_neg=int((y[msk] == 0).sum()))
        out[k] = dict(overall=agg, recall_by_slice=slices, operating_points=ops, weights_by_slice=wsl, probe=probe)
        print(TAG, k, "F1 %.1f acc %.1f spec %.1f recall %.1f" % (100 * agg["f1"][0], 100 * agg["acc"][0], 100 * agg["specificity"][0], 100 * agg["recall"][0]),
              "| slices", {a: round(100 * b, 1) for a, b in slices.items()}, flush=True)
        for o in ops: print("    ", o["kind"], o["budget"], "recall %.3f fpr %.3f prec %.3f" % (o["recall"], o["fpr"], o["precision"]))
        if probe: print("    probe", {a: (round(b["recall"][0], 3), round(b["fpr"][0], 3)) for a, b in list(probe.items())[:6]})
    json.dump(out, open(os.path.join(gv.RES, "logit_headline.json"), "w"), indent=1)
