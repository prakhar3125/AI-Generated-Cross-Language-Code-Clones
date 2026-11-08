"""Gate variants motivated by diag_gate_loss.py (output-form and evidence-quality hypotheses), compared with the paper's gate
and the direct classifier under the SAME protocol (corrected Eq. 2 features, same lr/batch as the regime's selected values,
early stopping on validation BCE, validation-tuned threshold, 8 seeds). Nothing here is tuned on the test partition.

  base        paper's gate: softmax weights over the three expert scores, fused = weighted mean              (reference)
  logit       weights act in log-odds: sigmoid(tau * sum_i w_i logit(S_i) + b); tau, b learned scalars
  resid       fused score kept, plus a small additive correction in log-odds: sigmoid(logit(fused) + r(x)); r starts at 0
  feat        base gate whose weight network also sees evidence-quality inputs (log min length, |log length ratio|, log complexity)
  logit_feat  logit gate with the same extra inputs
  direct      equal-capacity direct classifier on X6 (reference);  direct_feat: same with the extra inputs

python -I gate_variants.py prep                (once: cache cohort features)
REGIME=A|B|C python -I gate_variants.py       -> results_<R>/gate_variants.json
"""
import json, os, pickle, sys
from multiprocessing import Pool
import numpy as np, pandas as pd
import torch, torch.nn as nn
from sklearn.metrics import roc_auc_score, roc_curve

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE
from exp_lib import REGIME, SC, SEEDS, TAG, X6, load, trunk, tune_threshold

RES = os.path.join(HERE, "results_" + TAG)
CACHE = os.path.join(DATA, "_gate_variants_cohort_cache.pkl")
EPS = 0.01

def extras(cc1, cc2, n1, n2):
    n1, n2 = np.asarray(n1, float), np.asarray(n2, float)
    return np.stack([np.log1p(np.minimum(n1, n2)), np.abs(np.log1p(n1) - np.log1p(n2)), np.log1p(np.asarray(cc1, float) + np.asarray(cc2, float))], 1)

def cohort_tables():
    import compute_pair_features as cpf
    P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv")); F = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
    rows = []
    for r in P.itertuples():
        a, b = F[r.key1], F[r.key2]
        s_c, s_a, s_t = cpf.sem(a, b), cpf.ast_sim(a, b), cpf.tok_sim(a, b)
        rows.append((s_c, s_a, s_t, 0.0, abs(s_c - s_a), 1 - s_a, a["cc"], b["cc"], a["ntok"], b["ntok"]))
    return pd.DataFrame(rows, columns=X6 + ["cc1", "cc2", "ntok1", "ntok2"])

def get_cohort():
    if not os.path.exists(CACHE):
        pickle.dump(cohort_tables(), open(CACHE + ".tmp", "wb")); os.replace(CACHE + ".tmp", CACHE)
    return pickle.load(open(CACHE, "rb"))

# ------------------------------------------------------------------ models
class Gate(nn.Module):
    def __init__(self, kind, nin):
        super().__init__()
        self.kind = kind
        self.net = trunk(nin, 3)
        if "logit" in kind:
            self.raw_tau = nn.Parameter(torch.tensor(0.5413)); self.b = nn.Parameter(torch.tensor(0.0))
        if kind == "resid":
            self.res = nn.Sequential(nn.Linear(nin, 8), nn.ReLU(), nn.Linear(8, 1))
            nn.init.zeros_(self.res[2].weight); nn.init.zeros_(self.res[2].bias)
    def forward(self, x, s):
        w = torch.softmax(self.net(x), -1)
        if "logit" in self.kind:
            sc = s.clamp(EPS, 1 - EPS); z = (w * torch.log(sc / (1 - sc))).sum(1, keepdim=True)
            return torch.sigmoid(nn.functional.softplus(self.raw_tau) * z + self.b), w
        f = (w * s).sum(1, keepdim=True)
        if self.kind == "resid":
            f = f.clamp(1e-4, 1 - 1e-4)
            return torch.sigmoid(torch.log(f / (1 - f)) + self.res(x)), w
        return f, w

