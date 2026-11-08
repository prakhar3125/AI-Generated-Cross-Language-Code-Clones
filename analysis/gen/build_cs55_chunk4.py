import ast
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_cs55_chunk4_part1 import TRANSLATIONS_A
from build_cs55_chunk4_part2 import TRANSLATIONS_B
from build_cs55_chunk4_part3 import TRANSLATIONS_C, REFACTORS_A
from build_cs55_chunk4_part4 import REFACTORS_B

OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "claude-sonnet-5-5_chunk4.json")
SEED_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seeds", "chunk4.json")


def main():
    translations = {}
    translations.update(TRANSLATIONS_A)
    translations.update(TRANSLATIONS_B)
    translations.update(TRANSLATIONS_C)
    refactors = {}
    refactors.update(REFACTORS_A)
    refactors.update(REFACTORS_B)

    with open(SEED_PATH, encoding="utf-8") as f:
        seeds = json.load(f)

    items = []
    errors = []
    seen_ids = set()
    for seed in seeds:
        sid = seed["id"]
        if sid in seen_ids:
            errors.append("duplicate id in output: %s" % sid)
            continue
        seen_ids.add(sid)
        if seed["task"] == "translate":
            if sid not in translations:
                errors.append("missing translation: %s" % sid)
                continue
            outs = translations[sid]
            for lang in ("python", "c", "csharp"):
                code = outs[lang]
                if len(code.strip()) < 20:
                    errors.append("too short: %s/%s" % (sid, lang))
                if lang == "python":
                    try:
                        ast.parse(code)
                    except SyntaxError as e:
                        errors.append("python parse fail %s: %s" % (sid, e))
            items.append({"id": sid, "outputs": outs})
        else:
            if sid not in refactors:
                errors.append("missing refactor: %s" % sid)
                continue
            code = refactors[sid]
            if len(code.strip()) < 20:
                errors.append("too short: %s" % sid)
            if seed["lang"] == "python":
                try:
                    ast.parse(code)
                except SyntaxError as e:
                    errors.append("python parse fail %s: %s" % (sid, e))
            items.append({"id": sid, "output": code})

    missing = [s["id"] for s in seeds if s["id"] not in seen_ids]
    if missing:
        errors.append("missing ids: %s" % missing)

    if errors:
        for err in errors:
            print("ERROR:", err)
        sys.exit(1)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)
    print("OK: wrote %d items to %s" % (len(items), OUT_PATH))


if __name__ == "__main__":
    main()
