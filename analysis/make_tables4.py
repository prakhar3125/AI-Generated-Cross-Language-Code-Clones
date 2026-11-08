# -*- coding: utf-8 -*-
"""Tables of the E1-E8 experiments (reads saved JSON only).
python -I make_tables4.py -> tables/tab_baselines.tex, tab_retrained.tex, tab_encoder.tex, tab_cohort_detail.tex, tab_probe_auc.tex, tab_operating_all.tex, tab_attack.tex, facts4.json"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LO = os.environ.get("LOGIT_TABLES") == "1"
SUF = "lo" if LO else ""
OUT = os.path.join(HERE, "tables_lo" if LO else "tables")
os.makedirs(OUT, exist_ok=True)
FACTS = {}


def J(p):
    q = os.path.join(HERE, p)
    return json.load(open(q)) if os.path.exists(q) else None


def FILL(cap, ws=None):
    for w in ws or []:
        cap = cap.replace('%.2f', '%.2f' % w, 1)
    return cap


def v(x):
    return x[0] if isinstance(x, list) else x


def p1(x):
    return "%.1f" % (100 * v(x))


def wtex(name, lines):
    open(os.path.join(OUT, name), "w").write("\n".join(lines))


# ---------------------------------------------------------------- E1: fixed-weight and non-routing baselines
def baselines():
    E = {t: J("results_%s/e1_baselines.json" % (t + SUF if t in ("A", "B", "C") else t)) for t in ("A", "B", "C", "Aux", "Bux", "Cux", "Awh", "Bwh", "Cwh")}
    cb = ("A", "B", "C")
    ux = ("Aux", "Bux", "Cux")
    L = [r"\begin{table*}[t]", r"\centering",
         FILL(r"\caption{Fixed-weight and non-routing baselines on the three negative regimes (test partition; weights and thresholds chosen on the validation partition; "
         r"gradient-boosted trees and the trained models are means over eight seeds). Best convex weights: grid over the three-simplex in steps of 0.05, applied to the raw scores, to their logits "
         r"or to their $z$-scores (training statistics); the hand-coded rule scores same-language pairs by the token expert and cross-language pairs by the semantic expert with one threshold per language relation. "
         r"AUC: area under the ROC curve of the ensemble-mean score; R@1\% and R@5\%: recall at 1\% and 5\% false-positive rate read from the test ROC curve (an oracle operating point). "
         r"The block after the CodeBERT rows gives the raw expert cosine, AST statistics and the external tools (continuous similarities; cross-language pairs score zero for the tools); tuned rows: settings tried on the validation partition (recall at fixed false-positive rate not computed; the validation-selected Dolos setting in regime A is the default). "
         r"With the CodeBERT expert the selected convex weights are $(0.20,0,0.80)$, $(0,0,1)$ and $(0.05,0,0.95)$ in regimes A, B and C, that is the token expert alone or almost alone; with the UniXcoder expert they are $(%.2f,0,%.2f)$, $(%.2f,0,%.2f)$ and $(%.2f,0,%.2f)$ for regimes A, B and C." + (" The gating network of the CodeBERT block is the log-odds gate; the UniXcoder and whitened gating networks were not rerun and use mean fusion." if LO else "") + "}", [x for t in ux for x in (E[t]["best_convex"]["weights"][0], E[t]["best_convex"]["weights"][2])]),
         r"\label{tab:baselines-fixed}", r"\scriptsize", r"\setlength{\tabcolsep}{2.6pt}", r"\begin{tabular}{l|cccc|cccc|cccc}", r"\toprule",
         r" & \multicolumn{4}{c|}{Regime A (random)} & \multicolumn{4}{c|}{Regime B (mined, expert scores)} & \multicolumn{4}{c}{Regime C (mined, identifiers)} \\",
         r"\textbf{System} & $F_1$ & AUC & R@1\% & R@5\% & $F_1$ & AUC & R@1\% & R@5\% & $F_1$ & AUC & R@1\% & R@5\% \\", r"\midrule",
         r"\multicolumn{13}{l}{\emph{CodeBERT expert}} \\"]
    rows = [("Static averaging (equal weights)", "static"), ("Best convex weights, raw scores", "best_convex"), ("Best convex weights, logits", "best_convex_logit"),
            ("Best convex weights, $z$-scores", "best_convex_z"), ("Hand-coded rule by language relation", "hand_rule"), ("Token $k$-gram only", "token"),
            ("Logistic regression", "logreg"), ("Gradient-boosted trees", "gbt"), ("Direct classifier (no routing)", "direct"), ("Gating network", "gate")]

    def line(lab, k, tags):
        c = [lab]
        for t in tags:
            m = E[t][k]
            c += [p1(m["f1"]), "%.3f" % v(m["auc"]), p1(m["r1"]), p1(m["r5"])]
        return " & ".join(c) + r" \\"
    for lab, k in rows:
        L.append(line(lab, k, cb))
    # rows that formerly lived in the separate ranking table (tab_operating_all): raw expert scores and the external tools, same columns; every value is read from
    # results_<R>[lo]/e1_baselines.json (experts) and e8_tools.json (tools) and repeats a cell of tab_main / tab_ux
    T8 = {t: J("results_%s/e8_tools.json" % (t + SUF)) for t in ("A", "B", "C")}
    if all(T8.values()):
        L.append(r"\midrule")
        for lab, k in (("CodeBERT cosine (first expert alone)", "codebert"), ("AST statistics (second expert alone)", "ast")):
            L.append(line(lab, k, cb))
        for lab, k in (("JPlag 6.3.0", "jplag"), ("JPlag + TokenNorm", "tokennorm"), ("Dolos 2.10.0", "dolos")):
            c = [lab]
            for t in cb:
                m = T8[t][k]
                c += [p1(m["f1"]), "%.3f" % v(m["auc"]), p1(m["r1"]), p1(m["r5"])]
            L.append(" & ".join(c) + r" \\")
        TU = {t: J("results_%s/e8_tuned.json" % t) for t in ("A", "B", "C")}
        if all(TU.values()):
            for lab, k in (("JPlag, min.\\ match 5 (tuned)", "jplag_t5"), ("Dolos, $k=35$, window 25 (tuned)", "dolos_k35_w25")):
                c = [lab]
                for t in cb:
                    m = TU[t][k]
                    c += [p1(m["test_f1"]), "%.3f" % v(m["test_auc"]), "--", "--"]
                L.append(" & ".join(c) + r" \\")
    L += [r"\midrule", r"\multicolumn{13}{l}{\emph{UniXcoder expert (regimes A, B, C)}} \\"]
    L.append(line("UniXcoder cosine (zero-shot)", "codebert", ux))
    for lab, k in (("Best convex weights, raw scores", "best_convex"), ("Hand-coded rule by language relation", "hand_rule"), ("Gradient-boosted trees", "gbt"),
                   ("Direct classifier (no routing)", "direct"), ("Gating network", "gate")):
        L.append(line(lab, k, ux))
    if all(E[t] for t in ("Awh", "Bwh", "Cwh")):
        L += [r"\midrule", r"\multicolumn{13}{l}{\emph{Whitened CodeBERT expert (embedding space whitened with training statistics; regimes A, B, C)}} \\"]
        for lab, k in (("Zero-shot cosine of the first expert", "codebert"), ("Best convex weights, raw scores", "best_convex"), ("Hand-coded rule by language relation", "hand_rule"),
                       ("Gradient-boosted trees", "gbt"), ("Direct classifier (no routing)", "direct"), ("Gating network", "gate")):
            L.append(line(lab, k, ("Awh", "Bwh", "Cwh")))
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    wtex("tab_baselines.tex", L)
    FACTS["e1"] = {t: {k: E[t][k] for k in ("best_convex", "hand_rule", "gbt", "gate", "direct", "token")} for t in E}


# ---------------------------------------------------------------- E2: ablation by retraining
def retrained():
    E = {t: J("results_%s/e2_retrained.json" % (t + SUF if t in ("A", "B", "C") else t)) for t in ("A", "B", "C", "Aux", "Bux", "Cux")}
    tags = ("A", "B", "C", "Aux", "Bux", "Cux")
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Ablation by retraining without an expert: its score, and every feature derived from it, is removed from the input and the model is retrained and re-tuned (eight seeds). "
         r"Cells: $\Delta F_1$ against the full model of the same type and regime in points, then (in parentheses) cross-language recall in \%; $^\dagger$: not significant (Holm-adjusted cluster bootstrap $p\ge0.05$). "
         r"The leave-one-out rows of Table~\ref{tab:ablation} leave the expert's score in the gate's input and are not comparable with these." + (" Gating networks: log-odds fusion in the CodeBERT block, mean fusion in the UniXcoder block (not rerun)." if LO else "") + r"}",
         r"\label{tab:ablation-retrained}", r"\scriptsize", r"\setlength{\tabcolsep}{3pt}", r"\begin{tabular}{ll|ccc|ccc}", r"\toprule",
         r" & & \multicolumn{3}{c|}{CodeBERT expert} & \multicolumn{3}{c}{UniXcoder expert} \\",
         r"\textbf{Model} & \textbf{Removed} & A & B & C & A & B & C \\", r"\midrule"]
    names = {"full": "none (reference $F_1$; XL rec.)", "wo_sem": "semantic expert", "wo_str": "structural expert", "wo_syn": "syntactic (token) expert"}
    for kind, kn in (("gate", "Gating network"), ("direct", "Direct classifier")):
        for var in ("full", "wo_sem", "wo_str", "wo_syn"):
            c = [kn if var == "full" else "", names[var]]
            for t in tags:
                e = E[t]["%s|%s" % (kind, var)]
                if var == "full":
                    c.append("%s (%s)" % (p1(e["f1"]), p1(e["slices"]["cross-language"])))
                else:
                    dag = "$^\\dagger$" if e["p_holm"] >= 0.05 else ""
                    c.append("%+.1f%s (%s)" % (e["delta_f1_vs_full"], dag, p1(e["slices"]["cross-language"])))
            L.append(" & ".join(c) + r" \\")
        if kind == "gate":
            L.append(r"\midrule")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    wtex("tab_retrained.tex", L)
    FACTS["e2"] = E


# ---------------------------------------------------------------- E3: encoder control
def encoder():
    E = {t: J("results_%s/e3_encoder.json" % t) for t in ("A", "B", "C")}
    if not all(E.values()):
        return
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Encoder control: zero-shot cosine $F_1$ (validation-tuned threshold, test partition) by encoder and pooling, and by embedding normalisation fitted on the training split only "
         r"(centre: subtract the mean training embedding; whiten: centre and ZCA-whiten). ``CodeBERT, 3 windows'' is the symmetric top-3 window cosine of the semantic expert; the ``paper'' column additionally centres each snippet's windows across its own windows, as the expert does. "
         r"The lower block gives the $F_1$ of a siamese head on the frozen, normalised first-512-token embeddings (three seeds). Last column: mean cosine of random independent test pairs in regime A, from none to whitened.}",
         r"\label{tab:encoder-control}", r"\footnotesize", r"\setlength{\tabcolsep}{3pt}", r"\begin{tabular}{l|cccc|ccc|ccc|c}", r"\toprule",
         r" & \multicolumn{4}{c|}{Regime A} & \multicolumn{3}{c|}{Regime B} & \multicolumn{3}{c|}{Regime C} & \\",
         r"\textbf{Encoder, pooling} & none & paper & centre & whiten & none & centre & whiten & none & centre & whiten & rand.\ cos. \\", r"\midrule"]
    rows = [("CodeBERT, first 512 tokens", "cb_first"), ("CodeBERT, 3 windows", "cb_top3"), ("UniXcoder, first 512 tokens", "ux_first")]
    for lab, enc in rows:
        c = [lab]
        for t, nl in (("A", ("none", "paper", "center", "whiten")), ("B", ("none", "center", "whiten")), ("C", ("none", "center", "whiten"))):
            for n in nl:
                k = "%s|%s" % (enc, n)
                c.append(p1(E[t][k]["cos_f1"]) if k in E[t] else "--")
        c.append("%.2f$\\to$%.2f" % (E["A"]["%s|none" % enc]["rand_cos"], E["A"]["%s|whiten" % enc]["rand_cos"]))
        L.append(" & ".join(c) + r" \\")
    L += [r"\midrule", r"\multicolumn{12}{l}{\emph{Siamese head on the frozen embeddings}} \\"]
    for lab, enc in (rows[0], rows[2]):
        c = [lab]
        for t, nl in (("A", ("none", "paper", "center", "whiten")), ("B", ("none", "center", "whiten")), ("C", ("none", "center", "whiten"))):
            for n in nl:
                k = "%s|%s" % (enc, n)
                c.append(p1(E[t][k]["siamese_f1"]) if k in E[t] and "siamese_f1" in E[t][k] else "--")
        c.append("")
        L.append(" & ".join(c) + r" \\")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    wtex("tab_encoder.tex", L)
    FACTS["e3"] = E


# ---------------------------------------------------------------- E6: per-assignment cohort detail
def cohort_detail():
    d = J("results_A/e6_cohort_detail.json")
    if not d:
        return
    names = {"Progpedia19": "PROGpedia 19", "Progpedia56": "PROGpedia 56"}
    cols = ["Gate (CodeBERT)", "Gate, boilerplate removed", "Token, boilerplate removed", "JPlag", "Dolos default", "Dolos -M 0.5"]
    L = [r"\begin{table}[t]", r"\centering",
         r"\caption{Mean cohort AUROC per assignment (PROGpedia) and per task (IR-Plag); $n$ is the number of cohorts. BP: assignment boilerplate removed without labels. The gate columns are the mean-fusion gate trained on regime A (per-group values of the log-odds gate were not computed).}",
         r"\label{tab:cohort-detail}", r"\footnotesize", r"\setlength{\tabcolsep}{2.5pt}", r"\begin{tabular}{lr|cccccc}", r"\toprule",
         r"\textbf{Group} & $n$ & Gate & Gate BP & Token BP & JPlag & Dolos & Dolos $-$M 0.5 \\", r"\midrule"]
    for g, x in d["per_group"].items():
        L.append(" & ".join([names.get(g, g.replace("IRPlag-case-", "IR-Plag T")), str(x["n_cohorts"])] + ["%.3f" % x[c] for c in cols]) + r" \\")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    wtex("tab_cohort_detail.tex", L)
    FACTS["e6"] = d


# ---------------------------------------------------------------- E7: probe AUROC and recall at fixed FPR
def probe_auc():
    A, U = J("results_A%s/e7_probe.json" % SUF), J("results_Aux/e7_probe.json")
    if not (A and U):
        return
    gens = [("gpt3", "GPTCloneBench"), ("claude-sonnet-5-5", "claude-sonnet-5-5"), ("claude-sonnet-4-6", "claude-sonnet-4-6"), ("gpt-6-sol", "gpt-6-sol"), ("gpt-5.4-mini", "gpt-5.4-mini")]
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Generator probe without a single operating point: AUROC (with 95\% cluster-bootstrap interval, resampling seed problems; rewrite pairs by seed snippet) and recall at 5\% FPR (R@5) taken from the probe's own negatives. "
         r"CB: CodeBERT expert (regime A); UX: UniXcoder expert (lower block of Table~\ref{tab:probe}); the token expert is the same in both. First expert: the first expert's cosine alone. "
         r"$\Delta$: AUROC of the benchmark's own translations minus that of the generator, with its interval (same seed problems resampled).}",
         r"\label{tab:probe-auc}", r"\scriptsize", r"\setlength{\tabcolsep}{2.2pt}", r"\begin{tabular}{l|ccc|cc|cc|c|ccc|cc}", r"\toprule",
         r" & \multicolumn{3}{c|}{CB gate} & \multicolumn{2}{c|}{Token} & \multicolumn{2}{c|}{CB first expert} & & \multicolumn{3}{c|}{UX gate} & \multicolumn{2}{c}{UX first expert} \\",
         r"\textbf{Generator} & AUROC & 95\% CI & R@5 & AUROC & R@5 & AUROC & R@5 & $\Delta$ CB gate [CI] & AUROC & 95\% CI & R@5 & AUROC & R@5 \\", r"\midrule",
         r"\multicolumn{14}{l}{\emph{Translations}} \\"]

    def cells(S, sysn, g, kind, ci=False):
        k = "%s|%s|%s" % (sysn, g, kind)
        if k not in S:
            return ["--"] * (3 if ci else 2)
        e = S[k]
        return ["%.3f" % e["auc"]] + (["[%.3f,%.3f]" % tuple(e["auc_ci"])] if ci else []) + [p1(e["r5"])]
    for g, n in gens:
        d = A.get("gate|diff|%s" % g)
        dd = "%+.3f [%+.3f,%+.3f]" % (d["delta"], d["ci"][0], d["ci"][1]) if d else "--"
        L.append(" & ".join([n] + cells(A, "gate", g, "translate", True) + cells(A, "token", g, "translate") + cells(A, "first_expert", g, "translate") + [dd]
                            + cells(U, "gate", g, "translate", True) + cells(U, "first_expert", g, "translate")) + r" \\")
    L += [r"\midrule", r"\multicolumn{14}{l}{\emph{Same-language rewrites}} \\"]
    for g, n in gens[1:]:
        L.append(" & ".join([n] + cells(A, "gate", g, "refactor", True) + cells(A, "token", g, "refactor") + cells(A, "first_expert", g, "refactor") + [""]
                            + cells(U, "gate", g, "refactor", True) + cells(U, "first_expert", g, "refactor")) + r" \\")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    wtex("tab_probe_auc.tex", L)
    FACTS["e7"] = {"A": A, "Aux": U}


# ---------------------------------------------------------------- E8: operating points of every system
def operating_all():
    E = {t: J("results_%s/e1_baselines.json" % (t + SUF)) for t in ("A", "B", "C")}
    EU = {t: J("results_%sux/e1_baselines.json" % t) for t in ("A", "B", "C")}
    T = {t: J("results_%s/e8_tools.json" % (t + SUF)) for t in ("A", "B", "C")}
    if not all(T.values()):
        return
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Ranking quality of every system on the three negative regimes: AUROC and recall at 1\% and 5\% false-positive rate (R@1\%, R@5\%; read from the test ROC curve). "
         r"JPlag, JPlag with TokenNorm and Dolos enter with their continuous similarities, and cross-language pairs score zero for them (they cannot compare programs of different languages). "
         r"The UniXcoder rows replace the CodeBERT cosine of the first expert by the UniXcoder cosine." + (" The gating-network row of the CodeBERT block uses log-odds fusion; the UniXcoder gates use mean fusion (Table~\ref{tab:baselines-fixed} gives the UniXcoder and whitened gating networks)." if LO else "") + r"}",
         r"\label{tab:operating-all}", r"\footnotesize", r"\setlength{\tabcolsep}{3pt}", r"\begin{tabular}{l|ccc|ccc|ccc}", r"\toprule",
         r" & \multicolumn{3}{c|}{Regime A} & \multicolumn{3}{c|}{Regime B} & \multicolumn{3}{c}{Regime C} \\",
         r"\textbf{System} & AUC & R@1\% & R@5\% & AUC & R@1\% & R@5\% & AUC & R@1\% & R@5\% \\", r"\midrule"]

    def row(lab, getter):
        c = [lab]
        for t in "ABC":
            m = getter(t)
            c += ["%.3f" % v(m["auc"]), p1(m["r1"]), p1(m["r5"])]
        L.append(" & ".join(c) + r" \\")
    for lab, k in (("Static averaging", "static"), ("CodeBERT cosine", "codebert"), ("AST statistics", "ast"), ("Token $k$-gram", "token"), ("Logistic regression", "logreg"),
                   ("Gating network", "gate"), ("Direct classifier", "direct"), ("Gradient-boosted trees", "gbt")):
        row(lab, lambda t, k=k: E[t][k])
    L.append(r"\midrule")
    for lab, k in (("UniXcoder cosine", "codebert"), ("Gating network, UniXcoder expert", "gate"), ("Direct classifier, UniXcoder expert", "direct"), ("Gradient-boosted trees, UniXcoder expert", "gbt")):
        row(lab, lambda t, k=k: EU[t][k])
    L.append(r"\midrule")
    for lab, k in (("JPlag 6.3.0", "jplag"), ("JPlag + TokenNorm", "tokennorm"), ("Dolos 2.10.0", "dolos")):
        row(lab, lambda t, k=k: T[t][k])
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    wtex("tab_operating_all.tex", L)
    FACTS["e8"] = {"tools": T}


# ---------------------------------------------------------------- E4: lexical attack A1
def attack():
    R = {t: J("results_%s/e4_attack.json" % (t + SUF if t in ("A", "B") else t)) for t in ("A", "B", "Aux", "Bux")}
    if not all(R.values()):
        return
    import numpy as np
    import pandas as pd
    from sklearn.metrics import roc_auc_score
    pairs = pd.read_csv(os.path.join(HERE, "data", "e4_pairs.csv"))
    ts = pd.read_csv(os.path.join(HERE, "data", "e4_tool_scores.csv"))
    thr = J("results_A/main_eval.json")["thresholds"]
    TOOL = {}
    for t, neg in (("A", "negA"), ("B", "negB")):
        sub = pairs[pairs.kind.isin(["pos", neg])]
        y = sub.label.values
        TOOL[t] = {}
        for sysn, key in (("jplag", "jplag|val"), ("tokennorm", "tokennorm|val"), ("dolos", "dolos|val")):
            TOOL[t][sysn] = {}
            for var in ("orig", "attacked"):
                m = ts[(ts.system == sysn) & (ts.variant == var)].drop_duplicates("pair_id").set_index("pair_id").sim
                if sysn == "tokennorm":  # TokenNorm exists for Java/C only; elsewhere the plain JPlag similarity is used (as in the main evaluation)
                    mj = ts[(ts.system == "jplag") & (ts.variant == var)].drop_duplicates("pair_id").set_index("pair_id").sim
                    sc = sub.pair_id.map(m).fillna(sub.pair_id.map(mj)).fillna(0.0).values
                else:
                    sc = sub.pair_id.map(m).fillna(0.0).values
                th = max(thr[key][0], 1e-9)
                TOOL[t][sysn][var] = dict(recall=float((sc[y == 1] >= th).mean()), fpr=float((sc[y == 0] >= th).mean()), auc=float(roc_auc_score(y, sc)))
    FACTS["e4_tools"] = TOOL
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Attack A1 on same-language pairs: every identifier declared in the second snippet is renamed to $v_0,v_1,\dots$ and string literals are masked, for positives (refactored test pairs) and negatives alike "
         r"(300 positives and 300 negatives of regime A or B; no execution check). Recall and FPR at the frozen validation threshold, AUROC on the pair set; original / attacked. "
         r"Gate and first expert use the CodeBERT expert (regimes A, B) or the UniXcoder expert (UX).}",
         r"\label{tab:attack}", r"\scriptsize", r"\setlength{\tabcolsep}{3pt}", r"\begin{tabular}{ll|cc|cc|cc}", r"\toprule",
         r"\textbf{Regime} & \textbf{System} & \multicolumn{2}{c|}{Recall} & \multicolumn{2}{c|}{FPR} & \multicolumn{2}{c}{AUROC} \\",
         r" & & orig. & attack & orig. & attack & orig. & attack \\", r"\midrule"]
    for t, lab in (("A", "A"), ("B", "B"), ("Aux", "A, UX"), ("Bux", "B, UX")):
        for k, nm in (("gate", "Gating network"), ("direct", "Direct classifier"), ("first_expert", "First expert alone"), ("token", "Token expert")):
            e = R[t][k]
            L.append(" & ".join([lab if k == "gate" else "", nm, p1(e["orig"]["recall"]), p1(e["attacked"]["recall"]), p1(e["orig"]["fpr"]), p1(e["attacked"]["fpr"]),
                                 "%.3f" % e["orig"]["auc"], "%.3f" % e["attacked"]["auc"]]) + r" \\")
        if LO and t in ("A", "B"):   # mean-fusion gate of the same regime, from the released mean-fusion attack run (results_<R>/e4_attack.json)
            e = J("results_%s/e4_attack.json" % t)["gate"]
            L.append(" & ".join(["", "Gating network (mean fusion)", p1(e["orig"]["recall"]), p1(e["attacked"]["recall"]), p1(e["orig"]["fpr"]), p1(e["attacked"]["fpr"]),
                                 "%.3f" % e["orig"]["auc"], "%.3f" % e["attacked"]["auc"]]) + r" \\")
        if t in ("A", "B"):
            for sysn, nm in (("jplag", "JPlag"), ("tokennorm", "JPlag + TokenNorm"), ("dolos", "Dolos")):
                e = TOOL[t][sysn]
                L.append(" & ".join(["", nm, p1(e["orig"]["recall"]), p1(e["attacked"]["recall"]), p1(e["orig"]["fpr"]), p1(e["attacked"]["fpr"]),
                                     "%.3f" % e["orig"]["auc"], "%.3f" % e["attacked"]["auc"]]) + r" \\")
        L.append(r"\midrule" if t != "Bux" else "")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    wtex("tab_attack.tex", L)
    FACTS["e4"] = R


for fn in (baselines, retrained, encoder, cohort_detail, probe_auc, operating_all, attack):
    try:
        fn()
        print("ok", fn.__name__)
    except Exception as ex:  # a missing experiment must not stop the others
        print("SKIP", fn.__name__, repr(ex))
json.dump(FACTS, open(os.path.join(OUT, "facts4.json"), "w"), indent=1, default=float)
