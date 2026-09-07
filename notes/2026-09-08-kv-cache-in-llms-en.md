---
audio: false
generated: true
image: false
lang: en
layout: post
title: KV Cache in LLMs
translated: false
type: note
---

Question: What is KV cache (Key-Value cache) in the context of LLMs?

Answer:

KV cache (Key-Value cache) is an optimization technique used in transformer-based language models to avoid redundant computation during text generation.

**How transformers work (briefly):**
In the attention mechanism, every token produces three vectors: **Query (Q)**, **Key (K)**, and **Value (V)**. To generate each new token, the model computes attention over *all previous tokens* — meaning it needs their K and V vectors.

**The problem without caching:**
Without a cache, the model would recompute the K and V vectors for every previously seen token on *every single generation step* — extremely wasteful.

**What KV cache does:**
It stores the K and V vectors of already-processed tokens in memory (RAM or VRAM). When generating the next token, the model simply:

1. Computes K/V only for the *new* token
2. **Appends** it to the cached K/V vectors
3. Runs attention using the full cached history

This reduces per-step computation from O(n²) to roughly O(n), dramatically speeding up inference.

**Trade-offs:**

| Benefit | Cost |
| --- | --- |
| Much faster token generation | High memory usage |
| Reduced redundant computation | Memory grows with context length |
| Essential for long contexts | Can limit batch size on GPUs |

**Where you'll encounter it:**

- Anthropic's **prompt caching** feature — caches the KV state of a reused system prompt so you don't pay compute cost on repeated calls
- vLLM's **PagedAttention** — manages KV cache memory like OS virtual memory
- **Speculative decoding** — shares KV cache between draft and target models

References:

- [Anthropic Prompt Caching Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Efficient Memory Management for LLM Serving with PagedAttention](https://arxiv.org/abs/2309.06180)
- [The Illustrated Transformer – Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
