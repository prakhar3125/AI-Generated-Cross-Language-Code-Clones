# Requirements: pip install transformers torch torch-geometric tree-sitter==0.20.4 networkx numpy scikit-learn langid pandas tqdm
import pandas as pd
import itertools
import random
from tqdm import tqdm
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from tree_sitter import Language, Parser, Node
import os
import sys
import re
import argparse

from typing import List, Dict, Tuple, Any
from collections import Counter
import statistics
from functools import lru_cache
from sklearn.metrics.pairwise import cosine_similarity # Needed for semantic sim
from sklearn.cluster import DBSCAN # Needed for optional DBSCAN

# Prevent recursion depth issues
sys.setrecursionlimit(2000)

print("=" * 80)
print("FEATURE GENERATION SCRIPT FOR GATING NETWORK TRAINING (V9 - Corrected)")
print("=" * 80)

# -------------------------------
# 1. LOAD MODELS & PARSERS
# -------------------------------
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# --- Tree-sitter Initialization ---
LIB_PATH = 'build/my-languages.so'
if not os.path.exists(LIB_PATH):
    print(f"❌ CRITICAL ERROR: Tree-sitter library not found at '{LIB_PATH}'")
    sys.exit(1)
else:
    print(f"Found tree-sitter library: {LIB_PATH}")

LANG_NAME_MAP = {
    'java': 'java', 'python': 'python', 'c': 'c', 'csharp': 'c_sharp'
}
parsers = {}
print("\nLoading tree-sitter parsers...")
for our_name, ts_name in LANG_NAME_MAP.items():
    try:
        lang_obj = Language(LIB_PATH, ts_name)
        parser = Parser()
        parser.set_language(lang_obj)
        parsers[our_name] = parser
        print(f"✓ Loaded parser for: {our_name} (using '{ts_name}')")
    except Exception as e:
        print(f"⚠️ Failed to load language '{our_name}' using name '{ts_name}': {e}")
if not parsers or len(parsers) < len(LANG_NAME_MAP):
    print("\n❌ CRITICAL ERROR: Not all required tree-sitter parsers were loaded.")
    sys.exit(1)

# --- CodeBERT Initialization ---
print("\nLoading CodeBERT model...")
try:
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    codebert_model = AutoModel.from_pretrained("microsoft/codebert-base").to(device)
    codebert_model.eval()
    print("CodeBERT loaded.")
except Exception as e:
    print(f"ERROR loading CodeBERT: {e}")
    sys.exit(1)

# -------------------------------
# 2. CORE ALGORITHM EXTRACTION
# -------------------------------
def extract_core_algorithm(code: str, lang: str) -> str:
    """Extracts main method/function bodies, falling back to basic cleaning."""
    try:
        if lang not in parsers: return code
        parser = parsers[lang]
        tree = parser.parse(bytes(code, "utf8"))
        core_segments = []

        def extract_bodies(node):
            if node.type in ['method_declaration', 'function_definition', 'function_declaration']:
                for child in node.children:
                    if child.type in ['block', 'compound_statement', 'suite']:
                        body = child.text.decode('utf8', errors='ignore').strip()
                        if len(body) > 20: # Skip tiny bodies
                            core_segments.append(body)
            for child in node.children:
                extract_bodies(child)

        extract_bodies(tree.root_node)

        if core_segments:
            print(f"  Extracted {len(core_segments)} core segments for {lang}")
            return '\n\n'.join(core_segments) # Use double newline for separation

        # Fallback: strip imports/comments if no bodies found
        lines = [l for l in code.split('\n') if not (
            l.strip().startswith(('import ', 'package ', 'using ', '#include', 'from '))
            or (l.strip().startswith('//') and len(l.strip()) < 50)
            or (l.strip().startswith('#') and len(l.strip()) < 50)
        )]
        print(f"  Fallback cleaning used for {lang}")
        return '\n'.join(lines)
    except Exception as e:
        print(f"  Core extraction error for {lang}: {e}. Returning original.")
        return code

# -------------------------------
# 3. SIMILARITY FUNCTIONS
# -------------------------------

## 3.1 Semantic Similarity (Corrected Windowing)

def mean_pool(token_embeddings, attention_mask):
    """Mean pooling helper (Unchanged)."""
    mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * mask_expanded, 1)
    sum_mask = torch.clamp(mask_expanded.sum(1), min=1e-9)
    # Ensure numpy array on CPU
    pooled = (sum_embeddings / sum_mask)
    return pooled.cpu().numpy()

def get_window_embeddings_ids(code: str, window_size: int = 512, overlap: float = 0.25) -> List[np.ndarray]:
    """Window directly from token IDs. Returns LIST of (1, D) numpy arrays."""
    tokens = tokenizer.encode(code, add_special_tokens=False, truncation=False)
    stride = max(1, int(window_size * (1.0 - overlap)))
    cls_id, sep_id = tokenizer.cls_token_id, tokenizer.sep_token_id
    out: List[np.ndarray] = []

    if not tokens: # Handle empty code after core extraction
        print("  Warning: Empty code for windowing, returning zero embedding")
        return [np.zeros((1, codebert_model.config.hidden_size), dtype=np.float32)]

    if len(tokens) <= window_size - 2: # Single window case
        ids = [cls_id] + tokens + [sep_id]
        input_ids = torch.tensor([ids], device=device, dtype=torch.long)
        attention_mask = torch.ones_like(input_ids, device=device, dtype=torch.long)
        with torch.no_grad():
            outputs = codebert_model(input_ids=input_ids, attention_mask=attention_mask)
        emb = mean_pool(outputs.last_hidden_state, attention_mask)
        out.append(emb)
        return out

    # Multiple sliding windows
    for start in range(0, len(tokens), stride):
        sub = tokens[start : start + (window_size - 2)]
        if not sub: continue
        ids = [cls_id] + sub + [sep_id]
        # Pad shorter sequences explicitly if needed by model (CodeBERT handles via attention mask)
        input_ids = torch.tensor([ids], device=device, dtype=torch.long)
        attention_mask = torch.ones_like(input_ids, device=device, dtype=torch.long)
        with torch.no_grad():
            outputs = codebert_model(input_ids=input_ids, attention_mask=attention_mask)
        emb = mean_pool(outputs.last_hidden_state, attention_mask)
        out.append(emb)

    if not out:
        print("  Warning: No valid windows generated, returning zero embedding")
        return [np.zeros((1, codebert_model.config.hidden_size), dtype=np.float32)]

    #print(f"  Generated {len(out)} window embeddings") # Optional debug
    return out

def extract_window_embeddings(code: str, lang: str) -> List[np.ndarray]:
    """Extract embeddings using ID-based windowing on core code."""
    core_code = extract_core_algorithm(code, lang)
    return get_window_embeddings_ids(core_code, window_size=512, overlap=0.25)

def _normalize(X: np.ndarray) -> np.ndarray:
    """De-anisotropy (mean-centering if N > 1) + L2 normalization."""
    X = X.astype(np.float32, copy=False)
    if X.shape[0] > 1:
        X = X - X.mean(axis=0, keepdims=True)
    denom = np.linalg.norm(X, axis=1, keepdims=True)
    denom = np.clip(denom, 1e-12, None)
    normalized_X = np.divide(X, denom, out=np.zeros_like(X), where=denom!=0)
    return normalized_X

def _symmetric_topk_agg(sim: np.ndarray, k: int = 3) -> float:
    """Symmetric top-k aggregation."""
    if sim.size == 0: return 0.0
    k = max(1, min(k, sim.shape[0], sim.shape[1]))
    # Use partition for efficiency (finds k-th largest, doesn't fully sort)
    row_topk = np.mean(np.mean(np.partition(sim, -k, axis=1)[:, -k:], axis=1))
    col_topk = np.mean(np.mean(np.partition(sim, -k, axis=0)[-k:, :], axis=0))
    return float(0.5 * (row_topk + col_topk))

