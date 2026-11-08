import ast
import json

GEN = r"C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen"
OUT = GEN + "/out/claude-sonnet-4-6_chunk4.json"

parts = ["build_cs46_chunk4_p1", "build_cs46_chunk4_p2", "build_cs46_chunk4_p3",
         "build_cs46_chunk4_p4", "build_cs46_chunk4_p5", "build_cs46_chunk4_p6"]

merged = {}
for name in parts:
    with open(GEN + "/" + name + ".py", encoding="utf-8") as f:
        ns = {}
        exec(compile(f.read(), name + ".py", "exec"), ns)
    for key, value in ns.items():
        if key.startswith("DATA"):
            for item_id, payload in value.items():
                if item_id in merged:
                    raise SystemExit("duplicate item: " + item_id)
                merged[item_id] = payload

with open(GEN + "/seeds/chunk4.json", encoding="utf-8") as f:
    seeds = json.load(f)

seed_ids = [s["id"] for s in seeds]
missing = [i for i in seed_ids if i not in merged]
extra = [i for i in merged if i not in set(seed_ids)]
assert not missing, "missing ids: %s" % missing
assert not extra, "extra ids: %s" % extra

items = []
for s in seeds:
    payload = merged[s["id"]]
    if s["task"] == "translate":
        outs = payload["outputs"] if isinstance(payload, dict) and "outputs" in payload else payload
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
        cleaned = payload.strip()
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
    assert "id" in o
    if o["id"].startswith("T"):
        assert set(o["outputs"]) == {"python", "c", "csharp"}, o["id"]
        for lang, code in o["outputs"].items():
            assert isinstance(code, str) and len(code) >= 20, (o["id"], lang)
    else:
        assert isinstance(o["output"], str) and len(o["output"]) >= 20, o["id"]
print("OK: %d items written to %s" % (len(check), OUT))
