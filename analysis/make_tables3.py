# -*- coding: utf-8 -*-
"""Cohort tables and figure (reads saved cohort_eval.json only).
python -I make_tables3.py -> tables/tab_cohort.tex, tab_cohort_thr.tex, tab_cohort_diff.tex, fig_cohort.pdf, facts3.json
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tables")
E = {t: json.load(open(os.path.join(HERE, "results_%s/cohort_eval.json" % t)))["systems"] for t in ("A", "B", "C", "Aux", "Bux", "Cux")}
N = json.load(open(os.path.join(HERE, "results_A/cohort_eval.json")))["n_cohorts"]
DOL = json.load(open(os.path.join(HERE, "data", "dolos_cohort_runs.json")))
PP = ["insert", "refactor", "gptobf"]
IR = ["L1", "L2", "L3", "L4", "L5", "L6"]
FACTS = {"n_cohorts": N}

ROWS = [
    ("Gate, CodeBERT expert", "A", "gate|plain"),
    ("Gate, UniXcoder expert", "Aux", "gate|plain"),
    ("Token $k$-gram only", "A", "token|plain"),
    ("UniXcoder cosine", "Aux", "codebert|plain"),
    ("CodeBERT cosine", "A", "codebert|plain"),
    ("Static averaging", "A", "static|plain"),
    ("AST statistics only", "A", "ast|plain"),
    ("JPlag 6.3.0", "A", "jplag|plain"),
    ("JPlag + TokenNorm", "A", "tokennorm|plain"),
    ("Dolos 2.10.0, default", "D", "default"),
    None,
    ("Gate, CodeBERT expert", "A", "gate|filt"),
    ("Gate, UniXcoder expert", "Aux", "gate|filt"),
    ("Token $k$-gram only", "A", "token|filt"),
    ("UniXcoder cosine", "Aux", "codebert|filt"),
    ("CodeBERT cosine", "A", "codebert|filt"),
    ("Dolos 2.10.0, $-$M 0.5", "D", "m50"),
]


def g(tag, s, ds, kind=None, key="auc"):
    if tag == "D":
        x = DOL[s][ds]
        key = key.replace("_t", "")
        if kind is None:
            return x[key]
        return x["by_kind_" + key][kind]
    x = E[tag][s][ds]
    return x[key] if kind is None else x["by_kind"][kind][key]


def f3(x):
    return "%.3f" % x


def pct(x):
    return "%.0f" % (100 * x)


def auc_table():
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Cohort screening on real student programs: mean cohort AUROC (share of a cohort's non-derived pairs scored below its derived pair; 0.5 is chance, and below 0.5 the derived pair looks less similar than honest pairs) "
         r"by derivation type. PROGpedia: %d cohorts from two assignments (27 and 28 real Java submissions) with an insertion variant (dead statements), an automatically refactored variant and LLM rewrites of five submissions under 16 prompts each~\cite{b36}. "
         r"IR-Plag: %d cohorts from seven tasks (lecturer solution plus independent solutions) with plagiarized versions at levels L1 (comments, layout) to L6 (program logic)~\cite{b37}. "
         r"Models are those of the benchmark evaluation, unchanged. Lower block: assignment boilerplate removed without labels (token 5-grams present in more than half of a cohort's honest submissions dropped; cohort mean embedding subtracted). "
         r"Gate rows are the mean-fusion gate of the original proposal trained on regime A (the log-odds gate is in Table~\ref{tab:logit-real}); the UniXcoder rows use the UniXcoder expert. The UniXcoder gate routes almost all of its weight to the UniXcoder cosine on the unfiltered cohorts (semantic weight 0.99 for the derived pair and 0.94 for honest pairs on PROGpedia, 1.00 on IR-Plag; structural 0.00), so its unfiltered rows coincide with the cosine; with boilerplate removal part of the weight moves to the token expert (semantic 0.93 and 0.75 on PROGpedia, 0.83 and 0.78 on IR-Plag).}" % (N["PROGpedia"], N["IR-Plag"]),
         r"\label{tab:cohort}", r"\scriptsize", r"\setlength{\tabcolsep}{3.5pt}", r"\begin{tabular}{l|cccc|ccccccc}", r"\toprule",
         r" & \multicolumn{4}{c|}{PROGpedia} & \multicolumn{7}{c}{IR-Plag} \\",
         r"\textbf{System} & Insert & Refact. & LLM & All & L1 & L2 & L3 & L4 & L5 & L6 & All \\", r"\midrule"]
    for r in ROWS:
        if r is None:
            L.append(r"\midrule")
            L.append(r"\multicolumn{12}{l}{\emph{Boilerplate removed per cohort (label-free)}} \\")
            continue
        lab, tag, s = r
        vals = [g(tag, s, "PROGpedia", k) for k in PP] + [g(tag, s, "PROGpedia")] + [g(tag, s, "IR-Plag", k) for k in IR] + [g(tag, s, "IR-Plag")]
        L.append(" & ".join([lab] + [f3(v) for v in vals]) + r" \\")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    open(os.path.join(OUT, "tab_cohort.tex"), "w").write("\n".join(L))


def thr_table():
    L = [r"\begin{table}[t]", r"\centering",
         r"\caption{Flagging behaviour on the cohorts (mean over cohorts; seeds averaged for trained systems), in per cent. Det.: derived pair flagged; False: share of the cohort's non-derived pairs flagged. "
         r"``Transferred'' is the validation threshold of the benchmark; ``adaptive'' is the label-free rule of Eq.~\ref{eq:eq12} and its $k$ rule with $\mu,\sigma$ computed over all pairs of the cohort. bp.: assignment boilerplate.}",
         r"\label{tab:cohort-thr}", r"\footnotesize", r"\setlength{\tabcolsep}{3pt}", r"\begin{tabular}{ll|cc|cc}", r"\toprule",
         r" & & \multicolumn{2}{c|}{PROGpedia} & \multicolumn{2}{c}{IR-Plag} \\",
         r"\textbf{System} & \textbf{Rule} & Det. & False & Det. & False \\", r"\midrule"]

    def row(lab, rule, tag, s, sfx):
        v = [g(tag, s, ds, key=k + sfx) for ds in ("PROGpedia", "IR-Plag") for k in ("det", "ff")]
        L.append(" & ".join([lab, rule] + [pct(x) for x in v]) + r" \\")
    for lab, tag in (("Gate, CodeBERT expert", "A"), ("Gate, UniXcoder expert", "Aux")):
        row(lab, "transferred", tag, "gate|plain", "_t")
        row("", "adaptive", tag, "gate|plain", "_a")
        row("", "bp.\\ removed, transferred", tag, "gate|filt", "_t")
        row("", "bp.\\ removed, adaptive", tag, "gate|filt", "_a")
        L.append(r"\midrule")
    row("Token $k$-gram only", "transferred", "A", "token|plain", "_t")
    row("", "bp.\\ removed, transferred", "A", "token|filt", "_t")
    L.append(r"\midrule")
    row("JPlag 6.3.0", "transferred", "A", "jplag|plain", "_t")
    row("JPlag + TokenNorm", "transferred", "A", "tokennorm|plain", "_t")
    L.append(r"\midrule")
    row("Dolos 2.10.0", "default ($-$M 0.9)", "D", "default", "_t")
    row("", "$-$M 0.5 (boilerplate)", "D", "m50", "_t")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    open(os.path.join(OUT, "tab_cohort_thr.tex"), "w").write("\n".join(L))


def diff_table():
    L = [r"\begin{table*}[t]", r"\centering",
         r"\caption{Paired differences in mean cohort AUROC with 95\% cluster-bootstrap intervals (clusters: source submissions; 2,000 resamples) and two-sided bootstrap $p$ (smallest attainable 0.0005). ``Filtered'' rows remove assignment boilerplate; ``token'' is the unfiltered token expert unless marked.}",
         r"\label{tab:cohort-diff}", r"\footnotesize", r"\setlength{\tabcolsep}{3pt}", r"\begin{tabular}{l|cc|cc}", r"\toprule",
         r" & \multicolumn{2}{c|}{PROGpedia} & \multicolumn{2}{c}{IR-Plag} \\", r"\textbf{Comparison} & $\Delta$ [95\% CI] & $p$ & $\Delta$ [95\% CI] & $p$ \\", r"\midrule"]
    items = [("Gate (CodeBERT) $-$ JPlag", "A", "gate|plain", "jplag"), ("Gate (CodeBERT) $-$ token", "A", "gate|plain", "token"),
             ("Token filtered $-$ JPlag", "A", "token|filt", "jplag"), ("Gate (CodeBERT) filtered $-$ JPlag", "A", "gate|filt", "jplag"),
             ("Gate (CodeBERT) filtered $-$ token filtered", "A", "gate|filt", "tokenfilt"), ("Gate (UniXcoder) filtered $-$ token filtered", "Aux", "gate|filt", "tokenfilt")]
    V = np.load(os.path.join(HERE, "results_A", "cohort_auc_vectors.npz"), allow_pickle=True)
    VU = np.load(os.path.join(HERE, "results_Aux", "cohort_auc_vectors.npz"), allow_pickle=True)
    vec = {"gate_plain": V["gate__plain"], "gate_filt": V["gate__filt"], "token_filt": V["token__filt"], "jplag": V["jplag__plain"],
           "dol_def": np.array(DOL["vec_auc"]["default"]), "dol_m50": np.array(DOL["vec_auc"]["m50"]), "gate_ux_filt": VU["gate__filt"]}
    cl, dsv = V["clusters"], V["ds"]
    rng = np.random.default_rng(1)

    def paired(a, b, ds):
        m = dsv == ds
        u, iv = np.unique(cl[m], return_inverse=True)
        cnt = np.bincount(iv, minlength=len(u))
        d = (a - b)[m]
        sums = np.bincount(iv, weights=d, minlength=len(u))
        bs = np.array([sums[x].sum() / cnt[x].sum() for x in (rng.integers(0, len(u), len(u)) for _ in range(2000))])
        pv = 2 * min((bs <= 0).mean(), (bs >= 0).mean())
        return dict(delta=float(d.mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], p=float(max(pv, 1 / 2000)))
    extra = [("Dolos default $-$ JPlag", "dol_def", "jplag"), ("Gate (CodeBERT) $-$ Dolos default", "gate_plain", "dol_def"),
             ("Token filtered $-$ Dolos $-$M 0.5", "token_filt", "dol_m50"), ("Gate (CodeBERT) filtered $-$ Dolos $-$M 0.5", "gate_filt", "dol_m50"),
             ("Gate (UniXcoder) filtered $-$ Dolos $-$M 0.5", "gate_ux_filt", "dol_m50")]
    FACTS["paired_extra"] = {}
    for lab, a, b in extra:
        cells = [lab]
        for ds in ("PROGpedia", "IR-Plag"):
            d = paired(vec[a], vec[b], ds)
            FACTS["paired_extra"][lab + "|" + ds] = d
            cells += ["%+.3f [%+.3f, %+.3f]" % (d["delta"], d["ci"][0], d["ci"][1]), ("%.4f" % d["p"]) if d["p"] >= 0.001 else r"$<$0.001"]
        L.append(" & ".join(cells) + r" \\")
    for lab, tag, s, ref in items:
        cells = [lab]
        for ds in ("PROGpedia", "IR-Plag"):
            d = E[tag][s][ds]["vs_" + ref]
            cells += ["%+.3f [%+.3f, %+.3f]" % (d["delta"], d["ci"][0], d["ci"][1]), ("%.4f" % d["p"]) if d["p"] >= 0.001 else r"$<$0.001"]
        L.append(" & ".join(cells) + r" \\")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    open(os.path.join(OUT, "tab_cohort_diff.tex"), "w").write("\n".join(L))


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 8, "font.family": "serif"})
    series = [("Gate (CodeBERT)", "A", "gate|plain", "#0072B2", "o", "-"), ("Gate (CodeBERT), boilerplate removed", "A", "gate|filt", "#0072B2", "o", "--"),
              ("Token 5-gram, boilerplate removed", "A", "token|filt", "#009E73", "s", "--"), ("UniXcoder cosine, boilerplate removed", "Aux", "codebert|filt", "#CC79A7", "^", "--"),
              ("JPlag", "A", "jplag|plain", "#D55E00", "D", "-"), ("JPlag + TokenNorm", "A", "tokennorm|plain", "#E69F00", "v", "-")]
    fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.9), gridspec_kw={"width_ratios": [1, 1.7]})
    for lab, tag, s, c, m, ls in series:
        i = [x[3] for x in series].index(c) if False else series.index((lab, tag, s, c, m, ls))
        ax[0].bar([j + (i - 2.5) * 0.14 for j in range(3)], [g(tag, s, "PROGpedia", k) for k in PP], width=0.13, color=c, alpha=0.55 if ls == "--" else 1.0,
                  hatch="//" if ls == "--" else None, edgecolor="white", lw=0.3, label=lab)
        ax[1].plot(range(6), [g(tag, s, "IR-Plag", k) for k in IR], color=c, marker=m, ls=ls, lw=1.2, ms=4)
    ax[0].set_xticks(range(3)); ax[0].set_xticklabels(["insertion", "refactoring", "LLM rewrite"]); ax[0].set_title("PROGpedia cohorts")
    ax[1].set_xticks(range(6)); ax[1].set_xticklabels(["L1", "L2", "L3", "L4", "L5", "L6"]); ax[1].set_title("IR-Plag cohorts (L1 layout ... L6 program logic)")
    for a in ax:
        a.axhline(0.5, color="0.6", lw=0.8, ls=":")
        a.set_ylim(0, 1.02)
        a.set_ylabel("cohort AUROC")
        a.grid(alpha=0.25, lw=0.4)
    fig.legend(*ax[0].get_legend_handles_labels(), loc="lower center", ncol=3, frameon=False, fontsize=7, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.17, 1, 1))
    fig.savefig(os.path.join(OUT, "fig_cohort.pdf"))


auc_table()
thr_table()
diff_table()
figure()
for ds in ("PROGpedia", "IR-Plag"):
    for t, s in (("A", "gate|plain"), ("A", "gate|filt"), ("A", "token|filt"), ("Aux", "gate|filt"), ("B", "gate|filt"), ("C", "gate|filt"), ("Bux", "gate|filt"), ("Cux", "gate|filt"),
                 ("A", "jplag|plain"), ("A", "tokennorm|plain"), ("A", "token|plain"), ("A", "direct|filt")):
        FACTS["%s|%s|%s" % (ds, t, s)] = {k: v for k, v in E[t][s][ds].items() if k != "by_kind"}
        FACTS["%s|%s|%s|kind" % (ds, t, s)] = E[t][s][ds]["by_kind"]
json.dump(FACTS, open(os.path.join(OUT, "facts3.json"), "w"), indent=1)
print("ok")
