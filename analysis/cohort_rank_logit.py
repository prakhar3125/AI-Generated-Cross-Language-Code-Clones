"""hit@k of the derived pair among a cohort's non-derived pairs for the log-odds gate (regime A, 8-seed mean score), from the saved
per-cohort scores -- recomputed here from gate_cohort_filt via the same featurization. python -I cohort_rank_logit.py"""
import os, pickle, sys
import numpy as np, pandas as pd
os.environ["REGIME"] = "A"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate_cohort_filt as g
from multiprocessing import Pool
if __name__ == "__main__":
    import torch; torch.set_num_threads(1)
    idx = g.indices()
    with Pool(5) as pool: res = pool.map(g.job, [("logit", s) for s in range(8)] + [("direct", s) for s in range(8)])
    ds = np.array(["PROGpedia" if k[0].startswith("Progpedia") else "IR-Plag" for k in idx])
    for kind in ("logit", "direct"):
        for v in ("plain", "filt"):
            sc = np.mean([x[3][v] for x in res if x[0] == kind], 0)
            ranks = np.array([1 + (sc[nd] > sc[dp]).sum() + 0.5 * (sc[nd] == sc[dp]).sum() for (gname, d), (dp, nd, src) in idx.items()])
            for d_ in ("PROGpedia", "IR-Plag"):
                r = ranks[ds == d_]
                print(kind, v, d_, "hit@1 %.3f hit@5 %.3f hit@10 %.3f median rank %.1f" % ((r <= 1).mean(), (r <= 5).mean(), (r <= 10).mean(), np.median(r)))
