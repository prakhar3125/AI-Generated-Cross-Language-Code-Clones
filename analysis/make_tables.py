# -*- coding: utf-8 -*-
"""Generate every LaTeX table of the manuscript (and facts.json) from the saved results.

python -I make_tables.py
Output: analysis/tables/*.tex , analysis/tables/facts.json
"""
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE  # noqa: E402

LO = os.environ.get("LOGIT_TABLES") == "1"          # 1: build the tables of the log-odds gate from results_<R>lo/ into tables_lo/
SUF = "lo" if LO else ""
OUT = os.path.join(HERE, "tables_lo" if LO else "tables")
os.makedirs(OUT, exist_ok=True)
FACTS = {}


def load_regime(r):
    env = dict(os.environ, REGIME=r)
    sys.modules.pop("exp_lib", None)
    os.environ["REGIME"] = r
    import importlib
    import exp_lib
    importlib.reload(exp_lib)
    d = exp_lib.load()
    base = os.path.join(HERE, "results_" + r + SUF)
    return dict(D=d, ev=json.load(open(os.path.join(base, "main_eval.json"))),
                post=json.load(open(os.path.join(base, "post_analysis.json"))),
                probe=json.load(open(os.path.join(base, "probe2.json"))) if os.path.exists(os.path.join(base, "probe2.json")) else None,
                P=np.load(os.path.join(base, "preds.npz")), S=np.load(os.path.join(base, "scores.npz")),
                train=json.load(open(os.path.join(base, "training_summary.json"))))


RG = {r: load_regime(r) for r in ("A", "B")}
NAMES = [("gate|val", "Gating network (%s)" % ("log-odds fusion" if LO else "mean fusion"), True), ("direct|val", "Direct classifier (equal capacity)", True),
         ("logreg|val", "Logistic regression", False), ("static|val", "Static averaging", False),
         ("codebert|val", "CodeBERT only", False), ("ast|val", "AST only", False), ("token|val", "Token $k$-gram only", False),
         ("jplag|val", "JPlag 6.3.0", False), ("tokennorm|val", "JPlag + token normalization", False),
         ("dolos|val", "Dolos 2.10.0", False)]


def pct(x, d=1):
    return ("%." + str(d) + "f") % (100 * x)


def cell(m, k, sd=False):
    v = m[k]
    s = pct(v[0])
    if sd and v[1] > 0:
        s += r"\,{\scriptsize$\pm$%s}" % pct(v[1])
    return s


# ---------------------------------------------------------------- T: main comparison
def main_table():
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Overall performance on the 5{,}652-pair test partition (2{,}652 derived, 3{,}000 non-derived pairs), "
         r"for the two negative regimes. Every system uses a decision threshold tuned on the validation partition. "
         r"Trained systems: mean $\pm$ s.d.\ over eight seeds; JPlag is deterministic (single run, no dispersion, no $\pm$). "
         r"Cross-language pairs receive score 0 from JPlag, which compares one language per run.}",
         r"\label{tab:comparison-models}", r"\footnotesize", r"\begin{tabular}{l|ccccc|ccccc}", r"\toprule",
         r" & \multicolumn{5}{c|}{Regime A: random independent negatives} & \multicolumn{5}{c}{Regime B: hard negatives} \\",
         r"\textbf{System} & Acc. & Prec. & Rec. & Spec. & $F_1$ & Acc. & Prec. & Rec. & Spec. & $F_1$ \\", r"\midrule"]
    for key, nm, sd in NAMES:
        row = [nm]
        for r in ("A", "B"):
            ev = RG[r]["ev"]["summary"]
            if key not in ev:
                row += ["--"] * 5
                continue
            m = ev[key]
            row += [cell(m, "acc"), cell(m, "precision"), cell(m, "recall"), cell(m, "specificity"), cell(m, "f1", sd)]
        L.append(" & ".join(row) + r" \\")
        if key in ("direct|val", "logreg|val"):
            pass
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    open(os.path.join(OUT, "tab_main.tex"), "w").write("\n".join(L))


