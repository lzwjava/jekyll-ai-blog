---
audio: false
generated: true
image: false
lang: en
layout: post
title: vLLM Continuous Batching Explained
translated: false
type: note
---

Looking at this trace — this is the **heart of vLLM**. Let me decode what you're seeing step by step.

## What This Trace Shows

You sent **10 requests simultaneously** with very different profiles:

| seq | Type | Prompt | Generation | Total |
|-----|------|--------|------------|-------|
| 6 | Short answer ("42") | 2 tok | 4 tok | **6 total** |
| 4 | Long context (fox dog ×50) | 507 tok | 8 tok | **515 total** |
| 2 | Short Q&A | 7 tok | 16 tok | **23 total** |
| 9 | Translation | 10 tok | 16 tok | **26 total** |
| 8 | Math problem | 14 tok | 24 tok | **38 total** |
| 3 | Medium Q&A | 9 tok | 32 tok | **41 total** |
| 11 | Multi-turn | 187 tok | 32 tok | **219 total** |
| 5 | Code generation | 10 tok | 48 tok | **58 total** |
| 10 | Long generation | 8 tok | 48 tok | **56 total** |
| 7 | Essay | 6 tok | 64 tok | **70 total** |

## The Critical Observation

**They all finish at DIFFERENT times:**

```
seq[6]  (4 tok gen)   → finishes at step 4   ← SHORTEST
seq[4]  (8 tok gen)   → finishes at step 7
seq[2]  (16 tok gen)  → finishes at step 17
seq[9]  (16 tok gen)  → finishes at step 17
seq[8]  (24 tok gen)  → finishes at step 23
seq[3]  (32 tok gen)  → finishes at step 33
seq[11] (32 tok gen)  → finishes at step 33
seq[5]  (48 tok gen)  → finishes at step 49
seq[10] (48 tok gen)  → finishes at step 49
seq[7]  (64 tok gen)  → finishes at step 64  ← LONGEST
```

## What This Means Visually

```
Time →  1   2   3   4   5   6   7  ...  17  ...  33  ...  49  ...  64
         │   │   │   │   │   │   │        │        │        │        │
seq[6]   ████▓─────────────────────────→  done
seq[4]   ██████████▓───────────────────→  done
seq[2]   ████████████████████▓─────────→  done
seq[9]   ████████████████████▓─────────→  done
seq[8]   ████████████████████████████▓─→  done
seq[3]   ████████████████████████████████████████▓──→  done
seq[11]  ████████████████████████████████████████▓──→  done
seq[5]   ██████████████████████████████████████████████████████▓──→  done
seq[10]  ██████████████████████████████████████████████████████▓──→  done
seq[7]   ████████████████████████████████████████████████████████████████████▓

         ├─prefill─┤  ↑                    ↑                    ↑
                      seq[6] leaves      seq[2] leaves        seq[5] leaves
                      batch: 10→9        batch: 9→8           batch: 3→1
```

## The Three Big Insights

### 1. Continuous Batching ≠ Static Batching

**Static batching** (the naive approach):
- Wait until you have N requests
- Pad all prompts to the same length
- Run ALL sequences for ALL max_tokens steps
- A short Q&A waits 64 steps while the essay finishes

**Continuous batching** (what vLLM does):
- Each sequence progresses independently
- Short ones finish and **leave immediately**
- New ones can **join mid-stream**
- The batch size changes every step

### 2. The "free_blocks" Tells the Memory Story

```
free_blocks:  6 → 1 → 7 → 11 → 14 → 16 → 23
```
- Starts at 6 (some blocks used by model weights)
- Drops to 1 during peak pressure (all 10 sequences active)
- **Climbs to 23** as sequences finish and free their KV cache blocks
- This is PagedAttention's block-level memory management in action

### 3. prompt_len vs total_len

Look at seq[11]:
```
prompt_len=187  total_len=219  blocks=1
```

It has **187 prompt tokens + 32 generated = 219 total** but only **1 block**. Why? Because the block size is 256 tokens. A single 256-token block holds all its KV cache. This is the **page** in PagedAttention.

## What Would Happen Without vLLM?

Without continuous batching + PagedAttention:

1. **Memory waste:** You'd allocate KV cache for ALL 10 sequences for `max(64, 48, 32, ...)` = 64 steps. Short sequences waste 60 steps worth of cache.
2. **No preemption:** If memory runs out, the system crashes.
3. **Fragmentation:** Sequential allocation creates gaps when sequences finish at different times.

With PagedAttention:
- Blocks are allocated on demand
- When seq[6] finishes, its block goes back to the free pool
- seq[7] (the essay) can use that block for its next token
- **Zero fragmentation, zero waste**

## The Sentence That Sums It Up

You're watching **virtual memory for transformers** — PagedAttention is to GPU memory what virtual memory paging is to CPU memory. Each sequence has a logical "page table" (block_table) mapping its tokens to physical GPU memory blocks. The scheduler is the operating system, allocating and freeing pages as sequences come and go.

This is why vLLM can serve 10x more concurrent users than naive implementations.
