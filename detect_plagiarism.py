# Requirements: pip install transformers torch torch-geometric tree-sitter==0.20.4 networkx numpy scikit-learn langid
import os
import re
from typing import Dict, Tuple, List, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GINConv, global_add_pool
from torch_geometric.data import Data
from torch_geometric.utils import from_networkx
import networkx as nx
from tree_sitter import Language, Parser, Node
from langid.langid import classify
from collections import defaultdict, Counter
import statistics
from functools import lru_cache
import sys
import argparse

# Prevent deep recursion errors
sys.setrecursionlimit(2000)

print("=" * 80)
print("DYNAMIC MULTI-MODAL PLAGIARISM DETECTION FRAMEWORK V9")
print("INTEGRATED WITH TRAINED GATING NETWORK")
print("=" * 80)

# Device Management
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# -------------------------------
# 1. GATING NETWORK (LOADED FROM TRAINING)
# -------------------------------
class GatingNetwork(nn.Module):
    def __init__(self, input_size=6, hidden_size=16, dropout=0.3):
        super(GatingNetwork, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, 3),  # 3 experts: CodeBERT, AST, Token
            nn.Softmax(dim=-1)
        )

    def forward(self, x):
        return self.network(x)

# Load the trained gating model
GATING_MODEL_PATH = 'best_gating_model.pth'
if not os.path.exists(GATING_MODEL_PATH):
    raise FileNotFoundError(f"Gating model not found: {GATING_MODEL_PATH}")

gating_model = GatingNetwork().to(device)
checkpoint = torch.load(GATING_MODEL_PATH, map_location=device)
gating_model.load_state_dict(checkpoint['model_state_dict'])
gating_model.eval()
print(f"Loaded trained gating model from {GATING_MODEL_PATH} (Best Val F1: {checkpoint.get('val_f1', 'N/A'):.4f})")

# -------------------------------
# Tree-sitter Setup
# -------------------------------
# --- FINAL CORRECTED TREE-SITTER INITIALIZATION ---
LIB_PATH = 'build/my-languages.so' # Define path first
LANG_REPOS = [ # Needed for error message below
    'tree-sitter-java',
    'tree-sitter-python',
    'tree-sitter-c',
    'tree-sitter-c-sharp'
]

# Check if the library exists
if not os.path.exists(LIB_PATH):
    print(f"❌ CRITICAL ERROR: Tree-sitter library not found at '{LIB_PATH}'")
    print("   Please build it manually using the Tree-sitter CLI:")
    print("   tree-sitter build --output build/my-languages.so tree-sitter-java tree-sitter-python tree-sitter-c tree-sitter-c-sharp")
    sys.exit(1)
else:
     print(f"Found tree-sitter library: {LIB_PATH}")

# Map of desired names -> tree-sitter internal names
LANG_NAME_MAP = {
    'java': 'java',
    'python': 'python',
    'c': 'c',
    'csharp': 'c_sharp' # Use internal name 'c_sharp' for C#
}

parsers = {}
print("\nLoading tree-sitter parsers...")
for our_name, ts_name in LANG_NAME_MAP.items():
    try:
        # Get the language object using the library path and internal name
        lang_obj = Language(LIB_PATH, ts_name) 
        
        parser = Parser()
        parser.set_language(lang_obj)
        parsers[our_name] = parser
        print(f"✓ Loaded parser for: {our_name} (using '{ts_name}')")
        
    except Exception as e:
        print(f"⚠️ Failed to load language '{our_name}' using name '{ts_name}': {e}")
        # Construct the expected repo name for the error message
        expected_repo = f"tree-sitter-{our_name.replace('csharp', 'c-sharp')}" # c-sharp for repo name
        print(f"   Make sure '{expected_repo}' was included when building '{LIB_PATH}'")

# Critical check
if not parsers or len(parsers) < len(LANG_NAME_MAP):
    print("\n❌ CRITICAL ERROR: Not all required tree-sitter parsers were loaded.")
    print(f"   Check previous error messages and ensure '{LIB_PATH}' exists and is up-to-date.")
    sys.exit(1)
    
# --- END CORRECTION ---

# CodeBERT (Keep this as it is)
print("\nLoading CodeBERT model...")
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
codebert_model = AutoModel.from_pretrained("microsoft/codebert-base").to(device)
codebert_model.eval()
print("CodeBERT loaded.")

