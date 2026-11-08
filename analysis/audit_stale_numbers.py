"""After the Eq. 2 retrain: for every regenerated table, list numbers that were in the OLD table row but are not in the NEW
row, then find where the manuscript prose quotes them (candidate stale sites for manual review).
python -I audit_stale_numbers.py"""
import glob, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(HERE, "..", "..", "backup_pre_eq2fix", "tables")
NEW = os.path.join(HERE, "tables")
PARTS = os.path.join(HERE, "..", "..", "r2", "parts")
prose = {}
for f in sorted(glob.glob(os.path.join(PARTS, "p[1-4]*.tex"))):
    prose[os.path.basename(f)] = open(f, encoding="utf8").read().split("\n")
num = re.compile(r"(?<![\d.])\d+\.\d+(?![\d])")
report = {}
for f in sorted(glob.glob(os.path.join(NEW, "tab_*.tex"))):
    b = os.path.basename(f)
    o = os.path.join(OLD, b)
    if not os.path.exists(o):
        continue
    ol, nl = open(o, encoding="utf8").read().split("\n"), open(f, encoding="utf8").read().split("\n")
    if len(ol) != len(nl):
        print("LINE COUNT DIFFERS", b); continue
    for a, c in zip(ol, nl):
        if a == c or "&" not in a:
            continue
        label = a.split("&")[0].strip()[:40]
        olds, news = num.findall(a), num.findall(c)
        gone = [x for x in olds if x not in news]
        for g in set(gone):
            report.setdefault(g, set()).add((b, label))
rows = []
for g, srcs in sorted(report.items()):
    hits = []
    for p, lines in prose.items():
        for i, l in enumerate(lines, 1):
            for m in re.finditer(r"(?<![\d.])" + re.escape(g) + r"(?![\d])", l):
                hits.append((p, i, l[max(0, m.start() - 55):m.end() + 35].replace("\n", " ")))
    if hits:
        rows.append((g, sorted(srcs)[:2], hits))
print("old values that disappeared from a table row AND occur in the prose:", len(rows))
for g, srcs, hits in rows:
    print("\n== %s   (table: %s)" % (g, "; ".join("%s/%s" % s for s in srcs)))
    for p, i, ctx in hits[:6]:
        print("   %s:%d  ...%s..." % (p, i, ctx))
