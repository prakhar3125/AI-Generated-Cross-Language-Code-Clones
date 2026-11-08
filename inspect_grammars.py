import pandas as pd
from tree_sitter import Language, Parser
import tree_sitter_python as tspy
import tree_sitter_java as tsjava
import tree_sitter_c as tsc
import tree_sitter_c_sharp as tscs

LANGS = {
    'python': Language(tspy.language()),
    'java': Language(tsjava.language()),
    'c': Language(tsc.language()),
    'csharp': Language(tscs.language()),
}
PARSERS = {k: Parser(v) for k, v in LANGS.items()}

df = pd.read_csv('code_clones.csv')
row = df.iloc[0]


def collect_types(node, acc):
    acc.add(node.type)
    for ch in node.children:
        collect_types(ch, acc)


for lang in ['python', 'java', 'c', 'csharp']:
    code = row[lang]
    tree = PARSERS[lang].parse(bytes(code, 'utf8'))
    types = set()
    collect_types(tree.root_node, types)
    print(lang, '->', sorted(types))
    print()