# Normalized AST Labels
UNIVERSAL_MAP = {
    # ===== LOOPS =====
    'for_statement': 'Loop',
    'while_statement': 'Loop',
    'do_statement': 'Loop',
    'enhanced_for_statement': 'Loop',
    'for_in_clause': 'Loop',
    'for_in_statement': 'Loop',
    'foreach_statement': 'Loop',
    'while_loop': 'Loop',
    'do_while_statement': 'Loop',
    
    # ===== CONDITIONALS =====
    'if_statement': 'If',
    'if_clause': 'If',
    'elif_clause': 'If',
    'else_clause': 'Else',
    'else_statement': 'Else',
    'conditional_expression': 'Ternary',
    'ternary_expression': 'Ternary',
    
    # ===== SWITCH/CASE =====
    'switch_statement': 'Switch',
    'switch_expression': 'Switch',
    'case_statement': 'Case',
    'switch_block': 'Switch',
    'switch_section': 'Case',
    'match_statement': 'Switch',  # Python 3.10+
    
    # ===== FUNCTIONS/METHODS =====
    'method_declaration': 'Function',
    'function_definition': 'Function',
    'function_declaration': 'Function',
    'constructor_declaration': 'Constructor',
    'lambda_expression': 'Lambda',
    'lambda': 'Lambda',
    'arrow_function': 'Lambda',
    'anonymous_function': 'Lambda',
    'method_invocation': 'FunctionCall',
    'call_expression': 'FunctionCall',
    'invocation_expression': 'FunctionCall',
    
    # ===== CLASSES/OBJECTS =====
    'class_declaration': 'Class',
    'class_definition': 'Class',
    'interface_declaration': 'Interface',
    'struct_declaration': 'Struct',
    'enum_declaration': 'Enum',
    'object_creation_expression': 'ObjectCreation',
    'new_expression': 'ObjectCreation',
    'class_instance_creation': 'ObjectCreation',
    
    # ===== DATA STRUCTURES =====
    'dictionary': 'Dictionary',
    'HashMap': 'Dictionary',
    'dict': 'Dictionary',
    'dictionary_literal': 'Dictionary',
    'list': 'List',
    'ArrayList': 'List',
    'list_literal': 'List',
    'array': 'Array',
    'array_creation_expression': 'Array',
    'array_initializer': 'Array',
    'set': 'Set',
    'set_literal': 'Set',
    'tuple': 'Tuple',
    'tuple_expression': 'Tuple',
    
    # ===== ASSIGNMENTS =====
    'assignment_expression': 'Assign',
    'assignment_statement': 'Assign',
    'augmented_assignment': 'AugAssign',
    'compound_assignment': 'AugAssign',
    'update_expression': 'UnaryAssign',
    'increment_expression': 'Increment',
    'decrement_expression': 'Decrement',
    
    # ===== OPERATORS =====
    'binary_expression': 'BinaryOp',
    'binary_operator': 'BinaryOp',
    'unary_expression': 'UnaryOp',
    'unary_operator': 'UnaryOp',
    'boolean_expression': 'BoolOp',
    'logical_expression': 'BoolOp',
    'comparison_operator': 'CompareOp',
    'relational_expression': 'CompareOp',
    'arithmetic_expression': 'ArithOp',
    'bitwise_expression': 'BitwiseOp',
    
    # ===== LITERALS =====
    'identifier': 'ID',
    'string_literal': 'STR',
    'string': 'STR',
    'interpolated_string': 'STR',
    'f_string': 'STR',
    'number_literal': 'NUM',
    'integer_literal': 'NUM',
    'decimal_integer_literal': 'NUM',
    'float_literal': 'NUM',
    'double_literal': 'NUM',
    'boolean_literal': 'BOOL',
    'true': 'BOOL',
    'false': 'BOOL',
    'null_literal': 'NULL',
    'none': 'NULL',
    'nil': 'NULL',
    
    # ===== EXCEPTION HANDLING =====
    'try_statement': 'Try',
    'catch_clause': 'Catch',
    'except_clause': 'Catch',
    'finally_clause': 'Finally',
    'throw_statement': 'Throw',
    'raise_statement': 'Throw',
    'throws': 'Throws',
    
    # ===== RETURN/CONTROL FLOW =====
    'return_statement': 'Return',
    'break_statement': 'Break',
    'continue_statement': 'Continue',
    'yield_statement': 'Yield',
    'goto_statement': 'Goto',
    'pass_statement': 'Pass',
    
    # ===== IMPORTS/INCLUDES =====
    'import_statement': 'Import',
    'import_declaration': 'Import',
    'from_import_statement': 'Import',
    'using_directive': 'Import',
    'include_directive': 'Include',
    'package_declaration': 'Package',
    'namespace_declaration': 'Namespace',
    
    # ===== BLOCKS/SCOPES =====
    'block': 'Block',
    'compound_statement': 'Block',
    'suite': 'Block',
    'statement_block': 'Block',
    'expression_statement': 'ExprStmt',
    
    # ===== VARIABLES/DECLARATIONS =====
    'variable_declaration': 'VarDecl',
    'local_variable_declaration': 'VarDecl',
    'field_declaration': 'FieldDecl',
    'parameter': 'Param',
    'formal_parameter': 'Param',
    'parameter_declaration': 'Param',
    
    # ===== MEMBER ACCESS =====
    'member_access_expression': 'MemberAccess',
    'field_access': 'MemberAccess',
    'attribute': 'MemberAccess',
    'dot_expression': 'MemberAccess',
    'subscript_expression': 'Subscript',
    'element_access_expression': 'Subscript',
    'array_access': 'Subscript',
    
    # ===== TYPE ANNOTATIONS =====
    'type_annotation': 'Type',
    'type_identifier': 'Type',
    'type_parameter': 'TypeParam',
    'generic_type': 'GenericType',
    'type_arguments': 'TypeArgs',
    
    # ===== ANNOTATIONS/DECORATORS =====
    'annotation': 'Annotation',
    'decorator': 'Decorator',
    'attribute_list': 'Attribute',
    'modifier': 'Modifier',
    
    # ===== POINTERS/REFERENCES (C/C#) =====
    'pointer_declarator': 'Pointer',
    'pointer_expression': 'PointerDeref',
    'address_of_expression': 'AddressOf',
    'reference_expression': 'Reference',
    'dereference_expression': 'Dereference',
    
    # ===== ASYNC/AWAIT =====
    'async_function': 'AsyncFunction',
    'await_expression': 'Await',
    'async_statement': 'Async',
    
    # ===== COMPREHENSIONS (Python) =====
    'list_comprehension': 'ListComp',
    'dictionary_comprehension': 'DictComp',
    'set_comprehension': 'SetComp',
    'generator_expression': 'GeneratorExp',
    
    # ===== LINQ (C#) =====
    'query_expression': 'Query',
    'from_clause': 'QueryFrom',
    'where_clause': 'QueryWhere',
    'select_clause': 'QuerySelect',
    
    # ===== COMMENTS/DOCS =====
    'comment': 'Comment',
    'line_comment': 'Comment',
    'block_comment': 'Comment',
    'documentation_comment': 'DocComment',
    
    # ===== ASSERTIONS =====
    'assert_statement': 'Assert',
    'static_assert_declaration': 'Assert',
    
    # ===== SIZEOF/TYPEOF =====
    'sizeof_expression': 'SizeOf',
    'typeof_expression': 'TypeOf',
    'instanceof_expression': 'InstanceOf',
    'is_expression': 'TypeCheck',
    
    # ===== CASTS/CONVERSIONS =====
    'cast_expression': 'Cast',
    'type_cast': 'Cast',
    'as_expression': 'SafeCast',
    
    # ===== WITH/USING (Resource Management) =====
    'with_statement': 'With',
    'using_statement': 'Using',
    
    # ===== GLOBAL/NONLOCAL =====
    'global_statement': 'Global',
    'nonlocal_statement': 'NonLocal',
    
    # ===== DELEGATES/EVENTS (C#) =====
    'delegate_declaration': 'Delegate',
    'event_declaration': 'Event',
    'event_field_declaration': 'Event',
    
    # ===== PROPERTIES (C#) =====
    'property_declaration': 'Property',
    'indexer_declaration': 'Indexer',
    
    # ===== VISIBILITY MODIFIERS =====
    'public': 'Public',
    'private': 'Private',
    'protected': 'Protected',
    'internal': 'Internal',
    'static': 'Static',
    'final': 'Final',
    'abstract': 'Abstract',
    'virtual': 'Virtual',
    'override': 'Override',
    
    # ===== PREPROCESSOR (C/C#) =====
    'preproc_def': 'PreprocessorDefine',
    'preproc_ifdef': 'PreprocessorIf',
    'preproc_include': 'PreprocessorInclude',
    'preprocessor_call': 'PreprocessorDirective',
    
    # ===== RANGES/SLICES =====
    'slice': 'Slice',
    'range_expression': 'Range',
    'spread_element': 'Spread',
    
    # ===== PATTERN MATCHING =====
    'pattern': 'Pattern',
    'declaration_pattern': 'DeclPattern',
    'constant_pattern': 'ConstPattern',
    'var_pattern': 'VarPattern',
}

