"""Re-run every CodeBERT-expert (regimes A, B, C) stage after the Eq. 2 fix (data/pair_features.csv recomputed by
recompute_sem_feature.py). Regimes run in parallel; each regime runs its stages in order and logs to data/rerun_eq2/.
UniXcoder (ux) and whitened (wh) variants do not use per-snippet window centring and are not re-run.
python -I rerun_after_eq2_fix.py [A B C]"""
import os, subprocess, sys, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "data", "rerun_eq2")
os.makedirs(LOG, exist_ok=True)

# stage -> regimes it applies to (as in the script docstrings)
STAGES = [
    ("run_experiments", "ABC"), ("evaluate_all", "ABC"), ("post_analysis", "ABC"), ("e1_baselines", "ABC"),
    ("e2_retrained_ablation", "ABC"), ("e3_encoder_control", "ABC"), ("failure_pooled", "AB"), ("e8_tool_metrics", "ABC"),
    ("dolos_bench_stats", "ABC"), ("split_variance", "ABC"),
    ("e4_eval", "AB"), ("e7_probe_reanalysis", "AB"), ("eval_external", "AB"), ("eval_probe2", "AB"),
    ("eval_cohorts", "ABC"), ("analyze_cohorts", "ABC"),
    ("e6_weights_and_tasks", "A"), ("eval_cohort_variants", "A"), ("sens_filter", "A"),
]
status = {}

def run_regime(r):
    for name, regs in STAGES:
        if r not in regs:
            continue
        t0 = time.time()
        env = dict(os.environ, REGIME=r, PYTHONHASHSEED="0")
        with open(os.path.join(LOG, "%s_%s.log" % (name, r)), "w", encoding="utf8") as f:
            rc = subprocess.call([sys.executable, "-I", name + ".py"], cwd=HERE, env=env, stdout=f, stderr=subprocess.STDOUT)
        status[(r, name)] = (rc, time.time() - t0)
        print("[%s] %-24s rc=%d %.0fs" % (r, name, rc, time.time() - t0), flush=True)
        if rc != 0 and name in ("run_experiments", "evaluate_all"):
            print("[%s] aborting regime after %s" % (r, name), flush=True)
            return

if __name__ == "__main__":
    regs = sys.argv[1:] or ["A", "B", "C"]
    ts = [threading.Thread(target=run_regime, args=(r,)) for r in regs]
    for t in ts: t.start()
    for t in ts: t.join()
    bad = {k: v for k, v in status.items() if v[0] != 0}
    print("DONE; failed stages:", bad if bad else "none", flush=True)