# --- Keep DBSCAN function if needed for weighted aggregation ---
def apply_dbscan_filtering(embeddings_batch: List[np.ndarray], eps=0.15, min_samples=3):
    """ Applies DBSCAN, returns weights. """
    # Stack list of (1,D) arrays into (N, D)
    valid_embeddings = [emb for emb in embeddings_batch if emb is not None and emb.shape == (1, codebert_model.config.hidden_size)]
    if not valid_embeddings:
         print("  Warning: No valid embeddings for DBSCAN.")
         # Return default weights or handle error appropriately
         return np.ones(len(embeddings_batch)) # Example: return all ones

    all_embeddings = np.vstack(valid_embeddings)

    if all_embeddings.shape[0] < min_samples:
        #print(f"  Skipping DBSCAN: Not enough samples ({all_embeddings.shape[0]} < {min_samples})")
        return np.ones(len(embeddings_batch)) # Not enough samples to cluster

    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
    labels = clustering.fit_predict(all_embeddings)

    unique_labels, counts = np.unique(labels[labels != -1], return_counts=True)
    cluster_sizes = dict(zip(unique_labels, counts))
    max_size = max(cluster_sizes.values()) if cluster_sizes else 1

    weights = []
    # Map back weights to original list size (including potential None/invalid entries)
    valid_idx = 0
    for i in range(len(embeddings_batch)):
         if embeddings_batch[i] is not None and embeddings_batch[i].shape == (1, codebert_model.config.hidden_size):
             label = labels[valid_idx]
             if label == -1:
                 weights.append(1.0)
             else:
                 size = cluster_sizes.get(label, 1) # Use get with default
                 weight = 1.0 - (0.7 * (size / max_size))
                 weights.append(max(0.3, weight))
             valid_idx += 1
         else:
              weights.append(1.0) # Default weight for invalid entries

    return np.array(weights)


def semantic_similarity_with_windowing(code1: str, code2: str, lang1: str, lang2: str,
                                       topk: int = 3,
                                       use_dbscan_weights: bool = False) -> float:
    """Computes semantic similarity using windowing, normalization, top-k, and optional DBSCAN."""
    try:
        emb_list_1 = extract_window_embeddings(code1, lang1)
        emb_list_2 = extract_window_embeddings(code2, lang2)

        # Check for empty lists
        if not emb_list_1 or not emb_list_2: return 0.0

        A = np.vstack(emb_list_1) # Should be (N1, D)
        B = np.vstack(emb_list_2) # Should be (N2, D)

        # Handle case where vstack might return 1D if list has one (1,D) item -> reshape
        if A.ndim == 1: A = A.reshape(1, -1)
        if B.ndim == 1: B = B.reshape(1, -1)

        A = _normalize(A)
        B = _normalize(B)

        weights_A, weights_B = None, None
        if use_dbscan_weights:
            # Pass list of (1,D) embeddings to DBSCAN helper
            all_w = apply_dbscan_filtering(emb_list_1 + emb_list_2)
            if all_w is not None and len(all_w) == len(emb_list_1) + len(emb_list_2):
                weights_A = all_w[:len(emb_list_1)].astype(np.float32, copy=False)
                weights_B = all_w[len(emb_list_1):].astype(np.float32, copy=False)
                #print(f"  DBSCAN Weights A: {weights_A.round(2)}") # Debug
                #print(f"  DBSCAN Weights B: {weights_B.round(2)}") # Debug


        sim = A @ B.T # Cosine similarity after normalization
        sim = np.clip(sim, -1.0, 1.0)

        if weights_A is None or weights_B is None or not use_dbscan_weights:
            return _symmetric_topk_agg(sim, k=topk)
        else:
            # Weighted symmetric top-k
            k = max(1, min(topk, sim.shape[0], sim.shape[1]))
            row_scores, col_scores = [], []

            # Ensure weights have correct dimensions for broadcasting/indexing if needed
            weights_A_col = weights_A.reshape(-1, 1) # (N1, 1)
            weights_B_row = weights_B.reshape(1, -1) # (1, N2)

            for i in range(sim.shape[0]): # Iterate rows (File A windows)
                 row = sim[i] # Shape (N2,)
                 idx = np.argpartition(row, -k)[-k:] # Indices of top k in row
                 vals = row[idx] # Top k scores (k,)
                 w = weights_B[idx] # Weights of corresponding File B windows (k,)
                 # Weighted average for this row's top k matches
                 row_scores.append(np.sum(vals * w) / (np.sum(w) + 1e-12))
            row_mean = float(np.mean(row_scores)) if row_scores else 0.0

            for j in range(sim.shape[1]): # Iterate columns (File B windows)
                 col = sim[:, j] # Shape (N1,)
                 idx = np.argpartition(col, -k)[-k:] # Indices of top k in column
                 vals = col[idx] # Top k scores (k,)
                 w = weights_A[idx] # Weights of corresponding File A windows (k,)
                 # Weighted average for this column's top k matches
                 col_scores.append(np.sum(vals * w) / (np.sum(w) + 1e-12))
            col_mean = float(np.mean(col_scores)) if col_scores else 0.0

            return 0.5 * (row_mean + col_mean)

    except Exception as e:
        print(f"  ERROR in semantic_similarity_with_windowing: {e}")
        import traceback
        traceback.print_exc()
        return 0.0