# Normalized AST Labels - Expanded and Comprehensive
NORMALIZED_LABELS = [
    # ===== CONTROL FLOW STRUCTURES =====
    'Loop(init, cond, update)',  # For loops
    'Loop(cond, body)',  # While loops
    'Loop(collection, body)',  # Foreach/enhanced for
    'Loop(body, cond)',  # Do-while loops
    'If(cond, then, else)',
    'If(cond, then)',
    'Switch(expr, cases)',
    'Case(value, body)',
    'Ternary(cond, true_expr, false_expr)',
    
    # ===== FUNCTIONS & METHODS =====
    'Function(params, body)',
    'Function(name, params, body, return_type)',
    'Constructor(params, body)',
    'Lambda(params, expr)',
    'Lambda(params, body)',
    'FunctionCall(name, args)',
    'FunctionCall(obj, method, args)',
    'Method(name, params, body)',
    
    # ===== CLASSES & OOP =====
    'Class(name, members)',
    'Class(name, base, members)',
    'Interface(name, members)',
    'Struct(name, fields)',
    'Enum(name, values)',
    'ObjectCreation(type, args)',
    'Constructor(name, params)',
    'Destructor(name)',
    
    # ===== DATA STRUCTURES =====
    'Dictionary',
    'Dictionary(pairs)',
    'List',
    'List(elements)',
    'Array',
    'Array(elements)',
    'Array(type, size)',
    'Set',
    'Set(elements)',
    'Tuple',
    'Tuple(elements)',
    
    # ===== ASSIGNMENTS =====
    'Assign(left, right)',
    'AugAssign(left, op, right)',
    'UnaryAssign(var, op)',
    'Increment(var)',
    'Decrement(var)',
    'MultiAssign(targets, value)',
    
    # ===== OPERATORS =====
    'BinaryOp(left, op, right)',
    'UnaryOp(op, operand)',
    'BoolOp(left, op, right)',
    'CompareOp(left, op, right)',
    'ArithOp(left, op, right)',
    'BitwiseOp(left, op, right)',
    'LogicalOp(left, op, right)',
    
    # ===== LITERALS & IDENTIFIERS =====
    'ID',
    'ID(name)',
    'STR',
    'STR(value)',
    'NUM',
    'NUM(value)',
    'BOOL',
    'BOOL(value)',
    'NULL',
    
    # ===== EXCEPTION HANDLING =====
    'Try(body, handlers, finally)',
    'Catch(exception, body)',
    'Finally(body)',
    'Throw(exception)',
    'Throws(exceptions)',
    
    # ===== RETURN & CONTROL =====
    'Return',
    'Return(value)',
    'Break',
    'Break(label)',
    'Continue',
    'Continue(label)',
    'Yield(value)',
    'Goto(label)',
    'Pass',
    
    # ===== IMPORTS & MODULES =====
    'Import(module)',
    'Import(module, alias)',
    'Import(module, names)',
    'Include(file)',
    'Package(name)',
    'Namespace(name, body)',
    'Using(namespace)',
    
    # ===== BLOCKS & STATEMENTS =====
    'Block',
    'Block(statements)',
    'ExprStmt(expr)',
    'Program',
    'Program(statements)',
    'Scope(body)',
    
    # ===== VARIABLES & DECLARATIONS =====
    'VarDecl(type, name)',
    'VarDecl(type, name, value)',
    'FieldDecl(type, name)',
    'FieldDecl(modifiers, type, name, value)',
    'Param(type, name)',
    'Param(name, default)',
    'ConstDecl(type, name, value)',
    
    # ===== MEMBER ACCESS =====
    'MemberAccess(obj, member)',
    'Subscript(obj, index)',
    'Subscript(obj, slice)',
    'Attribute(obj, attr)',
    'DotExpr(left, right)',
    
    # ===== TYPE SYSTEM =====
    'Type(name)',
    'TypeParam(name)',
    'GenericType(base, args)',
    'TypeArgs(types)',
    'TypeAnnotation(expr, type)',
    'Cast(type, expr)',
    'SafeCast(expr, type)',
    'TypeCheck(expr, type)',
    'InstanceOf(expr, type)',
    'TypeOf(expr)',
    'SizeOf(type)',
    
    # ===== ANNOTATIONS & MODIFIERS =====
    'Annotation(name, args)',
    'Decorator(name, args)',
    'Attribute(name, value)',
    'Modifier(type)',
    'Public',
    'Private',
    'Protected',
    'Internal',
    'Static',
    'Final',
    'Abstract',
    'Virtual',
    'Override',
    
    # ===== POINTERS & REFERENCES =====
    'Pointer(type)',
    'PointerDeref(ptr)',
    'AddressOf(expr)',
    'Reference(expr)',
    'Dereference(expr)',
    
    # ===== ASYNC/CONCURRENCY =====
    'AsyncFunction(params, body)',
    'Await(expr)',
    'Async(body)',
    'Lock(obj, body)',
    'Synchronized(obj, body)',
    
    # ===== COMPREHENSIONS (Python) =====
    'ListComp(expr, generators)',
    'DictComp(key, value, generators)',
    'SetComp(expr, generators)',
    'GeneratorExp(expr, generators)',
    
    # ===== QUERY EXPRESSIONS (C# LINQ) =====
    'Query(clauses)',
    'QueryFrom(var, collection)',
    'QueryWhere(condition)',
    'QuerySelect(projection)',
    'QueryJoin(left, right, on)',
    'QueryGroupBy(key)',
    'QueryOrderBy(key, direction)',
    
    # ===== RESOURCE MANAGEMENT =====
    'With(expr, body)',
    'Using(resource, body)',
    'Dispose(obj)',
    
    # ===== SCOPE MODIFIERS =====
    'Global(vars)',
    'NonLocal(vars)',
    
    # ===== DELEGATES & EVENTS (C#) =====
    'Delegate(return_type, params)',
    'Event(type, name)',
    'EventHandler(name, handler)',
    
    # ===== PROPERTIES & INDEXERS (C#) =====
    'Property(type, name, accessors)',
    'Getter(body)',
    'Setter(body)',
    'Indexer(type, params, accessors)',
    
    # ===== PREPROCESSOR =====
    'PreprocessorDefine(name, value)',
    'PreprocessorIf(condition)',
    'PreprocessorInclude(file)',
    'PreprocessorDirective(name, args)',
    
    # ===== RANGES & SLICES =====
    'Slice(start, stop, step)',
    'Range(start, end)',
    'Spread(expr)',
    'Unpack(expr)',
    
    # ===== PATTERN MATCHING =====
    'Pattern(expr, cases)',
    'DeclPattern(type, var)',
    'ConstPattern(value)',
    'VarPattern(name)',
    'WildcardPattern',
    
    # ===== ASSERTIONS & TESTING =====
    'Assert(condition)',
    'Assert(condition, message)',
    
    # ===== MISCELLANEOUS =====
    'Comment',
    'DocComment',
    'Empty',
    'Ellipsis',
    'Placeholder',
    
    # ===== LEGACY/COMPATIBILITY =====
    'block',
    'program',
    'expression_statement',
    'return_statement',
    'formal_parameter_list',
    'call_expression',
    'method_invocation',
    'parameters',
    'arguments',
    'ERROR',
]

