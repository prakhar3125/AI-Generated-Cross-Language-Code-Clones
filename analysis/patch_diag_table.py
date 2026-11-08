"""One-off patch of make_tables.py: the diagnostic-cases table must use the stored fused score (log-odds fusion is not a weighted sum)."""
p = 'make_tables.py'
s = open(p, encoding='utf8', newline='').read()

def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)

rep('    W = r["S"]["test__gate_w"][0]\n',
    '    W = r["S"]["test__gate_w"][0]\n    FUS = r["S"]["test__gate"][0]          # stored fused score of seed 0 (weighted mean, or log-odds fusion when LO)\n')
rep('        fus = float((w * S3).sum())\n', '        fus = float(FUS[i])\n')
old = r'The gate column is $\sum_i w_i S_i$; the static column is the unweighted mean of the three scores.}",'
new = (r'The gate column is the fused score (" + (r"log-odds fusion, Eq.~\ref{eq:logit}" if LO else r"$\sum_i w_i S_i$") '
       r'+ r"); the static column is the unweighted mean of the three scores.}",')
rep(old, new)
open(p, 'w', encoding='utf8', newline='').write(s)
print('patched')
