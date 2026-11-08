"""Paired cluster-bootstrap tests on the filtered / plain cohort AUROC vectors of gate_cohort_filt.py (clusters = source submissions).
python -I gate_cohort_filt_sig.py -> gate_cohort_filt_sig.json"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE
from stats_tools import boot_p, holm
PAIRS = [("logit|filt", "token|filt"), ("logit|filt", "direct|filt"), ("logit|filt", "base|filt"), ("logit|filt", "logit|plain")]
out = {}
for r in "ABC":
    V = np.load(os.path.join(HERE, "results_" + r, "gate_cohort_filt_vectors.npz"), allow_pickle=True); out[r] = {}
    for ds in ("PROGpedia", "IR-Plag"):
        sel = V["_ds"] == ds; u, inv = np.unique(V["_cl"][sel], return_inverse=True); cnt = np.bincount(inv)
        rng = np.random.default_rng(0); boots = [rng.integers(0, len(u), len(u)) for _ in range(4000)]
        st = lambda v: np.array([np.bincount(inv, weights=v[sel], minlength=len(u))[b].sum() / cnt[b].sum() for b in boots])
        res, ps = {}, []
        for a, b in PAIRS:
            d = st(V[a]) - st(V[b]); ps.append(boot_p(d))
            res["%s-%s" % (a, b)] = dict(delta=float(V[a][sel].mean() - V[b][sel].mean()), ci=[float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))])
        for (a, b), p in zip(PAIRS, holm(ps)): res["%s-%s" % (a, b)]["p_holm"] = float(p)
        out[r][ds] = res
        for k, v in res.items(): print(r, ds, "%-28s d %+.3f CI [%+.3f, %+.3f] p_holm %.3f" % (k, v["delta"], *v["ci"], v["p_holm"]))
json.dump(out, open(os.path.join(HERE, "gate_cohort_filt_sig.json"), "w"), indent=1)
