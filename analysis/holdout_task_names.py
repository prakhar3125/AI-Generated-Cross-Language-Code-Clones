"""A2: effect of train/test task overlap. Names = the ALGO function names (build_convergence.py) that have problem groups in
both train/val and test (22 of 38). Every train and validation pair that contains a snippet with one of these names is
removed, the gate and the direct classifier are retrained (same lr/batch as the main run, 8 seeds, threshold re-tuned on
the filtered validation set) and scored on the unchanged test partition and on the 193 convergence pairs.
REGIME=A|B|C python -I holdout_task_names.py -> results_<R>/holdout_names.json"""
import json, os, pickle, sys
from multiprocessing import Pool
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE
import feature_pipeline as fp
from compute_pair_features import pair_features
from exp_lib import SC, SEEDS, TAG, X6, load, score, train_model, tune_threshold

RES = os.path.join(HERE, "results_" + TAG)
src = open(os.path.join(HERE, "build_convergence.py"), encoding="utf8").read()
ns = {"fp": fp}
exec(src[src.index("ALGO = "):src.index("\n", src.index("ALGO = "))], ns)
exec(src[src.index("def first_name"):src.index("by = collections")], ns)
ALGO, first_name = ns["ALGO"], ns["first_name"]

D = load()
tr, va, te = D["train"], D["val"], D["test"]
S = pickle.load(open(os.path.join(DATA, "snippets.pkl"), "rb"))
name_cache = {}
def nm(k):
    if k not in name_cache:
        lang, code = S[k]
        name_cache[k] = first_name(code, lang) if len(code.splitlines()) >= 4 else None
    return name_cache[k]

def keys(df): return set(df.key1) | set(df.key2)
tv_names = {nm(k) for k in keys(tr) | keys(va)} & ALGO
te_names = {nm(k) for k in keys(te)} & ALGO
HELD = tv_names & te_names
trh = tr[~(tr.key1.map(nm).isin(HELD) | tr.key2.map(nm).isin(HELD))].reset_index(drop=True)
vah = va[~(va.key1.map(nm).isin(HELD) | va.key2.map(nm).isin(HELD))].reset_index(drop=True)

summ = json.load(open(os.path.join(RES, "training_summary.json")))
LR, BS = summ["selected"]["lr"], summ["selected"]["batch"]
arr = lambda df, c: df[c].values.astype(np.float64)

cv = pd.read_csv(os.path.join(DATA, "convergence_pairs.csv"))
Fb = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
rows = [pair_features(Fb[r.key1], Fb[r.key2]) for r in cv.itertuples()]
cvf = pd.DataFrame(rows, columns=["S_CodeBERT", "S_AST", "S_Token"])
cvf["D_lang"] = 0.0; cvf["S_CodeBERT_minus_S_AST"] = (cvf.S_CodeBERT - cvf.S_AST).abs(); cvf["one_minus_S_AST"] = 1 - cvf.S_AST
cvf["cc1"] = [Fb[k]["cc"] for k in cv.key1]

def f1(y, p):
    tp = ((p == 1) & (y == 1)).sum()
    return float(2 * tp / max(2 * tp + ((p == 1) & (y == 0)).sum() + ((p == 0) & (y == 1)).sum(), 1))

def job(a):
    kind, filt, seed = a
    t, v = (trh, vah) if filt else (tr, va)
    routing = kind == "gate"
    m, _, _ = train_model(arr(t, X6), arr(t, SC), t.label.values, arr(v, X6), arr(v, SC), v.label.values, seed, routing, LR, BS)
    sv = score(m, arr(v, X6), arr(v, SC), routing)[0]
    thr = tune_threshold(sv, v.label.values)
    st = score(m, arr(te, X6), arr(te, SC), routing)[0]
    sc = score(m, arr(cvf, X6), arr(cvf, SC), routing)[0]
    p = (st >= thr).astype(int)
    return kind, filt, seed, f1(te.label.values, p), float(((sc >= thr)).mean()), float(p[te.label.values == 0].mean())

if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    print("held-out names (%d):" % len(HELD), sorted(HELD))
    print("train pairs %d -> %d, val pairs %d -> %d" % (len(tr), len(trh), len(va), len(vah)), flush=True)
    with Pool(8) as pool:
        res = pool.map(job, [(k, f, s) for k in ("gate", "direct") for f in (False, True) for s in SEEDS])
    out = {"held_names": sorted(HELD), "n_train": [len(tr), len(trh)], "n_val": [len(va), len(vah)]}
    for kind in ("gate", "direct"):
        for filt in (False, True):
            r = [x for x in res if x[0] == kind and x[1] == filt]
            key = "%s|%s" % (kind, "heldout" if filt else "full")
            out[key] = dict(f1=[float(np.mean([x[3] for x in r])), float(np.std([x[3] for x in r], ddof=1))],
                            convergence_flag_rate=float(np.mean([x[4] for x in r])), test_fpr=float(np.mean([x[5] for x in r])))
            print(TAG, key, out[key], flush=True)
    json.dump(out, open(os.path.join(RES, "holdout_names.json"), "w"), indent=1)