# NEW: Core Algorithm Extraction
def extract_core_algorithm(code: str, lang: str) -> str:
    """
    Extract only the main algorithmic logic, removing boilerplate code.
    This prevents CodeBERT from matching on common patterns like imports, 
    class declarations, error handling boilerplate, etc.
    """
    try:
        if lang not in parsers: return code
        parser = parsers[lang]
        tree = parser.parse(bytes(code, "utf8"))
        
        core_code_segments = []
        
        def extract_method_bodies(node: Node, depth: int = 0):
            """Recursively extract method/function bodies"""
            # For Java/C#: method_declaration
            # For Python: function_definition
            # For C: function_definition
            if node.type in ['method_declaration', 'function_definition', 'function_declaration']:
                # Find the block/body child
                for child in node.children:
                    if child.type in ['block', 'compound_statement', 'suite']:
                        body_text = child.text.decode('utf8', errors='ignore')
                        # Skip mock/stub methods (very short methods)
                        if len(body_text.strip()) > 20:
                            core_code_segments.append(body_text)
            
            # Recursively process children
            for child in node.children:
                extract_method_bodies(child, depth + 1)
        
        extract_method_bodies(tree.root_node)
        
        # If no methods found or extraction failed, return cleaned code
        if not core_code_segments:
            # Remove imports and package declarations at minimum
            lines = code.split('\n')
            filtered_lines = []
            for line in lines:
                stripped = line.strip()
                # Skip imports, package declarations, and single-line comments
                if not (stripped.startswith('import ') or 
                       stripped.startswith('package ') or
                       stripped.startswith('using ') or
                       stripped.startswith('#include') or
                       stripped.startswith('from ') or
                       (stripped.startswith('//') and len(stripped) < 50) or
                       (stripped.startswith('#') and len(stripped) < 50)):
                    filtered_lines.append(line)
            return '\n'.join(filtered_lines)
        
        # Combine all method bodies
        combined = '\n'.join(core_code_segments)
        print(f"  Core algorithm extraction: {len(code)} chars -> {len(combined)} chars (method bodies only)")
        return combined
    
    except Exception as e:
        print(f"  Warning: Core algorithm extraction failed for {lang}: {e}")
        return code  # Return original on error


def mean_pool(token_embeddings, attention_mask):
    """Mean pooling helper"""
    mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * mask_expanded, 1)
    sum_mask = torch.clamp(mask_expanded.sum(1), min=1e-9)
    return (sum_embeddings / sum_mask).cpu().numpy()


