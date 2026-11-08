# -*- coding: utf-8 -*-
"""Shared paths and helpers for the problem-grouped evaluation protocol."""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PROJECT = os.path.dirname(REPO)
DATA = os.path.join(HERE, "data")
EVAL_DIR = os.path.join(PROJECT, "eval_dataset")
BUILD_DIR = r"C:/Users/prakhar.sinha/Projects/GPTCloneBench_build"
RELEASE = r"C:/Users/prakhar.sinha/Downloads/GPTCloneBench_extracted/GPTCloneBench/standalone"
TSC = os.path.join(RELEASE, "true_semantic_clones")
FSC = os.path.join(RELEASE, "false_semantic_clones")

CANON = {"java": "java", "py": "python", "c": "c", "cs": "csharp"}
LANGS = ["java", "python", "c", "csharp"]
SEED = 42

os.makedirs(DATA, exist_ok=True)
if BUILD_DIR not in sys.path:
    sys.path.insert(0, BUILD_DIR)


def read(p):
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def split_two(txt):
    """Split a standalone release file into snippets (runs of >=2 blank lines)."""
    parts, cur, blanks = [], [], 0
    for line in txt.splitlines():
        if line.strip() == "":
            blanks += 1
        else:
            if blanks >= 2 and cur:
                parts.append("\n".join(cur))
                cur = []
            blanks = 0
            cur.append(line)
    if cur:
        parts.append("\n".join(cur))
    return parts


def two_snippets(txt):
    parts = split_two(txt)
    if len(parts) < 2:
        return None
    if len(parts) > 2:
        parts = sorted(parts, key=len, reverse=True)[:2]
    s1, s2 = parts[0].strip(), parts[1].strip()
    if len(s1) < 20 or len(s2) < 20:
        return None
    return s1, s2


def skey(lang, code):
    """Snippet identity: language + whitespace-normalised text hash."""
    h = hashlib.md5(re.sub(r"\s+", " ", code.strip()).encode("utf8")).hexdigest()[:16]
    return "%s:%s" % (lang, h)


class UnionFind:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        r = x
        while self.p[r] != r:
            r = self.p[r]
        while self.p[x] != r:
            self.p[x], x = r, self.p[x]
        return r

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb
