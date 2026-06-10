---
audio: false
generated: true
image: false
lang: en
layout: post
title: Prefill-then-fork KV cache pattern
translated: false
type: note
---

**Question:** How does the `prefill` method in nanochat's KV cache work — what is it for, and what is each line doing?

**Answer:**

## The big picture: process the prompt once, sample N times

This is the **prefill-then-fork** pattern. When you want multiple samples from the same prompt (best-of-N, pass@k eval, parallel rollouts in RL), the naive approach runs the prompt through the model N times. But the prompt's KV cache is identical for all N samples — so nanochat does:

```
1. Build a KV cache with batch_size=1
2. Run the prompt through the model once  → fills `other`
3. Build a second cache with batch_size=N (this one, `self`)
4. self.prefill(other)                    → copy/broadcast prompt KV into all N rows
5. Decode N samples in parallel, diverging from the same prefix
```

Prompt compute drops from `O(N · prompt_len)` to `O(prompt_len)`. For a 2,000-token prompt and 16 samples, that's a 16x saving on the prefill phase.

## Line by line

```python
assert self.get_pos() == 0, "Cannot prefill a non-empty KV cache"
```
`self` must be fresh — prefill is a wholesale copy into position `[0, other_pos)`, not an append. Merging into a partially-filled cache would corrupt the positional alignment.

```python
assert self.n_layers == other.n_layers and self.n_heads == other.n_heads and self.head_dim == other.head_dim
assert self.max_seq_len >= other.max_seq_len
```
Geometry must match (same model), and the destination needs at least as much sequence room — typically more, since `self` will keep decoding past the prompt.

```python
other_pos = other.get_pos()
self.k_cache[:, :, :other_pos, :, :] = other.k_cache[:, :, :other_pos, :, :]
self.v_cache[:, :, :other_pos, :, :] = other.v_cache[:, :, :other_pos, :, :]
```

This is the core trick. The cache layout is 5D:

```
(batch, n_layers, seq_len, n_kv_heads, head_dim)
   │       │         │
   │       │         └── sliced to :other_pos (only the filled prompt region)
   │       └── all layers copied in one assignment
   └── THE BROADCAST: other has batch=1, self has batch=N
```

PyTorch broadcasting rules kick in on dim 0: assigning a `(1, L, P, H, D)` tensor into a `(N, L, P, H, D)` slice **replicates the single prompt cache across all N batch rows** with no explicit loop or `repeat()`. One fused copy kernel, done.

Minimal repro of the mechanic:

```python
import torch
N, L, T, H, D = 4, 2, 8, 2, 3
src = torch.randn(1, L, 5, H, D)        # batch=1 prefill, 5 prompt tokens
dst = torch.zeros(N, L, T, H, D)        # batch=4 decode cache
dst[:, :, :5, :, :] = src               # broadcast over dim 0
assert (dst[0, :, :5] == dst[3, :, :5]).all()  # every row got the prompt KV
```

```python
self.cache_seqlens.fill_(other_pos)
```
`cache_seqlens` is a per-sequence length tensor of shape `(batch,)` — this is the FlashAttention `flash_attn_with_kvcache` convention. It tells the attention kernel where each sequence's valid KV ends, i.e., where the next decoded token's K/V should be written. Setting all N entries to `other_pos` means: every row's "write head" starts right after the prompt.

```python
if other.prev_embedding is not None:
    self.prev_embedding = other.prev_embedding.expand(self.batch_size, -1, -1).clone()
```
This carries over the **smear state** — nanochat mixes the previous token's embedding into the current token's representation (the "token smearing" trick inherited from the modded-nanogpt lineage), so decoding step `other_pos` needs the embedding of token `other_pos - 1`. Two details matter:

- `.expand(N, -1, -1)` creates a **zero-copy view** with stride 0 on the batch dim — all N rows alias the same memory.
- `.clone()` then **materializes** it into N independent rows. This is required: once the N samples diverge, each row's `prev_embedding` gets overwritten with its own token, and writing into a stride-0 expanded view would either error or silently corrupt all rows.

`expand().clone()` is the idiomatic "broadcast then own the memory" pattern — cheaper to reason about than `repeat()`, identical result here.

## Why two cache objects instead of one batch=N cache from the start?

You *could* prefill with the prompt repeated N times in a batch, but that wastes both compute (N identical forward passes worth of FLOPs in one batched call) and bandwidth. Prefill is compute-bound (big matmuls over the whole prompt); decode is memory-bandwidth-bound (one token at a time). Running prefill at batch=1 and forking the cache gives you the cheap version of each phase. The only cost is the one-time `O(N · L · P · H · D)` memory copy — pure bandwidth, no FLOPs, microseconds on GPU.

One thing to internalize: this works because the KV cache **is** the entire sequence state of a transformer decoder. Copy the cache + the smear embedding, and the N samples are bitwise-indistinguishable from having each processed the prompt themselves — they only diverge once sampling picks different tokens.

**References:**

- [nanochat repository (karpathy/nanochat)](https://github.com/karpathy/nanochat)
- [flash_attn_with_kvcache — FlashAttention interface](https://github.com/Dao-AILab/flash-attention/blob/main/flash_attn/flash_attn_interface.py)
