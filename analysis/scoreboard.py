"""Scoreboard of the corrected pipeline: the gate against every comparator on every reported parameter.
Every number is read from results_*/ (post Eq. 2 fix) or computed here from released scores. python -I scoreboard.py"""
import json, os, pickle, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE
R = lambda r, f: json.load(open(os.path.join(HERE, "results_" + r, f)))
v0 = lambda x: x[0] if isinstance(x, list) else x

print("=== 1. Benchmark F1 (test, 5,652 pairs, validation-tuned threshold, mean of 8 seeds), %")
sysn = [("Gate (CodeBERT)", "gate|val"), ("Direct classifier", "direct|val"), ("Logistic regression", "logreg|val"), ("Token expert alone", "token|val"),
        ("Equal weights", "static|val"), ("CodeBERT alone", "codebert|val"), ("AST alone", "ast|val"), ("JPlag", "jplag|val"), ("JPlag+TokenNorm", "tokennorm|val"), ("Dolos", "dolos|val")]
print("%-22s %7s %7s %7s" % ("system", "A", "B", "C"))
for nm, k in sysn:
    print("%-22s" % nm + "".join(" %7.1f" % (100 * v0(R(r, "main_eval.json")["summary"][k]["f1"])) for r in "ABC"))
for r in "ABC":
    e = R(r, "e1_baselines.json")
    if r == "A": print("%-22s" % "Best fixed convex wts" + "".join(" %7.1f" % (100 * v0(R(x, "e1_baselines.json")["best_convex"]["f1"])) for x in "ABC"))
print("%-22s" % "Gradient-boosted trees" + "".join(" %7.1f" % (100 * v0(R(x, "e1_baselines.json")["gbt"]["f1"])) for x in "ABC"))
print("%-22s" % "Hand rule (lang rel.)" + "".join(" %7.1f" % (100 * v0(R(x, "e1_baselines.json")["hand_rule"]["f1"])) for x in "ABC"))

print("\n=== 2. AUROC (test) and recall at 1% FPR (oracle op. point), regime B")
e = R("B", "e1_baselines.json"); pa = R("B", "post_analysis.json")
for nm, k in (("Gate", "gate"), ("Direct", "direct"), ("Trees", "gbt"), ("Best convex", "best_convex")):
    d = e[k]; print("%-14s AUC %.3f  R@1%% %.1f  R@5%% %.1f" % (nm, v0(d["auc"]), 100 * v0(d["r1"]), 100 * v0(d["r5"])))

print("\n=== 3. Recall by derivation type and specificity, regime A (gate, validation-tuned threshold), %")
sl = R("A", "main_eval.json")["summary"]["gate|val"]["slices"]
print({k: round(100 * v[0], 1) for k, v in sl.items()})
for nm, k in (("Direct", "direct|val"), ("Token", "token|val"), ("JPlag", "jplag|val"), ("Dolos", "dolos|val")):
    s = R("A", "main_eval.json")["summary"][k]["slices"]; print("  %-8s" % nm, {a: round(100 * b[0], 1) for a, b in s.items()})

print("\n=== 4. Gate FPR by language relation (mean of seeds), %: same / cross")
for r in "ABC":
    d = R(r, "post_analysis.json")["gate_fpr_by_dlang_over_seeds"]; print(" regime", r, round(100 * d["same_language"]["mean"], 1), "/", round(100 * d["cross_language"]["mean"], 1))

print("\n=== 5. Independent-convergence flag rate (193 pairs), %")
for r in "AB":
    try:
        x = R(r, "external.json"); cv = x["gate"]["convergence"]["flag_rate"][0] if "gate" in x else None
        print(" regime", r, "gate", None if cv is None else round(100 * cv, 1), "| direct", round(100 * x["direct"]["convergence"]["flag_rate"][0], 1), "| token", round(100 * x["token"]["convergence"]["flag_rate"][0], 1))
    except Exception as ex:
        print(" regime", r, "unavailable:", repr(ex)[:80])

print("\n=== 6. Cohorts: mean AUROC, PROGpedia / IR-Plag (625 Java cohorts, corrected pipeline)")
c = R("A", "cohort_eval.json")["systems"]
for nm, k in (("Gate (CodeBERT)", "gate|plain"), ("Gate, boilerplate removed", "gate|filt"), ("Direct", "direct|plain"), ("Token", "token|plain"), ("Token, boilerplate removed", "token|filt"),
              ("JPlag", "jplag|plain"), ("JPlag+TokenNorm", "tokennorm|plain"), ("Dolos", "dolos_default|plain"), ("Static avg", "static|plain"), ("AST alone", "ast|plain")):
    print("  %-28s %.3f / %.3f" % (nm, c[k]["PROGpedia"]["auc"], c[k]["IR-Plag"]["auc"]))
w = R("Awh", "diag_wh_cohorts.json")
print("  %-28s %.3f / %.3f   (whitened expert, unfiltered)" % ("Gate (whitened)", w["gate"]["prog_mean"], w["gate"]["irplag_mean"]))
print("  %-28s %.3f / %.3f" % ("Direct (whitened)", w["direct"]["prog_mean"], w["direct"]["irplag_mean"]))

print("\n=== 7. Renaming attack, recall (%) before -> after, regime A")
a = R("A", "e4_attack.json"); print({k: (v if not isinstance(v, dict) else list(v)[:6]) for k, v in list(a.items())[:3]})
