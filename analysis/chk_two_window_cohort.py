"""Eq. 2 two-window degeneracy: recompute the CodeBERT-cosine cohort rows with window-centring applied
only to programs with >=3 windows (2-window programs are left uncentred), and bound the benchmark impact.
python -I chk_two_window_cohort.py"""
import os, pickle, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA
import compute_pair_features as cpf

def norm_fixed(X, min_w=3):
    X = X.astype(np.float32, copy=False)
    if X.shape[0] >= min_w:
        X = X - X.mean(axis=0, keepdims=True)
    return X / np.clip(np.linalg.norm(X, axis=1, keepdims=True), 1e-12, None)

def sem_fixed(a, b):
    A, B = norm_fixed(a["win"]), norm_fixed(b["win"])
    return cpf._topk(np.clip(A @ B.T, -1, 1), 3)

P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv"))
M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv"))
S = pd.read_csv(os.path.join(DATA, "cohort_subs.csv"))
F = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
nwin = {k: len(v["win"]) for k, v in F.items()}
two = {k for k, n in nwin.items() if n == 2}
print("cohort files:", len(F), "2-window:", len(two))

honest = {g: G[G.role == "honest"].key.tolist() for g, G in S.groupby("group")}
mwin = {g: np.mean([F[k]["win"].mean(0) for k in ks], axis=0) for g, ks in honest.items()}

def scores(variant, fn):
    out = []
    for r in P.itertuples():
        a, b = F[r.key1], F[r.key2]
        if variant == "filt":
            a = dict(a, win=a["win"] - mwin[r.group]); b = dict(b, win=b["win"] - mwin[r.group])
        out.append(fn(a, b))
    return np.array(out)

# index sets exactly as analyze_cohorts.py
honest_id = {g: set(G[G.role == "honest"].id) for g, G in S.groupby("group")}
idx = {}
for g, G in P.groupby("group"):
    h = honest_id[g]
    hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
    for d in M[M.group == g].itertuples():
        dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
        nd = np.array([i for i in dm if i != d.derived_pair and not ((P.id1[i] == d.src) or (P.id2[i] == d.src))])
        idx[(g, d.derived)] = (int(P.index[P.pair_id == d.derived_pair][0]), np.concatenate([hh, nd]))
M["ds"] = np.where(M.group.str.startswith("Progpedia"), "PROGpedia", "IR-Plag")
pair2 = np.array([(r.key1 in two) or (r.key2 in two) for r in P.itertuples()])

def auc_vec(sc):
    o = np.zeros(len(M))
    for i, d in enumerate(M.itertuples()):
        dp, nd = idx[(d.group, d.derived)]
        x = sc[nd]; o[i] = (x < sc[dp]).mean() + 0.5 * (x == sc[dp]).mean()
    return o
touch = np.array([pair2[idx[(d.group, d.derived)][0]] or pair2[idx[(d.group, d.derived)][1]].any() for d in M.itertuples()])
dp2 = np.array([pair2[idx[(d.group, d.derived)][0]] for d in M.itertuples()])
print("cohorts (derived entries) touching a 2-window file in any scored pair:", int(touch.sum()), "of", len(M), "; derived pair itself affected:", int(dp2.sum()))
print("pairs with a 2-window file:", int(pair2.sum()), "of", len(P), "; pairs with both 2-window:", int(np.array([(r.key1 in two) and (r.key2 in two) for r in P.itertuples()]).sum()))
for variant in ("plain", "filt"):
    cur = scores(variant, cpf.sem); fix = scores(variant, sem_fixed)
    vc, vf = auc_vec(cur), auc_vec(fix)
    print("\n== variant", variant, " max |score change| over pairs: %.3f; pairs changed >1e-6: %d" % (np.abs(cur - fix).max(), int((np.abs(cur - fix) > 1e-6).sum())))
    for ds in ("PROGpedia", "IR-Plag", "all"):
        m = (M.ds == ds).values if ds != "all" else np.ones(len(M), bool)
        print("  %-9s AUROC current %.3f  fixed %.3f  | cohorts unaffected only: current %.3f" % (ds, vc[m].mean(), vf[m].mean(), vc[m & ~touch].mean()))
    for kd in ("insert", "refactor", "llm"):
        pass
    if variant == "plain":
        mm = (M.ds == "PROGpedia").values
        for kd in M[mm].kind.unique():
            k = mm & (M.kind == kd).values
            print("   PROGpedia", kd, "current %.3f fixed %.3f" % (vc[k].mean(), vf[k].mean()))
    np.save(os.path.join(DATA, "..", "tables", "cb_cos_fixed_%s.npy" % variant), vf)

# ---- benchmark bound
pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
B = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
two_b = {k for k, v in B.items() if len(v["win"]) == 2}
m = (pf.key1.isin(two_b) | pf.key2.isin(two_b)).values
both = (pf.key1.isin(two_b) & pf.key2.isin(two_b)).values
print("\nbenchmark: 2-window snippets", len(two_b), "of", len(B), "; pairs touched", int(m.sum()), "of", len(pf), "; both 2-window", int(both.sum()))
print(" touched pairs by split:", pf[m].groupby("split").size().to_dict(), " label mix in test touched:", pf[m & (pf.split == "test")].label.value_counts().to_dict())
t = pf[m & (pf.split == "test")]
print(" mean S_CodeBERT of touched test pairs: pos %.3f neg %.3f ; both-2win pairs by label %s" % (
    t[t.label == 1].S_CodeBERT.mean(), t[t.label == 0].S_CodeBERT.mean(), pf[both & (pf.split == "test")].label.value_counts().to_dict()))
# recompute the semantic feature on touched pairs with the fix
fx = []
for r in pf[m].itertuples():
    fx.append(sem_fixed(B[r.key1], B[r.key2]))
fx = np.array(fx)
d = fx - pf[m].S_CodeBERT.values
print(" recomputed S_CodeBERT on touched pairs: mean change %.3f, abs mean %.3f, max %.3f" % (d.mean(), np.abs(d).mean(), np.abs(d).max()))
pf2 = pf.copy(); pf2.loc[m, "S_CodeBERT"] = fx
pf2.to_csv(os.path.join(DATA, "..", "tables", "pair_features_semfixed.csv"), index=False)
# AUROC of the raw CodeBERT cosine on test before/after, whole test set and touched subset
from sklearn.metrics import roc_auc_score
te = pf.split == "test"; te2 = pf2.split == "test"
print(" test AUROC of S_CodeBERT alone: current %.4f fixed %.4f ; whole-test pairs untouched %.4f" % (
    roc_auc_score(pf[te].label, pf[te].S_CodeBERT), roc_auc_score(pf2[te2].label, pf2[te2].S_CodeBERT),
    roc_auc_score(pf[te & ~m].label, pf[te & ~m].S_CodeBERT)))
tm = te & m
print(" touched test pairs (n=%d) AUROC S_CodeBERT: current %.3f fixed %.3f ; S_AST %.3f ; S_Token %.3f" % (
    tm.sum(), roc_auc_score(pf[tm].label, pf[tm].S_CodeBERT), roc_auc_score(pf2[tm].label, pf2[tm].S_CodeBERT),
    roc_auc_score(pf[tm].label, pf[tm].S_AST), roc_auc_score(pf[tm].label, pf[tm].S_Token)))