SHORT = {"gate|val": "Gating network", "direct|val": "Direct classifier", "logreg|val": "Logistic regression", "static|val": "Static averaging", "codebert|val": "CodeBERT only", "ast|val": "AST only", "token|val": "Token only", "jplag|val": "JPlag", "tokennorm|val": "JPlag + norm.", "dolos|val": "Dolos"}


def slice_table():
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Detection rate (recall, \%) by derivation type and specificity on non-derived pairs at the validation-tuned "
         r"threshold; slice sizes $n$ (23, 102, 1{,}599, 928 and 3{,}000 test pairs) are those of Table~\ref{tab:protocol}. Mean over eight seeds for trained systems.}",
         r"\label{tab:clone-f1}", r"\scriptsize", r"\setlength{\tabcolsep}{3.5pt}", r"\begin{tabular}{l|ccccc|ccccc}", r"\toprule",
         r" & \multicolumn{5}{c|}{Regime A: random independent negatives} & \multicolumn{5}{c}{Regime B: hard negatives} \\",
         r"\textbf{System} & Exact & Renamed & Refact. & Cross-lang. & Spec. & Exact & Renamed & Refact. & Cross-lang. & Spec. \\",
         r"\midrule"]
    for key, nm, sd in NAMES:
        row = [SHORT[key]]
        for r in ("A", "B"):
            ev = RG[r]["ev"]["summary"]
            if key not in ev:
                row += ["--"] * 5
                continue
            s_ = ev[key]["slices"]
            row += [pct(s_[k][0]) for k in ("exact", "renamed", "refactored", "cross-language")] + [pct(s_["independent_specificity"][0])]
        L.append(" & ".join(row) + r" \\")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    open(os.path.join(OUT, "tab_slices.tex"), "w").write("\n".join(L))


def fmt_p(p):
    if p <= 0.0016:
        return "$<0.002$"
    if p < 1e-2:
        return "%.3f" % p
    return "%.2f" % p


def sg(x):
    return "0.0" if abs(x) < 0.05 else "%+.1f" % x


def ablation_table():
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Component ablation on the problem-grouped test partition, for both negative regimes. $\Delta F_1$ is the change "
         r"(points) relative to the full trained gate, averaged over eight seeds, with a 95\% cluster-bootstrap interval "
         r"(resampling base-problem groups, 20{,}000 resamples). $p$ is the two-sided bootstrap $p$ value of the seed-averaged $\Delta F_1$, Holm-adjusted across the "
         r"comparisons of that regime (floor $1.5\times10^{-3}$).}",
         r"\label{tab:ablation}", r"\footnotesize", r"\begin{tabular}{ll|ccc|ccc}", r"\toprule",
         r" & & \multicolumn{3}{c|}{Regime A} & \multicolumn{3}{c}{Regime B} \\",
         r"\textbf{Group} & \textbf{Configuration} & $\Delta F_1$ & 95\% CI & $p_{\mathrm{Holm}}$ & $\Delta F_1$ & 95\% CI & $p_{\mathrm{Holm}}$ \\", r"\midrule"]
    ga, gb = RG["A"]["post"]["gate_f1"], RG["B"]["post"]["gate_f1"]
    L.append(r"--- & Full trained gate ($F_1$) & \multicolumn{3}{c|}{$%.1f\pm%.1f$} & \multicolumn{3}{c}{$%.1f\pm%.1f$} \\" % (ga[0], ga[1], gb[0], gb[1]))
    L.append(r"\midrule")
    last = None
    ra, rb = RG["A"]["post"]["ablation"], RG["B"]["post"]["ablation"]
    for a, b in zip(ra, rb):
        g = a["group"] if a["group"] != last else ""
        if a["group"] != last and last is not None:
            L.append(r"\midrule")
        last = a["group"]
        L.append("%s & %s & %s & [%s, %s] & %s & %s & [%s, %s] & %s \\\\" % (
            g, a["config"].replace("Eq. 12", "Eq.~"+chr(92)+"ref{eq:eq12}"), sg(a["delta"]), sg(a["ci"][0]), sg(a["ci"][1]), fmt_p(a["p_cluster_holm"]),
            sg(b["delta"]), sg(b["ci"][0]), sg(b["ci"][1]), fmt_p(b["p_cluster_holm"])))
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    open(os.path.join(OUT, "tab_ablation.tex"), "w").write("\n".join(L))


