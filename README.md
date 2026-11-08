# Enhancing Plagiarism Detection in AI-Generated Code: Dynamic Multi-Modal Semantic-Structural Analysis

Code, data and results for a gated late-fusion detector that screens AI-obfuscated code plagiarism. Three fixed experts (CodeBERT semantic similarity, AST structural similarity, token 5-gram Jaccard) are combined by a small gating network that outputs per-pair expert weights. The evaluation uses problem-grouped splits (no problem group is shared between training and test), three negative regimes (A random, B mined with the expert scores, C mined by identifier overlap), cluster-aware statistics, real baseline tools (JPlag, Dolos) and cohort screening on real student programs.

This README is organised for review: **Section 1** says where each dataset is, **Section 2** maps every table and figure of the paper to the script and result file that produce it, **Section 3** explains how to rerun.

## 1. Datasets

All pair tables are CSV files in `analysis/data/`. The program text behind every key is exported as plain JSONL in `dataset/snippets/` (a pair row refers to snippets by `key`, e.g. `java:c87cd5ff4d784d6d`; each JSONL line is `{"key", "lang", "code"}`). Regenerate the JSONL with `python -I analysis/export_dataset.py`.

| Dataset (paper section) | Pair / label table | Snippet text | Size |
| :--- | :--- | :--- | :--- |
| GPTCloneBench benchmark, problem-grouped protocol, regimes A / B / C (III-A, III-B; Table 1) | `analysis/data/pairs.csv` (31,992 rows: protocol pairs plus the regime-B `hard_independent` and regime-C `tfidf_independent` negative pools; columns `split`, `slice`, `label`, `key1`, `key2`, `group1`, `group2`, `source`), `problem_group_manifest.csv`, `cross_language_problem_manifest.csv`, `protocol_stats.json` | `dataset/snippets/benchmark_snippets.jsonl` | 10,506 snippets |
| Independent-convergence pairs (IV-I) | `analysis/data/convergence_pairs.csv` | benchmark snippets | 193 pairs |
| PROGpedia same-author / cross-author check (III-I, IV-I) | `analysis/data/progpedia_pairs.csv` | `dataset/snippets/progpedia_snippets.jsonl` | 4,144 files |
| Cohorts with derived submissions: PROGpedia (2 assignments) and IR-Plag (7 tasks) (III-J, IV-H) | `analysis/data/cohort_pairs.csv`, `cohort_meta.csv`, `cohort_subs.csv` | `dataset/snippets/cohort_snippets.jsonl` | 771 programs |
| Cross-language cohorts: 100 cohorts whose derived submission is an AI-written translation of an honest Java program (III-J, IV-H) | `analysis/data/xl2_cohort_pairs.csv`, `xl2_cohort_meta.csv`, `xl2_cohort_subs.csv` | `dataset/snippets/cross_language_cohort_snippets.jsonl` | 155 programs |
| Generator probe: seeds and outputs of four current models (IV-K) | `analysis/data/probe2_pairs.csv`; seeds and raw outputs in `analysis/gen/seeds`, `analysis/gen/out`; reading audit in `analysis/gen/audit` | `dataset/snippets/generator_probe_snippets.jsonl` | 2,991 snippets |
| Lexical attack A1 (IV-L) | `analysis/data/e4_pairs.csv` (`key1`/`key2` original, `akey2` attacked second snippet) | `dataset/snippets/benchmark_snippets.jsonl` and `attack_a1_snippets.jsonl` | 300 positives, 300 negatives each of regime A and B |

