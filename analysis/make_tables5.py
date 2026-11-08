"""Tables for the log-odds gate (repair of the mean-fusion gate). Every cell is read from a logged run:
results_<R>/gate_variants.json, gate_variants_sig.json, gate_shortcut.json, gate_cohort_sig.json (repo/analysis), results_A/xl2_eval.json,
results_<R>/cohort_eval.json (token expert). -> tables/tab_logit_bench.tex, tab_logit_real.tex, facts5.json
python -I make_tables5.py   (run after make_tables4.py)"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "tables")
R = lambda r, f: json.load(open(os.path.join(HERE, "results_" + r, f)))
gv = {r: R(r, "gate_variants.json") for r in "ABC"}
sig = {r: R(r, "gate_variants_sig.json") for r in "ABC"}
sc = {r: R(r, "gate_shortcut.json") for r in "ABC"}
xl = R("A", "xl2_eval.json")
# one aggregation for every R@1% / F1 cell of the paper: the released per-regime runs (e1_baselines.json, post_analysis.json)
E1 = {r: R(r + "lo", "e1_baselines.json") for r in "ABC"}; E1M = {r: R(r, "e1_baselines.json") for r in "ABC"}; POST = {r: R(r + "lo", "post_analysis.json") for r in "ABC"}
csig = json.load(open(os.path.join(HERE, "gate_cohort_sig.json")))
coh = R("A", "cohort_eval.json")["systems"]
f1 = lambda v: "%.1f" % (100 * (v[0] if isinstance(v, list) else v))
pm = lambda v: "%.1f\\,{\\scriptsize$\\pm$%.1f}" % (100 * v[0], 100 * v[1])
def sg(d):
    return "%+.1f" % (100 * d["delta"]) + ("$^{*}$" if d["p_holm"] < 0.05 else "")
def sg3(d):
    return "%+.3f" % d["delta"] + ("$^{*}$" if d["p_holm"] < 0.05 else "")

# ---------------------------------------------------------------- benchmark table
L = [r"\begin{table*}[t]", r"\centering",
     r"\caption{Log-odds fusion against the mean-fusion gate of the original proposal, the equal-capacity direct classifier and gradient-boosted trees (test partition, validation-tuned thresholds, the same eight-seed runs as Tables~\ref{tab:ablation} and~\ref{tab:baselines-fixed}; trees: HistGradientBoosting on the same six inputs). Mean fusion averages the three expert scores with the gate's softmax weights; log-odds fusion averages their logits with the same weights and maps the result through a learned scale and bias (Section~\ref{subsec:phase4}). $\Delta F_1$: log-odds gate minus direct classifier in points, with the paired cluster bootstrap over problem groups and Holm adjustment of Table~\ref{tab:ablation} (\textsuperscript{*}: $p_{\text{Holm}}<0.05$); R@1\%: recall at 1\% false-positive rate read from the ROC curve of the ensemble-mean test score, the convention of Table~\ref{tab:baselines-fixed}. The last two columns report a classifier that sees only the lengths and complexities of the two programs (AUROC) and the log-odds gate's $F_1$ on a length-matched subset (positives and negatives balanced within deciles of the length ratio).}",
     r"\label{tab:logit-bench}", r"\footnotesize", r"\setlength{\tabcolsep}{3pt}",
     r"\begin{tabular}{l|cccc|c|cccc|cc}", r"\toprule",
     r" & \multicolumn{4}{c|}{$F_1$ (\%)} & $\Delta F_1$ & \multicolumn{4}{c|}{R@1\% FPR} & Length-only & Matched \\",
     r"\textbf{Regime} & Mean & Log-odds & Direct & Trees & log-odds$-$direct & Mean & Log-odds & Direct & Trees & AUROC & $F_1$ \\", r"\midrule"]
names = {"A": "A (random negatives)", "B": "B (hard, expert-mined)", "C": "C (hard, identifier-mined)"}
for r in "ABC":
    e, em, po = E1[r], E1M[r], POST[r]
    dd = [x for x in po["ablation"] if x["config"].startswith("Direct classifier")][0]
    dtxt = "%+.1f" % (-dd["delta"]) + ("$^{*}$" if dd["p_cluster_holm"] < 0.05 else "")
    L.append(" & ".join([names[r], pm(em["gate"]["f1"]), pm(e["gate"]["f1"]), pm(e["direct"]["f1"]), pm(e["gbt"]["f1"]), dtxt,
                         f1(em["gate"]["r1"]), f1(e["gate"]["r1"]), f1(e["direct"]["r1"]), f1(e["gbt"]["r1"]), "%.2f" % sc[r]["length_only_auc"], f1(sc[r]["logit"]["f1_matched"])]) + r" \\")
L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
open(os.path.join(OUT, "tab_logit_bench.tex"), "w").write("\n".join(L))

# ---------------------------------------------------------------- real-code table
L = [r"\begin{table*}[t]", r"\centering",
     r"\caption{Real-code evaluation of the three fusion rules trained on each benchmark regime and applied unchanged: mean cohort AUROC (share of a cohort's non-derived pairs scored below its derived pair) on the 270 PROGpedia and 355 IR-Plag cohorts (Java), and on the 100 cross-language cohorts (honest Java submissions of two PROGpedia assignments; derived submission: a translation of one of them into Python or C\# made by Claude, parse-checked but not checked for behavioural equivalence; none of the cohort programs occurs in any benchmark pair). Token expert: $k$-gram overlap alone. The last three columns give the differences of the log-odds gate to the mean-fusion gate, the direct classifier and the token expert; the first two on the Java cohorts and all three on the cross-language cohorts are paired cluster bootstraps over source submissions, Holm-adjusted (\textsuperscript{*}: $p<0.05$), and the token-expert difference on the Java cohorts is a point difference without a test. JPlag and Dolos cannot score the cross-language pairs.}",
     r"\label{tab:logit-real}", r"\scriptsize", r"\setlength{\tabcolsep}{3pt}",
     r"\begin{tabular}{ll|cccc|ccc}", r"\toprule",
     r"\textbf{Cohorts} & \textbf{Regime} & Mean & Log-odds & Direct & Token & log-odds$-$mean & log-odds$-$direct & log-odds$-$token \\", r"\midrule"]
tok = {ds: coh["token|plain"][ds]["auc"] for ds in ("PROGpedia", "IR-Plag")}
for ds, lab in (("PROGpedia", "PROGpedia (270)"), ("IR-Plag", "IR-Plag (355)")):
    for r in "ABC":
        key = "cohort_prog" if ds == "PROGpedia" else "cohort_irplag"; c = csig[r][ds]
        L.append(" & ".join([lab if r == "A" else "", r, "%.3f" % gv[r]["base"][key], "%.3f" % gv[r]["logit"][key], "%.3f" % gv[r]["direct"][key], "%.3f" % tok[ds],
                             sg3(c["logit-base"]), sg3(c["logit-direct"]), "%+.3f" % (gv[r]["logit"][key] - tok[ds])]) + r" \\")
    L.append(r"\midrule")
for r in "ABC":
    x = xl[r]
    L.append(" & ".join(["Cross-language (100)" if r == "A" else "", r, "%.3f" % x["mean_auc"]["base"], "%.3f" % x["mean_auc"]["logit"], "%.3f" % x["mean_auc"]["direct"], "%.3f" % x["mean_auc"]["token"],
                         sg3(x["vs"]["logit-base"]), sg3(x["vs"]["logit-direct"]), sg3(x["vs"]["logit-token"])]) + r" \\")
L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
open(os.path.join(OUT, "tab_logit_real.tex"), "w").write("\n".join(L))

json.dump({"gate_variants": gv, "sig": sig, "shortcut": sc, "xl2": xl, "cohort_sig": csig}, open(os.path.join(OUT, "facts5.json"), "w"), indent=1, default=float)
print("wrote tab_logit_bench.tex, tab_logit_real.tex, facts5.json")

# ---------------------------------------------------------------- filtered log-odds differences (companion of tab:cohort-diff)
fs = json.load(open(os.path.join(HERE, "gate_cohort_filt_sig.json")))
def fcell(d):
    p = d["p_holm"]
    return "%+.3f [%+.3f, %+.3f] & %s" % (d["delta"], d["ci"][0], d["ci"][1], ("$<$0.002" if p < 0.002 + 1e-9 else "%.3f" % p))
rows = [("logit|filt-token|filt", r"Log-odds gate filtered $-$ token expert filtered"), ("logit|filt-direct|filt", r"Log-odds gate filtered $-$ direct classifier filtered"),
        ("logit|filt-base|filt", r"Log-odds gate filtered $-$ mean-fusion gate filtered"), ("logit|filt-logit|plain", r"Log-odds gate filtered $-$ log-odds gate unfiltered")]
def _rows(fn, skip):
    out = []
    for l in open(os.path.join(OUT, fn), encoding="utf8").read().split(chr(10)):
        if "&" in l and not l.startswith(chr(92)) and not l.startswith(skip) and "multicolumn" not in l:
            out.append(l.strip().rstrip(chr(92)).rstrip())
    return out
# the 11 comparison rows of the former Table cohort-diff (mean-fusion gate of the original proposal and tools, regime A) and the 9 per-group rows of the former
# Table cohort-detail are carried into this table verbatim (restore register: r2_pre_reduction/tables/tab_cohort_diff.tex and tab_cohort_detail.tex)
t18 = _rows("tab_cohort_diff.tex", ("Comparison", chr(92)))
t17 = _rows("tab_cohort_detail.tex", ("Group", chr(92)))
L = [r"\begin{table*}[t]", r"\centering",
     r"\caption{Paired differences in mean cohort AUROC (top) and per-group cohort AUROC (bottom). Top, 95\% cluster-bootstrap interval of the difference (clusters: source submissions): first block, boilerplate-filtered log-odds gate (CodeBERT expert) by training regime, with Holm-adjusted two-sided bootstrap $p$ over the comparisons of each regime and collection (entries at the resampling floor are printed as $<$0.002); second block, regime A, the mean-fusion gate of the original proposal and the tools, with unadjusted two-sided bootstrap $p$ from 2,000 resamples (smallest attainable 0.0005, printed $<$0.001); ``filtered'' rows remove assignment boilerplate and ``token'' is the unfiltered token expert unless marked. Bottom, mean cohort AUROC per assignment (PROGpedia) and per task (IR-Plag), $n$ cohorts each; BP: boilerplate removed without labels; the gate columns are the mean-fusion gate trained on regime A (per-group values of the log-odds gate were not computed).}",
     r"\label{tab:cohort-filt-diff}", r"\scriptsize", r"\setlength{\tabcolsep}{3pt}", r"\begin{tabular}{ll|cc|cc}", r"\toprule",
     r" & & \multicolumn{2}{c|}{PROGpedia} & \multicolumn{2}{c}{IR-Plag} \\", r"\textbf{Comparison} & \textbf{Reg.} & $\Delta$ [95\% CI] & $p$ & $\Delta$ [95\% CI] & $p$ \\", r"\midrule"]
for k, nm in rows:
    for r in "ABC":
        L.append(" & ".join([nm if r == "A" else "", r, fcell(fs[r]["PROGpedia"][k]), fcell(fs[r]["IR-Plag"][k])]) + r" \\")
    L.append(r"\midrule")
L.append(r"\multicolumn{6}{l}{\emph{Mean-fusion gate of the original proposal and tools (regime A)}} \\")
for r_ in t18:
    c = r_.split("&")
    L.append(" & ".join([c[0].strip(), "A"] + [x.strip() for x in c[1:]]) + r" \\")
L += [r"\bottomrule", r"\end{tabular}", r"\par\vspace{4pt}", r"\begin{tabular}{lr|cccccc}", r"\toprule",
      r"\textbf{Group} & $n$ & Gate & Gate BP & Token BP & JPlag & Dolos & Dolos $-$M 0.5 \\", r"\midrule"]
L += [r_ + r" \\" for r_ in t17]
L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
open(os.path.join(OUT, "tab_cohort_filt_diff.tex"), "w").write(chr(10).join(L))
print("wrote tab_cohort_filt_diff.tex")

# ---------------------------------------------------------------- probe: the UniXcoder-expert block of the former Table probe-ux becomes a second block of tab_probe
# (same columns, same rows; every cell is carried verbatim; the former tab_probe_ux.tex is restored from r2_pre_reduction/ if ever needed)
def _tab(fn):
    return open(os.path.join(OUT, fn), encoding="utf8").read()
tp, tu = _tab("tab_probe.tex"), _tab("tab_probe_ux.tex")
if "UniXcoder expert" not in tp:
    BSL = chr(92)
    body_u = tu[tu.index(BSL + "midrule") + len(BSL + "midrule"):tu.index(BSL + "bottomrule")]
    head_u = [l for l in tu.split(chr(10)) if l.startswith(" & & " + BSL + "multicolumn")][0]
    cap = tp[tp.index(BSL + "caption{"):tp.index(BSL + "label{")]
    cap_new = cap.rstrip().rstrip("}") + (" Lower block: the same probe with the UniXcoder expert (gate and expert trained on the benchmark, then frozen; same pairs and threshold procedure; "
                                          "the UniXcoder-cosine columns are one deterministic score per pair, but its validation-tuned threshold is set per regime (0.525 in regime A, 0.535 in regime B), "
                                          "so its recall and FPR differ slightly between the regimes).}" + chr(10))
    tp2 = tp.replace(cap, cap_new)
    k = tp2.index(BSL + "bottomrule")
    tp2 = tp2[:k] + BSL + "midrule" + chr(10) + BSL + "multicolumn{10}{l}{" + BSL + "emph{UniXcoder expert}} " + BSL + BSL + chr(10) + head_u + chr(10) + body_u.strip(chr(10)) + chr(10) + tp2[k:]
    open(os.path.join(OUT, "tab_probe.tex"), "w").write(tp2)
    print("merged tab_probe_ux into tab_probe")

# ---------------------------------------------------------------- split re-draws (former Table split-variance) merged under the regime-C table (same float, second tabular).
# All 10 per-draw rows and both mean+-s.d. rows (incl. the direct-classifier means 91.4+-0.6 / 90.5+-0.3) are carried verbatim.
def _read(fn):
    return open(os.path.join(OUT, fn), encoding="utf8").read()
rc, sv_ = _read("tab_regime_c.tex"), _read("tab_splitvar.tex")
if "tab:split-variance" not in rc:
    BSL = chr(92)
    cap_sv = sv_[sv_.index(BSL + "caption{") + len(BSL + "caption{"):sv_.index(BSL + "label{")].rstrip().rstrip("}")
    tab_sv = sv_[sv_.index(BSL + "footnotesize"):sv_.index(BSL + "end{table}")]
    rc2 = rc.replace(BSL + "end{table}", BSL + "par" + BSL + "vspace{4pt}" + chr(10) + BSL + "label{tab:split-variance}" + chr(10) + BSL + "noindent{" + BSL + "footnotesize " + BSL + "textbf{(b)} " + cap_sv + "}" + chr(10) + BSL + "par" + BSL + "vspace{2pt}" + chr(10) + tab_sv + BSL + "end{table}")
    rc2 = rc2.replace(BSL + "caption{Regime C:", BSL + "caption{(a) Regime C:", 1)
    open(os.path.join(OUT, "tab_regime_c.tex"), "w").write(rc2)
    print("merged tab_splitvar into tab_regime_c")
