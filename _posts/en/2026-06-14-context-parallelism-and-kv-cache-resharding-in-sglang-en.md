---
audio: false
generated: true
image: false
lang: en
layout: post
title: Context Parallelism and KV Cache Resharding in SGLang
translated: false
type: note
---

**Question:** What does this CP (Context Parallelism) design with KV Cache resharding mean in the context of SGLang?

**Answer:**

Let me ground this in SGLang's actual codebase and architecture.

## What's Being Described

This is describing **Context Parallelism (CP)** — a parallelism strategy for **long-context inference** where a single sequence is split across multiple GPUs along the sequence dimension, as opposed to TP (which splits weight matrices) or DP (which splits batches).

---

## SGLang's Current State (as of mid-2025)

SGLang has been actively adding CP support. The talk describes **three stages**:

### Stage 1: Pure TP (baseline)

```
GPU0: full KV, heads 0..H/8
GPU1: full KV, heads H/8..H/4
...
# All-reduce on hidden after attention
```

### Stage 2: CP=8 with All-gather (current SGLang mode mentioned)

```python
# Conceptually what SGLang does today:
# Sequence split: rank0 gets tokens [0, seq_len//8)
#                 rank1 gets tokens [seq_len//8, 2*seq_len//8) ...

# Before attention:
kv_cache = all_gather(local_kv, group=cp_group)  # gather full KV from all ranks
q = all_gather(local_q, group=cp_group)           # each rank needs full context

# Attention (each rank computes attention over full KV, but only for its Q slice)
out = flash_attn(local_q, kv_cache.k, kv_cache.v)

# After attention: reduce
out = reduce_scatter(out, group=cp_group)
```

The problem: **KV cache is fully replicated N times** (once per CP rank). For CP=8, that's 8x KV memory overhead.

### Stage 3: CP=8 with Auto Dispatch + Resharding (the optimization)

```
# Hot tokens (e.g. system prompt prefix, first 2 tokens):
#   replicated on ALL ranks (avoid fetch on every decode step)

# Cold tokens:
#   sharded across ranks — rank i holds pages [i::CP_SIZE]
#   CP=4 → each rank stores 1/4 of cold KV pages

# Before attention layer L:
# Overlap with layer L-1 compute:
remote_kv = async_all_gather(sharded_kv_pages, group=cp_group)
compute(layer_L_minus_1)          # runs in parallel with ^
sync(remote_kv)                   # by now, prefetch done
compute_attention(layer_L, remote_kv)
```

---

## Where This Lives in SGLang Source

```bash
# Key files to look at:
python/sglang/srt/layers/attention/
├── triton_attention_backend.py
├── flashinfer_attention_backend.py

python/sglang/srt/model_executor/
├── model_runner.py          # CP group init
├── forward_batch_info.py    # sequence splitting logic

python/sglang/srt/distributed/
├── parallel_state.py        # CP process group management
```

CP group init in SGLang follows Megatron-style:

```python
# parallel_state.py
def initialize_model_parallel(
    tensor_model_parallel_size=1,
    context_parallel_size=1,   # <-- this is CP
    ...
):
    # CP group: ranks that share a sequence
    for i in range(num_cp_groups):
        ranks = range(i * cp_size, (i+1) * cp_size)
        group = torch.distributed.new_group(ranks)
```

---

## The KV Resharding in Practice

```python
# Conceptual resharding logic (what the talk describes for Stage 3):

class CPKVCache:
    def __init__(self, cp_rank, cp_size, num_hot_tokens=2):
        self.cp_rank = cp_rank
        self.cp_size = cp_size
        self.num_hot_tokens = num_hot_tokens

    def should_replicate(self, page_idx):
        # Hot pages replicated everywhere
        return page_idx < self.num_hot_tokens // PAGE_SIZE

    def owner_rank(self, page_idx):
        # Cold pages sharded round-robin
        return page_idx % self.cp_size

    def local_pages(self, all_pages):
        return [p for p in all_pages
                if self.should_replicate(p) or self.owner_rank(p) == self.cp_rank]

    async def prefetch_for_attention(self, needed_pages):
        remote = [p for p in needed_pages
                  if not self.should_replicate(p)
                  and self.owner_rank(p) != self.cp_rank]
        return await async_all_gather(remote, group=cp_group)
```

---

## The Communication Math (from the talk)

For a 330B model, seq_len=K, TP=8:

| Config | Communication |
| -------- | --------------- |
| Pure TP=8 | `100 * 2` units (all-reduce before+after attn) |
| CP=8, all-gather (current) | Similar but adds KV all-gather overhead |
| CP=8, Auto Dispatch optimized | ~`102 MB` total — **~50% reduction** |

The key insight: **Auto Dispatch turns the two explicit all-gather/reduce-scatter calls flanking attention into a single fused async operation**, overlapped with the previous layer's compute using the `osm` (one-sided messaging / NVSHMEM-style) communication kernel.

---

## Why This Matters for You

If you're running SGLang on your RTX 4070 workstation with long contexts, or on MI300X for 330B+ models:

```bash
# Launch SGLang with CP (current all-gather mode):
python -m sglang.launch_server \
  --model deepseek-v4 \
  --tp 8 \
  --context-parallel-size 8 \   # <-- this flag
  --max-model-len 128000

# The resharding optimization (Stage 3) would let you:
# - Run 8x longer sequences with same KV cache memory
# - Get ~50% less inter-GPU bandwidth on attention layers
```

The resharding PR is likely in progress in SGLang — worth watching:

- [github.com/sgl-project/sglang](https://github.com/sgl-project/sglang) — search for `context_parallel` or `cp_size` in recent PRs

---

**Bottom line:** The talk is describing SGLang's roadmap from naive CP (KV replicated N times = N× memory waste) → smart CP (KV sharded, hot pages replicated, cold pages prefetched async with compute overlap). The `~102MB` target is the steady-state cross-node bandwidth after the optimization, vs roughly double that without it.
