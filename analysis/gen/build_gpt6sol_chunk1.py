import ast
import json

GEN = r"C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen"
OUT = GEN + "/out/gpt-6-sol_chunk1.json"

namespace = {}
for part in ("gpt6s_c1_t1", "gpt6s_c1_t2", "gpt6s_c1_t3", "gpt6s_c1_r1", "gpt6s_c1_r2"):
    with open(GEN + "/" + part + ".py", encoding="utf-8") as f:
        code = f.read()
    exec(compile(code, part + ".py", "exec"), namespace)

merged = {}
for key, value in namespace.items():
    if key.startswith("DATA") and isinstance(value, dict):
        merged.update(value)

with open(GEN + "/seeds/chunk1.json", encoding="utf-8") as f:
    seeds = json.load(f)

seed_ids = [s["id"] for s in seeds]
assert len(seed_ids) == len(set(seed_ids)), "duplicate seed ids"
missing = [i for i in seed_ids if i not in merged]
extra = [i for i in merged if i not in set(seed_ids)]
assert not missing, "missing ids: %s" % missing
assert not extra, "extra ids: %s" % extra

def as_translate(item):
    if isinstance(item, dict) and "outputs" not in item and set(item) == {"python", "c", "csharp"}:
        return {"outputs": item}
    return item

for s in seeds:
    item = as_translate(merged[s["id"]])
    if s["task"] == "translate":
        outs = item["outputs"]
        assert set(outs) == {"python", "c", "csharp"}, s["id"]
        for lang, snippet in outs.items():
            cleaned = snippet.strip()
            assert len(cleaned) >= 20, (s["id"], lang, len(cleaned))
            if lang == "python":
                ast.parse(cleaned)
    else:
        cleaned = item.strip()
        assert len(cleaned) >= 20, (s["id"], len(cleaned))
        if s["lang"] == "python":
            ast.parse(cleaned)

items = []
for s in seeds:
    item = as_translate(merged[s["id"]])
    if s["task"] == "translate":
        items.append({"id": s["id"], "outputs": item["outputs"]})
    else:
        items.append({"id": s["id"], "output": item})

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=True, indent=1)

with open(OUT, encoding="utf-8") as f:
    check = json.load(f)
assert len(check) == 50
for o in check:
    if o["id"].startswith("T"):
        assert set(o["outputs"]) == {"python", "c", "csharp"}, o["id"]
    else:
        assert isinstance(o["output"], str), o["id"]
print("OK: %d items written to %s" % (len(check), OUT))
