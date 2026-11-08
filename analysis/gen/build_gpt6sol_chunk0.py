import ast
import json

GEN = "C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen"
OUT = GEN + "/out/gpt-6-sol_chunk0.json"

merged = {}
for part in ("gpt6sol_c0_p1", "gpt6sol_c0_p2", "gpt6sol_c0_p3", "gpt6sol_c0_p4",
             "gpt6sol_c0_p5", "gpt6sol_c0_p6", "gpt6sol_c0_p7"):
    with open(GEN + "/" + part + ".py", encoding="utf-8") as f:
        code = f.read()
    namespace = {}
    exec(compile(code, part + ".py", "exec"), namespace)
    for key, value in namespace.items():
        if key.startswith("DATA") and isinstance(value, dict):
            for item_id, item in value.items():
                if item_id in merged:
                    raise AssertionError("duplicate id across parts: " + item_id)
                merged[item_id] = item

with open(GEN + "/seeds/chunk0.json", encoding="utf-8") as f:
    seeds = json.load(f)

seed_ids = [s["id"] for s in seeds]
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
        for lang, snippet in outs.items():
            cleaned = snippet.strip()
            assert len(cleaned) >= 20, (s["id"], lang, len(cleaned))
            if lang == "python":
                ast.parse(cleaned)
        items.append({"id": s["id"], "outputs": outs})
    else:
        cleaned = item["output"].strip()
        assert len(cleaned) >= 20, (s["id"], len(cleaned))
        if s["lang"] == "python":
            ast.parse(cleaned)
        items.append({"id": s["id"], "output": item["output"]})

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=True, indent=1)

with open(OUT, encoding="utf-8") as f:
    check = json.load(f)
assert len(check) == 50
for o in check:
    assert "id" in o, o
    if o["id"].startswith("T"):
        assert set(o["outputs"]) == {"python", "c", "csharp"}, o["id"]
    else:
        assert isinstance(o["output"], str), o["id"]
print("OK: %d items written to %s" % (len(check), OUT))