def protocol_table():
    pr = pd.read_csv(os.path.join(DATA, "pairs.csv"))
    st = json.load(open(os.path.join(DATA, "protocol_stats.json")))
    L = [r"\begin{table}[t]", r"\centering",
         r"\caption{Problem-grouped evaluation protocol. A \emph{group} is a connected component of snippets linked by any "
         r"GPTCloneBench pair; each group lies in exactly one split. Regimes B (nearest-neighbor mining with the expert scores) and C (mining by identifier overlap) replace the independent negatives (regime A) by an equal "
         r"number of mined independent pairs.}",
         r"\label{tab:protocol}", r"\footnotesize", r"\begin{tabular}{lrrr}", r"\toprule",
         r"\textbf{Pair type} & \textbf{Train} & \textbf{Val.} & \textbf{Test} \\", r"\midrule"]

    def n(sp, sl):
        return int(((pr.split == sp) & (pr.slice == sl)).sum())
    rows = [("Exact", "exact"), ("Renamed", "renamed"), ("Refactored (MT3 + T4)", "refactored"),
            ("Same-language (train/val)", "same-language"), ("Cross-language", "cross-language"),
            ("Independent negatives", "independent"), ("Hard negatives (regime B)", "hard_independent"), ("Identifier-mined negatives (regime C)", "tfidf_independent")]
    for nm, sl in rows:
        L.append("%s & %s & %s & %s \\\\" % (nm, *[("{:,}".format(n(sp, sl)).replace(",", "{,}") if n(sp, sl) else "--") for sp in ("train", "val", "test")]))
    L.append(r"\midrule")
    g = st["distinct_groups_by_split"]
    L.append("Problem groups & %s & %s & %s \\\\" % (g["train"], g["val"], "{:,}".format(g["test"]).replace(",", "{,}")))
    cx = st["cross_language_problems_by_split"]
    L.append("Cross-language problems & %s & %s & %s \\\\" % (cx["train"], cx["val"], cx["test"]))
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    open(os.path.join(OUT, "tab_protocol.tex"), "w").write("\n".join(L))
    FACTS["protocol"] = st


def ops_table():
    L = [r"\begin{table}[t]", r"\centering",
         r"\caption{Operating points of the gating network chosen on the validation partition and applied unchanged to the test "
         r"partition (ensemble of eight seeds): the threshold that keeps the validation false-positive rate at or below the budget, "
         r"or the recall target on validation.}",
         r"\label{tab:operating-points}", r"\footnotesize", r"\begin{tabular}{llccc}", r"\toprule",
         r"\textbf{Regime} & \textbf{Target (validation)} & \textbf{Rec.} & \textbf{Prec.} & \textbf{FPR} \\", r"\midrule"]
    for r in ("A", "B"):
        ops = RG[r]["post"]["operating_points"]["gate"]
        for o in ops:
            tgt = ("FPR $\\leq$ %d\\%%" % round(100 * o["budget"])) if o["kind"] == "fpr_budget_val" else ("recall $=$ %d\\%%" % round(100 * o["budget"]))
            L.append("%s & %s & %s & %s & %s \\\\" % (r, tgt, pct(o["recall"]), pct(o["precision"]), pct(o["fpr"])))
        if r == "A":
            L.append(r"\midrule")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    open(os.path.join(OUT, "tab_ops.tex"), "w").write("\n".join(L))


def probe_table():
    L = [r"\begin{table}[t]", r"\centering",
         r"\caption{Zero-shot cross-generator probe on 292 held-out problems: Java seed paired with its benchmark translation "
         r"(training generator) or its GPT-4 translation (unseen generator). Thresholds are frozen on the GPT-3 validation partition. "
         r"Recall over 876 derived pairs per generator; FPR over 876 independent cross-language pairs per generator.}",
         r"\label{tab:probe}", r"\small", r"\begin{tabular}{llcccc}", r"\toprule",
         r" & & \multicolumn{2}{c}{Recall} & \multicolumn{2}{c}{FPR} \\",
         r"\textbf{Regime} & \textbf{System} & GPT-3 & GPT-4 & GPT-3 & GPT-4 \\", r"\midrule"]
    for r in ("A", "B"):
        pr = RG[r]["probe"]
        if pr is None:
            continue
        for k, nm in (("gate", "Gating network"), ("direct", "Direct classifier"), ("static", "Static averaging"),
                      ("codebert", "CodeBERT only"), ("token", "Token only")):
            L.append("%s & %s & %s & %s & %s & %s \\\\" % (r, nm, pct(pr[k]["gpt3"]["recall"][0]), pct(pr[k]["gpt4"]["recall"][0]),
                                                           pct(pr[k]["gpt3"]["fpr"][0]), pct(pr[k]["gpt4"]["fpr"][0])))
        if r == "A":
            L.append(r"\midrule")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    open(os.path.join(OUT, "tab_probe.tex"), "w").write("\n".join(L))


def diag_table():
    """Five representative test pairs: the pair of each category whose S_CodeBERT is closest to the category median."""
    r = RG["B"]
    te = r["D"]["test"]
    W = r["S"]["test__gate_w"][0]
    FUS = r["S"]["test__gate"][0]          # stored fused score of seed 0 (weighted mean, or log-odds fusion when LO)
    cats = [("Exact", te.slice == "exact"), ("Renamed", te.slice == "renamed"), ("Refactored", te.slice == "refactored"),
            ("Cross-language", te.slice == "cross-language"), ("Hard negative", te.slice == "hard_independent")]
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Five representative test pairs (regime B gate, seed 0): in each category the pair whose $S_{\text{sem}}$ is closest "
         r"to the category median. The gate column is the fused score (" + (r"log-odds fusion, Eq.~\ref{eq:logit}" if LO else r"$\sum_i w_i S_i$") + r"); the static column is the unweighted mean of the three scores.}",
         r"\label{tab:diagnostic-cases}", r"\footnotesize", r"\begin{tabular}{lcccccccccl}", r"\toprule",
         r"\textbf{Category} & $S_{\text{sem}}$ & $S_{\text{str}}$ & $S_{\text{syn}}$ & $D_{\text{lang}}$ & $w_{\text{sem}}$ & $w_{\text{str}}$ & $w_{\text{syn}}$ & Gate / Static & Outcome \\", r"\midrule"]
    thr = r["ev"]["thresholds"]["gate|val"][0]
    diag = []
    for nm, m in cats:
        idx = np.where(m.values)[0]
        med = np.median(te.S_CodeBERT.values[idx])
        i = idx[np.argmin(np.abs(te.S_CodeBERT.values[idx] - med))]
        S3 = te.loc[i, ["S_CodeBERT", "S_AST", "S_Token"]].values.astype(float)
        w = W[i]
        fus = float(FUS[i])
        stat = float(S3.mean())
        flag = fus >= thr
        outcome = ("Flagged" if flag else "Not flagged")
        diag.append(dict(cat=nm, S=S3.tolist(), D=int(te.D_lang[i]), w=w.tolist(), fused=fus, static=stat, flagged=bool(flag)))
        L.append("%s & %.3f & %.3f & %.3f & %d & %.3f & %.3f & %.3f & %.3f / %.3f & %s \\\\" % (nm, *S3, int(te.D_lang[i]), *w, fus, stat, outcome))
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    open(os.path.join(OUT, "tab_diag.tex"), "w").write("\n".join(L))
    FACTS["diag"] = diag
    FACTS["diag_threshold"] = thr
    # extreme hard negative for Proposition 2
    j = int(np.argmax(np.where(te.slice.values == "hard_independent", te.S_CodeBERT.values, -1)))
    FACTS["prop2_negative"] = dict(S=te.loc[j, ["S_CodeBERT", "S_AST", "S_Token"]].astype(float).tolist())
    hn = te[te.slice == "hard_independent"]
    FACTS["hard_neg_semantic_quantiles"] = {q: float(np.quantile(hn.S_CodeBERT, q)) for q in (0.5, 0.9, 0.99)}
    FACTS["frac_hardneg_sem_ge_099"] = float((hn.S_CodeBERT >= 0.99).mean())
    FACTS["frac_hardneg_sem_ge_095"] = float((hn.S_CodeBERT >= 0.95).mean())


