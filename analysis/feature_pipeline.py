# -*- coding: utf-8 -*-
"""Per-snippet feature extraction for the three experts (one pass, cached).

This is a faithful port of repo/extract_features.py (the implementation the
released checkpoint was trained with) to the tree-sitter >= 0.22 API, with two
efficiency changes that do not alter the definition of any score:

  * every snippet is processed once and cached, instead of once per pair;
  * CodeBERT windows are encoded in padded batches (attention-masked, so the
    result equals the unbatched computation up to floating-point tolerance).

Per snippet we store
  win   : (n_windows, 768) mean-pooled CodeBERT window embeddings of the
          core-algorithm text (512-token windows, 25% overlap)
  grams : set of 5-grams of tree-sitter leaf tokens (comments / literals dropped)
  ast   : the 8-dimensional normalised AST feature vector
  cc    : McCabe cyclomatic complexity (1 + decision points)

python -I feature_pipeline.py [--limit N]
"""
import argparse
import ast as pyast
import os
import pickle
import re
import sys
import time
from collections import Counter

import numpy as np
import torch
import tree_sitter_c as tsc
import tree_sitter_c_sharp as tscs
import tree_sitter_java as tsjava
import tree_sitter_python as tspy
from tree_sitter import Language, Parser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, REPO  # noqa: E402

sys.setrecursionlimit(5000)

PARSERS = {
    "python": Parser(Language(tspy.language())),
    "java": Parser(Language(tsjava.language())),
    "c": Parser(Language(tsc.language())),
    "csharp": Parser(Language(tscs.language())),
}


def _load_universal_map():
    src = open(os.path.join(REPO, "extract_features.py"), encoding="utf8").read()
    a = src.index("UNIVERSAL_MAP = {")
    b = src.index("\n}", a)
    return pyast.literal_eval(src[a + len("UNIVERSAL_MAP = "):b + 2])


UNIVERSAL_MAP = _load_universal_map()


# ------------------------------------------------------------------ core text
def core_text(code, lang):
    try:
        tree = PARSERS[lang].parse(bytes(code, "utf8"))
        segs = []

        def walk(node):
            if node.type in ("method_declaration", "function_definition", "function_declaration"):
                for ch in node.children:
                    if ch.type in ("block", "compound_statement", "suite"):
                        body = ch.text.decode("utf8", errors="ignore").strip()
                        if len(body) > 20:
                            segs.append(body)
            for ch in node.children:
                walk(ch)

        walk(tree.root_node)
        if segs:
            return "\n\n".join(segs)
        lines = [l for l in code.split("\n") if not (
            l.strip().startswith(("import ", "package ", "using ", "#include", "from "))
            or (l.strip().startswith("//") and len(l.strip()) < 50)
            or (l.strip().startswith("#") and len(l.strip()) < 50))]
        return "\n".join(lines)
    except Exception:
        return code


# ------------------------------------------------------------------ token grams
_SKIP = {"comment", "string_literal", "number_literal", "integer_literal", "float_literal",
         "boolean_literal", "null_literal"}


def leaf_tokens(code, lang):
    toks = []
    tree = PARSERS[lang].parse(bytes(code, "utf8"))

    def trav(node):
        if node.type in _SKIP:
            return
        if not node.children:
            t = node.text.decode("utf8", errors="ignore").strip()
            if t:
                toks.append(t)
        else:
            for c in node.children:
                trav(c)

    trav(tree.root_node)
    return toks


def kgrams(toks, k=5):
    if len(toks) < k:
        return frozenset()
    return frozenset(tuple(toks[i:i + k]) for i in range(len(toks) - k + 1))


# ------------------------------------------------------------------ AST vector
def ast_vector(code, lang):
    """8-d vector exactly as extract_features.get_ast_sim builds it."""
    tree = PARSERS[lang].parse(bytes(code, "utf8"))
    nodes = []          # (raw_type, parent, [child ids])
    q = [(tree.root_node, -1)]
    qi = 0
    while qi < len(q):
        node, parent = q[qi]
        qi += 1
        nid = len(nodes)
        nodes.append([node.type, parent, []])
        if parent != -1:
            nodes[parent][2].append(nid)
        for ch in node.children:
            q.append((ch, nid))
    total = len(nodes)
    feats = Counter()
    uniq = set()
    branch_nodes = total_branches = 0
    for raw, _, kids in nodes:
        nt = UNIVERSAL_MAP.get(raw, raw)
        feats[nt] += 1
        uniq.add(nt)
        if "Loop" in nt or "If" in nt:
            branch_nodes += 1
            b = 0
            for c in kids:
                ct = nodes[c][0]
                if "statement" in ct or "block" in ct or "suite" in ct:
                    b += 1
            total_branches += b
    depth = [0] * total
    max_depth = 0
    for i in range(1, total):
        depth[i] = depth[nodes[i][1]] + 1
        max_depth = max(max_depth, depth[i])
    avg_branches = total_branches / branch_nodes if branch_nodes else 0.0
    t = max(total, 1)
    return np.array([
        feats.get("Loop", 0) / t, feats.get("If", 0) / t, feats.get("Function", 0) / t,
        feats.get("Assign", 0) / t, feats.get("BinaryOp", 0) / t,
        min(max_depth / 20.0, 1.0), min(avg_branches / 5.0, 1.0), min(len(uniq) / 50.0, 1.0),
    ], dtype=np.float64)