## 3.2 Syntactic Similarity (Token-based)

def get_token_sim(code_a: str, code_b: str, lang_a: str, lang_b: str) -> float:
    """Calculates Jaccard similarity based on k-grams of tokens."""
    def tokenize(code, lang):
        try:
            if lang not in parsers: return []
            tree = parsers[lang].parse(bytes(code, "utf8"))
            tokens = []
            def traverse(node):
                # Skip comments and literals, keep identifiers and keywords/operators
                if node.type not in ['comment', 'string_literal', 'number_literal', 'integer_literal', 'float_literal', 'boolean_literal', 'null_literal']:
                    if not node.children:
                        t = node.text.decode('utf8', errors='ignore').strip()
                        if t: tokens.append(t)
                    else:
                        for c in node.children: traverse(c)
            traverse(tree.root_node)
            return tokens
        except Exception as e:
            print(f"Tokenize Error ({lang}): {e}")
            return []

    toks_a = tokenize(code_a, lang_a)
    toks_b = tokenize(code_b, lang_b)
    if not toks_a or not toks_b: return 0.0

    k = 5 # Use k=5 as per methodology
    grams_a = {tuple(toks_a[i:i+k]) for i in range(len(toks_a)-k+1)} if len(toks_a) >= k else set()
    grams_b = {tuple(toks_b[i:i+k]) for i in range(len(toks_b)-k+1)} if len(toks_b) >= k else set()

    if not grams_a or not grams_b: return 0.0

    intersection = len(grams_a.intersection(grams_b))
    union = len(grams_a.union(grams_b))
    return intersection / union if union > 0 else 0.0

## 3.3 Structural Similarity (AST-based)

