# Enhancing Plagiarism Detection in AI-Generated Code: Dynamic Multi-Modal Semantic-Structural Analysis

Code and results for a gated late-fusion detector that screens AI-obfuscated code plagiarism. Three fixed experts (CodeBERT semantic similarity, AST structural similarity, token 5-gram Jaccard) are combined by a small gating network that outputs per-pair expert weights. The evaluation uses problem-grouped splits (no problem group is shared between training and test), three negative regimes (A random, B mined with the expert scores, C mined by identifier overlap), cluster-aware statistics, real baseline tools (JPlag, Dolos) and cohort screening on real student programs.

## Data source

The benchmark is GPTCloneBench (https://github.com/srlabUsask/GPTCloneBench; Zenodo record 10198952), built from SemanticCloneBench seeds and LLM-generated clones. This repository uses its stand-alone true-clone, cross-language (`cross_language.zip`, `cross_language_part_2.zip`) and false-pair archives. Cohort data come from the Maisch et al. replication package (PROGpedia assignments, Zenodo 10.5281/zenodo.18089904, CC BY 4.0) and IR-Plag.

## Evaluation pipeline

All numbers in the manuscript come from `analysis/` (run with `python -I <script>` from that folder; fixed seeds reproduce every model).

| Script | Purpose |
| :--- | :--- |
| `build_protocol.py` | Builds problem groups (connected components of snippet hashes), the train/val/test split, positives and regime-A (random independent) negatives; writes `data/pairs.csv`, `data/problem_group_manifest.csv`, `data/cross_language_problem_manifest.csv`, `data/protocol_stats.json`. Needs the GPTCloneBench release (Zenodo 10198952) and `eval_dataset/`. |
| `feature_pipeline.py`, `compute_pair_features.py` | One-pass snippet features (CodeBERT windows, tree-sitter AST vector and 5-gram tokens, cyclomatic complexity) and the six gate inputs per pair. |
| `build_hard_negatives.py` | Regime-B nearest-neighbour independent negatives. |
| `run_experiments.py`, `evaluate_all.py`, `post_analysis.py` | Hyper-parameter grid, 8-seed training of gate / direct classifier / ablations, decision rules, cluster-aware statistics, threshold study, operating points (`REGIME=A|B`). |
| `run_jplag.py` | Real JPlag 6.3.0 (+ `--normalize`) on same-language pairs (needs a JDK and the JPlag jar, not included). |
| `build_probe_claude.py`, `eval_probe2.py` | Zero-shot probe: translations and same-language rewrites by four current models (seeds in `gen/seeds`, outputs in `gen/out`). |
| `make_tables.py` | Generates every LaTeX table of the manuscript. |
| `build_cohorts.py`, `encode_unixcoder_cohort.py`, `jplag_cohort.py` | Cohort sets with real derived submissions: PROGpedia assignments Progpedia19/56 from the Maisch et al. replication package (Zenodo 10.5281/zenodo.18089904, CC BY 4.0) and the seven IR-Plag tasks (Karnalim et al.); one cohort per derived file; JPlag run once per assignment. Download both datasets yourself into `tools/maisch_dl/x/datasets` and `tools/irplag_dl/x/IR-Plag-Dataset`. |
| `eval_cohorts.py`, `analyze_cohorts.py`, `sens_filter.py` | Frozen models scored on every cohort pair (plain and boilerplate-removed features), cohort AUROC, detection and false-flag rates, the label-free adaptive threshold per cohort, cluster-bootstrap intervals, and the boilerplate-filter sensitivity sweep (`results_*/cohort_eval.json`, `results_A/sens_filter.json`). |
| `dolos_benchmark.py`, `dolos_cohort.py`, `dolos_cohort_runs.py`, `dolos_bench_stats.py` | Dolos 2.10.0 (official container `ghcr.io/dodona-edu/dolos-cli`, pulled with Docker) on the benchmark's same-language pairs and on the cohorts (one run per cohort, default and `-M 0.5`), plus the cluster-bootstrap comparison with the gate and JPlag. |
| `eval_cohort_variants.py`, `eval_probe2_ux.py`, `encode_unixcoder_probe2.py` | Robustness of the boilerplate filter on the gate's inputs, and the generator probe repeated with the UniXcoder expert (`REGIME=A|B SEM=ux`). |
| `e1_baselines.py`, `e2_retrained_ablation.py`, `e3_encoder_control.py` | Fixed-weight and non-routing baselines (best convex weights, hand-coded rule, gradient-boosted trees), ablation by retraining without an expert, and the encoder / pooling / normalization control. |
| `compute_whiten_feature.py` (`SEM=wh`) | Whitened CodeBERT semantic expert (training-split ZCA) used as a drop-in replacement; `run_experiments.py` and `e1_baselines.py` then run with `SEM=wh`. |
| `e4_build.py`, `e4_tools.py`, `e4_eval.py` | Lexical attack A1 (rename declared identifiers, mask string literals) on same-language pairs; JPlag, Dolos and the learned systems on original and attacked pairs. |
| `e6_weights_and_tasks.py`, `e7_probe_reanalysis.py` | Per-assignment cohort AUROC and gate weights on derived versus honest pairs; probe AUROC, recall at fixed FPR and cluster-bootstrap intervals over seed problems. |
| `e8_tune_tools.py`, `e8_tool_metrics.py`, `failure_pooled.py`, `make_pr_figure.py`, `make_tables4.py` | Tuning of JPlag / Dolos settings, operating-point metrics of every system, failure analysis pooled over seeds, stacked precision-recall figure, tables of these experiments. |
| `make_tables2.py`, `make_tables3.py` | Stronger-encoder, external-check and cohort tables and Fig. `fig_cohort.pdf` (run after `make_tables.py`). |

Outputs: `analysis/results_A`, `analysis/results_B`, `analysis/results_C` (scores, per-pair predictions, JSON summaries).

Note: `analysis/data/pairs.csv` holds the protocol pairs plus the regime-B (`hard_independent`) and regime-C (`tfidf_independent`) negative pools (31,992 rows).

## Additional outputs

* `analysis/results_{A,B,C}/e8_tuned.json`: tuned JPlag (minimum match 5) and Dolos (k=35, window 25) test F1 and AUROC, reported in the fixed-weight baselines table.
* `analysis/results_{A,B,C}lo/`, `analysis/tables_lo/`: log-odds-fusion gate runs and the tables generated from them; `analysis/rebuild_all_tables.sh` regenerates every manuscript table in the correct order (`make_tables.py` through `make_tables5.py`; run the whole script, since `make_tables.py` alone omits the merged regime-C part (b)).
* `analysis/gen/`: generator-probe seeds, model outputs and the reading-audit files.

## Not included

Large caches and model weights (`*.pkl`, `*.pth`, `*.npz`), run logs, the per-pair tool-score CSVs, and the generator scripts and data of the cross-language derived cohorts (the `xl_cohort` files) are omitted. The cohort summaries quoted in the manuscript can be regenerated with the cohort scripts listed above.
