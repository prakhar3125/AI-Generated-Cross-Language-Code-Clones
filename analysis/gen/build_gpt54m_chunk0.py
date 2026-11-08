# -*- coding: utf-8 -*-
"""Assembly builder for out/gpt-5.4-mini_chunk0.json. Run with: python -I <path>"""
import ast
import json
import os

GEN = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(GEN, "seeds", "chunk0.json")
OUT = os.path.join(GEN, "out", "gpt-5.4-mini_chunk0.json")

if os.path.exists(OUT):
    raise SystemExit("output already exists: %s" % OUT)

ns = {}
for i in range(1, 8):
    part = os.path.join(GEN, "build_gpt54m_p%d.py" % i)
    with open(part, "r", encoding="utf-8") as f:
        exec(compile(f.read(), part, "exec"), ns)

DATA = {}
for i in range(1, 8):
    for k, v in ns["DATA%d" % i].items():
        if k in DATA:
            raise SystemExit("duplicate key across parts: %s" % k)
        DATA[k] = v

with open(SEED, "r", encoding="utf-8") as f:
    seeds = json.load(f)

ids = [s["id"] for s in seeds]
assert len(ids) == len(set(ids)) == 50, "expected 50 unique seed ids"
missing = [i for i in ids if i not in DATA]
extra = [k for k in DATA if k not in ids]
assert not missing, "missing items: %s" % missing
assert not extra, "extra items: %s" % extra

items = []
for s in seeds:
    if s["task"] == "translate":
        out = DATA[s["id"]]
        assert set(out.keys()) == {"python", "c", "csharp"}, s["id"]
        for lang in ("python", "c", "csharp"):
            code = out[lang]
            assert isinstance(code, str) and len(code) >= 20, (s["id"], lang)
            if lang == "python":
                ast.parse(code)
        items.append({"id": s["id"], "outputs": {"python": out["python"], "c": out["c"], "csharp": out["csharp"]}})
    else:
        code = DATA[s["id"]]
        assert isinstance(code, str) and len(code) >= 20, s["id"]
        assert code.strip() != s["code"].strip(), s["id"]
        if s["lang"] == "python":
            ast.parse(code)
        items.append({"id": s["id"], "output": code})

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=True, indent=1)

with open(OUT, "r", encoding="utf-8") as f:
    reloaded = json.load(f)
assert len(reloaded) == 50, len(reloaded)
t = sum(1 for it in reloaded if "outputs" in it)
r = sum(1 for it in reloaded if "output" in it)
assert t == 25 and r == 25, (t, r)
print("OK: wrote %s with %d entries (%d translate, %d refactor)" % (OUT, len(reloaded), t, r))