# AST Map remains the same
UNIVERSAL_MAP = {
    # (omitted for brevity - same as before)
     'for_statement': 'Loop','while_statement': 'Loop','do_statement': 'Loop','enhanced_for_statement': 'Loop','for_in_clause': 'Loop','for_in_statement': 'Loop','foreach_statement': 'Loop','while_loop': 'Loop','do_while_statement': 'Loop','if_statement': 'If','if_clause': 'If','elif_clause': 'If','else_clause': 'Else','else_statement': 'Else','conditional_expression': 'Ternary','ternary_expression': 'Ternary','switch_statement': 'Switch','switch_expression': 'Switch','case_statement': 'Case','switch_block': 'Switch','switch_section': 'Case','match_statement': 'Switch','method_declaration': 'Function','function_definition': 'Function','function_declaration': 'Function','constructor_declaration': 'Constructor','lambda_expression': 'Lambda','lambda': 'Lambda','arrow_function': 'Lambda','anonymous_function': 'Lambda','method_invocation': 'FunctionCall','call_expression': 'FunctionCall','invocation_expression': 'FunctionCall','class_declaration': 'Class','class_definition': 'Class','interface_declaration': 'Interface','struct_declaration': 'Struct','enum_declaration': 'Enum','object_creation_expression': 'ObjectCreation','new_expression': 'ObjectCreation','class_instance_creation': 'ObjectCreation','dictionary': 'Dictionary','HashMap': 'Dictionary','dict': 'Dictionary','dictionary_literal': 'Dictionary','list': 'List','ArrayList': 'List','list_literal': 'List','array': 'Array','array_creation_expression': 'Array','array_initializer': 'Array','set': 'Set','set_literal': 'Set','tuple': 'Tuple','tuple_expression': 'Tuple','assignment_expression': 'Assign','assignment_statement': 'Assign','augmented_assignment': 'AugAssign','compound_assignment': 'AugAssign','update_expression': 'UnaryAssign','increment_expression': 'Increment','decrement_expression': 'Decrement','binary_expression': 'BinaryOp','binary_operator': 'BinaryOp','unary_expression': 'UnaryOp','unary_operator': 'UnaryOp','boolean_expression': 'BoolOp','logical_expression': 'BoolOp','comparison_operator': 'CompareOp','relational_expression': 'CompareOp','arithmetic_expression': 'ArithOp','bitwise_expression': 'BitwiseOp','identifier': 'ID','string_literal': 'STR','string': 'STR','interpolated_string': 'STR','f_string': 'STR','number_literal': 'NUM','integer_literal': 'NUM','decimal_integer_literal': 'NUM','float_literal': 'NUM','double_literal': 'NUM','boolean_literal': 'BOOL','true': 'BOOL','false': 'BOOL','null_literal': 'NULL','none': 'NULL','nil': 'NULL','try_statement': 'Try','catch_clause': 'Catch','except_clause': 'Catch','finally_clause': 'Finally','throw_statement': 'Throw','raise_statement': 'Throw','throws': 'Throws','return_statement': 'Return','break_statement': 'Break','continue_statement': 'Continue','yield_statement': 'Yield','goto_statement': 'Goto','pass_statement': 'Pass','import_statement': 'Import','import_declaration': 'Import','from_import_statement': 'Import','using_directive': 'Import','include_directive': 'Include','package_declaration': 'Package','namespace_declaration': 'Namespace','block': 'Block','compound_statement': 'Block','suite': 'Block','statement_block': 'Block','expression_statement': 'ExprStmt','variable_declaration': 'VarDecl','local_variable_declaration': 'VarDecl','field_declaration': 'FieldDecl','parameter': 'Param','formal_parameter': 'Param','parameter_declaration': 'Param','member_access_expression': 'MemberAccess','field_access': 'MemberAccess','attribute': 'MemberAccess','dot_expression': 'MemberAccess','subscript_expression': 'Subscript','element_access_expression': 'Subscript','array_access': 'Subscript','type_annotation': 'Type','type_identifier': 'Type','type_parameter': 'TypeParam','generic_type': 'GenericType','type_arguments': 'TypeArgs','annotation': 'Annotation','decorator': 'Decorator','attribute_list': 'Attribute','modifier': 'Modifier','pointer_declarator': 'Pointer','pointer_expression': 'PointerDeref','address_of_expression': 'AddressOf','reference_expression': 'Reference','dereference_expression': 'Dereference','async_function': 'AsyncFunction','await_expression': 'Await','async_statement': 'Async','list_comprehension': 'ListComp','dictionary_comprehension': 'DictComp','set_comprehension': 'SetComp','generator_expression': 'GeneratorExp','query_expression': 'Query','from_clause': 'QueryFrom','where_clause': 'QueryWhere','select_clause': 'QuerySelect','comment': 'Comment','line_comment': 'Comment','block_comment': 'Comment','documentation_comment': 'DocComment','assert_statement': 'Assert','static_assert_declaration': 'Assert','sizeof_expression': 'SizeOf','typeof_expression': 'TypeOf','instanceof_expression': 'InstanceOf','is_expression': 'TypeCheck','cast_expression': 'Cast','type_cast': 'Cast','as_expression': 'SafeCast','with_statement': 'With','using_statement': 'Using','global_statement': 'Global','nonlocal_statement': 'NonLocal','delegate_declaration': 'Delegate','event_declaration': 'Event','event_field_declaration': 'Event','property_declaration': 'Property','indexer_declaration': 'Indexer','public': 'Public','private': 'Private','protected': 'Protected','internal': 'Internal','static': 'Static','final': 'Final','abstract': 'Abstract','virtual': 'Virtual','override': 'Override','preproc_def': 'PreprocessorDefine','preproc_ifdef': 'PreprocessorIf','preproc_include': 'PreprocessorInclude','preprocessor_call': 'PreprocessorDirective','slice': 'Slice','range_expression': 'Range','spread_element': 'Spread','pattern': 'Pattern','declaration_pattern': 'DeclPattern','constant_pattern': 'ConstPattern','var_pattern': 'VarPattern',
}

