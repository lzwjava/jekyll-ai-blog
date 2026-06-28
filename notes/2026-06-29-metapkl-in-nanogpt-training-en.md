---
audio: false
generated: true
image: false
lang: en
layout: post
title: meta.pkl in nanoGPT Training
translated: false
type: note
---

**Question:** What is `meta.pkl` in nanoGPT training?

**Answer:**

`meta.pkl` is the vocabulary metadata file produced by the character-level prep scripts (e.g. `data/shakespeare_char/prepare.py`). It pickles the tokenizer mapping so training and sampling share the same encoding.

It contains exactly three things:

```python
meta = {
    'vocab_size': vocab_size,   # number of unique chars
    'itos': itos,               # int -> str  (decode)
    'stoi': stoi,               # str -> int  (encode)
}
with open('meta.pkl', 'wb') as f:
    pickle.dump(meta, f)
```

Why it exists:

1. **`train.py`** looks for `meta.pkl` in the data dir to auto-set `meta_vocab_size`, so the model's embedding/output layer is sized correctly:

```python
meta_path = os.path.join(data_dir, 'meta.pkl')
if os.path.exists(meta_path):
    with open(meta_path, 'rb') as f:
        meta = pickle.load(f)
    meta_vocab_size = meta['vocab_size']  # else defaults to GPT-2's 50304
```

2. **`sample.py`** loads it to decode generated token ids back to text:

```python
stoi, itos = meta['stoi'], meta['itos']
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: ''.join([itos[i] for i in l])
```

The key point: it's **only generated for the char-level datasets**. GPT-2/BPE datasets (`openwebtext`, `shakespeare` word-level) skip it because they use the fixed tiktoken `gpt2` encoding — there `train.py` falls back to `vocab_size=50304` and `sample.py` uses `tiktoken.get_encoding("gpt2")`.

So: no `meta.pkl` = "use GPT-2 BPE"; `meta.pkl` present = "use this custom char vocab."

**References:**

- [karpathy/nanoGPT — data/shakespeare_char/prepare.py](https://github.com/karpathy/nanoGPT/blob/master/data/shakespeare_char/prepare.py)
- [karpathy/nanoGPT — train.py](https://github.com/karpathy/nanoGPT/blob/master/train.py)
