"""Paired cluster-bootstrap tests on the per-cohort AUROC vectors saved by gate_shortcut.py (clusters = source submissions, as in
analyze_cohorts.py). Compares each gate variant with the direct classifier and with the original gate, per dataset.
Also adds the token expert, boilerplate-free references from cohort_auc_vectors.npz (regime A) for context.
python -I gate_cohort_sig.py -> results_<R>/gate_cohort_sig.json"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE
from stats_tools import boot_p, holm

PAIRS = [("logit", "base"), ("logit_len", "base"), ("logit_feat", "base"), ("logit", "direct"), ("logit_len", "direct_len"), ("logit_feat", "direct_feat"),
         ("direct", "base")]
out = {}
for r in "ABC":
    V = np.load(os.path.join(HERE, "results_" + r, "gate_cohort_vectors.npz"), allow_pickle=True)
    cl, grp = V["_clusters"], V["_group"]
    out[r] = {}
    for ds, sel in (("PROGpedia", np.array([g.startswith("Progpedia") for g in grp])), ("IR-Plag", np.array([not g.startswith("Progpedia") for g in grp]))):
        u, inv = np.unique(cl[sel], return_inverse=True); cnt = np.bincount(inv); rng = np.random.default_rng(0)
        boots = [rng.integers(0, len(u), len(u)) for _ in range(4000)]
        def stat(v):
            sums = np.bincount(inv, weights=v[sel], minlength=len(u)); return np.array([sums[b].sum() / cnt[b].sum() for b in boots])
        res, ps = {}, []
        for a, b in PAIRS:
            d = stat(V[a]) - stat(V[b]); p = boot_p(d); ps.append(p)
            res["%s-%s" % (a, b)] = dict(delta=float(V[a][sel].mean() - V[b][sel].mean()), ci=[float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))])
        for (a, b), p in zip(PAIRS, holm(ps)): res["%s-%s" % (a, b)]["p_holm"] = float(p)
        out[r][ds] = res
        for k, v in res.items():
            print(r, ds, "%-24s d %+.3f  CI [%+.3f, %+.3f]  p_holm %.3f" % (k, v["delta"], *v["ci"], v["p_holm"]))
json.dump(out, open(os.path.join(HERE, "gate_cohort_sig.json"), "w"), indent=1)
