"""Export the snippet text behind every pair table as plain JSONL (one object per line: key, lang, code),
so the dataset can be inspected without unpickling. Reads analysis/data/*.pkl; writes ../dataset/snippets/*.jsonl.
Run: python -I export_dataset.py"""
import json, os, pickle
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "dataset", "snippets")
os.makedirs(OUT, exist_ok=True)
SETS = {
    "snippets.pkl": "benchmark_snippets.jsonl",              # GPTCloneBench snippets (pairs.csv keys key1/key2)
    "probe2_snippets.pkl": "generator_probe_snippets.jsonl",  # four-model probe seeds + outputs (probe2_pairs.csv)
    "cohort_snippets.pkl": "cohort_snippets.jsonl",          # PROGpedia + IR-Plag cohorts (cohort_pairs.csv)
    "progpedia_snippets.pkl": "progpedia_snippets.jsonl",    # PROGpedia same-author / cross-author check (progpedia_pairs.csv)
    "e4_snippets.pkl": "attack_a1_snippets.jsonl",            # renamed / masked second snippets of the lexical attack (e4_pairs.csv akey2)
    "xl2_cohort_snippets.pkl": "cross_language_cohort_snippets.jsonl",  # 100 cross-language cohorts (xl2_cohort_pairs.csv)
}
for src, dst in SETS.items():
    d = pickle.load(open(os.path.join(HERE, "data", src), "rb"))
    with open(os.path.join(OUT, dst), "w", encoding="utf8", newline="\n") as f:
        for k in sorted(d):
            lang, code = d[k][0], d[k][1]
            f.write(json.dumps({"key": k, "lang": lang, "code": code}, ensure_ascii=False) + "\n")
    print(dst, len(d))