# REPLACE embed_with_sliding_window WITH THIS:
def get_window_embeddings(code: str, window_size=512, overlap=0.25) -> List[np.ndarray]:
    """
    Process code using sliding windows with overlap for CodeBERT.
    Returns a LIST of mean-pooled embeddings, one for each window.
    """
    stride = int(window_size * (1 - overlap))  # 384 for 25% overlap
    
    # Tokenize full code
    tokens = tokenizer.encode(code, add_special_tokens=False, truncation=False)
    
    window_embeddings = [] # This will be our return value

    if len(tokens) <= window_size - 2: # Account for [CLS] and [SEP]
        # Single window case
        inputs = tokenizer(code, return_tensors="pt", 
                          truncation=True, max_length=window_size).to(device)
        with torch.no_grad():
            outputs = codebert_model(**inputs)
        window_embeddings.append(mean_pool(outputs.last_hidden_state, inputs['attention_mask']))
        return window_embeddings # Return as list
    
    # Multiple windows
    for start_idx in range(0, len(tokens), stride):
        end_idx = min(start_idx + window_size - 2, len(tokens)) # -2 for [CLS], [SEP]
        window_tokens = tokens[start_idx:end_idx]
        
        if not window_tokens:
            continue
            
        # Decode back to text and re-encode with special tokens
        window_text = tokenizer.decode(window_tokens, skip_special_tokens=True)
        inputs = tokenizer(window_text, return_tensors="pt", 
                          truncation=True, max_length=window_size).to(device)
        
        with torch.no_grad():
            outputs = codebert_model(**inputs)
        
        window_emb = mean_pool(outputs.last_hidden_state, inputs['attention_mask'])
        window_embeddings.append(window_emb)
        
    if not window_embeddings:
        print("  Warning: No valid windows processed, returning zero embedding")
        return [np.zeros((1, 768))] # Return list with a zero vector
        
    print(f"  Aggregated {len(window_embeddings)} windows")
    return window_embeddings # Return the full list

# REPLACE extract_embedding WITH THIS:
def extract_window_embeddings(code: str, lang: str) -> List[np.ndarray]:
    """Extract a list of window embeddings using sliding window on core code."""
    core_code = extract_core_algorithm(code, lang)
    # Call the new function
    return get_window_embeddings(core_code, window_size=512, overlap=0.25)

def apply_dbscan_filtering(embeddings_batch: List[np.ndarray], 
                           eps=0.15, min_samples=3):
    """
    Apply DBSCAN to identify boilerplate clusters.
    Returns weights for each embedding (lower weight = common boilerplate).
    """
    # Stack all embeddings
    all_embeddings = np.vstack(embeddings_batch)
    
    # Cluster
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
    labels = clustering.fit_predict(all_embeddings)
    
    # Calculate cluster sizes
    unique_labels, counts = np.unique(labels[labels != -1], return_counts=True)
    cluster_sizes = dict(zip(unique_labels, counts))
    
    # Assign weights: larger clusters get lower weights (boilerplate)
    weights = []
    max_size = max(cluster_sizes.values()) if cluster_sizes else 1
    
    for label in labels:
        if label == -1:  # Noise points (unique code)
            weights.append(1.0)
        else:
            # Inverse weight: common clusters get 0.3-0.5, unique get 1.0
            size = cluster_sizes[label]
            weight = 1.0 - (0.7 * (size / max_size))
            weights.append(max(0.3, weight))
    
    return np.array(weights)


# Modified semantic similarity for batch processing
# ADD THIS NEW FUNCTION (and delete semantic_similarity_with_filtering)
def semantic_similarity_with_windowing(code1, code2, lang1, lang2) -> float:
    """
    Compute semantic similarity by comparing all windows from code1
    against all windows from code2.
    """
    # 1. Get lists of embeddings for each window
    emb_list_1 = extract_window_embeddings(code1, lang1)
    emb_list_2 = extract_window_embeddings(code2, lang2)

    # 2. Stack them into 2D numpy arrays
    # (N_windows_1, 768) and (N_windows_2, 768)
    all_embeddings_1 = np.vstack(emb_list_1)
    all_embeddings_2 = np.vstack(emb_list_2)

    # 3. Compute the pairwise similarity matrix
    # Shape: (N_windows_1, N_windows_2)
    similarity_matrix = cosine_similarity(all_embeddings_1, all_embeddings_2)

    # 4. Find the best match for each window in file 1
    # (i.e., for each row, find the max value)
    best_matches_for_1 = np.max(similarity_matrix, axis=1)
    
    # 5. Find the best match for each window in file 2
    # (i.e., for each column, find the max value)
    best_matches_for_2 = np.max(similarity_matrix, axis=0)

    # 6. The final score is the average of all these best matches
    final_sim = (np.mean(best_matches_for_1) + np.mean(best_matches_for_2)) / 2.0
    
    return float(final_sim)
# Phase 1: Semantic (FIXED - Extract core algorithm + use sliding windows)
def semantic_similarity_pair(code1: str, code2: str, lang1: str = 'java', lang2: str = 'java') -> float:
    """Compute semantic similarity using CodeBERT with windowing."""
    try:
        # Call the new windowing function
        sim = semantic_similarity_with_windowing(code1, code2, lang1, lang2)
        return float(sim)
    except Exception as e:
        print(f"  ERROR in semantic similarity: {e}")
        import traceback
        traceback.print_exc()
        return 0.0

# Phase 2: Syntactic
def tokenize_code(code: str, lang: str) -> List[str]:
    """Extract tokens from code using tree-sitter parser"""
    try:
        if lang not in parsers: return []
        parser = parsers[lang]
        tree = parser.parse(bytes(code, "utf8"))
        tokens = []
        
        def traverse(node: Node):
            # Skip comments and literals
            if node.type in ['comment', 'string_literal', 'number_literal', 'integer_literal']:
                return
            if not node.children:
                token_text = node.text.decode('utf8', errors='ignore').strip()
                if token_text and len(token_text) > 0:
                    tokens.append(token_text)
            else:
                for child in node.children:
                    traverse(child)
        
        traverse(tree.root_node)
        return tokens
    
    except Exception as e:
        print(f"  Error tokenizing code ({lang}): {e}")
        return []


def syntactic_similarity(code1: str, code2: str, lang1: str, lang2: str, k: int = 5) -> float:
    """Compute syntactic similarity using k-gram token overlap"""
    toks1 = tokenize_code(code1, lang1)
    toks2 = tokenize_code(code2, lang2)
    
    if not toks1 or not toks2: 
        return 0.0
    
    def kgrams(toks, k_val):
        if len(toks) < k_val: 
            return set()
        return {tuple(toks[i:i+k_val]) for i in range(len(toks) - k_val + 1)}
    
    grams1 = kgrams(toks1, k)
    grams2 = kgrams(toks2, k)
    
    if not grams1 or not grams2:
        return 0.0
    
    intersection = len(grams1 & grams2)
    union = len(grams1 | grams2)
    
    return intersection / union if union > 0 else 0.0


