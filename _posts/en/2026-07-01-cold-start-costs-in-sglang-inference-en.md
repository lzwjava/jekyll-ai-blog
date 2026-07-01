---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cold-Start Costs in SGLang Inference
translated: false
type: note
---

**Question:** What do "CUDA graph capture" and "KV cache allocation" mean as cold-start costs in SGLang, and why does TTFT drop from 8.5s to ~17ms after warmup?

**Answer:**

These are one-time initialization costs paid on the first request, not per-token costs. Let me break down each.

### CUDA Graph Capture

Normally, every CUDA kernel launch goes through the CPU: Python → PyTorch dispatcher → CUDA runtime → GPU. For a transformer decode step you launch *hundreds* of tiny kernels (attention, layernorm, GEMMs, RoPE, sampling). At small batch sizes, the GPU finishes each kernel faster than the CPU can queue the next one — you're **launch-bound**, not compute-bound. The GPU sits idle waiting for CPU dispatch overhead (~5–10µs per launch × hundreds of kernels).

A **CUDA graph** records the entire sequence of kernel launches once into a static graph, then replays it with a single `cudaGraphLaunch` call. No Python, no per-kernel dispatch.

```python
# Conceptually what capture does:
g = torch.cuda.CUDAGraph()
# warmup so cuBLAS picks algorithms, allocator settles
with torch.cuda.graph(g):
    static_out = model.decode_step(static_input)   # records all kernel launches

# later, every decode step is just:
g.replay()   # one launch, replays hundreds of kernels
```

The cost: SGLang captures graphs for **multiple batch sizes** (1, 2, 4, 8, … up to `--cuda-graph-max-bs`). Each capture runs the model, allocates static I/O buffers, and lets cuBLAS/cuDNN autotune. That's most of your 8.5s. It's startup work, not first-token work — once captured, decode steps replay the graph and the launch overhead vanishes (a big part of how you get to 17ms).

### KV Cache Allocation

SGLang preallocates the **entire KV cache pool** up front rather than `malloc`-ing per request. It computes how many tokens fit in remaining VRAM and reserves one giant contiguous block:

```
kv_bytes_per_token = 2 (K and V)
                   × num_layers
                   × num_kv_heads          # GQA → fewer than query heads
                   × head_dim
                   × dtype_size            # 2 bytes for fp16/bf16

total_tokens = floor(free_vram × mem_fraction / kv_bytes_per_token)
```

This block is partitioned into fixed-size **pages** (PagedAttention-style). The first allocation touches/reserves all of it — a one-time CUDA allocator cost. After that, serving a request just hands out page indices from the pool; no allocation in the hot path.

### Radix Tree (RadixAttention) — why warm TTFT is 17ms

This is SGLang's signature feature and the reason the *second* request is near-instant if it shares a prefix. SGLang stores cached KV blocks in a **radix tree keyed on token sequences**. A new request walks the tree; any matching prefix is reused instead of recomputed.

```
Request 1: "You are a helpful assistant. Translate: hello"
Request 2: "You are a helpful assistant. Translate: world"
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ shared prefix
```

For request 2, the system prompt's KV is already in the tree — prefill skips it entirely and only computes the new suffix tokens. TTFT collapses to the cost of a single short prefill + first decode step replayed via CUDA graph → ~17ms.

So the three costs map cleanly:

| Cost | When | Why it's gone after warmup |
| ------ | ------ | ---------------------------- |
| CUDA graph capture | First request | Graphs recorded once, replayed thereafter |
| KV cache allocation | First request | Pool preallocated once, pages reused |
| Prefix recompute | Per request | RadixAttention reuses shared-prefix KV |

The 8.5s → 17ms drop isn't the model getting "warmer" — it's that all the static infrastructure (graphs + cache pool) gets built on request one, and request two only pays for the genuinely new tokens.

**References:**

- [SGLang RadixAttention paper (Zheng et al., 2023)](https://arxiv.org/abs/2312.07104)
- [SGLang docs — hyperparameter tuning & CUDA graphs](https://docs.sglang.ai/backend/hyperparameter_tuning.html)
- [PyTorch CUDA Graphs](https://pytorch.org/blog/accelerating-pytorch-with-cuda-graphs/)
- [vLLM PagedAttention (same KV-paging idea)](https://arxiv.org/abs/2309.06180)
