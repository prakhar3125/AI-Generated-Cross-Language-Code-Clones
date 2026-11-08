import re
import pickle
import numpy as np
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModel
from tree_sitter import Language, Parser
import tree_sitter_python as tspy
import tree_sitter_java as tsjava
import tree_sitter_c as tsc
import tree_sitter_c_sharp as tscs

LOOP_TYPES = {'for_statement', 'while_statement', 'do_statement', 'foreach_statement'}
IF_TYPES = {'if_statement'}
ASSIGN_TYPES = {'assignment', 'assignment_expression'}
FUNC_TYPES = {'function_definition', 'method_declaration', 'local_function_statement', 'constructor_declaration'}
BINOP_TYPES = {'binary_expression', 'binary_operator', 'comparison_operator'}

LANGS = {
    'python': Language(tspy.language()),
    'java': Language(tsjava.language()),
    'c': Language(tsc.language()),
    'csharp': Language(tscs.language()),
}
PARSERS = {k: Parser(v) for k, v in LANGS.items()}


def ast_feature_vector(code, lang):
    tree = PARSERS[lang].parse(bytes(code, 'utf8'))
    counts = {'loop': 0, 'if': 0, 'assign': 0, 'func': 0, 'binop': 0}
    total = 0

    def walk(node):
        nonlocal total
        total += 1
        t = node.type
        if t in LOOP_TYPES:
            counts['loop'] += 1
        if t in IF_TYPES:
            counts['if'] += 1
        if t in ASSIGN_TYPES:
            counts['assign'] += 1
        if t in FUNC_TYPES:
            counts['func'] += 1
        if t in BINOP_TYPES:
            counts['binop'] += 1
        for ch in node.children:
            walk(ch)

    walk(tree.root_node)
    if total == 0:
        total = 1
    return np.array([counts['loop'], counts['if'], counts['assign'], counts['func'], counts['binop']],
                     dtype=float) / total


TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|[0-9]+\.?[0-9]*|==|!=|<=|>=|&&|\|\||[^\sA-Za-z0-9_]")


def kgrams(code, k=5):
    toks = TOKEN_RE.findall(code)
    if len(toks) < k:
        return {tuple(toks)} if toks else set()
    return {tuple(toks[i:i + k]) for i in range(len(toks) - k + 1)}


print("loading CodeBERT...")
tokenizer = AutoTokenizer.from_pretrained('microsoft/codebert-base')
model = AutoModel.from_pretrained('microsoft/codebert-base')
model.eval()


def codebert_embedding(code):
    enc = tokenizer(code, return_tensors='pt', truncation=True, max_length=512, padding=True)
    with torch.no_grad():
        out = model(**enc)
    hidden = out.last_hidden_state[0]
    mask = enc['attention_mask'][0].unsqueeze(-1).float()
    emb = (hidden * mask).sum(0) / mask.sum()
    return emb.numpy()


df = pd.read_csv('code_clones.csv')
print('problems:', len(df))

snippets = {}
for pid, row in df.iterrows():
    for lang in ['java', 'python', 'c', 'csharp']:
        snippets[(pid, lang)] = row[lang]

print('total snippets:', len(snippets))

embeddings = {}
ast_vecs = {}
kgram_sets = {}

t0 = None
import time
t0 = time.time()
for i, (key, code) in enumerate(snippets.items()):
    pid, lang = key
    embeddings[key] = codebert_embedding(code)
    ast_vecs[key] = ast_feature_vector(code, lang)
    kgram_sets[key] = kgrams(code, k=5)
    if (i + 1) % 200 == 0:
        elapsed = time.time() - t0
        rate = (i + 1) / elapsed
        eta = (len(snippets) - (i + 1)) / rate
        print(f"{i+1}/{len(snippets)}  elapsed={elapsed:.0f}s  eta={eta:.0f}s", flush=True)

print('done embedding, saving cache...')
with open('snippet_features_cache.pkl', 'wb') as f:
    pickle.dump({'embeddings': embeddings, 'ast_vecs': ast_vecs, 'kgram_sets': kgram_sets}, f)
print('saved snippet_features_cache.pkl')
