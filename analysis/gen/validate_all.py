import ast
import json
import os

GEN = r"C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen"

labels = ["claude-sonnet-5-5", "claude-sonnet-4-6", "gpt-6-sol", "gpt-5.4-mini"]

# load seeds
seeds = {}
for i in range(6):
    with open(GEN + "/seeds/chunk%d.json" % i, encoding="utf-8") as f:
        seeds[i] = json.load(f)

# verbatim-copy check helper: normalize whitespace
def norm(s):
    return "".join(s.split())

total_problems = []
for label in labels:
    for i in range(6):
        path = "%s/out/%s_chunk%d.json" % (GEN, label, i)
        if not os.path.exists(path):
            print("MISSING: %s_chunk%d" % (label, i))
            continue
        with open(path, encoding="utf-8") as f:
            items = json.load(f)
        seed_map = {s["id"]: s for s in seeds[i]}
        ids = [o["id"] for o in items]
        if len(ids) != 50:
            total_problems.append((label, i, "item count %d" % len(ids)))
        if len(set(ids)) != len(ids):
            total_problems.append((label, i, "duplicate ids"))
        for o in items:
            sid = o["id"]
            if sid not in seed_map:
                total_problems.append((label, i, "unknown id %s" % sid))
                continue
            s = seed_map[sid]
            if s["task"] == "translate":
                outs = o.get("outputs", {})
                if set(outs) != {"python", "c", "csharp"}:
                    total_problems.append((label, i, sid, "langs %s" % sorted(outs)))
                    continue
                for lang, snippet in outs.items():
                    if len(snippet.strip()) < 20:
                        total_problems.append((label, i, sid, lang, "too short"))
                    if lang == "python":
                        try:
                            ast.parse(snippet)
                        except SyntaxError as e:
                            total_problems.append((label, i, sid, "python SyntaxError: %s" % e))
            else:
                snippet = o.get("output", "")
                if not isinstance(snippet, str) or len(snippet.strip()) < 20:
                    total_problems.append((label, i, sid, "refactor bad"))
                if s["lang"] == "python":
                    try:
                        ast.parse(snippet)
                    except SyntaxError as e:
                        total_problems.append((label, i, sid, "python SyntaxError: %s" % e))
                if norm(snippet) == norm(s["code"]):
                    total_problems.append((label, i, sid, "VERBATIM COPY"))
        print("OK: %s_chunk%d (%d items)" % (label, i, len(items)))

print()
if total_problems:
    print("PROBLEMS (%d):" % len(total_problems))
    for p in total_problems:
        print(" ", p)
else:
    print("ALL EXISTING FILES VALID")
