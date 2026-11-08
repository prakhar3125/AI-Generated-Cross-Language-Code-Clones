import ast
import json

GEN = r"C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen"
OUT = GEN + "/out/gpt-6-sol_chunk4.json"

namespace = {}
for part in ("part_g6s4_a", "part_g6s4_a1", "part_g6s4_a2", "part_g6s4_a3",
             "part_g6s4_a4", "part_g6s4_a5", "part_g6s4_a6", "part_g6s4_a7",
             "part_g6s4_a8", "part_g6s4_b1", "part_g6s4_b2", "part_g6s4_b3",
             "part_g6s4_b4", "part_g6s4_b5", "part_g6s4_b6", "part_g6s4_b7",
             "part_g6s4_b8", "part_g6s4_b9", "part_g6s4_b10", "part_g6s4_b11",
             "part_g6s4_b12", "part_g6s4_b13", "part_g6s4_c1", "part_g6s4_c2",
             "part_g6s4_c3", "part_g6s4_c4", "part_g6s4_c5", "part_g6s4_d1",
             "part_g6s4_d2", "part_g6s4_d3", "part_g6s4_d4", "part_g6s4_d5",
             "part_g6s4_d6"):
    with open(GEN + "/" + part + ".py", encoding="utf-8") as f:
        code = f.read()
    exec(compile(code, part + ".py", "exec"), namespace)

merged = {}
for key, value in namespace.items():
    if key.startswith("DATA") and isinstance(value, dict):
        merged.update(value)

with open(GEN + "/seeds/chunk4.json", encoding="utf-8") as f:
    seeds = json.load(f)

seed_ids = [s["id"] for s in seeds]
assert len(seed_ids) == len(set(seed_ids)), "duplicate seed ids"
missing = [i for i in seed_ids if i not in merged]
extra = [i for i in merged if i not in set(seed_ids)]
assert not missing, "missing ids: %s" % missing
assert not extra, "extra ids: %s" % extra

for s in seeds:
    item = merged[s["id"]]
    if s["task"] == "translate":
        outs = item["outputs"] if isinstance(item, dict) and "outputs" in item else item
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
    item = merged[s["id"]]
    if s["task"] == "translate":
        outputs = item["outputs"] if isinstance(item, dict) and "outputs" in item else item
        items.append({"id": s["id"], "outputs": outputs})
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
