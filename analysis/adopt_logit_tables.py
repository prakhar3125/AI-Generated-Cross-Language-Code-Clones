"""Copy the log-odds versions of the gate-dependent tables (tables_lo/) over the manuscript tables (tables/); the mean-fusion originals are kept
in tables_mean/. Tables whose content does not involve the CodeBERT-expert gate (UniXcoder / whitened blocks, cohorts, JPlag/Dolos, encoder control)
are not touched. python -I adopt_logit_tables.py"""
import os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
ADOPT = ["tab_main", "tab_slices", "tab_same_language", "tab_ablation", "tab_retrained", "tab_splitvar", "tab_diag", "tab_ops", "tab_sens",
         "tab_attack", "tab_probe", "tab_probe_auc", "tab_external", "tab_regime_c", "tab_operating_all", "tab_baselines", "tab_ux"]
for t in ADOPT:
    src = os.path.join(HERE, "tables_lo", t + ".tex")
    if os.path.exists(src):
        shutil.copyfile(src, os.path.join(HERE, "tables", t + ".tex")); print("adopted", t)
    else:
        print("MISSING in tables_lo:", t)
shutil.copyfile(os.path.join(HERE, "tables_lo", "fig_pr_stacked.pdf"), os.path.join(HERE, "tables", "fig_pr_stacked.pdf")); print("adopted fig_pr_stacked.pdf")
