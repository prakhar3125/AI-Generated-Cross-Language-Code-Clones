import ast
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SEEDS = os.path.join(BASE, "seeds", "chunk3.json")
OUT = os.path.join(BASE, "out", "gpt-5.4-mini_chunk3.json")
PARTS = ["gpt54m_c3_p1.py", "gpt54m_c3_p2.py", "gpt54m_c3_p3.py", "gpt54m_c3_p4.py",
         "gpt54m_c3_p5.py", "gpt54m_c3_p6.py"]

with open(SEEDS, encoding="utf-8") as f:
    seeds = json.load(f)

merged = {}
for part in PARTS:
    ns = {}
    with open(os.path.join(BASE, part), encoding="utf-8") as f:
        exec(compile(f.read(), part, "exec"), ns)
    for name, data in ns.items():
        if name.startswith("DATA_"):
            merged.update(data)

errors = []
seen = set()
items = []
for s in seeds:
    sid = s["id"]
    if sid in seen:
        errors.append("duplicate seed id %s" % sid)
        continue
    seen.add(sid)
    if sid not in merged:
        errors.append("missing output for %s" % sid)
        continue
    item = merged[sid]
    if s["task"] == "translate":
        outs = item.get("outputs", {}) if isinstance(item, dict) and "outputs" in item else item
        if not isinstance(outs, dict):
            errors.append("%s translate output not a dict" % sid)
            continue
        for lang in ("python", "c", "csharp"):
            code = outs.get(lang, "")
            if len(code) < 20:
                errors.append("%s/%s too short" % (sid, lang))
            if lang == "python":
                try:
                    ast.parse(code)
                except SyntaxError as e:
                    errors.append("%s python parse: %s" % (sid, e))
        items.append({"id": sid, "outputs": outs})
    else:
        code = item if isinstance(item, str) else ""
        if len(code) < 20:
            errors.append("%s refactor too short" % sid)
        if code.strip() == s["code"].strip():
            errors.append("%s refactor verbatim copy" % sid)
        items.append({"id": sid, "output": code})

extra = set(merged) - seen
if extra:
    errors.append("unexpected outputs: %s" % sorted(extra))

if errors:
    print("VALIDATION ERRORS:")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=True, indent=1)
print("OK wrote %d items to %s" % (len(items), OUT))