class Direct(nn.Module):
    def __init__(self, nin):
        super().__init__(); self.net = trunk(nin, 1)
    def forward(self, x, s):
        return torch.sigmoid(self.net(x)), None

def build(kind, nin):
    return Direct(nin) if kind.startswith("direct") else Gate(kind, nin)

def train(kind, Xtr, Str, ytr, Xva, Sva, yva, seed, lr, bs, max_epochs=100, patience=10):
    torch.manual_seed(seed); np.random.seed(seed)
    m = build(kind, Xtr.shape[1])
    opt = torch.optim.AdamW(m.parameters(), lr=lr, weight_decay=1e-5); lf = nn.BCELoss()
    T = lambda a: torch.tensor(a, dtype=torch.float32)
    Xt, St, yt = T(Xtr), T(Str), T(ytr).unsqueeze(1); Xv, Sv, yv = T(Xva), T(Sva), T(yva).unsqueeze(1)
    best, state, bad = float("inf"), None, 0
    g = torch.Generator().manual_seed(seed)
    for ep in range(max_epochs):
        m.train(); perm = torch.randperm(len(Xt), generator=g)
        for i in range(0, len(perm), bs):
            j = perm[i:i + bs]; out, _ = m(Xt[j], St[j])
            loss = lf(out.clamp(1e-6, 1 - 1e-6), yt[j]); opt.zero_grad(); loss.backward(); opt.step()
        m.eval()
        with torch.no_grad():
            vl = lf(m(Xv, Sv)[0].clamp(1e-6, 1 - 1e-6), yv).item()
        if vl < best - 1e-5:
            best, bad = vl, 0; state = {k: v.clone() for k, v in m.state_dict().items()}
        else:
            bad += 1
            if bad >= patience: break
    m.load_state_dict(state); m.eval(); return m

@torch.no_grad()
def predict(m, X, S):
    out, w = m(torch.tensor(X, dtype=torch.float32), torch.tensor(S, dtype=torch.float32))
    return out.numpy().ravel(), (None if w is None else w.numpy())

# ------------------------------------------------------------------ data
D = load(); tr, va, te = D["train"], D["val"], D["test"]
summ = json.load(open(os.path.join(RES, "training_summary.json"))); LR, BS = summ["selected"]["lr"], summ["selected"]["batch"]
VARIANTS = ["base", "logit", "resid", "feat", "logit_feat", "direct", "direct_feat"]

def design(df, kind, ex_stats):
    X = df[X6].values.astype(np.float64)
    if kind.endswith("_feat") or kind == "feat" or kind.endswith("_len"):
        E = extras(df.cc1, df.cc2, df.ntok1, df.ntok2)
        lo, hi, mu, sd = ex_stats
        E = (np.clip(E, lo, hi) - mu) / sd          # cohort programs longer than any benchmark snippet are clipped to the training range
        if kind.endswith("_len"):
            E = E[:, [0, 2]]                        # evidence quantity only (min length, complexity): no length-RATIO input
        X = np.hstack([X, E])
    return X

Etr = extras(tr.cc1, tr.cc2, tr.ntok1, tr.ntok2)
EX = (Etr.min(0), Etr.max(0), Etr.mean(0), Etr.std(0) + 1e-9)

def job(a):
    kind, seed = a
    coh = get_cohort()
    out = {}
    m = train(kind, design(tr, kind, EX), tr[SC].values, tr.label.values, design(va, kind, EX), va[SC].values, va.label.values, seed, LR, BS)
    sv, _ = predict(m, design(va, kind, EX), va[SC].values)
    st, wt = predict(m, design(te, kind, EX), te[SC].values)
    sc, wc = predict(m, design(coh, kind, EX), coh[SC].values)
    return kind, seed, tune_threshold(sv, va.label.values), st, sc, (None if wt is None else wt.mean(0)), (None if wc is None else wc.mean(0))