# Phase 3: AST Extraction
@lru_cache(maxsize=1000)
def extract_ast_nodes(code: str, lang: str) -> List[Dict[str, Any]]:
    """Extract AST nodes with diagnostics"""
    try:
        if lang not in parsers: return [{'type': 'ERROR'}]
        parser = parsers[lang]
        tree = parser.parse(bytes(code, "utf8"))
        
        if tree.root_node.has_error:
            print(f"  WARNING: Syntax error detected in {lang} code")
        
        nodes = []
        
        def traverse(node: Node, parent_id: int = -1) -> int:
            node_id = len(nodes)
            node_dict = {
                'id': node_id,
                'type': node.type,
                'text': node.text.decode('utf8', errors='ignore') if not node.children else '',
                'children': [],
                'parent': parent_id,
                'attrs': {}
            }
            nodes.append(node_dict)
            
            for child in node.children:
                child_id = traverse(child, node_id)
                node_dict['children'].append(child_id)
            
            return node_id
        
        traverse(tree.root_node)
        
        # Diagnostics
        type_counts = Counter(node['type'] for node in nodes)
        print(f"  AST extracted for {lang}: {len(nodes)} nodes, top types: {type_counts.most_common(3)}")
        
        return nodes
    
    except Exception as e:
        print(f"  ERROR extracting AST for {lang}: {e}")
        return [{'id': 0, 'type': 'ERROR', 'text': '', 'children': [], 'parent': -1, 'attrs': {}}]


def normalize_ast_to_universal(nodes_to_process: List[Dict[str, Any]], 
                               all_nodes_lookup: List[Dict[str, Any]] = None) -> List[Dict]:
    """Normalize language-specific AST to universal representation"""
    if not nodes_to_process:
        return []
    
    if all_nodes_lookup is None:
        all_nodes_lookup = nodes_to_process
    
    normalized_root_nodes = []
    
    for node in nodes_to_process:
        if 'type' not in node or 'children' not in node:
            continue
        
        norm_type = UNIVERSAL_MAP.get(node['type'], node['type'])
        
        current_node_normalized = {
            'type': norm_type,
            'children': [],
            'attrs': {}
        }
        
        # Extract attributes
        attrs = {}
        try:
            if 'Function' in norm_type:
                params_children = [c for c in node['children'] 
                                 if c < len(all_nodes_lookup) and 
                                 all_nodes_lookup[c]['type'] in ['formal_parameter_list', 'parameters', 'parameter_list']]
                attrs['param_count'] = len(params_children)
            elif 'Loop' in norm_type or 'If' in norm_type:
                branch_children = [c for c in node['children']
                                 if c < len(all_nodes_lookup) and
                                 ('statement' in all_nodes_lookup[c]['type'] or 'block' in all_nodes_lookup[c]['type'])]
                attrs['branches'] = len(branch_children)
            
            current_node_normalized['attrs'] = attrs
        except (IndexError, KeyError):
            pass
        
        # Process children recursively
        norm_children = []
        for child_id in node['children']:
            if child_id < len(all_nodes_lookup):
                child_node = all_nodes_lookup[child_id]
                normalized_child = normalize_ast_to_universal([child_node], all_nodes_lookup)
                if normalized_child:
                    norm_children.extend(normalized_child)
        
        current_node_normalized['children'] = norm_children
        normalized_root_nodes.append(current_node_normalized)
    
    return normalized_root_nodes