# ------------------------------------------------------------------ McCabe CC
_DECISION = {
    "if_statement", "elif_clause", "for_statement", "enhanced_for_statement", "foreach_statement",
    "for_in_clause", "while_statement", "do_statement", "catch_clause", "except_clause",
    "case_statement", "switch_label", "switch_rule", "switch_section", "switch_expression_arm",
    "conditional_expression", "ternary_expression", "for_range_loop",
}


def cyclomatic(code, lang):
    tree = PARSERS[lang].parse(bytes(code, "utf8"))
    n = 0
    stack = [tree.root_node]
    while stack:
        node = stack.pop()
        t = node.type
        if t in _DECISION:
            n += 1
        elif t == "boolean_operator":                      # python and / or
            n += 1
        elif t == "binary_expression":
            op = node.child_by_field_name("operator")
            if op is not None and op.text in (b"&&", b"||"):
                n += 1
        stack.extend(node.children)
    return 1 + n


# ------------------------------------------------------------------ CodeBERT
def load_codebert():
    from transformers import AutoModel, AutoTokenizer
    tok = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    mdl = AutoModel.from_pretrained("microsoft/codebert-base").eval()
    return tok, mdl


def window_ids(tok, text, window=512, overlap=0.25):
    ids = tok.encode(text, add_special_tokens=False, truncation=False)
    cls_id, sep_id = tok.cls_token_id, tok.sep_token_id
    if not ids:
        return []
    if len(ids) <= window - 2:
        return [[cls_id] + ids + [sep_id]]
    stride = max(1, int(window * (1.0 - overlap)))
    out = []
    for s in range(0, len(ids), stride):
        sub = ids[s:s + window - 2]
        if sub:
            out.append([cls_id] + sub + [sep_id])
    return out


@torch.inference_mode()
def encode_windows(mdl, tok, wins, max_tokens=12000):
    """wins: list of id-lists -> (n, 768) float32 in the original order."""
    order = sorted(range(len(wins)), key=lambda i: len(wins[i]))
    out = np.zeros((len(wins), mdl.config.hidden_size), dtype=np.float32)
    i = 0
    t0 = time.time()
    while i < len(order):
        bs = 1
        while i + bs < len(order) and (bs + 1) * len(wins[order[i + bs]]) <= max_tokens and bs < 128:
            bs += 1
        idx = order[i:i + bs]
        maxlen = max(len(wins[j]) for j in idx)
        ids = torch.full((len(idx), maxlen), tok.pad_token_id, dtype=torch.long)
        att = torch.zeros((len(idx), maxlen), dtype=torch.long)
        for r, j in enumerate(idx):
            ids[r, :len(wins[j])] = torch.tensor(wins[j])
            att[r, :len(wins[j])] = 1
        h = mdl(input_ids=ids, attention_mask=att).last_hidden_state
        m = att.unsqueeze(-1).float()
        out[idx] = ((h * m).sum(1) / m.sum(1).clamp(min=1e-9)).numpy()
        i += bs
        if (i // 1500) != ((i - bs) // 1500):
            print("  encoded %d / %d windows (%.0fs)" % (i, len(order), time.time() - t0), flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--snippets", default=os.path.join(DATA, "snippets.pkl"))
    ap.add_argument("--out", default=os.path.join(DATA, "snippet_feats.pkl"))
    a = ap.parse_args()
    torch.set_num_threads(12)
    with open(a.snippets, "rb") as f:
        snips = pickle.load(f)
    keys = sorted(snips)
    if a.limit:
        keys = keys[:a.limit]
    print("snippets:", len(keys), flush=True)
    t0 = time.time()
    rec = {}
    for n, k in enumerate(keys):
        lang, code = snips[k]
        rec[k] = dict(lang=lang,
                      grams=kgrams(leaf_tokens(code, lang)),
                      ast=ast_vector(code, lang),
                      cc=cyclomatic(code, lang),
                      ntok=len(leaf_tokens(code, lang)))
        if n % 2000 == 0:
            print("  parsed", n, "%.0fs" % (time.time() - t0), flush=True)
    tok, mdl = load_codebert()
    wins, owner = [], []
    for k in keys:
        lang, code = snips[k]
        ws = window_ids(tok, core_text(code, lang))
        if not ws:
            rec[k]["win"] = np.zeros((1, mdl.config.hidden_size), dtype=np.float32)
            continue
        for w in ws:
            wins.append(w)
            owner.append(k)
    print("windows:", len(wins), "(snippets %d)" % len(keys), flush=True)
    emb = encode_windows(mdl, tok, wins)
    tmp = {}
    for e, k in zip(emb, owner):
        tmp.setdefault(k, []).append(e)
    for k, v in tmp.items():
        rec[k]["win"] = np.vstack(v)
    with open(a.out, "wb") as f:
        pickle.dump(rec, f)
    print("saved", a.out, "in %.0fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