def same_language_subset():
    """Metrics restricted to same-language test pairs (JPlag is applicable there)."""
    L = [r"\begin{table}[t]", r"\centering",
         r"\caption{Same-language test pairs only (the only pairs on which JPlag and Dolos can operate): $F_1$ and false-positive rate at the "
         r"validation-tuned thresholds (trained systems: mean over eight seeds).}",
         r"\label{tab:same-language}", r"\footnotesize", r"\begin{tabular}{l|cc|cc}", r"\toprule",
         r" & \multicolumn{2}{c|}{Regime A} & \multicolumn{2}{c}{Regime B} \\", r"\textbf{System} & $F_1$ & FPR & $F_1$ & FPR \\", r"\midrule"]
    out = {}
    for key, nm, sd in NAMES:
        row = [nm]
        for r in ("A", "B"):
            te = RG[r]["D"]["test"]
            if key not in RG[r]["P"].files:
                row += ["--", "--"]
                continue
            m = (te.D_lang.values == 0)
            y = te.label.values[m]
            f1s, fps = [], []
            for p in RG[r]["P"][key]:
                pp = p[m].astype(int)
                tp = ((y == 1) & (pp == 1)).sum(); fp = ((y == 0) & (pp == 1)).sum(); fn = ((y == 1) & (pp == 0)).sum()
                f1s.append(2 * tp / max(2 * tp + fp + fn, 1)); fps.append(fp / max((y == 0).sum(), 1))
            row += [pct(np.mean(f1s)), pct(np.mean(fps))]
            out["%s|%s" % (r, key)] = [float(np.mean(f1s)), float(np.mean(fps))]
        L.append(" & ".join(row) + r" \\")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    open(os.path.join(OUT, "tab_same_language.tex"), "w").write("\n".join(L))
    FACTS["same_language"] = out


def sens_table():
    L = [r"\begin{table}[t]", r"\centering",
         r"\caption{Sensitivity of the adaptive threshold (Eq.~\ref{eq:eq12}) to its constants, gate, mean of eight seeds: "
         r"$k_{\mathrm{simple}}\in\{1.2,1.5,1.8,2.1\}$ with $k_{\mathrm{complex}}=k_{\mathrm{simple}}-0.6$, complexity cut "
         r"$CC\le\{3,5,8,10\}$, clamp $\in\{[0.40,0.80],[0.30,0.90],[0.50,0.70]\}$ (48 settings). The reported setting is $k=1.8/1.2$, $CC\le5$, $[0.40,0.80]$.}",
         r"\label{tab:sensitivity}", r"\footnotesize", r"\setlength{\tabcolsep}{3pt}", r"\begin{tabular}{lcccc}", r"\toprule",
         r"\textbf{Regime / setting} & Acc. & $F_1$ & Rec. & FPR \\", r"\midrule"]
    for r in ("A", "B"):
        g = RG[r]["post"]["sensitivity"]
        rep = [x for x in g if x["k_simple"] == 1.8 and x["cc_cut"] == 5 and x["clamp"] == [0.4, 0.8]][0]
        L.append("%s: reported & %s & %s & %s & %s \\\\" % (r, pct(rep["acc"]), pct(rep["f1"]), pct(rep["recall"]), pct(rep["fpr"])))
        for k in ("acc", "f1", "recall", "fpr"):
            pass
        rng = RG[r]["post"]["sensitivity_range"]
        L.append("%s: grid range & %s--%s & %s--%s & %s--%s & %s--%s \\\\" % (
            r, pct(rng["acc"][0]), pct(rng["acc"][1]), pct(rng["f1"][0]), pct(rng["f1"][1]),
            pct(rng["recall"][0]), pct(rng["recall"][1]), pct(rng["fpr"][0]), pct(rng["fpr"][1])))
        if r == "A":
            L.append(r"\midrule")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    open(os.path.join(OUT, "tab_sens.tex"), "w").write("\n".join(L))


