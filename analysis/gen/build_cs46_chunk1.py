import ast
import json

GEN = r"C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen"
OUT = GEN + "/out/claude-sonnet-4-6_chunk1.json"

namespace = {}
for part in ("build_cs46_c1_p1", "build_cs46_c1_p2", "build_cs46_c1_p3", "build_cs46_c1_p4",
             "build_cs46_c1_p5", "build_cs46_c1_p6", "build_cs46_c1_p7", "build_cs46_c1_p8"):
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

items = []
for s in seeds:
    item = merged[s["id"]]
    if s["task"] == "translate":
        outs = item["outputs"]
        assert set(outs) == {"python", "c", "csharp"}, s["id"]
        cleaned_outs = {}
        for lang, snippet in outs.items():
            cleaned = snippet.strip()
            assert len(cleaned) >= 20, (s["id"], lang, len(cleaned))
            if lang == "python":
                ast.parse(cleaned)
            cleaned_outs[lang] = cleaned
        items.append({"id": s["id"], "outputs": cleaned_outs})
    else:
        cleaned = item.strip()
        assert len(cleaned) >= 20, (s["id"], len(cleaned))
        if s["lang"] == "python":
            ast.parse(cleaned)
        items.append({"id": s["id"], "output": cleaned})

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
