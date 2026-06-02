---
audio: false
generated: true
image: false
lang: en
layout: post
title: Load GloVe Vectors Two Ways
translated: false
type: note
---

You’ve got two easy ways to get GloVe vectors for words like `the`, `to`, `U.S.` and for your own text:

---

## Option A — Download Stanford GloVe and look up with `gensim`

This is the most common route and works fully offline once downloaded.

```python
# 1) Download & unzip (first run only)
import os, zipfile, urllib.request
url = "https://nlp.stanford.edu/data/glove.6B.zip"
zip_path = "glove.6B.zip"
if not os.path.exists(zip_path):
    urllib.request.urlretrieve(url, zip_path)
with zipfile.ZipFile(zip_path) as zf:
    zf.extract("glove.6B.300d.txt")  # 300-dim set

# 2) Convert GloVe format -> word2vec text format and load
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors

glove_path = "glove.6B.300d.txt"
w2v_path   = "glove.6B.300d.w2v.txt"
if not os.path.exists(w2v_path):
    glove2word2vec(glove_path, w2v_path)

vectors = KeyedVectors.load_word2vec_format(w2v_path, binary=False)
print(vectors.vector_size)  # 300

# 3) Single-word lookups
print(vectors['the'][:5])   # first 5 dims
print(vectors['to'][:5])

# NOTE: glove.6B vocabulary is lowercased.
# 'U.S.' -> 'u.s.' in this vocab (if present). Safer: lowercase your tokens.
print(vectors['u.s.'][:5])
```

Now embed your own text:

```python
import re, numpy as np

# simple tokenizer that keeps dots in tokens like u.s.
TOKEN_RE = re.compile(r"[A-Za-z0-9\.\-']+")

def tokenize(text: str):
    return TOKEN_RE.findall(text.lower())

def embed_tokens(tokens, kv: KeyedVectors):
    vecs = [kv[w] for w in tokens if w in kv.key_to_index]
    return np.stack(vecs) if vecs else np.zeros((0, kv.vector_size))

def embed_sentence_avg(text: str, kv: KeyedVectors):
    V = embed_tokens(tokenize(text), kv)
    return V.mean(axis=0) if V.size else np.zeros(kv.vector_size)

# Examples
print(embed_sentence_avg("The quick brown fox jumps over the lazy dog.", vectors)[:10])
print(embed_tokens(tokenize("U.S. interest rates rose today."), vectors).shape)  # (n_tokens, 300)
```

**Tips**

* `glove.6B.300d.txt` ≈ 1.1 GB in memory. If that’s heavy, try `100d` instead.
* The 6B set is **lowercased**; always lowercase your text, or use the larger **840B** set if you need more coverage (still largely uncased in practice).
* OOV (out-of-vocabulary) words return nothing; you can skip them or back off to subword heuristics.

---

## Option B — Let `torchtext` download and serve GloVe for you

This avoids manual downloading/conversion.

```python
import torch
from torchtext.vocab import GloVe
import re

glove = GloVe(name="6B", dim=300)  # auto-downloads to ~/.vector_cache
stoi = glove.stoi    # word -> index
vecs = glove.vectors # tensor [vocab, 300]

def get_word_vec(word: str):
    idx = stoi.get(word.lower())
    return vecs[idx] if idx is not None else None

print(get_word_vec("the")[:5])
print(get_word_vec("to")[:5])
print(get_word_vec("U.S.")[:5])     # becomes None in many builds; try "u.s.":
print(get_word_vec("u.s.")[:5])

# Sentence embedding (average)
TOKEN_RE = re.compile(r"[A-Za-z0-9\.\-']+")
def embed_sentence_avg(text: str):
    toks = TOKEN_RE.findall(text.lower())
    xs = [get_word_vec(t) for t in toks]
    xs = [x for x in xs if x is not None]
    return torch.stack(xs, dim=0).mean(0) if xs else torch.zeros(glove.dim)

print(embed_sentence_avg("The quick brown fox...")[:10])
```

---

## What you asked about the specific rows

Those rows like:

```
the  0.418 0.24968 -0.41242 0.1217 ... 0.34527  # 300 floats total
to   0.68047 -0.039263 -0.67412 0.056051 ... -0.067549
U.S. 0.3459  0.21513  -0.09982 0.25344 ... 0.024118
```

are exactly what you’ll see in the plain‐text `.txt` files: each line is `token` followed by `300` floats. With `gensim` or `torchtext`, you don’t need to parse lines yourself—they handle it and give you direct vector lookups.

---

## Common pitfalls (and fixes)

* **“KeyError: ‘U.S.’”** → Use `u.s.` with the 6B set, or pick a larger set with better coverage, and always lowercase before lookup.
* **Huge memory/time** → Use `100d` or `200d` instead of `300d`, or load only needed words by scanning the file and building a smaller vocab.
* **Sentence/Doc vectors** → Average or sum word vectors; for weighted averaging, try TF-IDF weights.

If you want, tell me your exact text processing goal (classification, similarity, clustering, etc.) and I’ll sketch a minimal pipeline using GloVe end-to-end.
