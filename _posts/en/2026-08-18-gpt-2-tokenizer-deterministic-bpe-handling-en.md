---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GPT-2 Tokenizer: Deterministic BPE Handling"
translated: false
type: note
---

Question: In LLM tokenizers (like those used in nanoGPT/GPT-2), how are punctuation, contractions, and non-English words handled — and can the same string tokenize differently in different contexts?

Answer:

**GPT-2 uses Byte Pair Encoding (BPE)**, implemented via the `tiktoken` library (or the original `gpt2` tokenizer). Here's how it handles your specific cases:

---

**Punctuation like `, . '`**

These are treated as separate tokens or merged with adjacent characters based on BPE merge rules. GPT-2's tokenizer also applies a **pre-tokenization regex** that splits text *before* BPE runs, roughly like:

```
's|'t|'re|'ve|'m|'ll|'d| ?\w+| ?\d+| ?[^\s\w\d]+|\s+
```

So punctuation is explicitly split off first, then BPE merges are applied within each chunk.

---

**Contractions like `I'm`**

The pre-tokenization regex handles common English contractions as **fixed patterns**:
- `I'm` → always splits into `I` + `'m` (two tokens)
- `don't` → `don` + `'t`
- `they're` → `they` + `'re`

So **no** — `I'm` will **not** sometimes be one token and sometimes two. The regex guarantees a consistent split *before* BPE ever runs. The tokenization is **deterministic and context-free** — the same string always produces the same tokens.

---

**Non-English words**

BPE operates on **bytes**, so any Unicode character is valid. However:
- Common English subwords have learned merge rules (e.g., `un` + `der` → `under`)
- Rare or non-English words get fragmented into small pieces or even **individual UTF-8 bytes**
- Example: a Chinese character like `你` might become 3 byte-tokens: `\xe4`, `\xbd`, `\xa0`

GPT-2's vocabulary of 50,257 tokens was trained almost entirely on English text, so non-English languages are very inefficient — a single Chinese word may cost 3–6 tokens vs. 1 for an English word.

---

**Is tokenization ever context-dependent?**

For GPT-2/tiktoken: **No.** It's a pure deterministic function. The same bytes → the same tokens, always.

Some newer tokenizers (like those used in T5 or some multilingual models) apply **sentencepiece** with normalization that *can* vary slightly by context, but that's a different design.

---

References:
- [OpenAI tiktoken](https://github.com/openai/tiktoken)
- [GPT-2 tokenizer (Hugging Face)](https://huggingface.co/docs/transformers/model_doc/gpt2#transformers.GPT2Tokenizer)
- [BPE explanation — Sennrich et al. 2016](https://arxiv.org/abs/1508.07909)
- [nanoGPT by Karpathy](https://github.com/karpathy/nanoGPT)