@lru_cache(maxsize=1024) # Increased cache size slightly
def extract_ast_nodes(code: str, lang: str) -> List[Dict[str, Any]]:
    """Extracts AST nodes (simplified, assumes UNIVERSAL_MAP applied later)."""
    try:
        if lang not in parsers: return [{'type': 'ERROR'}]
        parser = parsers[lang]
        tree = parser.parse(bytes(code, "utf8"))
        nodes = []
        q = [(tree.root_node, -1)] # Use iterative BFS instead of deep recursion
        visited_nodes = set()

        while q:
             current_node, parent_id = q.pop(0)
             if current_node.id in visited_nodes: continue
             visited_nodes.add(current_node.id)

             node_id = len(nodes)
             node_dict = {'id': node_id, 'type': current_node.type, 'children': [], 'parent': parent_id, 'attrs': {}}
             nodes.append(node_dict)

             # Add children to queue
             for child in current_node.children:
                  q.append((child, node_id))

             # Update parent's children list - find parent dict and append node_id
             if parent_id != -1 and parent_id < len(nodes):
                # This direct indexing might be wrong if BFS order != final nodes list order
                # We need a reliable way to link children back. Let's rebuild links post-traversal.
                pass # Rebuild links later based on parent_id


        # Rebuild children links (more robustly)
        node_map = {node['id']: node for node in nodes}
        for node in nodes:
            parent_id = node['parent']
            if parent_id != -1 and parent_id in node_map:
                parent_node = node_map[parent_id]
                parent_node['children'].append(node['id'])

        return nodes

    except Exception as e:
        print(f"AST Extract Error ({lang}): {e}")
        return [{'type': 'ERROR'}]


def normalize_ast_to_universal(nodes: List[Dict[str, Any]]) -> List[Dict]:
    """Applies UNIVERSAL_MAP and extracts simple branch counts."""
    if not nodes or nodes[0]['type'] == 'ERROR': return []
    
    normalized_nodes = []
    node_map = {node['id']: node for node in nodes} # For quick child lookup

    for node in nodes:
        norm_type = UNIVERSAL_MAP.get(node['type'], node['type'])
        attrs = {}
        # Simple branch count for If/Loop based on number of direct children mapped
        if 'Loop' in norm_type or 'If' in norm_type:
             branch_children_count = 0
             for child_id in node.get('children', []):
                  if child_id in node_map:
                     child_type = node_map[child_id].get('type', '')
                     # Count children that look like statement blocks
                     if 'statement' in child_type or 'block' in child_type or 'suite' in child_type:
                          branch_children_count += 1
             attrs['branches'] = branch_children_count

        normalized_nodes.append({
            'id': node['id'],
            'type': norm_type,
            'parent': node['parent'],
            'children': node.get('children', []), # Keep child IDs
            'attrs': attrs
        })
    return normalized_nodes

