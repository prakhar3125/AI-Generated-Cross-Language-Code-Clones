# -*- coding: utf-8 -*-
"""E4 (build): attack A1 on same-language benchmark pairs: every identifier DECLARED in the second snippet (variables, parameters, functions, classes) is renamed to a
canonical v0, v1, ... and string / character literals are masked; library names, keywords and structure are untouched.  A1 is a pure lexical transformation applied
to the second snippet of positives AND of negatives, so that 'attackedness' carries no label information.  No execution check is made (no tests are available for the
benchmark snippets); the label of a positive is preserved by construction only to the extent that renaming declared identifiers preserves behaviour.

python -I e4_build.py -> data/e4_snippets.pkl (attacked snippets), data/e4_pairs.csv ; then run feature_pipeline.py and encode_unixcoder on the new pickle
"""
import os
import pickle
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, skey  # noqa: E402
from feature_pipeline import PARSERS  # noqa: E402

DECL_PARENT = {
    "java": {"variable_declarator": "name", "formal_parameter": "name", "method_declaration": "name", "class_declaration": "name", "enhanced_for_statement": "name",
             "catch_formal_parameter": "name", "lambda_expression": None},
    "csharp": {"variable_declarator": None, "parameter": "name", "method_declaration": "name", "class_declaration": "name", "foreach_statement": "left"},
    "c": {},
    "python": {"function_definition": "name", "class_definition": "name"},
}
STR_RE = re.compile(r'"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'')


def declared_names(code, lang):
    tree = PARSERS[lang].parse(bytes(code, "utf8"))
    names = set()

    def ident(n):
        return n.text.decode("utf8", "ignore") if n is not None and n.type == "identifier" else None

    def declarator_name(n):
        # descend through pointer/array/function declarators in C
        while n is not None and n.type in ("pointer_declarator", "array_declarator", "function_declarator", "init_declarator", "parenthesized_declarator"):
            n = n.child_by_field_name("declarator")
        return ident(n)

    def walk(n):
        t = n.type
        if lang in ("java", "csharp"):
            if t in DECL_PARENT[lang]:
                f = DECL_PARENT[lang][t]
                c = n.child_by_field_name(f) if f else (n.children[0] if n.children else None)
                x = ident(c)
                if x:
                    names.add(x)
        elif lang == "python":
            if t in DECL_PARENT["python"]:
                x = ident(n.child_by_field_name("name"))
                if x:
                    names.add(x)
            elif t == "parameters":
                for c in n.children:
                    x = ident(c) or ident(c.child_by_field_name("name") if c.type in ("default_parameter", "typed_parameter", "typed_default_parameter") else None) \
                        or (ident(c.children[0]) if c.type in ("typed_parameter",) and c.children else None)
                    if x:
                        names.add(x)
            elif t in ("assignment", "augmented_assignment", "for_statement"):
                left = n.child_by_field_name("left")
                if left is not None:
                    for c in ([left] if left.type == "identifier" else left.children):
                        x = ident(c)
                        if x:
                            names.add(x)
        else:  # c
            if t in ("init_declarator", "parameter_declaration", "function_definition"):
                x = declarator_name(n.child_by_field_name("declarator"))
                if x:
                    names.add(x)
            elif t == "declaration":
                for c in n.children:
                    if c.type in ("identifier", "pointer_declarator", "array_declarator", "init_declarator"):
                        x = declarator_name(c) or ident(c)
                        if x:
                            names.add(x)
        for c in n.children:
            walk(c)

    walk(tree.root_node)
    names -= {"main", "self", "cls", "__init__", "Main", "args"}
    return names


def attack(code, lang):
    names = declared_names(code, lang)
    if not names:
        return None
    order = {}
    # rename by order of first appearance
    for m in re.finditer(r"[A-Za-z_][A-Za-z0-9_]*", code):
        w = m.group(0)
        if w in names and w not in order:
            order[w] = "v%d" % len(order)
    pieces, last = [], 0
    out = []
    for m in STR_RE.finditer(code):
        out.append(("code", code[last:m.start()]))
        q = m.group(0)[0]
        out.append(("lit", q + "s" + q))
        last = m.end()
    out.append(("code", code[last:]))
    res = "".join(re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*\b", lambda m: order.get(m.group(0), m.group(0)), t) if k == "code" else t for k, t in out)
    return res


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    pf = pd.read_csv(os.path.join(DATA, "pair_features.csv"))
    S = pickle.load(open(os.path.join(DATA, "snippets.pkl"), "rb"))
    te = pf[(pf.split == "test") & (pf.D_lang == 0)]
    pools = {"pos": te[te.slice == "refactored"], "negA": te[te.slice == "independent"], "negB": te[te.slice == "hard_independent"]}
    rows, snips = [], {}
    for kind, df in pools.items():
        df = df.sample(frac=1.0, random_state=0)
        n = 0
        for r in df.itertuples():
            lang, code = S[r.key2]
            a = attack(code, lang)
            if a is None or a == code:
                continue
            k = skey(lang, a)
            snips[k] = (lang, a)
            rows.append(dict(pair_id="E4%05d" % len(rows), kind=kind, label=int(kind == "pos"), lang1=r.lang1, lang2=r.lang2, key1=r.key1, key2=r.key2, akey2=k, orig_pair=r.pair_id, D_lang=0))
            n += 1
            if n >= 300:
                break
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(DATA, "e4_pairs.csv"), index=False)
    pickle.dump(snips, open(os.path.join(DATA, "e4_snippets.pkl"), "wb"))
    print(out.groupby(["kind", "lang1"]).size().unstack(fill_value=0), len(snips))
    k = out.iloc[0]
    print(S[k.key2][1][:400]); print("-----"); print(snips[k.akey2][1][:400])
