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


rows = []

# Positive pairs: all C(4,2)=6 cross-language pairs within each of the 884 problems.
for pid in range(n_problems):
    for i in range(len(LANGS)):
        for j in range(i + 1, len(LANGS)):
            la, lb = LANGS[i], LANGS[j]
            ka, kb = (pid, la), (pid, lb)
            s_code, s_ast, s_tok, d_lang, disagree, one_minus_ast = pair_features(ka, kb, 1.0)
            rows.append({
                'problem_id_a': pid, 'problem_id_b': pid,
                'S_CodeBERT': s_code, 'S_AST': s_ast, 'S_Token': s_tok,
                'D_lang': d_lang,
                'S_CodeBERT_minus_S_AST': disagree, 'one_minus_S_AST': one_minus_ast,
                'label': 1,
            })

print('positive pairs built:', len(rows))

# Negative pairs: 5304 pairs of DIFFERENT problems, ~74.7% cross-language / ~25.3% same-language,
# matching the real released data's negative D_lang composition.
n_neg = 5304
n_neg_cross = round(n_neg * 3962 / 5304)
n_neg_same = n_neg - n_neg_cross

seen = set()


def sample_neg(same_lang, target_count):
    made = 0
    attempts = 0
    while made < target_count and attempts < target_count * 50:
        attempts += 1
        pa, pb = rng.randint(0, n_problems, size=2)
        if pa == pb:
            continue
        if same_lang:
            la = lb = LANGS[rng.randint(0, 4)]
        else:
            la, lb = LANGS[rng.randint(0, 4)], LANGS[rng.randint(0, 4)]
            if la == lb:
                continue
        key = tuple(sorted([(pa, la), (pb, lb)]))
        if key in seen:
            continue
        seen.add(key)
        ka, kb = (pa, la), (pb, lb)
        s_code, s_ast, s_tok, d_lang, disagree, one_minus_ast = pair_features(ka, kb, 1.0 if la != lb else 0.0)
        rows.append({
            'problem_id_a': pa, 'problem_id_b': pb,
            'S_CodeBERT': s_code, 'S_AST': s_ast, 'S_Token': s_tok,
            'D_lang': d_lang,
            'S_CodeBERT_minus_S_AST': disagree, 'one_minus_S_AST': one_minus_ast,
            'label': 0,
        })
        made += 1
    return made


made_cross = sample_neg(False, n_neg_cross)
made_same = sample_neg(True, n_neg_same)
print('negative pairs built:', made_cross, '(cross-lang) +', made_same, '(same-lang)')

full = pd.DataFrame(rows)
full.to_csv('leakage_safe_features.csv', index=False)
print('total pairs:', len(full))
print(full['label'].value_counts())

# ---- Problem-grouped 70/15/15 split ----
problem_ids = np.arange(n_problems)
rng.shuffle(problem_ids)
n_train = int(0.70 * n_problems)
n_val = int(0.15 * n_problems)
train_probs = set(problem_ids[:n_train].tolist())
val_probs = set(problem_ids[n_train:n_train + n_val].tolist())
test_probs = set(problem_ids[n_train + n_val:].tolist())
print('problems: train', len(train_probs), 'val', len(val_probs), 'test', len(test_probs))


def assign_partition(row):
    a, b = row['problem_id_a'], row['problem_id_b']
    if a in train_probs and b in train_probs:
        return 'train'
    if a in val_probs and b in val_probs:
        return 'val'
    if a in test_probs and b in test_probs:
        return 'test'
    return 'drop'  # negative pair spanning two different partitions -- excluded to avoid leakage


full['partition'] = full.apply(assign_partition, axis=1)
print(full['partition'].value_counts())
full.to_csv('leakage_safe_features.csv', index=False)
print('saved leakage_safe_features.csv with partition column')