def get_ast_sim(code_a: str, lang_a: str, code_b: str, lang_b: str) -> float:
    """Calculates structural similarity using ratio-based features on normalized AST."""
    ast_nodes1 = extract_ast_nodes(code_a, lang_a)
    ast_nodes2 = extract_ast_nodes(code_b, lang_b)

    if not ast_nodes1 or ast_nodes1[0]['type'] == 'ERROR': return 0.0
    if not ast_nodes2 or ast_nodes2[0]['type'] == 'ERROR': return 0.0

    norm_ast1 = normalize_ast_to_universal(ast_nodes1)
    norm_ast2 = normalize_ast_to_universal(ast_nodes2)

    if not norm_ast1 or not norm_ast2: return 0.0

    def extract_features(norm_ast_list):
        features = Counter()
        unique_types = set()
        total_branches = 0
        branch_nodes = 0
        max_depth = 0
        node_map = {node['id']: node for node in norm_ast_list} # ID to node mapping

        # Calculate depth iteratively
        depths = {}
        q = [(0, 0)] # Start BFS from root (assuming root is id 0)
        visited_depth = set()

        while q:
            node_id, d = q.pop(0)
            if node_id not in node_map or node_id in visited_depth: continue
            visited_depth.add(node_id)
            depths[node_id] = d
            max_depth = max(max_depth, d)
            node = node_map[node_id]
            for child_id in node.get('children', []):
                 q.append((child_id, d + 1))


        for node in norm_ast_list:
            node_type = node.get('type', 'UNKNOWN')
            features['total_nodes'] += 1
            features[node_type] += 1
            unique_types.add(node_type)

            if 'Loop' in node_type or 'If' in node_type:
                branch_nodes += 1
                total_branches += node.get('attrs', {}).get('branches', 0)

        features['max_depth'] = max_depth
        features['avg_branches'] = total_branches / branch_nodes if branch_nodes > 0 else 0.0
        features['unique_type_count'] = len(unique_types)
        return features

    feat1 = extract_features(norm_ast1)
    feat2 = extract_features(norm_ast2)

    def normalize_features(feat):
        total = max(feat['total_nodes'], 1)
        # Use more descriptive keys consistent with methodology
        return {
            'loop_ratio': feat.get('Loop', 0) / total,
            'if_ratio': feat.get('If', 0) / total,
            'function_ratio': feat.get('Function', 0) / total,
            'assignment_ratio': feat.get('Assign', 0) / total,
            'binary_op_ratio': feat.get('BinaryOp', 0) / total,
            'depth_normalized': min(feat.get('max_depth', 0) / 20.0, 1.0), # Normalize depth
            'branches_normalized': min(feat.get('avg_branches', 0) / 5.0, 1.0), # Normalize branches
            'type_diversity': min(feat.get('unique_type_count', 0) / 50.0, 1.0) # Normalize type count
        }

    norm_feat1 = normalize_features(feat1)
    norm_feat2 = normalize_features(feat2)

    feature_names = list(norm_feat1.keys()) # Dynamically get keys
    vec1 = np.array([norm_feat1.get(f, 0.0) for f in feature_names], dtype=float)
    vec2 = np.array([norm_feat2.get(f, 0.0) for f in feature_names], dtype=float)

    # Use combined Euclidean and Cosine similarity
    euclidean_dist = np.linalg.norm(vec1 - vec2)
    euclidean_sim = np.exp(-2.0 * euclidean_dist) # Sensitive decay

    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    cosine_sim = 0.0
    if norm1 > 1e-9 and norm2 > 1e-9:
        cosine_sim = np.dot(vec1, vec2) / (norm1 * norm2)
        cosine_sim = max(0.0, cosine_sim) # Clamp [-1, 1] -> [0, 1]

    # Return the minimum for a conservative score
    similarity = min(euclidean_sim, cosine_sim)
    return float(np.clip(similarity, 0.0, 1.0))


## 3.4 Language Difference

def get_lang_diff(lang_a: str, lang_b: str) -> float:
    """Returns 1.0 if languages differ, 0.0 otherwise."""
    return 0.0 if lang_a == lang_b else 1.0

