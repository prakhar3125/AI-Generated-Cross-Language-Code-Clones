# -*- coding: utf-8 -*-
"""E8 (part): tune the INTERNAL settings of JPlag (minimum token match) and Dolos (k-gram length / window) on the validation partition.

Scores every same-language validation and test pair of the benchmark under extra configurations (default configurations already exist in
jplag_scores*.csv and dolos_scores.csv); the best configuration per regime is selected by validation F1 (decision threshold tuned on validation as well).
python -I e8_tune_tools.py score   -> data/e8_tuned_scores.csv
python -I e8_tune_tools.py report  -> results_<R>/e8_tuned.json
"""
import csv
import json
import os
import pickle
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, HERE, PROJECT  # noqa: E402

JPLAG_T = [3, 5, 15]
DOLOS_KW = [(10, 8), (15, 12), (35, 25)]
IMG = "ghcr.io/dodona-edu/dolos-cli@sha256:64ca9827208a4893975a9a2adcc22a8f16c53341f773f4139c1410cf948930af"
W = os.path.join(PROJECT, "tools", "e8_work")
LANG = {"java": "java", "python": "python", "c": "c", "csharp": "c-sharp"}
EXT = {"java": "java", "python": "py", "c": "c", "csharp": "cs"}


def score():
    from run_jplag import EXT as JEXT, JAR, JAVA, LANG_ARG, wrap
    d = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
    d = d[d.split.isin(["val", "test"]) & (d.lang1 == d.lang2)].drop_duplicates("pair_id")
    S = pickle.load(open(os.path.join(DATA, "snippets.pkl"), "rb"))
    rows = []

    def jplag(job):
        lang, bi, recs, t = job
        root = os.path.join(W, "j_%s_%d_%d" % (lang, bi, t))
        shutil.rmtree(root, ignore_errors=True)
        sub = os.path.join(root, "subs")
        os.makedirs(sub)
        for pid, a, b in recs:
            for side, code in (("a", a), ("b", b)):
                dd = os.path.join(sub, "%s_%s" % (pid, side))
                os.makedirs(dd)
                with open(os.path.join(dd, "Main" + JEXT[lang]), "w", encoding="utf-8", newline="\n") as f:
                    f.write(wrap(code, lang))
        res = os.path.join(root, "res")
        cmd = [JAVA, "--enable-native-access=ALL-UNNAMED", "-jar", JAR, sub, "-l", LANG_ARG[lang], "-r", res, "-n", "-1", "--csv-export", "--cluster-skip", "--overwrite", "-M", "RUN", "-t", str(t)]
        subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        out = {}
        p = os.path.join(res, "results.csv")
        if os.path.exists(p):
            with open(p, newline="", encoding="utf-8") as f:
                rd = csv.reader(f)
                next(rd)
                for r in rd:
                    out[(r[0], r[1])] = float(r[2])
        res_ = [(pid, "jplag_t%d" % t, out.get(("%s_a" % pid, "%s_b" % pid), out.get(("%s_b" % pid, "%s_a" % pid), 0.0))) for pid, a, b in recs]
        shutil.rmtree(root, ignore_errors=True)
        return res_

    def dolos(job):
        lang, bi, recs, k, w = job
        root = os.path.join(W, "d_%s_%d_%d_%d" % (lang, bi, k, w))
        shutil.rmtree(root, ignore_errors=True)
        inp = os.path.join(root, "in")
        os.makedirs(inp)
        os.makedirs(os.path.join(root, "out"))
        names = []
        for pid, a, b in recs:
            for side, code in (("a", a), ("b", b)):
                fn = "%s_%s.%s" % (pid, side, EXT[lang])
                with open(os.path.join(inp, fn), "w", encoding="utf-8", newline="\n") as f:
                    f.write(wrap(code, lang))
                names.append(fn)
        cmd = ["docker", "run", "--rm", "-v", inp + ":/in:ro", "-v", os.path.join(root, "out") + ":/out", IMG, "run", "-l", LANG[lang], "-f", "csv", "-o", "/out/res", "-k", str(k), "-w", str(w)] + ["/in/" + n for n in names]
        subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        sims = {}
        p = os.path.join(root, "out", "res", "pairs.csv")
        if os.path.exists(p):
            with open(p, newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    a, b = os.path.basename(row["leftFilePath"]), os.path.basename(row["rightFilePath"])
                    sims[(a, b)] = sims[(b, a)] = float(row["similarity"])
        res_ = [(pid, "dolos_k%d_w%d" % (k, w), sims.get(("%s_a.%s" % (pid, EXT[lang]), "%s_b.%s" % (pid, EXT[lang])), 0.0)) for pid, a, b in recs]
        shutil.rmtree(root, ignore_errors=True)
        return res_

    from run_jplag import wrap  # noqa
    jobs_j, jobs_d = [], []
    for lang, g in d.groupby("lang1"):
        recs = [(r.pair_id, S[r.key1][1], S[r.key2][1]) for r in g.itertuples()]
        for bi in range(0, len(recs), 120):
            for t in JPLAG_T:
                jobs_j.append((lang, bi, recs[bi:bi + 120], t))
        for bi in range(0, len(recs), 100):
            for k, w in DOLOS_KW:
                jobs_d.append((lang, bi, recs[bi:bi + 100], k, w))
    os.makedirs(W, exist_ok=True)
    with ThreadPoolExecutor(3) as ex:
        fj = [ex.submit(jplag, j) for j in jobs_j]
        fd = [ex.submit(dolos, j) for j in jobs_d]
        for i, f in enumerate(fj + fd):
            rows += f.result()
            if i % 40 == 0:
                print(i, len(fj) + len(fd), flush=True)
    pd.DataFrame(rows, columns=["pair_id", "cfg", "sim"]).to_csv(os.path.join(DATA, "e8_tuned_scores.csv"), index=False)
    print("saved", len(rows))


def report():
    pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
    ts = pd.read_csv(os.path.join(DATA, "e8_tuned_scores.csv"))
    jp = pd.concat([pd.read_csv(os.path.join(DATA, f)) for f in ("jplag_scores.csv", "jplag_scores_hard.csv", "jplag_scores_tfidf.csv")], ignore_index=True)
    jp = jp[jp.cond == "plain"].drop_duplicates("pair_id").set_index("pair_id").col2.astype(float)
    dol = pd.read_csv(os.path.join(DATA, "dolos_scores.csv")).drop_duplicates("pair_id").set_index("pair_id").sim.astype(float)
    sims = {"jplag_default": jp, "dolos_default": dol}
    for c, g in ts.groupby("cfg"):
        sims[c] = g.drop_duplicates("pair_id").set_index("pair_id").sim
    NEG = {"A": "independent", "B": "hard_independent", "C": "tfidf_independent"}

    def f1(y, p):
        tp = ((p == 1) & (y == 1)).sum()
        return 2 * tp / max(2 * tp + ((p == 1) & (y == 0)).sum() + ((p == 0) & (y == 1)).sum(), 1)
    for r in "ABC":
        sel = ~pf.slice.isin({"independent", "hard_independent", "tfidf_independent"} - {NEG[r]})
        va, te = pf[sel & (pf.split == "val")], pf[sel & (pf.split == "test")]
        out = {}
        for c, s in sims.items():
            sv = np.where(va.D_lang.values == 0, va.pair_id.map(s).fillna(0).values, 0.0)
            st = np.where(te.D_lang.values == 0, te.pair_id.map(s).fillna(0).values, 0.0)
            best, bt = -1, 1e-9
            for t in np.arange(0, 1.0001, 0.005):
                f = f1(va.label.values, (sv >= t).astype(int))
                if f > best + 1e-12:
                    best, bt = f, max(t, 1e-9)
            p = (st >= bt).astype(int)
            out[c] = dict(val_f1=float(best), val_auc=float(roc_auc_score(va.label.values, sv)), test_f1=float(f1(te.label.values, p)), test_auc=float(roc_auc_score(te.label.values, st)), thr=float(bt))
        fam = {"jplag": [k for k in out if k.startswith("jplag")], "dolos": [k for k in out if k.startswith("dolos")]}
        out["selected"] = {f: max(ks, key=lambda k: out[k]["val_auc"]) for f, ks in fam.items()}   # validation AUROC: the validation F1 of JPlag is that of flagging every pair for every setting
        json.dump(out, open(os.path.join(HERE, "results_%s" % r, "e8_tuned.json"), "w"), indent=1)
        print(r, out["selected"], {k: (round(v["val_auc"], 3), round(v["test_f1"], 3), round(v["test_auc"], 3)) for k, v in out.items() if isinstance(v, dict) and "val_f1" in v})


if __name__ == "__main__":
    {"score": score, "report": report}[sys.argv[1]]()
