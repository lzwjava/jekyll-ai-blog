---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang Global KV Cache Reuse Explained
translated: false
type: note
---

**Question:** What does this SGLang technical description mean? Explain the Global KV Cache Reuse, memory allocator adjustments, and performance results described above.

**Answer:**

This is describing SGLang's **Context Parallelism (CP) + Global KV Cache Resharding** feature — a way to share KV cache across multiple GPU ranks instead of each rank maintaining its own isolated cache. Let me break it down layer by layer.

---

## Background: What Problem Is Being Solved?

In standard LLM serving, KV cache (the materialized K and V tensors from attention) is stored **locally per GPU rank**. With tensor parallelism (TP=8), each rank holds a shard of the KV cache for its own sequence chunk. This means:

- **Cache hit on rank 0** ≠ usable by rank 1
- Prefix reuse is local — cross-request sharing is rank-local only
- Long sequences require large per-rank KV cache budgets

The goal here is to make KV cache **globally reusable** across CP ranks.

---

## Part 1: Radix Cache → Global Cache Tree

SGLang's existing prefix cache uses a **Radix Tree** (trie over token sequences):

```
Root
├── [sys_prompt_tokens] → Node A (rc=2, last_access=T1)
│   ├── [user_tokens_1] → Node B
│   └── [user_tokens_2] → Node C
```

Each node stores:

- Token IDs for this prefix segment
- Pointer to KV pages
- Reference count (prevent eviction while in use)
- Last access time (LRU eviction)

**The CP extension adds one field per page: `CP Owner` (which rank holds this KV page).**

```python
@dataclass
class KVPage:
    token_ids: List[int]
    kv_data: Tensor        # actual K,V values
    cp_owner: int          # NEW: which CP rank owns this page
    ref_count: int
    last_access: float
```

Now the Radix Tree becomes a **global index** — every rank can see the full tree and knows:

- Which pages are local (cp_owner == self.rank)
- Which pages are remote (cp_owner != self.rank, but fetchable via NVLink/RDMA)

This preserves **SPMD** (Single Program Multiple Data) design: every rank runs identical tree insert/lookup code. The `CP Owner Manager` determines placement policy (replicate redundant pages, shard unique ones).

---

## Part 2: Eviction — Leader Rank Pattern

Eviction is the one place SPMD breaks down, because different ranks have different memory pressure. The solution:

```
R0 (Leader) traverses global tree
    → selects pages to evict (LRU policy)
    → broadcasts decision via AllReduce/Broadcast over CP group
All ranks execute identical eviction
    → tree stays consistent across all ranks
```

This is a classic **distributed consensus via single leader** pattern — simple, correct, and avoids split-brain. The downside is R0 is slightly more loaded, but eviction is infrequent so it's fine.

---

## Part 3: Memory Allocator — Collective Alloc

When CP splits sequences along the sequence dimension, token counts per rank are **uneven** (padding or ragged batches). So:

```
Rank 0: 1024 tokens → needs N pages
Rank 1: 987 tokens  → needs M pages
```

Before allocating, they do a **collective communication** (`all_reduce` of free page counts):

```python
local_free = allocator.free_pages()
global_min_free = dist.all_reduce(local_free, op=MIN)
if global_min_free < required:
    trigger_eviction()
    # repeat until all ranks have enough
```

Then allocation logic has 3 cases:

```
1. Local cache hit    → no-op, reuse directly
2. Remote cache hit   → allocate local pages, pull KV from remote rank
3. Cache miss         → allocate + compute from scratch
```

The key insight: **this operates at Page abstraction level**, so it's agnostic to:

- Model architecture (MLA, GQA, MHA all just produce KV pages)
- Data types (BF16, FP8, FP4 — just affects page size)
- Attention variants (DeepSeek MLA's compressed KV still pages the same way)

---

## Part 4: Performance Numbers (DeepSeek 235B on H100)

| Config | TTFT (p50) | Notes |
|--------|-----------|-------|
| TP=8, EP=8 (baseline) | 631ms | Standard config |
| Attn CP=2, MoE DP=2, EP=4 | 452ms | **-28%** |
| Attn CP=2, EP=8 | ~630ms | No improvement yet |
| 2-node, 16xH100, 32K seq | 764ms | Weak scaling, not ideal |

Why CP=2 + EP=4 wins:

1. **CP reduces attention communication** — each rank handles half the sequence, so attention all-to-all is smaller
2. **EP=4 (smaller expert parallelism)** — MoE load imbalance gets worse with more EP ranks; EP=4 distributes experts with less skew

Why CP=2 + EP=8 doesn't help yet: the communication reduction code path isn't merged — CP overhead cancels the benefit.

Why 2-node 32K is 764ms (not ~631ms): KV cache all-gather is still on the **critical path** — the communication isn't overlapped with compute yet.

---

## Part 5: KV Cache Resharding — The Core Win

**Resharding** = when a request hits a cached KV page owned by a different CP rank, instead of recomputing, you **pull and redistribute** that page.

Results (TP=4, varying CP):

| Metric | Effect |
|--------|--------|
| Precision | No change (exact same values) |
| KV Cache memory usage | **-50%** (deduplication across ranks) |
| Cache hit rate | **+50%** more hits possible |
| Throughput at 8K | -7% (all-gather overhead) |
| Throughput at 16K | -21% (80% from KV all-gather, 20% scheduler) |

The 16K breakdown is important:

- **80% of the 21% loss** = KV all-gather latency → **fully eliminatable via compute-communication overlap**
- **20% of the 21% loss** = scheduler CPU overhead → fixable via CPU optimization + async scheduler

So the theoretical steady-state overhead after overlapping is just ~4% — that's the scheduler cost.

---

## Summary Mental Model

```
Before CP:
  Rank 0: [KV_A, KV_B, ...]   ← isolated
  Rank 1: [KV_C, KV_D, ...]   ← isolated

After Global KV Resharding:
  Global Radix Tree (visible to all ranks):
    prefix_1 → page_id=42, cp_owner=0
    prefix_2 → page_id=43, cp_owner=1

  Any rank can serve any prefix by fetching from owner rank
  → 50% memory reduction (no redundant replication)
  → Global cache hit rate improves dramatically for long-context serving
```

This is essentially building a **distributed KV store** (like Redis Cluster, but for attention KV tensors, with LRU eviction and prefix-aware routing) on top of GPU HBM, integrated directly into SGLang's scheduler.
