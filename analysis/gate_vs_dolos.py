"""Paired cluster-bootstrap of the filtered LOG-ODDS gate against Dolos -M 0.5 and the Dolos default, per dataset and regime
(clusters = source submissions). Vectors: results_<R>/gate_cohort_filt_vectors.npz and results_A/cohort_auc_vectors.npz.
python -I gate_vs_dolos.py"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE
from stats_tools import boot_p, holm
D = np.load(os.path.join(HERE, "results_A", "cohort_auc_vectors.npz"), allow_pickle=True)
DR = json.load(open(os.path.join(HERE, "data", "dolos_cohort_runs.json")))
out = {}
for r in "ABC":
    V = np.load(os.path.join(HERE, "results_" + r, "gate_cohort_filt_vectors.npz"), allow_pickle=True)
    assert (V["_cl"] == D["clusters"]).all() and (V["_ds"] == D["ds"]).all(), "cohort order differs"
    out[r] = {}
    for ds in ("PROGpedia", "IR-Plag"):
        sel = V["_ds"] == ds; u, inv = np.unique(V["_cl"][sel], return_inverse=True); cnt = np.bincount(inv)
        rng = np.random.default_rng(0); boots = [rng.integers(0, len(u), len(u)) for _ in range(4000)]
        st = lambda v: np.array([np.bincount(inv, weights=v[sel], minlength=len(u))[b].sum() / cnt[b].sum() for b in boots])
        res, ps = {}, []
        for nm, ref in (("dolos_m50_runs", np.array(DR["vec_auc"]["m50"])), ("dolos_default_runs", np.array(DR["vec_auc"]["default"]))):
            d = st(V["logit|filt"]) - st(ref); ps.append(boot_p(d))
            res["logit|filt - %s" % nm] = dict(delta=float(V["logit|filt"][sel].mean() - ref[sel].mean()), ci=[float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))])
        for k, p in zip(list(res), holm(ps)): res[k]["p_holm"] = float(p)
        out[r][ds] = res
        for k, v in res.items(): print(r, ds, "%-34s d %+.3f CI [%+.3f, %+.3f] p_holm %.3f" % (k, v["delta"], *v["ci"], v["p_holm"]))
json.dump(out, open(os.path.join(HERE, "gate_vs_dolos.json"), "w"), indent=1)
