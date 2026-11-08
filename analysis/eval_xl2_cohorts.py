"""Score the 100 cross-language cohorts (PROGpedia honest Java + LLM translations into Python / C#) with the gate variants and the
direct classifier trained on the benchmark (regimes A, B, C; 8 seeds; threshold-free: per-cohort AUROC).
Comparators that cannot score cross-language pairs (JPlag, Dolos) get no score here; the token expert is included (it can be computed).
Per-cohort AUROC = share of the cohort's non-derived pairs scored below the derived pair (ties 1/2), clusters = source submission.
Caveat to state in the paper: the translations are LLM-generated and parse-checked, not checked for behavioural equivalence.
python -I eval_xl2_cohorts.py -> results_<R>/xl2_eval.json   (all three regimes in one run)"""
import json, os, pickle, sys
from multiprocessing import Pool
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE
import compute_pair_features as cpf
from stats_tools import boot_p, holm

KINDS = ["base", "logit", "direct"]
P = pd.read_csv(os.path.join(DATA, "xl2_cohort_pairs.csv")); M = pd.read_csv(os.path.join(DATA, "xl2_cohort_meta.csv"))
S = pd.read_csv(os.path.join(DATA, "xl2_cohort_subs.csv")); F = pickle.load(open(os.path.join(DATA, "xl2_cohort_feats.pkl"), "rb"))

def feats():
    rows = []
    for r in P.itertuples():
        a, b = F[r.key1], F[r.key2]
        s_c, s_a, s_t = cpf.sem(a, b), cpf.ast_sim(a, b), cpf.tok_sim(a, b)
        rows.append((s_c, s_a, s_t, float(r.D_lang), abs(s_c - s_a), 1 - s_a, a["cc"], b["cc"], a["ntok"], b["ntok"]))
    return pd.DataFrame(rows, columns=["S_CodeBERT", "S_AST", "S_Token", "D_lang", "S_CodeBERT_minus_S_AST", "one_minus_S_AST", "cc1", "cc2", "ntok1", "ntok2"])

def cohort_auc(sc):
    hon = {g: set(G[G.role == "honest"].id) for g, G in S.groupby("group")}
    out = []
    for d in M.itertuples():
        G = P[P.group == d.group]
        nd = G[G.label == 0].index.values; dp = int(P.index[P.pair_id == d.derived_pair][0]); x = sc[nd]
        out.append((d.group.rsplit("-", 2)[0] + "|" + d.src, d.target, (x < sc[dp]).mean() + .5 * (x == sc[dp]).mean()))
    return out

def job(a):
    reg, kind, seed = a
    os.environ["REGIME"] = reg
    import importlib, exp_lib; importlib.reload(exp_lib)
    import gate_variants as gv; importlib.reload(gv)
    X = gv.design(coh, kind, gv.EX)
    m = gv.train(kind, gv.design(gv.tr, kind, gv.EX), gv.tr[gv.SC].values, gv.tr.label.values, gv.design(gv.va, kind, gv.EX), gv.va[gv.SC].values, gv.va.label.values, seed, gv.LR, gv.BS)
    s, w = gv.predict(m, X, coh[gv.SC].values)
    return reg, kind, seed, s

coh = feats()
if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    results = {}
    for reg in "ABC":
        os.environ["REGIME"] = reg
        with Pool(5) as pool:
            res = pool.map(job, [(reg, k, s) for k in KINDS for s in range(8)])
        vec = {}
        for k in KINDS:
            sc = np.mean([x[3] for x in res if x[1] == k], 0); cv = cohort_auc(sc)
            vec[k] = np.array([c[2] for c in cv]); vec["_cl"] = np.array([c[0] for c in cv]); vec["_tg"] = np.array([c[1] for c in cv])
        for nm, col in (("token", "S_Token"), ("ast", "S_AST")):
            vec[nm] = np.array([c[2] for c in cohort_auc(coh[col].values)])
        u, inv = np.unique(vec["_cl"], return_inverse=True); cnt = np.bincount(inv)
        rng = np.random.default_rng(0); boots = [rng.integers(0, len(u), len(u)) for _ in range(4000)]
        stat = lambda v: np.array([np.bincount(inv, weights=v, minlength=len(u))[b].sum() / cnt[b].sum() for b in boots])
        out = {"n_cohorts": int(len(M)), "n_clusters": int(len(u)), "mean_auc": {k: float(vec[k].mean()) for k in KINDS + ["token", "ast"]},
               "by_target": {t: {k: float(vec[k][vec["_tg"] == t].mean()) for k in KINDS} for t in ("python", "csharp")}, "vs": {}}
        pairs = [("logit", "base"), ("logit", "direct"), ("logit", "token"), ("direct", "token")]; ps = []
        for a, b in pairs:
            d = stat(vec[a]) - stat(vec[b]); ps.append(boot_p(d))
            out["vs"]["%s-%s" % (a, b)] = dict(delta=float(vec[a].mean() - vec[b].mean()), ci=[float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))])
        for (a, b), p in zip(pairs, holm(ps)): out["vs"]["%s-%s" % (a, b)]["p_holm"] = float(p)
        results[reg] = out
        print(reg, "mean AUROC", {k: round(v, 3) for k, v in out["mean_auc"].items()}, "| by target", {t: {k: round(v, 3) for k, v in d.items()} for t, d in out["by_target"].items()}, flush=True)
        for k, v in out["vs"].items(): print("  ", reg, "%-14s d %+.3f CI [%+.3f, %+.3f] p_holm %.3f" % (k, v["delta"], *v["ci"], v["p_holm"]), flush=True)
    json.dump(results, open(os.path.join(HERE, "results_A", "xl2_eval.json"), "w"), indent=1)
