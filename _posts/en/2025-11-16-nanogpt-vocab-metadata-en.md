---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: nanoGPT Vocabulary Metadata File
translated: false
type: note
---

In **nanoGPT** (https://github.com/karpathy/nanoGPT), the file **meta.pkl** is an optional pickle file that stores the vocabulary and encoding metadata for the dataset. It is used when you train on your own custom text dataset (not the default OpenWebText or Shakespeare char-level datasets).

### What meta.pkl typically contains
It’s a dictionary with these keys (example):

```python
{
    'vocab_size': 50257,       # size of the vocabulary
    'itos': {0: 'A', 1: 'B', ...},  # int → string (token)
    'stoi': {'A': 0, 'B': 1, ...},  # string → int (token)
    'encoder': ...,            # the encode function
    'decoder': ...,            # the decode function
}
```

### When nanoGPT loads or creates meta.pkl

1. During training (`train.py`):
   - If `data/your_dataset/meta.pkl` already exists → it loads the vocabulary from there.
   - If it does **not** exist → nanoGPT builds a new vocabulary from the text in your dataset (usually with SentencePiece, tiktoken, or a simple char-level vocab) and saves it as `meta.pkl` for future use.

2. During sampling/inference (`sample.py`):
   - When you see the message
     `No meta.pkl found, assuming GPT-2 encodings...`
     it means nanoGPT couldn’t find a meta.pkl file in your data directory.
   - So it falls back to the default GPT-2 BPE tokenizer (the same one used by OpenAI’s GPT-2) with vocab_size = 50257. That’s why your 29.94M parameter model (which is the smallest GPT-2 124M config but incorrectly reported sometimes) works fine even without meta.pkl when you train on OpenWebText or similar datasets.

### So, in short:

| Situation                              | What meta.pkl does                                      |
|----------------------------------------|----------------------------------------------------------|
| You train on a **custom dataset**      | Stores your custom vocabulary so encoding/decoding is consistent |
| You train on OpenWebText/Shakespeare   | Not needed → nanoGPT just uses GPT-2 tokenizer by default |
| `sample.py` can’t find meta.pkl        | Falls back to GPT-2 tokenizer (which is what you saw)    |

If you ever train your own dataset and want reproducible tokenization (or a different vocab size), you’ll see nanoGPT create meta.pkl automatically on the first training run. After that it will reuse it and you won’t get the “assuming GPT-2 encodings” warning anymore.