def probe_table():
    GEN = [("gpt3", "GPTCloneBench (training generator)"), ("claude-sonnet-5-5", "claude-sonnet-5-5"),
           ("claude-sonnet-4-6", "claude-sonnet-4-6"), ("gpt-6-sol", "gpt-6-sol"), ("gpt-5.4-mini", "gpt-5.4-mini")]
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Zero-shot generator probe on held-out seeds. Translation: Java seed paired with its translation into Python, C or C\# "
         r"(about 150 problems per generator; the GPTCloneBench row uses the benchmark's own translations of the same seeds). Refactoring: a "
         r"seed of any of the four languages paired with a functionally equivalent but structurally different same-language rewrite "
         r"(150 seeds per generator; none for GPTCloneBench). Negatives pair a seed with the output for a different seed. Gate, features and "
         r"thresholds are frozen on the GPTCloneBench training and validation partitions. Recall and FPR in \%, mean over eight seeds; "
         r"the token-expert columns are identical in both regimes because that expert has no trained component; the GPTCloneBench row has no refactoring seeds.}",
         r"\label{tab:probe}", r"\scriptsize", r"\setlength{\tabcolsep}{3.5pt}", r"\begin{tabular}{ll|cc|cc|cc|cc}", r"\toprule",
         r" & & \multicolumn{4}{c|}{Gating network} & \multicolumn{4}{c}{Token expert only} \\",
         r"\textbf{Regime} & \textbf{Generator} & \multicolumn{2}{c}{Translation} & \multicolumn{2}{c|}{Refactoring} & \multicolumn{2}{c}{Translation} & \multicolumn{2}{c}{Refactoring} \\",
         r" & & Rec. & FPR & Rec. & FPR & Rec. & FPR & Rec. & FPR \\", r"\midrule"]
    for r in ("A", "B"):
        pr = RG[r]["probe"]
        for gk, gn in GEN:
            row = [r if gk == "gpt3" else "", gn]
            for sysn in ("gate", "token"):
                for kind in ("translate", "refactor"):
                    d = pr[sysn].get("%s|%s" % (gk, kind))
                    row += [pct(d["recall"][0]), pct(d["fpr"][0])] if d else ["--", "--"]
            L.append(" & ".join(row) + r" \\")
        if r == "A":
            L.append(r"\midrule")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    open(os.path.join(OUT, "tab_probe.tex"), "w").write("\n".join(L))


RG["C"] = load_regime("C")


def regimec_table():
    ev = RG["C"]["ev"]["summary"]
    L = [r"\begin{table}[t]", r"\centering",
         r"\caption{Regime C: hard negatives mined only by the TF-IDF cosine of identifier vocabularies (no expert score used in the mining), "
         r"same test partition, validation-tuned thresholds, mean over eight seeds. A reading audit of 50 random regime-C test negatives "
         r"rated 8 as the same task and 5 as unsure, so the specificity here is a lower bound.}",
         r"\label{tab:regime-c}", r"\footnotesize", r"\setlength{\tabcolsep}{4pt}", r"\begin{tabular}{lccccc}", r"\toprule",
         r"\textbf{System} & Acc. & Prec. & Rec. & Spec. & $F_1$ \\", r"\midrule"]
    for key, nm, sd in NAMES:
        if key not in ev:
            continue
        m = ev[key]
        L.append(" & ".join([SHORT[key], cell(m, "acc"), cell(m, "precision"), cell(m, "recall"), cell(m, "specificity"), cell(m, "f1", sd)]) + r" \\")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    open(os.path.join(OUT, "tab_regime_c.tex"), "w").write("\n".join(L))
    FACTS["regime_c_auc"] = RG["C"]["post"]["auc"]