Sources: GPTCloneBench (https://github.com/srlabUsask/GPTCloneBench, Zenodo record 10198952), the Maisch et al. replication package (PROGpedia assignments Progpedia19 / Progpedia56, Zenodo 10.5281/zenodo.18089904, CC BY 4.0) and IR-Plag (Apache-2.0).

As the paper states: the 100 translated derived submissions of the cross-language cohorts and the probe outputs were written by AI models and were checked only for syntactic validity, not for behavioural equivalence; the audits of the mined negatives and of the probe positives were done by a single AI-assisted rater (see the manuscript's Acknowledgment).

## 2. Paper to repository map

Table and figure numbers are those of the manuscript. "Run" is the script that writes the result file; the LaTeX tables are generated from the result JSONs by the `make_tables*.py` scripts (`analysis/rebuild_all_tables.sh` runs them in the right order; output in `analysis/tables/`).

| Paper item | Result files (`analysis/results_{A,B,C}/`) | Run | Table script |
| :--- | :--- | :--- | :--- |
| Table 1 protocol sizes (III-B) | `data/protocol_stats.json` | `build_protocol.py`, `build_hard_negatives.py`, `build_negatives_c.py` | `make_tables.py` |
| Tables 2-4 comparison with baselines, clone-type recall, same-language comparison | `main_eval.json`, `post_analysis.json`, `e8_tools.json` | `run_experiments.py`, `evaluate_all.py`, `post_analysis.py`, `run_jplag.py`, `dolos_benchmark.py` | `make_tables.py` |
| Table 5 component ablation (leave-one-out, decision rules) | `post_analysis.json` | `post_analysis.py` | `make_tables.py` |
| Table 6 fixed-weight and non-routing baselines (incl. tuned JPlag and Dolos rows) | `e1_baselines.json`, `e8_tuned.json` | `e1_baselines.py`, `e8_tune_tools.py` | `make_tables4.py` |
| Table 7 ablation by retraining | `e2_retrained.json` | `e2_retrained_ablation.py` | `make_tables4.py` |
| Table 8 regime C and split re-draws | `main_eval.json`, `split_variance.json` | `run_experiments.py`, `split_variance.py` | `make_tables.py`, `make_tables5.py` |
| Tables 9-10 stronger encoder, encoder control | `results_{A,B,C}ux/`, `e3_encoder.json`, `embedding_baselines.json` | `encode_unixcoder.py`, `e3_encoder_control.py` | `make_tables2.py`, `make_tables4.py` |
| Tables 11-12 log-odds repair on the benchmark and on real / cross-language cohorts | `results_{A,B,C}lo/`, `logit_headline.json`, `gate_variants*.json`, `gate_shortcut.json`, `gate_cohort_filt.json`, `xl2_eval.json` | `logit_headline.py`, `rerun_logit_ablations.py`, `gate_variants.py`, `gate_shortcut.py`, `eval_xl2_cohorts.py` | `make_tables3.py`, `make_tables5.py` |
| Tables 13-15 cohort screening, filtered paired differences, flagging behaviour (IV-H) | `cohort_eval.json`, `cohort_variants.json`, `sens_filter.json`, `e6_cohort_detail.json`, `gate_cohort_filt.json` | `build_cohorts.py`, `eval_cohorts.py`, `analyze_cohorts.py`, `sens_filter.py`, `dolos_cohort_runs.py`, `jplag_cohort.py` | `make_tables3.py`, `make_tables5.py` |
| Table 16 same-author / convergence check (IV-I) | `external.json` | `build_progpedia.py`, `build_convergence.py`, `eval_external.py` | `make_tables.py`, `make_tables2.py` |
| Table 17 operating points, Fig. 2 precision-recall curves (IV-J) | `post_analysis.json`, `pr_curves.png` | `post_analysis.py`, `make_pr_figure.py` | `make_tables.py` |
| Tables 18-19 diagnostic cases, threshold sensitivity (IV-J) | `post_analysis.json` | `post_analysis.py` | `make_tables.py` |
| Tables 20-21 generator probe (IV-K) | `probe2.json`, `e7_probe.json` | `build_probe_claude.py`, `eval_probe2.py`, `e7_probe_reanalysis.py` | `make_tables.py`, `make_tables4.py` |
| Table 22 lexical attack A1 (IV-L) | `e4_attack.json` | `e4_build.py`, `e4_tools.py`, `e4_eval.py` | `make_tables4.py` |
| V-A failure analysis | `failure_pooled.json` | `failure_pooled.py` | prose |
| III-J cross-language cohorts (generation, evaluation) | `xl2_eval.json` | `eval_xl2_cohorts.py` (the cohort tables `xl2_cohort_*.csv` are provided; the AI-written translations themselves are in `dataset/snippets/cross_language_cohort_snippets.jsonl`) | `make_tables5.py` |

The scripts are named after the experiment they run; each file starts with a docstring that states its inputs and outputs.

## 3. Reproducing

Run scripts from `analysis/` with `python -I <script>`. Seeds are fixed, so trained models and tables reproduce exactly (no GPU needed). Requirements: Python 3.11, PyTorch, `transformers` (microsoft/codebert-base, microsoft/unixcoder-base), tree-sitter with the Java, Python, C and C# grammars. JPlag 6.3.0 needs a JDK and the JPlag jar, and Dolos 2.10.0 runs from its official container; neither is included. To regenerate all manuscript tables from the stored results run `bash analysis/rebuild_all_tables.sh` (the whole script; `make_tables.py` alone omits the merged regime-C part (b)).

## 4. Not included

Large caches and model weights (`*.pkl`, `*.pth`, `*.npz`: feature caches and UniXcoder embeddings, regenerated by `feature_pipeline.py` and the `encode_unixcoder_*.py` scripts), run logs and the per-pair tool-score CSVs are omitted. The snippet text of every dataset is in `dataset/snippets/`.
