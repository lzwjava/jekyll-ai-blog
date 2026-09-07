---
audio: false
generated: true
image: false
lang: en
layout: post
title: KV Cache Prefill Copy
translated: false
type: note
---

Question: What does the `prefill` method do in this KV cache implementation?

Answer:

This method **copies cached Key-Value data from one cache into another**, enabling efficient parallel sampling after a shared prefill pass.

## Context: Why This Exists

A common inference optimization pattern:

1. Run **prefill once** (batch=1) on the prompt — expensive, but only needed once
2. **Copy** that KV cache into N separate caches
3. Run **N parallel decode streams** (different samples/temperatures) — each starts from the same prompt state

---

## Step-by-Step Breakdown

```python
assert self.get_pos() == 0
```

The destination cache must be **empty** — you can't prefill into an already-used cache.

```python
assert self.n_layers == other.n_layers and self.n_heads == other.n_heads and self.head_dim == other.head_dim
```

Sanity check — both caches must have **compatible architecture dimensions**.

```python
assert self.max_seq_len >= other.max_seq_len
```

Destination must have **at least as much capacity** as the source.

```python
other_pos = other.get_pos()
self.k_cache[:, :, :other_pos, :, :] = other.k_cache[:, :, :other_pos, :, :]
self.v_cache[:, :, :other_pos, :, :] = other.v_cache[:, :, :other_pos, :, :]
```

Copies only the **filled portion** of the source K and V tensors (up to `other_pos`), leaving the rest untouched. The tensor shape is likely `[batch, n_layers, seq_len, n_heads, head_dim]`.

```python
self.cache_seqlens.fill_(other_pos)
```

Tells **every batch slot** in the destination that it currently holds `other_pos` tokens — so decoding resumes from the right position.

```python
if other.prev_embedding is not None:
    self.prev_embedding = other.prev_embedding.expand(self.batch_size, -1, -1).clone()
```

Handles a **"smear" operation**: the source has batch=1, but the destination has `num_samples` batch slots. `.expand()` broadcasts the single embedding across all batch slots, then `.clone()` makes it a concrete (non-view) tensor so each sample can diverge independently.

---

## Visual Flow

```
Source Cache (batch=1, after prompt prefill)
  k_cache: [1, layers, prompt_len, heads, dim]
  v_cache: [1, layers, prompt_len, heads, dim]
         │
         │  prefill()
         ▼
Dest Cache (batch=N, now ready to generate)
  k_cache: [N, layers, prompt_len, heads, dim]  ← same prompt KV for all N
  v_cache: [N, layers, prompt_len, heads, dim]
  cache_seqlens: [prompt_len, prompt_len, ..., prompt_len]  ← N slots
```

Each of the N decode streams then **appends new tokens independently** from this shared starting point.