def splitvar_table():
    L = [r"\begin{table}[t]", r"\centering",
         r"\caption{Sensitivity to the train/validation group assignment: five assignments of the non-test groups (draw 0 is the one used throughout; "
         r"negatives are regenerated inside each side), three seeds each, evaluated on the fixed test partition with validation-tuned thresholds. "
         r"$\Delta$ is direct classifier minus gate ($F_1$, points).}",
         r"\label{tab:split-variance}", r"\footnotesize", r"\setlength{\tabcolsep}{2.5pt}", r"\begin{tabular}{llccccc}", r"\toprule",
         r"\textbf{Reg.} & & Gate $F_1$ & Dir. $F_1$ & $\Delta$ & Cross-lang. rec. & FPR \\", r"\midrule"]
    for r in ("A", "B"):
        fp = os.path.join(HERE, "results_" + r + SUF, "split_variance.json")
        if not os.path.exists(fp):
            continue
        sv = json.load(open(fp))
        for d, v in sv["per_draw"].items():
            L.append("%s & draw %s & %.1f & %.1f & %+.1f & %.1f & %.1f \\\\" % (r if d == "0" else "", d, v["gate_f1"], v["direct_f1"], v["delta_direct_minus_gate"], v["gate_xl_recall"], v["gate_fpr"]))
        o = sv
        dv = [v["direct_f1"] for v in sv["per_draw"].values()]; dmean = sum(dv) / len(dv); dsd = (sum((x - dmean) ** 2 for x in dv) / (len(dv) - 1)) ** 0.5
        L.append(r"\multicolumn{2}{l}{\emph{mean $\pm$ s.d.}} & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%+.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ \\" % (
            o["gate_f1_over_draws"]["mean"], o["gate_f1_over_draws"]["sd"], dmean, dsd, o["delta_direct_minus_gate_over_draws"]["mean"], o["delta_direct_minus_gate_over_draws"]["sd"],
            o["gate_xl_recall_over_draws"]["mean"], o["gate_xl_recall_over_draws"]["sd"], o["gate_fpr_over_draws"]["mean"], o["gate_fpr_over_draws"]["sd"]))
        if r == "A":
            L.append(r"\midrule")
        FACTS["splitvar_" + r] = {k: v for k, v in sv.items() if k.endswith("draws")}
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    open(os.path.join(OUT, "tab_splitvar.tex"), "w").write("\n".join(L))


def baselines_table():
    NM = [("gate|val", "Gating network"), ("direct|val", "Direct classifier"), ("token|val", "Token only"),
          ("unixcoder_cos", "UniXcoder cosine (zero-shot)"), ("codebert_siamese", "CodeBERT siamese head (frozen)"),
          ("unixcoder_siamese", "UniXcoder siamese head (frozen)")]
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Embedding baselines on the same test partition and validation-tuned thresholds. Siamese heads are MLPs over $[|e_1-e_2|, e_1\odot e_2]$ "
         r"of frozen encoder embeddings trained on the training split (eight seeds); no encoder is fine-tuned. The first three rows repeat Table~\ref{tab:comparison-models}.}",
         r"\label{tab:embedding-baselines}", r"\footnotesize", r"\setlength{\tabcolsep}{3pt}", r"\begin{tabular}{l|ccc|ccc|ccc}", r"\toprule",
         r" & \multicolumn{3}{c|}{Regime A} & \multicolumn{3}{c|}{Regime B} & \multicolumn{3}{c}{Regime C} \\",
         r"\textbf{System} & $F_1$ & Rec. & Spec. & $F_1$ & Rec. & Spec. & $F_1$ & Rec. & Spec. \\", r"\midrule"]
    for key, nm in NM:
        row = [nm]
        for r in ("A", "B", "C"):
            if key.endswith("|val"):
                m = RG[r]["ev"]["summary"][key]
            else:
                fp_ = os.path.join(HERE, "results_" + r, "embedding_baselines.json")
                m = json.load(open(fp_))[key] if os.path.exists(fp_) else None
            row += [pct(m["f1"][0]), pct(m["recall"][0]), pct(m["specificity"][0])] if m else ["--"] * 3
        L.append(" & ".join(row) + r" \\")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    open(os.path.join(OUT, "tab_embedding_baselines.tex"), "w").write("\n".join(L))