# -------------------------------
# 4. MAIN FEATURE BUILDER
# -------------------------------
def create_feature_file(input_csv: str, output_csv: str, use_dbscan: bool = False):
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"ERROR: Input CSV '{input_csv}' not found.")
        return
    if df.empty:
        print(f"ERROR: Input CSV '{input_csv}' is empty.")
        return

    all_features = []
    print(f"Loaded {len(df)} rows from {input_csv}")
    available_langs = ['java', 'python', 'c', 'csharp'] # Ensure consistent order

    # --- Generate Positive Pairs (label=1, different languages from same row) ---
    print("\nGenerating Positive Pairs (label=1)...")
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Positive Pairs"):
        snippets = []
        for lang in available_langs:
            code = row.get(lang)
            # Check for NaN and sufficient length
            if pd.notna(code) and isinstance(code, str) and len(code.strip()) > 10:
                snippets.append((lang, code))

        # Create combinations of pairs FROM THE SAME ROW
        for (lang_a, code_a), (lang_b, code_b) in itertools.combinations(snippets, 2):
            s_codebert = semantic_similarity_with_windowing(code_a, code_b, lang_a, lang_b, use_dbscan_weights=use_dbscan)
            s_ast = get_ast_sim(code_a, lang_a, code_b, lang_b)
            s_token = get_token_sim(code_a, code_b, lang_a, lang_b)
            d_lang = get_lang_diff(lang_a, lang_b) # Will always be 1.0 here

            all_features.append({
                "S_CodeBERT": s_codebert, "S_AST": s_ast, "S_Token": s_token, "D_lang": d_lang,
                "S_CodeBERT_minus_S_AST": abs(s_codebert - s_ast),
                "one_minus_S_AST": 1.0 - s_ast,
                "label": 1
            })

    num_pos = len(all_features)
    if num_pos == 0:
        print("\nWARNING: No positive pairs generated. Check input CSV format and content.")
        # Decide if you want to stop or continue to generate negative pairs
        # return # Option to stop if no positives

    print(f"Generated {num_pos} positive pairs.")

    # --- Generate Negative Pairs (label=0, random snippets from different rows) ---
    print("\nGenerating Negative Pairs (label=0)...")
    num_neg_to_gen = num_pos if num_pos > 0 else max(100, len(df)) # Generate at least some negatives

    # Build master list: (row_idx, lang, code)
    all_snippets = []
    for idx, row in df.iterrows():
        for lang in available_langs:
            code = row.get(lang)
            if pd.notna(code) and isinstance(code, str) and len(code.strip()) > 10:
                all_snippets.append((idx, lang, code))

    if len(all_snippets) < 2:
        print("ERROR: Not enough valid snippets found in the CSV to generate negative pairs.")
        if num_pos == 0: return # Stop if no pairs generated at all
        # Otherwise, save the positive pairs if any exist
    else:
        neg_count = 0
        attempts = 0
        max_attempts = max(num_neg_to_gen * 10, 1000) # Safety limit

        with tqdm(total=num_neg_to_gen, desc="Negative Pairs") as pbar:
            while neg_count < num_neg_to_gen and attempts < max_attempts:
                attempts += 1
                # Ensure two different snippets are chosen
                idx1 = random.randrange(len(all_snippets))
                idx2 = random.randrange(len(all_snippets))
                if idx1 == idx2: continue # Simple retry if same index picked

                row_idx_a, lang_a, code_a = all_snippets[idx1]
                row_idx_b, lang_b, code_b = all_snippets[idx2]

                # Critical check: Must be from different original rows
                if row_idx_a == row_idx_b:
                    continue # Skip pairs from the same original problem/row

                # Compute features
                s_codebert = semantic_similarity_with_windowing(code_a, code_b, lang_a, lang_b, use_dbscan_weights=use_dbscan)
                s_ast = get_ast_sim(code_a, lang_a, code_b, lang_b)
                s_token = get_token_sim(code_a, code_b, lang_a, lang_b)
                d_lang = get_lang_diff(lang_a, lang_b)

                all_features.append({
                    "S_CodeBERT": s_codebert, "S_AST": s_ast, "S_Token": s_token, "D_lang": d_lang,
                    "S_CodeBERT_minus_S_AST": abs(s_codebert - s_ast),
                    "one_minus_S_AST": 1.0 - s_ast,
                    "label": 0
                })
                neg_count += 1
                pbar.update(1)
                attempts = 0 # Reset attempt counter on success

        print(f"Generated {neg_count} negative pairs (tried up to {max_attempts} times).")
        if neg_count < num_neg_to_gen:
             print(f"Warning: Could only generate {neg_count}/{num_neg_to_gen} negative pairs.")


    # --- Save ---
    if not all_features:
         print("\nERROR: No features were generated. Output file will not be created.")
         return

    feature_df = pd.DataFrame(all_features)
    # Shuffle the combined dataframe
    feature_df = feature_df.sample(frac=1, random_state=42).reset_index(drop=True)

    try:
        feature_df.to_csv(output_csv, index=False)
        print(f"\nSaved {len(feature_df)} total pairs to {output_csv}")
        print("\nFirst 5 rows of generated features:")
        print(feature_df.head())

        # Stats on generated data
        print("\nFeature Statistics:")
        print(feature_df.describe())
        print("\nLabel Distribution:")
        print(feature_df['label'].value_counts())

        if 'D_lang' in feature_df.columns:
            print("\nLanguage Dissimilarity Distribution (Negative Pairs):")
            print(feature_df[feature_df['label'] == 0]['D_lang'].value_counts())
        else:
            print("\n'D_lang' column not found for stats.")

    except Exception as e:
        print(f"\nERROR saving features to {output_csv}: {e}")

# -------------------------------
# 5. RUN
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate features for Gating Network training.")
    parser.add_argument('--input_csv', type=str, default='code_clones.csv', help="Input CSV file with code pairs per row.")
    parser.add_argument('--output_csv', type=str, default='gptclonebench_features.csv', help="Output CSV file for generated features.")
    parser.add_argument('--use_dbscan', action='store_true', help="Enable DBSCAN weighting during semantic similarity calculation.")
    args = parser.parse_args()

    create_feature_file(args.input_csv, args.output_csv, args.use_dbscan)