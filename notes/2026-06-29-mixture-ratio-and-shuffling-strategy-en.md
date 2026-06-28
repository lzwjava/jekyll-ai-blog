---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mixture Ratio and Shuffling Strategy
translated: false
type: note
---

Question: When training nanoGPT (or similar) on a 50% FineWeb / 50% GitHub code mix, should each batch be half code / half natural language, and should the training data be shuffled?

Answer:

Short version: you want the **mixture ratio to hold in expectation**, not exactly per-batch. And yes, shuffle — but *how* you shuffle matters more than the fact that you do.

## You don't need exactly half-and-half per batch

Forcing every batch to be precisely 50% code / 50% text is **stratified sampling**. It's not wrong, but it's usually unnecessary and adds complexity. With a 1024-sequence batch, random sampling from a 50/50 pool already gives you ~512±16 code sequences per batch (binomial std ≈ √(1024·0.5·0.5) ≈ 16). The gradient sees the right ratio over any handful of steps. The variance is noise that SGD absorbs fine.

When per-batch balancing *does* matter:
- **Tiny batches** (e.g. 8–16 seqs) where binomial variance is large relative to batch size.
- **Domain-conditioned losses / per-domain metrics** you want stable each step.
- **Curriculum or loss-weighting** schemes that treat domains differently.

For standard pretraining, mix-in-expectation is the norm. This is exactly how the big runs do it — you set sampling weights per source and draw randomly.

## The real question: token ratio vs document ratio

"50/50" is ambiguous. Do you mean 50% of *documents*, or 50% of *tokens*? These diverge hard because code and prose tokenize differently (code has more whitespace, shorter lines, more punctuation). You almost always want **50% of tokens**, because the model learns from tokens, not documents. Compute the token counts per corpus first, then set sampling weights to hit the token ratio you want.

## Shuffling: the nanoGPT reality

nanoGPT doesn't shuffle a list of documents at train time. It pre-tokenizes everything into one giant flat `train.bin` (a `uint16` memmap), then samples random offsets:

```python
# nanoGPT data loading — the actual mechanism
data = np.memmap('train.bin', dtype=np.uint16, mode='r')

def get_batch():
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([torch.from_numpy(data[i:i+block_size].astype(np.int64)) for i in ix])
    y = torch.stack([torch.from_numpy(data[i+1:i+1+block_size].astype(np.int64)) for i in ix])
    return x, y
```

So the "shuffle" is **random offset sampling**, not list permutation. The critical consequence: **how you lay out the .bin determines your mix.** If you write all FineWeb first, then all GitHub, random offsets still cover both regions uniformly over an epoch — but any *single* batch's composition depends on where its offsets land, and sequences spanning the boundary are garbage.

Two clean approaches:

**Approach A — interleave at write time (single .bin):**
Shuffle documents *before* tokenizing so code and text are interspersed in the flat buffer. Then random offset sampling naturally yields mixed batches.

```python
import numpy as np, random

# docs: list of token arrays, each tagged by source
docs = fineweb_docs + github_docs
random.shuffle(docs)  # interleave sources in the buffer

# concatenate with a doc separator (EOT token) between docs
sep = np.array([eot_token], dtype=np.uint16)
buf = np.concatenate([np.concatenate([d, sep]) for d in docs])
buf.tofile('train.bin')
```

**Approach B — separate .bins + weighted sampling (cleaner for ratio control):**
Keep `fineweb.bin` and `github.bin` separate, and pick the source per-sequence by weight. This decouples ratio from disk layout and lets you change the mix without re-tokenizing:

```python
fw = np.memmap('fineweb.bin', dtype=np.uint16, mode='r')
gh = np.memmap('github.bin',  dtype=np.uint16, mode='r')

# token-weighted: w = fraction of tokens you want from each
weights = {'fw': 0.5, 'gh': 0.5}

def get_batch(batch_size, block_size):
    xs, ys = [], []
    for _ in range(batch_size):
        src = fw if random.random() < weights['fw'] else gh
        i = random.randint(0, len(src) - block_size - 1)
        xs.append(torch.from_numpy(src[i:i+block_size].astype(np.int64)))
        ys.append(torch.from_numpy(src[i+1:i+1+block_size].astype(np.int64)))
    return torch.stack(xs), torch.stack(ys)
```

I'd use **Approach B**. It's how production data loaders work (think Megatron's blended dataset / DataMix), gives exact ratio control, and you can sweep mix ratios cheaply.

## Two things people get wrong

1. **EOT separators between documents.** Without an end-of-text token between concatenated docs, sequences bleed across document boundaries and the model learns spurious continuations from FineWeb prose into a code file. Always insert the EOT token (`<|endoftext|>` = 50256 for GPT-2 BPE) between docs.

2. **Tokenizer for code.** GPT-2's BPE is bad at code (no good whitespace/indent handling — runs of spaces blow up token counts). If code is 50% of your data, this matters. Consider a tokenizer with whitespace merges (GPT-4's `cl100k`/`o200k` via tiktoken, or train your own BPE on the mixed corpus). This also fixes your token-ratio math, since FineWeb prose and code tokenize at very different bytes-per-token.

## Bottom line

- Mix **in expectation**, not exactly per-batch — random sampling handles the rest.
- Target **token** ratio, not document ratio.
- "Shuffle" in nanoGPT = random offset sampling; ensure your **layout or weighted sampler** delivers the mix, and **separate .bins + weighted draw** is the cleanest way.
- Insert **EOT tokens** between docs, and reconsider the **tokenizer** if code is half your data.

References:

- [nanoGPT — karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
- [tiktoken](https://github.com/openai/tiktoken)
- [Megatron-LM blendable dataset](https://github.com/NVIDIA/Megatron-LM)
