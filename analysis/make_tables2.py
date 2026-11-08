# -*- coding: utf-8 -*-
"""Tables for the stronger-encoder variant and the external checks (reads saved JSON only).

python -I make_tables2.py   -> tables/tab_ux.tex, tables/tab_external.tex, tables/facts2.json
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LO = os.environ.get("LOGIT_TABLES") == "1"
SUF = "lo" if LO else ""
OUT = os.path.join(HERE, "tables_lo" if LO else "tables")
os.makedirs(OUT, exist_ok=True)
FACTS = {}


def J(path):
    p = os.path.join(HERE, path)
    return json.load(open(p)) if os.path.exists(p) else None


def pct(x, d=1):
    return ("%." + str(d) + "f") % (100 * x)


def cell(m, k, sd=False):
    s = pct(m[k][0])
    if sd and m[k][1] > 0:
        s += r"\,{\scriptsize$\pm$%s}" % pct(m[k][1])
    return s


def ux_table():
    ev = {r: J("results_%s/main_eval.json" % (r + SUF))["summary"] for r in ("A", "B", "C")}
    ux = {r: J("results_%sux/main_eval.json" % r)["summary"] for r in ("A", "B", "C")}
    eb = {r: J("results_%s/embedding_baselines.json" % r) for r in ("A", "B", "C")}
    rows = [
        ("UniXcoder cosine, zero-shot", lambda r: ux[r]["codebert|val"], False),
        ("UniXcoder siamese head (frozen)", lambda r: eb[r]["unixcoder_siamese"], False),
        ("Gating network, UniXcoder expert", lambda r: ux[r]["gate|val"], True),
        ("Direct classifier, UniXcoder expert", lambda r: ux[r]["direct|val"], True),
        ("Static averaging, UniXcoder expert", lambda r: ux[r]["static|val"], False),
        ("Gating network, CodeBERT expert", lambda r: ev[r]["gate|val"], True),
        ("CodeBERT siamese head (frozen)", lambda r: eb[r]["codebert_siamese"], False),
        ("Token $k$-gram only", lambda r: ev[r]["token|val"], False),
        ("JPlag 6.3.0", lambda r: ev[r]["jplag|val"], False),
        ("Dolos 2.10.0", lambda r: ev[r]["dolos|val"], False),
    ]
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Effect of the semantic encoder on the three negative regimes (test partition, validation-tuned thresholds; eight seeds for trained systems). "
         r"``UniXcoder expert'' replaces the CodeBERT cosine of the first expert by the cosine of mean-pooled UniXcoder embeddings (first 512 tokens), "
         r"everything else unchanged. Siamese heads are MLPs over $[|e_1-e_2|, e_1\odot e_2]$ of frozen embeddings." + (" The CodeBERT gating network uses log-odds fusion; the UniXcoder gating network was not rerun and uses mean fusion." if LO else "") + r"}",
         r"\label{tab:ux}", r"\scriptsize", r"\setlength{\tabcolsep}{3pt}", r"\begin{tabular}{l|ccc|ccc|ccc}", r"\toprule",
         r" & \multicolumn{3}{c|}{Regime A (random)} & \multicolumn{3}{c|}{Regime B (mined, expert scores)} & \multicolumn{3}{c}{Regime C (mined, identifiers)} \\",
         r"\textbf{System} & $F_1$ & Rec. & Spec. & $F_1$ & Rec. & Spec. & $F_1$ & Rec. & Spec. \\", r"\midrule"]
    for nm, fn, sd in rows:
        row = [nm]
        for r in ("A", "B", "C"):
            m = fn(r)
            row += [cell(m, "f1", sd), cell(m, "recall"), cell(m, "specificity")]
        L.append(" & ".join(row) + r" \\")
        if nm.startswith("Static"):
            L.append(r"\midrule")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    open(os.path.join(OUT, "tab_ux.tex"), "w").write("\n".join(L))
    # facts: significance of gate vs UniXcoder alone / direct (UX variants)
    f = {}
    for r in ("A", "B", "C"):
        q = J("results_%sux/post_analysis.json" % r)
        d = {a["config"]: a for a in q["ablation"]}
        f[r] = {k: dict(delta=d[k]["delta"], ci=d[k]["ci"], p_holm=d[k]["p_boot_holm"]) for k in
                ("Semantic (CodeBERT) alone", "Syntactic (Token) alone", "Equal weights (static averaging)", "Direct classifier (no routing)",
                 "without semantic expert", "without syntactic expert", "without structural expert")}
        f[r]["auc"] = q["auc"]
        f[r]["gate_f1"] = q["gate_f1"]
    FACTS["ux_ablation"] = f


def external_table():
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{External checks at thresholds fixed on the benchmark validation partition (no retuning). PROGpedia: real student programs "
         r"(whole files, no boilerplate stripping); \emph{same-author} pairs are two attempts by one submitter on one assignment (derived by the same person), "
         r"\emph{cross-author} pairs join different submitters (independent work plus an unknown amount of real copying, so their flag rate bounds false flags from above). "
         r"AUC separates same-author from cross-author pairs with no threshold. Convergence: same-named algorithmic functions by different authors inside the benchmark "
         r"(same task, no derivation), flag rate of the 193 pairs.}",
         r"\label{tab:external}", r"\footnotesize", r"\setlength{\tabcolsep}{3pt}", r"\begin{tabular}{ll|cccccc|c}", r"\toprule",
         r" & & \multicolumn{6}{c|}{PROGpedia (13{,}351 same-author, 18{,}600 cross-author pairs)} & Conv. \\",
         r"\textbf{Reg.} & \textbf{System} & AUC & Recall & Flag all & Flag Java & Flag Py. & Flag C & flag \\", r"\midrule"]
    systems = [("A", "", "gate", "Gate, CodeBERT expert"), ("A", "", "token", "Token only"), ("A", "", "jplag", "JPlag"), ("A", "", "tokennorm", "JPlag + norm."),
               ("B", "", "gate", "Gate, CodeBERT expert"),
               ("A", "ux", "codebert", "UniXcoder cosine"), ("A", "ux", "gate", "Gate, UniXcoder expert"), ("B", "ux", "gate", "Gate, UniXcoder expert")]
    last = None
    for reg, tag, key, nm in systems:
        ex = J("results_%s%s/external.json" % (reg, tag if tag else SUF))
        if ex is None or key not in ex:
            continue
        pg = ex[key]["progpedia"]
        row = [reg if reg != last else "", nm, "%.2f" % ex["auc_progpedia"][key]["all"], pct(pg["all"]["recall_same_author"][0]), pct(pg["all"]["flag_rate_cross_author"][0])]
        row += [pct(pg[l]["flag_rate_cross_author"][0]) for l in ("java", "python", "c")]
        row += [pct(ex[key]["convergence"]["flag_rate"][0])]
        L.append(" & ".join(row) + r" \\")
        last = reg
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    open(os.path.join(OUT, "tab_external.tex"), "w").write("\n".join(L))


def probe_ux_table():
    GEN = [("gpt3", "GPTCloneBench (training generator)"), ("claude-sonnet-5-5", "claude-sonnet-5-5"), ("claude-sonnet-4-6", "claude-sonnet-4-6"),
           ("gpt-6-sol", "gpt-6-sol"), ("gpt-5.4-mini", "gpt-5.4-mini")]
    P = {r: J("results_%sux/probe2.json" % r) for r in ("A", "B")}
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Generator probe of Table~\ref{tab:probe} repeated with the UniXcoder expert (gate and expert trained on the benchmark, then frozen). "
         r"Recall and FPR in \%, mean over eight seeds for the gate; the UniXcoder-cosine columns are one deterministic score per pair, but its validation-tuned threshold is set per regime (0.525 in regime A, 0.535 in regime B), so its recall and FPR differ slightly between the regimes. The GPTCloneBench row has no refactoring seeds.}",
         r"\label{tab:probe-ux}", r"\footnotesize", r"\setlength{\tabcolsep}{3.5pt}", r"\begin{tabular}{ll|cc|cc|cc|cc}", r"\toprule",
         r" & & \multicolumn{4}{c|}{Gating network, UniXcoder expert} & \multicolumn{4}{c}{UniXcoder cosine only} \\",
         r"\textbf{Regime} & \textbf{Generator} & \multicolumn{2}{c}{Translation} & \multicolumn{2}{c|}{Refactoring} & \multicolumn{2}{c}{Translation} & \multicolumn{2}{c}{Refactoring} \\",
         r" & & Rec. & FPR & Rec. & FPR & Rec. & FPR & Rec. & FPR \\", r"\midrule"]
    for r in ("A", "B"):
        pr = P[r]
        if pr is None:
            continue
        for gk, gn in GEN:
            row = [r if gk == "gpt3" else "", gn]
            for sysn in ("gate", "unixcoder_cosine"):
                for kind in ("translate", "refactor"):
                    d = pr[sysn].get("%s|%s" % (gk, kind))
                    row += [pct(d["recall"][0]), pct(d["fpr"][0])] if d else ["--", "--"]
            L.append(" & ".join(row) + r" \\")
        if r == "A":
            L.append(r"\midrule")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    open(os.path.join(OUT, "tab_probe_ux.tex"), "w").write("\n".join(L))


ux_table()
external_table()
probe_ux_table()
json.dump(FACTS, open(os.path.join(OUT, "facts2.json"), "w"), indent=1)
print("ok")