# CRITICAL FIX: Ratio-based structural similarity
def structural_similarity(code1: str, lang1: str, code2: str, lang2: str) -> float:
    """
    Compute structural similarity using ratio-based deterministic AST features.
    FIXED: Uses ratios instead of absolute counts to prevent large 'total_nodes' 
    from dominating the similarity calculation.
    Note: Production system utilizes deterministic ratio-based approach (not GIN).
    """
    ast_nodes1 = extract_ast_nodes(code1, lang1)
    ast_nodes2 = extract_ast_nodes(code2, lang2)
    
    # Check for parse failures
    if not ast_nodes1 or ast_nodes1[0]['type'] == 'ERROR':
        print(f"  Structural similarity: 0.0 (parse error in {lang1})")
        return 0.0
    if not ast_nodes2 or ast_nodes2[0]['type'] == 'ERROR':
        print(f"  Structural similarity: 0.0 (parse error in {lang2})")
        return 0.0
    
    # FIXED: Pass root node and full lookup
    root1 = ast_nodes1[0] if ast_nodes1 else {'type': 'ERROR', 'children': []}
    root2 = ast_nodes2[0] if ast_nodes2 else {'type': 'ERROR', 'children': []}
    norm_ast1 = normalize_ast_to_universal([root1], ast_nodes1)
    norm_ast2 = normalize_ast_to_universal([root2], ast_nodes2)
    
    if not norm_ast1 or not norm_ast2:
        print(f"  Structural similarity: 0.0 (normalization failed)")
        return 0.0
    
    # Extract structural features
    def extract_features(norm_ast):
        features = {
            'loop_count': 0,
            'if_count': 0,
            'function_count': 0,
            'assignment_count': 0,
            'binary_op_count': 0,
            'total_nodes': 0,
            'max_depth': 0,
            'avg_branches': 0.0,
            'unique_types': set()
        }
        
        total_branches = 0
        branch_nodes = 0
        
        def traverse(node, depth=0):
            nonlocal total_branches, branch_nodes
            features['total_nodes'] += 1
            features['max_depth'] = max(features['max_depth'], depth)
            
            node_type = node.get('type', '')
            features['unique_types'].add(node_type)
            
            if 'Loop' in node_type:
                features['loop_count'] += 1
                branch_nodes += 1
                total_branches += node.get('attrs', {}).get('branches', 0)
            elif 'If' in node_type:
                features['if_count'] += 1
                branch_nodes += 1
                total_branches += node.get('attrs', {}).get('branches', 0)
            elif 'Function' in node_type:
                features['function_count'] += 1
            elif 'Assign' in node_type:
                features['assignment_count'] += 1
            elif 'BinaryOp' in node_type:
                features['binary_op_count'] += 1
            
            for child in node.get('children', []):
                traverse(child, depth + 1)
        
        for root in norm_ast:
            traverse(root)
        
        features['avg_branches'] = total_branches / branch_nodes if branch_nodes > 0 else 0.0
        features['unique_type_count'] = len(features['unique_types'])
        del features['unique_types']
        
        return features
    
    feat1 = extract_features(norm_ast1)
    feat2 = extract_features(norm_ast2)
    
    print(f"  Raw features {lang1}: loops={feat1['loop_count']}, ifs={feat1['if_count']}, "
          f"funcs={feat1['function_count']}, assigns={feat1['assignment_count']}, "
          f"binops={feat1['binary_op_count']}, nodes={feat1['total_nodes']}")
    print(f"  Raw features {lang2}: loops={feat2['loop_count']}, ifs={feat2['if_count']}, "
          f"funcs={feat2['function_count']}, assigns={feat2['assignment_count']}, "
          f"binops={feat2['binary_op_count']}, nodes={feat2['total_nodes']}")
    
    # CRITICAL FIX: Normalize to ratios to prevent absolute count domination
    def normalize_features(feat):
        total = max(feat['total_nodes'], 1)
        return {
            'loop_ratio': feat['loop_count'] / total,
            'if_ratio': feat['if_count'] / total,
            'function_ratio': feat['function_count'] / total,
            'assignment_ratio': feat['assignment_count'] / total,
            'binary_op_ratio': feat['binary_op_count'] / total,
            'depth_normalized': min(feat['max_depth'] / 20.0, 1.0),
            'branches_normalized': min(feat['avg_branches'] / 5.0, 1.0),
            'type_diversity': min(feat['unique_type_count'] / 50.0, 1.0)
        }
    
    norm_feat1 = normalize_features(feat1)
    norm_feat2 = normalize_features(feat2)
    
    print(f"  Normalized {lang1}: {norm_feat1}")
    print(f"  Normalized {lang2}: {norm_feat2}")
    
    # Create feature vectors
    feature_names = ['loop_ratio', 'if_ratio', 'function_ratio', 'assignment_ratio',
                     'binary_op_ratio', 'depth_normalized', 'branches_normalized', 'type_diversity']
    vec1 = np.array([norm_feat1[f] for f in feature_names], dtype=float)
    vec2 = np.array([norm_feat2[f] for f in feature_names], dtype=float)
    
    # CRITICAL FIX: Use Euclidean distance + cosine similarity
    # Euclidean distance is more sensitive to differences in ratios
    euclidean_dist = np.linalg.norm(vec1 - vec2)
    euclidean_sim = np.exp(-2.0 * euclidean_dist)  # Exponential decay, factor of 2 for sensitivity
    
    # Also compute cosine similarity
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 > 1e-9 and norm2 > 1e-9:
        cosine_sim = np.dot(vec1, vec2) / (norm1 * norm2)
        cosine_sim = max(0.0, cosine_sim)  # Clamp negative values
    else:
        cosine_sim = 0.0
    
    print(f"  Euclidean distance: {euclidean_dist:.3f} -> similarity: {euclidean_sim:.3f}")
    print(f"  Cosine similarity: {cosine_sim:.3f}")
    
    # Use minimum of both metrics (conservative approach)
    similarity = min(euclidean_sim, cosine_sim)
    similarity = max(0.0, min(1.0, similarity))
    
    print(f"  Final structural similarity: {similarity:.3f}")
    
    return similarity


# Phase 4: Dynamic Scoring (INTEGRATED WITH GATING MODEL)
def compute_d_lang(code1: str, code2: str, lang1: str = None, lang2: str = None) -> float:
    """
    Compute language dissimilarity using explicit parameters.
    Returns 0.0 if same language, 1.0 if different.
    """
    if lang1 is not None and lang2 is not None:
        result = 0.0 if lang1 == lang2 else 1.0
        return result
    
    # Fallback to langid (unreliable)
    try:
        detected1, _ = classify(code1)
        detected2, _ = classify(code2)
        return 0.0 if detected1 == detected2 else 1.0
    except:
        return 0.5


def gating_weights(s_codebert: float, s_ast: float, s_token: float, d_lang: float) -> Tuple[float, float, float]:
    """Predict weights using the trained gating network."""
    # REMOVED THE s_codebert_adjusted PATCH
    s_codebert_minus_s_ast = abs(s_codebert - s_ast) # Use the real s_codebert
    one_minus_s_ast = 1.0 - s_ast
    
    x_input = np.array([
        [s_codebert, s_ast, s_token, d_lang, s_codebert_minus_s_ast, one_minus_s_ast]
    ], dtype=np.float32)
    
    x_tensor = torch.from_numpy(x_input).to(device)
    
    with torch.no_grad():
        weights = gating_model(x_tensor)
        w_codebert, w_ast, w_token = weights[0].cpu().numpy()
    
    print(f"  Gating Network Weights - CodeBERT: {w_codebert:.3f}, AST: {w_ast:.3f}, Token: {w_token:.3f}")
    
    return w_codebert, w_ast, w_token

def compute_complexity(ast_nodes: List[Dict[str, Any]]) -> float:
    """Compute code complexity from AST"""
    if not ast_nodes:
        return 0.5
    
    num_branches = 0
    node_count = len(ast_nodes)
    
    for node in ast_nodes:
        node_type = node.get('type', '')
        if any(keyword in node_type for keyword in ['if', 'for', 'while', 'switch', 'case', '?']):
            num_branches += 1
    
    max_depth = 0
    visited = {}
    
    def get_depth(node_id: int):
        nonlocal max_depth
        if node_id in visited:
            return visited[node_id]
        if node_id >= len(ast_nodes):
            return 0
        
        children = ast_nodes[node_id].get('children', [])
        if not children:
            visited[node_id] = 1
            return 1
        
        child_depths = [get_depth(cid) for cid in children if cid < len(ast_nodes)]
        depth = 1 + (max(child_depths) if child_depths else 0)
        visited[node_id] = depth
        max_depth = max(max_depth, depth)
        return depth
    
    if ast_nodes:
        get_depth(0)
    
    cyclomatic = num_branches + 1
    complexity_score = (max_depth * 0.4) + (cyclomatic * 0.4) + (node_count * 0.2 / 50.0)
    
    return min(complexity_score / 10.0, 1.0)


