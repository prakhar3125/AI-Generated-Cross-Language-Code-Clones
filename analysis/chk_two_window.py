import pickle, os, sys, collections
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA
F = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
c = collections.Counter(len(v["win"]) for v in F.values())
print("benchmark snippets by window count:", sorted(c.items())[:6], "total", len(F))
two = {k for k, v in F.items() if len(v["win"]) == 2}
pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
print(pf.columns.tolist()[:12])
k1 = "key1" if "key1" in pf else pf.columns[0]
k2 = "key2" if "key2" in pf else pf.columns[1]
m = pf[k1].isin(two) | pf[k2].isin(two)
print("pairs with a 2-window snippet:", int(m.sum()), "of", len(pf), "%.2f%%" % (100 * m.mean()))
print(pf[m].groupby("split").size().to_dict() if "split" in pf else "")
C = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
try:
    cc = collections.Counter(len(v["win"]) for v in C.values()); print("cohort files by windows", sorted(cc.items())[:6])
except Exception as e:
    print("cohort pkl structure", type(C), repr(e))
