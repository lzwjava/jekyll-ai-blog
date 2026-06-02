---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 Training Progress Report
translated: false
type: note
---

Here's the full picture:

**When trained:**
- Started: **2025-11-16**
- Checkpoint saved: **2025-11-21 21:51** (took ~5 days)

**Training progress:**
- Iteration: **11,500 / 12,000** (96% complete)
- Best val loss: **3.3174**

**Model — GPT-2 (124M):**

| Param           | Value                                 |
| --------------- | ------------------------------------- |
| Architecture    | Transformer (GPT-2)                   |
| Layers          | 12                                    |
| Heads           | 12                                    |
| Embedding dim   | 768                                   |
| Context length  | 1024 tokens                           |
| Vocab size      | 50,304 (BPE)                          |
| **Parameters**  | **~124M**                             |
| Checkpoint size | **1.4 GB** (includes optimizer state) |

**Training config:**
- Dataset: FineWeb
- Batch size: 8 × grad_accum 64 = effective batch **512**
- dtype: bfloat16
- Multi-GPU: nccl backend
- LR: 3e-4 → 3e-5 (cosine decay over 12k iters)
