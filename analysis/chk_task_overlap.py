"""Train/test task overlap for the 38 ALGO function names of build_convergence.py."""
import collections, os, pickle, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA
import feature_pipeline as fp
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_convergence.py"), encoding="utf8").read()
# reuse ALGO and first_name without executing the script body
ns = {"fp": fp}
a = src.index("ALGO = "); b = src.index("\n", a)
exec(src[a:b], ns)
c = src.index("def first_name"); d = src.index("by = collections")
exec(src[c:d], ns)
ALGO, first_name = ns["ALGO"], ns["first_name"]

pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
S = pickle.load(open(os.path.join(DATA, "snippets.pkl"), "rb"))
F = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
grp, spl = {}, {}
order = {"train": 0, "val": 1, "test": 2, "aux": 3}
for r in pf.itertuples():
    for k, g in ((r.key1, r.group1), (r.key2, r.group2)):
        grp[k] = g
        spl.setdefault(k, set()).add(r.split)
conv = pd.read_csv(os.path.join(DATA, "convergence_pairs.csv"))
conv_keys = set(conv.key1) | set(conv.key2)

rows = []
for k, (lang, code) in S.items():
    if k not in grp or len(code.splitlines()) < 4:
        continue
    nm = first_name(code, lang)
    if nm in ALGO:
        rows.append((k, lang, nm, grp[k], spl[k]))
df = pd.DataFrame(rows, columns=["key", "lang", "name", "group", "splits"])
print("snippets with ALGO name (>=4 lines):", len(df), "names present:", df.name.nunique())
def has(s, which): return any(x in s for x in which)
df["tt"] = df.splits.apply(lambda s: has(s, ("train", "val")))
df["te"] = df.splits.apply(lambda s: "test" in s)
print("snippets by split membership: trainval", int(df.tt.sum()), "test", int(df.te.sum()), "both", int((df.tt & df.te).sum()))
per = df.groupby("name").agg(g_tv=("group", lambda x: len(set(x[df.loc[x.index, "tt"]]))),
                              g_te=("group", lambda x: len(set(x[df.loc[x.index, "te"]]))))
both = per[(per.g_tv > 0) & (per.g_te > 0)]
print("names with groups in both train/val and test:", len(both), "of", len(per), " present in test:", int((per.g_te > 0).sum()))
print("per-name (name lang-agnostic) groups:\n", per.sort_values("g_te", ascending=False).to_string())
# nearest neighbour: each convergence-pair snippet vs train/val snippets with the same (lang,name)
def mean_win(k):
    w = F[k]["win"]; v = w.mean(0); return v / max(np.linalg.norm(v), 1e-12)
def jac(a, b):
    ga, gb = F[a]["grams"], F[b]["grams"]
    return len(ga & gb) / max(1, len(ga | gb))
nn_cos, nn_jac = [], []
tv = df[df.tt & ~df.te]
bykey = {kk: g for kk, g in tv.groupby(["lang", "name"])}
for r in df[df.key.isin(conv_keys)].itertuples():
    g = bykey.get((r.lang, r.name))
    if g is None:
        continue
    q = mean_win(r.key)
    nn_cos.append(max(float(q @ mean_win(k)) for k in g.key))
    nn_jac.append(max(jac(r.key, k) for k in g.key))
for nm_, v in (("cosine(mean window)", nn_cos), ("token 5-gram Jaccard", nn_jac)):
    v = np.array(v)
    print("NN sim to train/val same (lang,name):", nm_, "n=%d" % len(v), "median %.3f mean %.3f p90 %.3f max %.3f" % (np.median(v), v.mean(), np.percentile(v, 90), v.max()))
nconv = df[df.key.isin(conv_keys)]
print("convergence snippets:", len(nconv), " with a same-(lang,name) train/val snippet:", len(nn_cos))

# centred cosine (remove corpus mean) to avoid anisotropy
allv = np.stack([F[k]["win"].mean(0) for k in F]); mu = allv.mean(0)
def cv(k):
    v = F[k]["win"].mean(0) - mu; return v / max(np.linalg.norm(v), 1e-12)
cc_same, cc_rand = [], []
rng = np.random.default_rng(0)
tvall = list(tv.key)
for r in df[df.key.isin(conv_keys)].itertuples():
    g = bykey.get((r.lang, r.name))
    if g is None: continue
    q = cv(r.key)
    cc_same.append(max(float(q @ cv(k)) for k in g.key))
    cc_rand.append(max(float(q @ cv(k)) for k in rng.choice(tvall, len(g), replace=False)))
print("centred cosine NN same-name: median %.3f p90 %.3f | size-matched random train/val: median %.3f p90 %.3f" % (np.median(cc_same), np.percentile(cc_same, 90), np.median(cc_rand), np.percentile(cc_rand, 90)))
name_of = dict(zip(df.key, df.name)); lang_of = dict(zip(df.key, df.lang))
has_nb = lambda k: (lang_of[k], name_of[k]) in bykey
n_any = sum(1 for r in conv.itertuples() if has_nb(r.key1) or has_nb(r.key2))
n_both = sum(1 for r in conv.itertuples() if has_nb(r.key1) and has_nb(r.key2))
print("convergence pairs", len(conv), "with >=1 snippet having same-name train/val neighbour:", n_any, "both:", n_both)
print("names in conv pairs:", conv.name.nunique(), "of which with train/val groups:", sum(1 for n in conv.name.unique() if n in set(both.index)))