def external_table():
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{External checks at the thresholds fixed on the benchmark validation partition (no retuning). PROGpedia: real student programs (whole files, "
         r"no boilerplate stripping); \emph{same-author} pairs are two attempts by one submitter on one assignment (derived by the same person), \emph{cross-author} "
         r"pairs join different submitters (independent work plus an unknown amount of real copying, so their flag rate is an upper bound on false flags). "
         r"Convergence: same-named algorithmic functions by different authors inside the benchmark (same task, no derivation). "
         r"All: pooled over Java, Python and C; AUC separates same-author from cross-author pairs without a threshold. The token-only, JPlag and JPlag + norm. rows are identical in regimes A and B (no trained component) and are shown once. UniXcoder rows: UniXcoder expert (mean-fusion gate; the cosine alone is one score).}",
         r"\label{tab:external}", r"\scriptsize", r"\setlength{\tabcolsep}{3pt}", r"\begin{tabular}{ll|c|cccc|cccc|c}", r"\toprule",
         r" & & & \multicolumn{4}{c|}{Same-author recall} & \multicolumn{4}{c|}{Cross-author flag rate} & Convergence \\",
         r"\textbf{Regime} & \textbf{System} & AUC & All & Java & Python & C & All & Java & Python & C & flag rate \\", r"\midrule"]
    def ext_row(first, nm, ex, key):
        pg = ex[key]["progpedia"]
        row = [first, nm, "%.2f" % ex["auc_progpedia"][key]["all"]]
        row += [pct(pg[l]["recall_same_author"][0]) for l in ("all", "java", "python", "c")]
        row += [pct(pg[l]["flag_rate_cross_author"][0]) for l in ("all", "java", "python", "c")]
        row += [pct(ex[key]["convergence"]["flag_rate"][0])]
        return " & ".join(row) + r" \\"
    for r in ("A", "B"):
        fp_ = os.path.join(HERE, "results_" + r + SUF, "external.json")
        if not os.path.exists(fp_):
            continue
        ex = json.load(open(fp_))
        for key, nm in (("gate", "Gating network"), ("direct", "Direct classifier"), ("token", "Token only"), ("static", "Static averaging"),
                        ("jplag", "JPlag"), ("tokennorm", "JPlag + norm.")):
            if key not in ex:
                continue
            if not (r == "B" and key in ("token", "jplag", "tokennorm")):   # those rows are byte-identical to regime A (no trained component): stated once in the caption
                L.append(ext_row(r if key == "gate" else "", nm, ex, key))
            if LO and key == "tokennorm":   # mean-fusion gate of the same regime, from the released mean-fusion run (results_<R>/external.json)
                fm = os.path.join(HERE, "results_" + r, "external.json")
                if os.path.exists(fm):
                    L.append(ext_row("", "Gating network (mean fusion)", json.load(open(fm)), "gate"))
        if LO:   # UniXcoder-expert gate (and the UniXcoder cosine in regime A): results_<R>ux/external.json, mean-fusion gate
            fu = os.path.join(HERE, "results_" + r + "ux", "external.json")
            if os.path.exists(fu):
                eu = json.load(open(fu))
                if r == "A":
                    L.append(ext_row("", "UniXcoder cosine", eu, "codebert"))
                L.append(ext_row("", "Gating network, UniXcoder expert", eu, "gate"))
        if r == "A":
            L.append(r"\midrule")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    open(os.path.join(OUT, "tab_external.tex"), "w").write("\n".join(L))


for fn in (baselines_table, external_table, regimec_table,splitvar_table, main_table,slice_table, ablation_table, protocol_table, ops_table, probe_table, diag_table, same_language_subset, sens_table):
    try:
        fn()
        print("ok", fn.__name__)
    except Exception as e:
        import traceback
        traceback.print_exc()
for r in ("A", "B"):
    FACTS["thresholds_" + r] = RG[r]["post"]["thresholds"]
    FACTS["error_" + r] = RG[r]["post"]["error_analysis"]
    FACTS["weights_" + r] = RG[r]["post"]["mean_weights"]
    FACTS["train_" + r] = RG[r]["train"]
    FACTS["aux_" + r] = {k: RG[r]["ev"]["summary"][k].get("aux_flag_rate") for k in ("gate|val", "direct|val", "token|val", "static|val", "codebert|val", "jplag|val", "tokennorm|val") if k in RG[r]["ev"]["summary"]}
json.dump(FACTS, open(os.path.join(OUT, "facts.json"), "w"), indent=1)
