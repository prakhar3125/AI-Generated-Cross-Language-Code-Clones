import ast
import json

GEN = r"C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen"
OUT = GEN + "/out/gpt-6-sol_chunk3.json"

namespace = {}
for part in ("gpt6sol_c3_p1", "gpt6sol_c3_p2", "gpt6sol_c3_p3", "gpt6sol_c3_p4"):
    with open(GEN + "/" + part + ".py", encoding="utf-8") as f:
        code = f.read()
    exec(compile(code, part + ".py", "exec"), namespace)

merged = {}
for key, value in namespace.items():
    if key.startswith("DATA") and isinstance(value, dict):
        for item_id in value:
            assert item_id not in merged, "duplicate id across parts: " + item_id
        merged.update(value)

with open(GEN + "/seeds/chunk3.json", encoding="utf-8") as f:
    seeds = json.load(f)

seed_ids = [s["id"] for s in seeds]
assert len(seed_ids) == len(set(seed_ids)), "duplicate seed ids"
missing = [i for i in seed_ids if i not in merged]
extra = [i for i in merged if i not in set(seed_ids)]
assert not missing, "missing ids: %s" % missing
assert not extra, "extra ids: %s" % extra

def get_outputs(item):
    return item["outputs"] if "outputs" in item else item

ast_failures = 0
for s in seeds:
    item = merged[s["id"]]
    if s["task"] == "translate":
        outs = get_outputs(item)
        assert set(outs) == {"python", "c", "csharp"}, s["id"]
        for lang, snippet in outs.items():
            cleaned = snippet.strip()
            assert len(cleaned) >= 20, (s["id"], lang, len(cleaned))
            if lang == "python":
                try:
                    ast.parse(cleaned)
                except SyntaxError as e:
                    ast_failures += 1
                    print("AST FAIL %s/%s: %s" % (s["id"], lang, e))
    else:
        cleaned = item.strip()
        assert len(cleaned) >= 20, (s["id"], len(cleaned))
        if s["lang"] == "python":
            try:
                ast.parse(cleaned)
            except SyntaxError as e:
                ast_failures += 1
                print("AST FAIL %s: %s" % (s["id"], e))

assert ast_failures == 0, "ast failures: %d" % ast_failures

items = []
for s in seeds:
    item = merged[s["id"]]
    if s["task"] == "translate":
        items.append({"id": s["id"], "outputs": get_outputs(item)})
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
