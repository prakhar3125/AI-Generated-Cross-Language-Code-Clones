import ast
import json
import os
import sys

GEN = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(GEN, "seeds", "chunk5.json")
OUT = os.path.join(GEN, "out", "claude-sonnet-5-5_chunk5.json")

items = []
for name in ("part_t1.py", "part_t2.py", "part_t3.py", "part_r1.py", "part_r2.py", "part_r3.py"):
    with open(os.path.join(GEN, name), encoding="utf-8") as f:
        source = f.read()
    namespace = {}
    exec(compile(source, name, "exec"), namespace)
    items.extend(namespace["PART"])

with open(SEED, encoding="utf-8") as f:
    seed = json.load(f)

seed_ids = [entry["id"] for entry in seed]
out_ids = [entry["id"] for entry in items]

assert len(out_ids) == len(set(out_ids)), "duplicate ids in output"
assert sorted(seed_ids) == sorted(out_ids), "id mismatch vs seed"

for entry in items:
    if entry["task"] == "translate":
        for lang in ("python", "c", "csharp"):
            code = entry["outputs"][lang]
            assert len(code) >= 20, "too short: %s %s" % (entry["id"], lang)
    else:
        assert len(entry["output"]) >= 20, "too short: %s" % entry["id"]

python_refactor_ids = {"R4a34d3a4cc", "R1cabb3fa54", "R17e5e197a9", "R1ab11e56ab", "Rfbf7d4f5c2", "R63b6384687", "Rda752e8442"}
for entry in items:
    if entry["task"] == "translate":
        ast.parse(entry["outputs"]["python"])
    elif entry["task"] == "refactor" and entry["id"] in python_refactor_ids:
        ast.parse(entry["output"])

clean = []
for entry in items:
    if entry["task"] == "translate":
        clean.append({"id": entry["id"], "outputs": entry["outputs"]})
    else:
        clean.append({"id": entry["id"], "output": entry["output"]})

if os.path.exists(OUT):
    sys.exit("refusing to overwrite existing output")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(clean, f, indent=1)

print("OK: wrote %d entries to %s" % (len(items), OUT))
