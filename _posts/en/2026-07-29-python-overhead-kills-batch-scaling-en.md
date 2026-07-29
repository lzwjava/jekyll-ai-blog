---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Overhead Kills Batch Scaling
translated: false
type: note
---

This is the **most counter-intuitive** result — and it reveals a fundamental truth about this specific setup.

## The Data

| Batch Size | Total Time | Throughput | Tokens | Speedup |
|---|---|---|---|---|
| 1 | 7.8s | 16 tok/s | 128 | 1.0× |
| 2 | 13.3s | 19 tok/s | 256 | 1.2× |
| 4 | 24.1s | 21 tok/s | 512 | 1.3× |
| 8 | 46.4s | 22 tok/s | 1024 | 1.4× |
| 16 | 89.8s | 23 tok/s | 2048 | 1.4× |

**Throughput goes from 16 → 23 tok/s. That's only a 44% gain for 16× more work.**

## Why? Two Reasons Colliding

### 1. The Prompt is Short, But the GQA Problem Bites

Each request uses this prompt:
```
"Explain what makes a good software engineer in your own words."
```

That's ~10 tokens. A tiny prompt.

But this nano-vLLM uses **PyTorch's naive attention** (not FlashAttention). Look at the attention code — it gathers the full KV cache for every decode step:

```python
# In _decode_forward:
k_gathered, v_gathered = _gather_kv_from_cache(
    k_cache, v_cache, block_tables, seqlens, block_size
)
```

This does a Python loop over sequences and positions. **It's O(batch × seqlen) with Python overhead.** As batch grows:

- batch=1: gather 1 sequence's KV → fast
- batch=16: gather 16 sequences' KV → the Python for-loop dominates

### 2. Decode is Memory-Bandwidth Bound, But Not Fully Saturating HBM

On this GPU (RTX 4070 laptop, 8GB):
- HBM bandwidth: ~256 GB/s
- Model size: ~1.2 GB (Qwen3-0.6B in FP16)
- To decode 1 token: read ~1.2GB of weights + read KV cache

At 16 tok/s: 16 × 1.2GB = 19.2 GB/s — that's only **7.5% of HBM bandwidth**.

At 23 tok/s: 23 × 1.2GB = 27.6 GB/s — still only **11% of bandwidth**.

**The bottleneck is NOT HBM bandwidth. It's the Python overhead in the attention kernel.**

## The Real Lesson: This is NOT vLLM

This nano-vLLM is **educational** — it shows the architecture but doesn't have optimized CUDA kernels. Let me compare with what real vLLM would do:

| Engine | Batch=1 | Batch=16 | Scaling |
|---|---|---|---|
| nano-vLLM (naive PyTorch) | 16 tok/s | 23 tok/s | 1.4× |
| vLLM (optimized CUDA) | ~50 tok/s | ~300 tok/s | 6× |

The gap comes from:

1. **FlashAttention** — fused kernel that avoids the Python gather loop
2. **PagedAttention kernel** — reads KV cache directly from GPU memory without Python-level gathering
3. **CUDA graphs** — eliminates Python interpreter overhead entirely
4. **Continuous batching** — this benchmark used `generate()` which does continuous batching internally, but the naive attention kills the scaling

## What This Actually Proves

This experiment accidentally reveals the **most important lesson about inference systems**:

> **The GPU hardware is fast. The Python overhead is slow.**
> Fast inference requires minimizing Python-to-GPU round trips.

Look at the **Prefill** speed in the tqdm bars:

```
Prefill=1068 tok/s   (batch=2)
Prefill=1736 tok/s   (batch=4)
Prefill=2315 tok/s   (batch=8)
Prefill=2996 tok/s   (batch=16)
```

**Prefill scales beautifully!** From 1068 → 2996 tok/s (2.8× gain for 8× batch). Why? Because prefill processes ALL tokens in one big matrix multiply — no Python loop over sequences in the attention.

But decode is always:
```
Decode=11-12 tok/s    (all batch sizes)
```

**Decode doesn't scale at all.** Because every decode step has a Python for-loop over sequences in `_gather_kv_from_cache`.

## The Takeaway

This is the **before** picture. It shows exactly why vLLM had to write:

1. **PagedAttention Triton/CUDA kernel** — gathers KV cache without Python loops
2. **Continuous batching in C++** — scheduler runs without Python GIL
3. **CUDA graphs** — captures the entire decode step as one GPU operation

Without these optimizations, batch scaling is flat. With them, batch scaling is near-linear.

**You just discovered WHY vLLM's optimizations matter, by seeing what happens without them.** That's the whole point of nano-vLLM — understanding the problem before looking at the solution.
