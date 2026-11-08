"""Scale-consistent semantic expert on cohorts. S_sem^w = symmetric top-3 window cosine in an embedding space ZCA-whitened with
TRAINING-split statistics only (compute_whiten_feature.py): no per-program centring, so the score has the same scale for 1, 2 or 3+ windows.
Gate and direct classifier are trained on the benchmark with S_sem^w (SEM=wh, regime A), then scored on the PROGpedia / IR-Plag cohorts
(plain featurization; the whitening statistics are the benchmark's, nothing is fitted on cohort data).
REGIME=A SEM=wh python -I diag_wh_cohorts.py"""
import json, os, pickle, sys
from multiprocessing import Pool
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE
import compute_pair_features as cpf
from exp_lib import SC, SEEDS, X6, load, score, train_model

D = load(); tr, va = D["train"], D["val"]
summ = json.load(open(os.path.join(HERE, "results_Awh", "training_summary.json")))
LR, BS = summ["selected"]["lr"], summ["selected"]["batch"]
arr = lambda df, c: df[c].values.astype(np.float64)

B = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
tk = sorted(set(pf[pf.split == "train"].key1) | set(pf[pf.split == "train"].key2))
X = np.vstack([B[k]["win"] for k in tk]).astype(np.float64)
mu = X.mean(0); w_, V = np.linalg.eigh(np.cov((X - mu).T))
Wm = V @ np.diag(1.0 / np.sqrt(np.maximum(w_, 0) + 1e-3 * w_.mean())) @ V.T

def zw(win):
    Z = (win.astype(np.float64) - mu) @ Wm
    return Z / np.clip(np.linalg.norm(Z, axis=1, keepdims=True), 1e-9, None)

def sem_w(a, b):
    return cpf._topk(np.clip(zw(a["win"]) @ zw(b["win"]).T, -1, 1), 3)

P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv")); M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv"))
S = pd.read_csv(os.path.join(DATA, "cohort_subs.csv")); F = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
rows = []
for r in P.itertuples():
    a, b = F[r.key1], F[r.key2]
    s_ = sem_w(a, b); sa = cpf.ast_sim(a, b)
    rows.append((s_, sa, cpf.tok_sim(a, b), 0.0, abs(s_ - sa), 1 - sa, a["cc"], max(len(a["win"]), len(b["win"]))))
coh = pd.DataFrame(rows, columns=["S_CodeBERT", "S_AST", "S_Token", "D_lang", "S_CodeBERT_minus_S_AST", "one_minus_S_AST", "cc1", "w"])

hon = {g: set(G[G.role == "honest"].id) for g, G in S.groupby("group")}
idx = {}
for g, G in P.groupby("group"):
    h = hon[g]; hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
    for d in M[M.group == g].itertuples():
        dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
        nd = np.array([i for i in dm if i != d.derived_pair and not ((P.id1[i] == d.src) or (P.id2[i] == d.src))])
        idx[(g, d.derived)] = (int(P.index[P.pair_id == d.derived_pair][0]), np.concatenate([hh, nd]))
M["ds"] = np.where(M.group.str.startswith("Progpedia"), "PROGpedia", "IR-Plag")
def auc(sc, ds):
    v = []
    for d in M[M.ds == ds].itertuples():
        dp, nd = idx[(d.group, d.derived)]; x = sc[nd]; v.append((x < sc[dp]).mean() + .5 * (x == sc[dp]).mean())
    return float(np.mean(v))

def job(a):
    kind, seed = a
    routing = kind == "gate"
    m, _, _ = train_model(arr(tr, X6), arr(tr, SC), tr.label.values, arr(va, X6), arr(va, SC), va.label.values, seed, routing, LR, BS)
    s, w = score(m, arr(coh, X6), arr(coh, SC), routing)
    return kind, seed, s, (w.mean(0) if w is not None else None)

if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    cs = coh.S_CodeBERT.values; wmax = coh.w.values
    der = P.pair_id.isin(M.derived_pair).values
    q = lambda x: np.round(np.quantile(x, [.1, .5, .9]), 3).tolist()
    print("whitened S_sem on cohorts, p10/p50/p90:")
    for nm, m in (("both<=1", wmax == 1), ("max>=3", wmax >= 3)):
        print("  %-8s derived %s  non-derived %s" % (nm, q(cs[m & der]), q(cs[m & ~der])))
    with Pool(8) as p:
        res = p.map(job, [(k, s) for k in ("gate", "direct") for s in SEEDS])
    out = {}
    for kind in ("gate", "direct"):
        r = [x for x in res if x[0] == kind]
        per = [auc(x[2], "PROGpedia") for x in r]
        out[kind] = dict(prog_mean=round(float(np.mean(per)), 3), prog_per_seed=[round(v, 3) for v in per],
                         irplag_mean=round(float(np.mean([auc(x[2], "IR-Plag") for x in r])), 3),
                         weights=None if r[0][3] is None else [round(float(v), 3) for v in np.mean([x[3] for x in r], 0)])
        print(kind, out[kind], flush=True)
    for nm, c in (("S_sem^w alone", "S_CodeBERT"), ("S_AST alone", "S_AST"), ("S_Token alone", "S_Token")):
        v = coh[c].values
        out[nm] = dict(prog=round(auc(v, "PROGpedia"), 3), irplag=round(auc(v, "IR-Plag"), 3)); print(nm, out[nm])
    json.dump(out, open(os.path.join(HERE, "results_Awh", "diag_wh_cohorts.json"), "w"), indent=1)