def cohort_auc(sc, P, M, S):
    hon = {g: set(G[G.role == "honest"].id) for g, G in S.groupby("group")}
    res = {"PROGpedia": [], "IR-Plag": []}
    for g, G in P.groupby("group"):
        h = hon[g]; hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
        for d in M[M.group == g].itertuples():
            dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
            nd = np.concatenate([hh, np.array([i for i in dm if i != d.derived_pair and not ((P.id1[i] == d.src) or (P.id2[i] == d.src))])])
            dp = int(P.index[P.pair_id == d.derived_pair][0]); x = sc[nd]
            res["PROGpedia" if g.startswith("Progpedia") else "IR-Plag"].append((x < sc[dp]).mean() + .5 * (x == sc[dp]).mean())
    return {k: float(np.mean(v)) for k, v in res.items()}

def f1(y, p):
    tp = ((p == 1) & (y == 1)).sum(); return float(2 * tp / max(2 * tp + ((p == 1) & (y == 0)).sum() + ((p == 0) & (y == 1)).sum(), 1))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prep":
        get_cohort(); print("cohort cache ready"); sys.exit(0)
    torch.set_num_threads(1)
    P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv")); M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv")); S = pd.read_csv(os.path.join(DATA, "cohort_subs.csv"))
    with Pool(5) as pool:
        res = pool.map(job, [(k, s) for k in VARIANTS for s in SEEDS])
    y = te.label.values; neg_x = (y == 0) & (te.D_lang.values == 1); out = {}
    for k in VARIANTS:
        r = sorted([x for x in res if x[0] == k], key=lambda z: z[1])
        f1s = [f1(y, (x[3] >= x[2]).astype(int)) for x in r]
        aucs = [roc_auc_score(y, x[3]) for x in r]
        def rat(s, f):
            fpr, tpr, _ = roc_curve(y, s); return tpr[np.searchsorted(fpr, f, side="right") - 1]
        r1 = [rat(x[3], .01) for x in r]; r5 = [rat(x[3], .05) for x in r]
        fxl = [float((x[3][neg_x] >= x[2]).mean()) for x in r]
        ens = np.mean([x[4] for x in r], 0); ca = cohort_auc(ens, P, M, S)
        sl = {s: float(np.mean([(x[3][(te.slice == s).values] >= x[2]).mean() for x in r])) for s in ("exact", "renamed", "refactored", "cross-language")}
        out[k] = dict(f1=[float(np.mean(f1s)), float(np.std(f1s, ddof=1))], auc=float(np.mean(aucs)), r1=float(np.mean(r1)), r5=float(np.mean(r5)),
                      fpr_crosslang=float(np.mean(fxl)), recall_by_slice=sl, cohort_prog=ca["PROGpedia"], cohort_irplag=ca["IR-Plag"],
                      mean_w_test=None if r[0][5] is None else [round(float(v), 3) for v in np.mean([x[5] for x in r], 0)],
                      mean_w_cohort=None if r[0][6] is None else [round(float(v), 3) for v in np.mean([x[6] for x in r], 0)])
        print(TAG, "%-12s F1 %.1f+-%.1f  AUC %.3f  R@1%% %.3f  R@5%% %.3f  xlangFPR %.3f  coh %.3f/%.3f  w_test %s" % (
            k, 100 * out[k]["f1"][0], 100 * out[k]["f1"][1], out[k]["auc"], out[k]["r1"], out[k]["r5"], out[k]["fpr_crosslang"], out[k]["cohort_prog"], out[k]["cohort_irplag"], out[k]["mean_w_test"]), flush=True)
    json.dump(out, open(os.path.join(RES, "gate_variants.json"), "w"), indent=1)
