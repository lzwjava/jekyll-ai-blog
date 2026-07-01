---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tokenization and File Compression Ratios Explained
translated: false
type: note
---

Yes, this is completely normal! Here's why:

## The Math

**Raw text** → **Tokenized (uint16)** conversion:

```
Original:  "The cat sat on the mat"
Chars:     20 characters × 1 byte = 20 bytes
Tokens:    ~5 tokens × 2 bytes = 10 bytes  (GPT-2 BPE tokenization)
```

**Compression ratio: ~2-4x from text to tokens**

## Your Numbers

| File | Size | Token Count | Calculation |
| ------ | ------ | ------------- | ------------ |
| Raw text (full) | 61 GB | ~15B tokens* | 61GB ÷ ~4 chars/token |
| Raw text (sample) | 477 MB | ~114M tokens | 477MB ÷ ~4 chars/token |
| `train.bin` | **27 MB** | **14M tokens** | 14M × 2 bytes |
| `val.bin` | **191 MB** | **100M tokens** | 100M × 2 bytes |

*Assuming ~4 chars/token average for English text with GPT-2 tokenizer

## Why So Small?

1. **Text → Tokens**: English compresses ~2-4x when tokenized (common words become single tokens)
2. **uint16**: Each token stored as 2 bytes (vs ~4 bytes for Python int)
3. **Partial data**: You only prepared a **477MB sample** of the 61GB file (less than 1%)

## Real-World Comparison

nanoGPT's standard Shakespeare dataset:

- Raw text: ~1MB
- Tokenized `train.bin`: ~1MB
- FineWeb full (10B tokens): ~20GB tokenized

---

**So 27MB train.bin from 477MB text sample = ~18x compression. That's normal.** If you prepared the full 61GB, you'd get ~30GB of `.bin` files total.
