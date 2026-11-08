# -*- coding: utf-8 -*-
"""Mean-pooled UniXcoder embeddings (first 512 tokens) for every benchmark snippet -> data/unixcoder_emb.npz"""
import os
import pickle
import sys
import time

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA  # noqa: E402

torch.set_num_threads(10)
tok = AutoTokenizer.from_pretrained("microsoft/unixcoder-base")
mdl = AutoModel.from_pretrained("microsoft/unixcoder-base").eval()
S = pickle.load(open(os.path.join(DATA, "snippets.pkl"), "rb"))
keys = sorted(S)
order = sorted(range(len(keys)), key=lambda i: len(S[keys[i]][1]))
emb = np.zeros((len(keys), mdl.config.hidden_size), dtype=np.float32)
t0 = time.time()
with torch.inference_mode():
    i = 0
    while i < len(order):
        bs = 32
        idx = order[i:i + bs]
        enc = tok([S[keys[j]][1] for j in idx], return_tensors="pt", padding=True, truncation=True, max_length=512)
        h = mdl(**enc).last_hidden_state
        m = enc["attention_mask"].unsqueeze(-1).float()
        emb[idx] = ((h * m).sum(1) / m.sum(1)).numpy()
        i += bs
        if (i // bs) % 40 == 0:
            print(i, len(order), "%.0fs" % (time.time() - t0), flush=True)
np.savez_compressed(os.path.join(DATA, "unixcoder_emb.npz"), keys=np.array(keys), emb=emb)
print("saved", time.time() - t0)
