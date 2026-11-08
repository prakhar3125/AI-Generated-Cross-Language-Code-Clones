"""Where does the gate's PROGpedia-cohort collapse come from after the Eq. 2 fix?
2x2: gate trained on OLD or NEW benchmark features (backup_pre_eq2fix/pair_features.csv vs data/pair_features.csv),
scored on cohort pairs featurized with the OLD (centre from 2 windows) or NEW (centre from 3 windows) S_sem.
Also reports mean gate weights and the S_sem/S_AST/S_Token seen by the gate on cohorts. REGIME=A python -I diag_collapse_2x2.py"""
import json, os, pickle, sys
from multiprocessing import Pool
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE
import compute_pair_features as cpf
from exp_lib import SC, SEEDS, X6, score, train_model, NEG_SLICE

BK = os.path.join(HERE, "..", "..", "backup_pre_eq2fix", "pair_features.csv")
LR, BS = 1e-3, 32
arr = lambda df, c: df[c].values.astype(np.float64)

def load_pf(path):
    df = pd.read_csv(path)
    df = df[~df.slice.isin({"independent", "hard_independent", "tfidf_independent"} - {NEG_SLICE})]
    return {sp: df[df.split == sp].reset_index(drop=True) for sp in ("train", "val")}

def sem_old(a, b):
    def nrm(X):
        X = X.astype(np.float32)
        if X.shape[0] > 1:
            X = X - X.mean(0, keepdims=True)
        return X / np.clip(np.linalg.norm(X, axis=1, keepdims=True), 1e-12, None)
    return cpf._topk(np.clip(nrm(a["win"]) @ nrm(b["win"]).T, -1, 1), 3)

P = pd.read_csv(os.path.join(DATA, "cohort_pairs.csv")); M = pd.read_csv(os.path.join(DATA, "cohort_meta.csv"))
S = pd.read_csv(os.path.join(DATA, "cohort_subs.csv")); F = pickle.load(open(os.path.join(DATA, "cohort_feats.pkl"), "rb"))
def feats(semfn):
    rows = []
    for r in P.itertuples():
        a, b = F[r.key1], F[r.key2]
        sc_, sa, st = semfn(a, b), cpf.ast_sim(a, b), cpf.tok_sim(a, b)
        rows.append((sc_, sa, st, 0.0, abs(sc_ - sa), 1 - sa, a["cc"]))
    return pd.DataFrame(rows, columns=["S_CodeBERT", "S_AST", "S_Token", "D_lang", "S_CodeBERT_minus_S_AST", "one_minus_S_AST", "cc1"])
COH = {"old": feats(sem_old), "new": feats(cpf.sem)}
TRAIN = {"old": load_pf(BK), "new": load_pf(os.path.join(DATA, "pair_features.csv"))}
UNTOUCHED = os.environ.get("DIAG_UNTOUCHED") == "1"
if UNTOUCHED:   # drop every train/val pair that contains a 2-window snippet: old and new features are then identical
    _B = pickle.load(open(os.path.join(DATA, "snippet_feats.pkl"), "rb"))
    _two = {k for k, v in _B.items() if len(v["win"]) == 2}
    for _t in TRAIN:
        for _sp in ("train", "val"):
            _d = TRAIN[_t][_sp]
            TRAIN[_t][_sp] = _d[~(_d.key1.isin(_two) | _d.key2.isin(_two))].reset_index(drop=True)
        print("untouched-only", _t, {sp: len(TRAIN[_t][sp]) for sp in ("train", "val")}, flush=True)

hon = {g: set(G[G.role == "honest"].id) for g, G in S.groupby("group")}
idx = {}
for g, G in P.groupby("group"):
    h = hon[g]; hh = G.index[G.id1.isin(h) & G.id2.isin(h)].values
    for d in M[M.group == g].itertuples():
        dm = G.index[(G.id1 == d.derived) | (G.id2 == d.derived)].values
        nd = np.array([i for i in dm if i != d.derived_pair and not ((P.id1[i] == d.src) or (P.id2[i] == d.src))])
        idx[(g, d.derived)] = (int(P.index[P.pair_id == d.derived_pair][0]), np.concatenate([hh, nd]))
M["ds"] = np.where(M.group.str.startswith("Progpedia"), "PROGpedia", "IR-Plag")
def auc(sc, ds):
    v = []
    for d in M[M.ds == ds].itertuples():
        dp, nd = idx[(d.group, d.derived)]; x = sc[nd]; v.append((x < sc[dp]).mean() + .5 * (x == sc[dp]).mean())
    return float(np.mean(v))

def job(a):
    tr_tag, seed = a
    tr, va = TRAIN[tr_tag]["train"], TRAIN[tr_tag]["val"]
    m, _, _ = train_model(arr(tr, X6), arr(tr, SC), tr.label.values, arr(va, X6), arr(va, SC), va.label.values, seed, True, LR, BS)
    out = {}
    for ct in ("old", "new"):
        s, w = score(m, arr(COH[ct], X6), arr(COH[ct], SC), True)
        out[ct] = (s, w)
    return tr_tag, seed, out

if __name__ == "__main__":
    import torch
    torch.set_num_threads(1)
    with Pool(8) as p:
        res = p.map(job, [(t, s) for t in ("old", "new") for s in SEEDS])
    out = {}
    for tr_tag in ("old", "new"):
        for ct in ("old", "new"):
            r = [x for x in res if x[0] == tr_tag]
            per = [auc(x[2][ct][0], "PROGpedia") for x in r]
            w = np.mean([x[2][ct][1].mean(0) for x in r], 0)
            out["train_%s|cohort_%s" % (tr_tag, ct)] = dict(prog_auc=round(float(np.mean(per)), 3), prog_per_seed=[round(v, 3) for v in per],
                                                       irplag_auc=round(float(np.mean([auc(x[2][ct][0], "IR-Plag") for x in r])), 3),
                                                       mean_weights_sem_str_syn=[round(float(v), 3) for v in w])
            print("train", tr_tag, "cohort", ct, out["train_%s|cohort_%s" % (tr_tag, ct)], flush=True)
    for ct in ("old", "new"):
        f = COH[ct]; print("cohort", ct, "mean S_sem %.3f S_ast %.3f S_tok %.3f" % (f.S_CodeBERT.mean(), f.S_AST.mean(), f.S_Token.mean()))
    for tg in ("old", "new"):
        t = TRAIN[tg]["train"]; print("train", tg, "mean S_sem pos %.3f neg %.3f" % (t[t.label == 1].S_CodeBERT.mean(), t[t.label == 0].S_CodeBERT.mean()))
    json.dump(out, open(os.path.join(HERE, "results_A", ("diag_collapse_untouched.json" if UNTOUCHED else "diag_collapse_2x2.json")), "w"), indent=1)
