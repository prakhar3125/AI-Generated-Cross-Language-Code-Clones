"""Win / tie / loss count of the paper's gate (corrected pipeline, original CodeBERT expert) against every comparator, per metric and regime.
Win/loss = gate better/worse by more than TOL on that metric; otherwise tie. This is a descriptive count of point estimates:
it is NOT a significance test (the paired tests are gate_variants_sig.py and e2/e1 cluster tests).
python -I win_loss_count.py"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE
R = lambda r, f: json.load(open(os.path.join(HERE, "results_" + r, f)))
v0 = lambda x: x[0] if isinstance(x, list) else x
TOL = 0.01          # 1 point of F1 / 0.01 AUROC-style units

rows = []       # (family, comparator, regime, metric, gate, other)
def add(fam, comp, reg, met, g, o, higher=True):
    rows.append((fam, comp, reg, met, g, o, higher))

for r in "ABC":
    s = R(r, "main_eval.json")["summary"]; e1 = R(r, "e1_baselines.json")
    g = v0(s["gate|val"]["f1"])
    for nm, k in (("Direct classifier", "direct|val"), ("Logistic regression", "logreg|val"), ("Token expert", "token|val"), ("Equal weights", "static|val"),
                  ("CodeBERT alone", "codebert|val"), ("AST alone", "ast|val"), ("JPlag", "jplag|val"), ("JPlag+TokenNorm", "tokennorm|val"), ("Dolos", "dolos|val")):
        add("learned" if nm in ("Direct classifier", "Logistic regression") else "fixed/tool", nm, r, "F1", g, v0(s[k]["f1"]))
    for nm, k in (("Best fixed convex", "best_convex"), ("Hand rule", "hand_rule"), ("Gradient-boosted trees", "gbt")):
        add("learned" if k == "gbt" else "fixed/tool", nm, r, "F1", g, v0(e1[k]["f1"]))
    # ranking
    for nm, k in (("Direct classifier", "direct"), ("Gradient-boosted trees", "gbt"), ("Best fixed convex", "best_convex"), ("Hand rule", "hand_rule")):
        add("learned" if k in ("direct", "gbt") else "fixed/tool", nm, r, "AUROC", v0(e1["gate"]["auc"]), v0(e1[k]["auc"]))
        add("learned" if k in ("direct", "gbt") else "fixed/tool", nm, r, "R@1%FPR", v0(e1["gate"]["r1"]), v0(e1[k]["r1"]))
# cohorts (Java), original-expert gate, mean AUROC
c = R("A", "cohort_eval.json")["systems"]
for ds in ("PROGpedia", "IR-Plag"):
    g = c["gate|plain"][ds]["auc"]
    for nm, k, fam in (("Direct classifier", "direct|plain", "learned"), ("Token expert", "token|plain", "fixed/tool"), ("JPlag", "jplag|plain", "fixed/tool"),
                       ("JPlag+TokenNorm", "tokennorm|plain", "fixed/tool"), ("Dolos", "dolos_default|plain", "fixed/tool"), ("Equal weights", "static|plain", "fixed/tool"), ("AST alone", "ast|plain", "fixed/tool")):
        add(fam, nm, "cohort", "AUROC " + ds, g, c[k][ds]["auc"])

def verdict(g, o): return "win" if g - o > TOL else ("loss" if o - g > TOL else "tie")
import collections
tally = collections.defaultdict(lambda: collections.Counter())
for fam, comp, reg, met, g, o, hi in rows:
    v = verdict(g, o); tally["ALL"][v] += 1; tally[fam][v] += 1; tally["regime " + reg][v] += 1
    tally["metric " + met.split()[0]][v] += 1
n = sum(tally["ALL"].values())
print("comparisons:", n, "(each = one comparator x one regime/dataset x one metric; tolerance %.2f)" % TOL)
for k in ("ALL", "fixed/tool", "learned", "regime A", "regime B", "regime C", "regime cohort", "metric F1", "metric AUROC", "metric R@1%FPR"):
    t = tally[k]; m = sum(t.values())
    print("%-16s n=%3d  win %5.1f%%  tie %5.1f%%  loss %5.1f%%" % (k, m, 100 * t["win"] / m, 100 * t["tie"] / m, 100 * t["loss"] / m))
print("\nlosses (comparator, regime, metric, gate, other):")
for fam, comp, reg, met, g, o, hi in rows:
    if verdict(g, o) == "loss": print("  %-24s %-7s %-16s gate %.3f  other %.3f" % (comp, reg, met, g, o))
