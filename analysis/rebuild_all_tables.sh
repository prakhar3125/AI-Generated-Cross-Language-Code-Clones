#!/bin/bash
# canonical order for the manuscript tables (log-odds adoption, then the merge steps of make_tables5.py)
cd "$(dirname "$0")"
for f in make_tables.py make_tables2.py make_tables3.py make_tables4.py; do LOGIT_TABLES=1 python -I $f 2>&1 | grep -E "Traceback|Error"; done
python -I adopt_logit_tables.py > /dev/null
for f in make_tables.py make_tables2.py make_tables3.py make_tables4.py; do python -I $f > /dev/null 2>&1; done   # non-gate tables (protocol etc.) from the unmodified run
LOGIT_TABLES=1 python -I make_tables.py > /dev/null 2>&1; python -I adopt_logit_tables.py > /dev/null
python -I make_tables5.py | tail -3
