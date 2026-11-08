import pickle
import numpy as np
import pandas as pd

rng = np.random.RandomState(42)

with open('snippet_features_cache.pkl', 'rb') as f:
    cache = pickle.load(f)
embeddings = cache['embeddings']
ast_vecs = cache['ast_vecs']
kgram_sets = cache['kgram_sets']

df = pd.read_csv('code_clones.csv')
n_problems = len(df)
LANGS = ['java', 'python', 'c', 'csharp']


def cosine(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def ast_similarity(fa, fb):
    d = np.linalg.norm(fa - fb)
    e = np.exp(-2 * d)
    c = cosine(fa, fb)
    return min(e, c)


def jaccard(sa, sb):
    if not sa and not sb:
        return 0.0
    inter = len(sa & sb)
    union = len(sa | sb)
    return inter / union if union else 0.0


def pair_features(key_a, key_b, d_lang):
    s_code = cosine(embeddings[key_a], embeddings[key_b])
    s_ast = ast_similarity(ast_vecs[key_a], ast_vecs[key_b])
    s_tok = jaccard(kgram_sets[key_a], kgram_sets[key_b])
    return s_code, s_ast, s_tok, d_lang, abs(s_code - s_ast), 1 - s_ast


# ---- Problem-grouped 70/15/15 split, decided FIRST ----
problem_ids = np.arange(n_problems)
rng.shuffle(problem_ids)
n_train = int(0.70 * n_problems)
n_val = int(0.15 * n_problems)
partitions = {
    'train': problem_ids[:n_train].tolist(),
    'val': problem_ids[n_train:n_train + n_val].tolist(),
    'test': problem_ids[n_train + n_val:].tolist(),
}
for k, v in partitions.items():
    print(k, 'problems:', len(v))

rows = []

# Positive pairs: all C(4,2)=6 cross-language pairs within each problem, tagged with its partition.
part_of = {}
for part, plist in partitions.items():
    for p in plist:
        part_of[p] = part

for pid in range(n_problems):
    part = part_of[pid]
    for i in range(len(LANGS)):
        for j in range(i + 1, len(LANGS)):
            la, lb = LANGS[i], LANGS[j]
            ka, kb = (pid, la), (pid, lb)
            s_code, s_ast, s_tok, d_lang, disagree, one_minus_ast = pair_features(ka, kb, 1.0)
            rows.append({
                'problem_id_a': pid, 'problem_id_b': pid, 'partition': part,
                'S_CodeBERT': s_code, 'S_AST': s_ast, 'S_Token': s_tok,
                'D_lang': d_lang,
                'S_CodeBERT_minus_S_AST': disagree, 'one_minus_S_AST': one_minus_ast,
                'label': 1,
            })

pos_counts = {p: sum(1 for r in rows if r['partition'] == p) for p in partitions}
print('positive pairs per partition:', pos_counts)

# Negative pairs: sampled WITHIN each partition only (both problems from the same partition),
# targeting the same count as that partition's positives (balanced 50/50), with the same
# ~74.7% cross-language / ~25.3% same-language composition as the real released data.
seen = set()

for part, plist in partitions.items():
    target = pos_counts[part]
    n_cross = round(target * 3962 / 5304)
    n_same = target - n_cross
    made = 0
    attempts = 0
    plist_arr = np.array(plist)
    while made < n_cross and attempts < n_cross * 100:
        attempts += 1
        pa, pb = rng.choice(plist_arr, size=2, replace=False)
        la, lb = LANGS[rng.randint(0, 4)], LANGS[rng.randint(0, 4)]
        if la == lb:
            continue
        key = tuple(sorted([(pa, la), (pb, lb)]))
        if key in seen:
            continue
        seen.add(key)
        ka, kb = (pa, la), (pb, lb)
        s_code, s_ast, s_tok, d_lang, disagree, one_minus_ast = pair_features(ka, kb, 1.0)
        rows.append({
            'problem_id_a': pa, 'problem_id_b': pb, 'partition': part,
            'S_CodeBERT': s_code, 'S_AST': s_ast, 'S_Token': s_tok,
            'D_lang': d_lang,
            'S_CodeBERT_minus_S_AST': disagree, 'one_minus_S_AST': one_minus_ast,
            'label': 0,
        })
        made += 1
    made_same = 0
    attempts = 0
    while made_same < n_same and attempts < n_same * 100:
        attempts += 1
        pa, pb = rng.choice(plist_arr, size=2, replace=False)
        la = lb = LANGS[rng.randint(0, 4)]
        key = tuple(sorted([(pa, la), (pb, lb)]))
        if key in seen:
            continue
        seen.add(key)
        ka, kb = (pa, la), (pb, lb)
        s_code, s_ast, s_tok, d_lang, disagree, one_minus_ast = pair_features(ka, kb, 0.0)
        rows.append({
            'problem_id_a': pa, 'problem_id_b': pb, 'partition': part,
            'S_CodeBERT': s_code, 'S_AST': s_ast, 'S_Token': s_tok,
            'D_lang': d_lang,
            'S_CodeBERT_minus_S_AST': disagree, 'one_minus_S_AST': one_minus_ast,
            'label': 0,
        })
        made_same += 1
    print(part, 'negatives made: cross=%d same=%d target=%d' % (made, made_same, target))

full = pd.DataFrame(rows)
full.to_csv('leakage_safe_balanced_features.csv', index=False)
print('total pairs:', len(full))
print(full.groupby('partition')['label'].value_counts())