def adaptive_threshold(original_scores: List[float], complexities: List[float] = None) -> float:
    """
    Compute adaptive threshold using methodology-compliant k values (1.2-1.8).
    """
    if not original_scores:
        return 0.5  # Default for gating model (binary classification)
    
    mu = statistics.mean(original_scores)
    sigma = statistics.stdev(original_scores) if len(original_scores) > 1 else 0.10
    avg_comp = np.mean(complexities) if complexities and len(complexities) > 0 else 0.5
    
    # Simple assignments (low complexity) constrain the solution space, so honest students
    # converge on similar-looking code and the detector needs more evidence before flagging --
    # hence the larger multiplier. Complex assignments admit many distinct correct solutions,
    # so genuine convergence is unlikely and a smaller margin is already informative.
    # (Matches Equation 13 / Section "Adaptive Threshold" in the manuscript.)
    k = 1.2 if avg_comp >= 0.6 else 1.8
    threshold = mu + k * sigma
    
    # Reasonable bounds
    return max(0.40, min(0.80, threshold))


def dynamic_score(s_codebert: float, s_ast: float, s_token: float, d_lang: float,
                  original_scores: List[float] = None, complexities: List[float] = None) -> Dict[str, Any]:
    """Compute final dynamic score using GATING WEIGHTS"""
    w_codebert, w_ast, w_token = gating_weights(s_codebert, s_ast, s_token, d_lang)  # ✅ Fixed order
    final_score = w_codebert * s_codebert + w_ast * s_ast + w_token * s_token
    threshold = adaptive_threshold(original_scores or [], complexities or [])
    
    return {
        'weights': {'codebert': w_codebert, 'ast': w_ast, 'token': w_token},
        'final_score': final_score,
        'threshold': threshold,
        'is_plagiarism': final_score > threshold
    }


def load_code_from_file(file_path: str) -> str:
    """Load code from file"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def process_pair(original_code: str, gpt_code: str, lang1: str = 'java', lang2: str = 'java',
                 original_scores: List[float] = None) -> Dict[str, Any]: # REMOVED batch_embeddings
    """Process a code pair and compute all metrics"""
    print(f"\n{'=' * 80}")
    print(f"PROCESSING: {lang1} vs {lang2}")
    print(f"{'=' * 80}")
    
    d_lang = compute_d_lang(original_code, gpt_code, lang1, lang2)
    print(f"Language dissimilarity: {d_lang:.3f}")
    
    print("\nComputing semantic similarity (with sliding window comparison)...")
    s_codebert = semantic_similarity_pair(original_code, gpt_code, lang1, lang2) # This now calls the correct logic
    print(f"Semantic similarity: {s_codebert:.3f}")
    
    print("\nComputing syntactic similarity...")
    s_token = syntactic_similarity(original_code, gpt_code, lang1, lang2)
    print(f"Syntactic similarity: {s_token:.3f}")
    
    print("\nComputing structural similarity (ratio-based)...")
    s_ast = structural_similarity(original_code, lang1, gpt_code, lang2)
    
    ast_nodes_orig = extract_ast_nodes(original_code, lang1)
    comp = compute_complexity(ast_nodes_orig) if ast_nodes_orig and ast_nodes_orig[0]['type'] != 'ERROR' else 0.5
    
    result = dynamic_score(s_codebert, s_ast, s_token, d_lang, original_scores, [comp])
    result.update({
        'semantic': s_codebert,
        'syntactic': s_token,
        'structural': s_ast,
        'd_lang': d_lang,
        'complexity': comp
    })
    
    return result


# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plagiarism Detection with Gating Model")
    parser.add_argument('--file1', type=str, required=True, help="Path to first code file")
    parser.add_argument('--file2', type=str, required=True, help="Path to second code file")
    parser.add_argument('--lang1', type=str, default='java', choices=['java', 'python', 'c', 'csharp'], help="Language of file1")
    parser.add_argument('--lang2', type=str, default='java', choices=['java', 'python', 'c', 'csharp'], help="Language of file2")
    args = parser.parse_args()

    # Load code from files
    code1 = load_code_from_file(args.file1)
    code2 = load_code_from_file(args.file2)

    # Process the pair
    result = process_pair(code1, code2, args.lang1, args.lang2)

    # Output
    print(f"\n{'=' * 80}")
    print(f"FINAL RESULTS: {os.path.basename(args.file1)} vs {os.path.basename(args.file2)}")
    print(f"{'=' * 80}")
    print(f"  Semantic Similarity:    {result['semantic']:.3f}")
    print(f"  Syntactic Similarity:   {result['syntactic']:.3f}")
    print(f"  Structural Similarity:  {result['structural']:.3f}")
    print(f"  Language Dissimilarity: {result['d_lang']:.3f}")
    print(f"  Complexity:             {result['complexity']:.3f}")
    print(f"  Gating Weights (CodeBERT/AST/Token): {result['weights']['codebert']:.3f} / {result['weights']['ast']:.3f} / {result['weights']['token']:.3f}")
    print(f"  Final Score:            {result['final_score']:.3f}")
    print(f"  Threshold:              {result['threshold']:.3f}")
    print(f"  Prediction:             {'PLAGIARISM (CLONE)' if result['is_plagiarism'] else 'NO PLAGIARISM'}")
    print(f"  Confidence Margin:      {result['final_score'] - result['threshold']:.3f}")
    print(f"{'=' * 80}")

    print("\n✓ Detection complete!")
    print("\nUsage: python detector_v9.py --file1 path/to/code1.java --file2 path/to/code2.py --lang1 java --lang2 python")