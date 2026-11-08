"""Rerun the mean-fusion-only analyses for the LOG-ODDS gate (FUSION=logit): main training + all systems (run_experiments), decisions
(evaluate_all), post analysis (leave-one-out, capacity control, thresholds, weights), retrained ablation (e2), split re-draws, failure analysis
and the renaming attack (e4). Results go to results_<R>lo/ (TAG gets an 'lo' suffix); the mean-fusion results are untouched.
JPlag/Dolos score files are read from the mean-fusion regime directory (they do not depend on the gate): copied in first.
python -I rerun_logit_ablations.py [A B C]"""
import os, shutil, subprocess, sys, threading, time
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "data", "rerun_logit"); os.makedirs(LOG, exist_ok=True)
STAGES = [("run_experiments", "ABC"), ("evaluate_all", "ABC"), ("post_analysis", "AB"), ("e2_retrained_ablation", "ABC"),
          ("failure_pooled", "AB"), ("split_variance", "ABC"), ("e4_eval", "AB")]
status = {}
def run_regime(r):
    for name, regs in STAGES:
        if r not in regs: continue
        t0 = time.time()
        env = dict(os.environ, REGIME=r, FUSION="logit", PYTHONHASHSEED="0")
        with open(os.path.join(LOG, "%s_%s.log" % (name, r)), "w", encoding="utf8") as f:
            rc = subprocess.call([sys.executable, "-I", name + ".py"], cwd=HERE, env=env, stdout=f, stderr=subprocess.STDOUT)
        status[(r, name)] = rc
        print("[%s] %-24s rc=%d %.0fs" % (r, name, rc, time.time() - t0), flush=True)
        if rc != 0 and name in ("run_experiments", "evaluate_all"):
            print("[%s] aborting regime after %s" % (r, name), flush=True); return
if __name__ == "__main__":
    regs = sys.argv[1:] or ["A", "B", "C"]
    for r in regs:
        os.makedirs(os.path.join(HERE, "results_%slo" % r), exist_ok=True)
    ts = [threading.Thread(target=run_regime, args=(r,)) for r in regs]
    for t in ts: t.start()
    for t in ts: t.join()
    bad = {k: v for k, v in status.items() if v}
    print("DONE; failed stages:", bad if bad else "none", flush=True)
