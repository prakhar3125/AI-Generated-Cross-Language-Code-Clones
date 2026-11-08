import ast
import json

GEN = "C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen"
OUT = GEN + "/out/gpt-5.4-mini_chunk4.json"

namespace = {}
for part in ("build_gpt54m_c4_p1", "build_gpt54m_c4_p2", "build_gpt54m_c4_p3",
             "build_gpt54m_c4_p4", "build_gpt54m_c4_p5", "build_gpt54m_c4_p6",
             "build_gpt54m_c4_p7", "build_gpt54m_c4_p8", "build_gpt54m_c4_p9"):
    with open(GEN + "/" + part + ".py", encoding="utf-8") as f:
        code = f.read()
    exec(compile(code, part + ".py", "exec"), namespace)

merged = {}
for key in ("DATA_T1", "DATA_T2", "DATA_T3", "DATA_T4", "DATA_T5",
            "DATA_R1", "DATA_R2", "DATA_R3", "DATA_R4"):
    merged.update(namespace[key])

with open(GEN + "/seeds/chunk4.json", encoding="utf-8") as f:
    seeds = json.load(f)

seed_ids = [s["id"] for s in seeds]
assert len(seed_ids) == len(set(seed_ids)), "duplicate seed ids"
missing = [i for i in seed_ids if i not in merged]
extra = [i for i in merged if i not in set(seed_ids)]
assert not missing, "missing ids: %s" % missing
assert not extra, "extra ids: %s" % extra

smap = {s["id"]: s for s in seeds}
items = []
for s in seeds:
    value = merged[s["id"]]
    if s["task"] == "translate":
        outs = value["outputs"]
        assert set(outs) == {"python", "c", "csharp"}, s["id"]
        for lang, snippet in outs.items():
            cleaned = snippet.strip()
            assert len(cleaned) >= 20, (s["id"], lang, len(cleaned))
            if lang == "python":
                ast.parse(cleaned)
        items.append({"id": s["id"], "outputs": {k: v.strip() for k, v in outs.items()}})
    else:
        cleaned = value.strip()
        assert len(cleaned) >= 20, (s["id"], len(cleaned))
        if s["lang"] == "python":
            ast.parse(cleaned)
        items.append({"id": s["id"], "output": cleaned})

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=True, indent=1)

with open(OUT, encoding="utf-8") as f:
    check = json.load(f)
assert len(check) == 50, len(check)
for o in check:
    assert "id" in o, o
    if o["id"].startswith("T"):
        assert set(o["outputs"]) == {"python", "c", "csharp"}, o["id"]
    else:
        assert isinstance(o["output"], str), o["id"]
print("OK: %d items written to %s" % (len(check), OUT))
