# -*- coding: utf-8 -*-
"""Can the base-problem ID be recovered from the released feature file?

884 problems x C(4,2)=6 language pairings = 5,304 = exactly the positive count.
If the rows were written in generation order, positive row i belongs to problem
i // 6. Test that by comparing within-group to between-group feature variance:
pairs from the same problem should resemble each other more than random pairs do.
"""
import numpy as np
import pandas as pd

F = ["S_CodeBERT", "S_AST", "S_Token"]
df = pd.read_csv("gptclonebench_features.csv")

pos = df[df.label == 1].reset_index(drop=True)
print("positive rows: %d  (884 x 6 = %d)" % (len(pos), 884 * 6))
print("positives contiguous in file?", bool(
    (df.label.values[:len(pos)] == 1).all() or (df.label.values[-len(pos):] == 1).all()))
print("label sequence, first 24 rows:", "".join(str(v) for v in df.label.values[:24]))
print()

X = pos[F].values
grp = np.arange(len(pos)) // 6            # hypothesised problem id

within = []
for g in range(len(pos) // 6):
    block = X[g * 6:(g + 1) * 6]
    within.append(block.var(axis=0).mean())
within = float(np.mean(within))

rng = np.random.default_rng(0)
between = []
for _ in range(len(pos) // 6):
    idx = rng.choice(len(X), 6, replace=False)
    between.append(X[idx].var(axis=0).mean())
between = float(np.mean(between))

print("mean within-block feature variance (blocks of 6, assumed one problem): %.5f" % within)
print("mean variance of 6 randomly chosen positives                        : %.5f" % between)
ratio = within / between if between else float("nan")
print("ratio: %.3f" % ratio)
print()
if ratio < 0.75:
    print("=> Blocks of 6 are markedly more homogeneous than random draws.")
    print("   Consistent with rows being in generation order, so problem_id = index // 6")
    print("   is recoverable and a grouped split can be built WITHOUT re-running CodeBERT.")
elif ratio > 0.95:
    print("=> Blocks of 6 look no more homogeneous than random draws.")
    print("   Rows are probably shuffled; problem_id is NOT recoverable this way and a")
    print("   grouped split would require regenerating features with IDs attached.")
else:
    print("=> Inconclusive; weak structure. Would need the generation script to confirm.")
