---
audio: false
generated: true
image: false
lang: en
layout: post
title: Batch Size Scaling Analysis
translated: false
type: note
---

Let me compare the three runs side by side. Here's what happened when we increased batch size:

| | batch=16 | batch=32 | batch=64 | batch=128 |
|---|---|---|---|---|
| **VRAM** | 54 GB (38%) | **93 GB (65%)** | OOM (133 GB) | OOM (139 GB) |
| **Tok/sec** | 129K | **135K** | — | — |
| **MFU** | 62% | **65%** | — | — |
| **Step time** | 4.1s | 7.8s | — | — |
| **Grad accum** | 16 | 16 | — | — |
| **Batch/step** | 524K | **1M** | — | — |
| **Total steps** | 29,000 | 14,500 | — | — |
| **ETA** | ~33h | **~31h** | — | — |
| **LR** | 1.0 | **×1.414** (auto-scaled) | — | — |

**What happened with the increase to batch=32:**

1. **Throughput stayed the same** — 135K vs 129K tok/s. The GPU is compute-bound, not memory-bound, so doubling batch doesn't halve time. Step time doubled (4.1→7.8s) because each step processes 2× tokens.

2. **MFU improved slightly** — 65% vs 62%. Bigger matmuls are slightly more efficient on H200 tensor cores.

3. **Total steps halved** — 14,500 vs 29,000. Same total tokens in fewer steps. Wall time is roughly the same (~31h vs ~33h).

4. **Gradients are cleaner** — 1M tokens per step instead of 524K. Half the gradient variance (Var ∝ 1/B). The auto-scaled LR (×1.414) accounts for this — you can take bigger steps when the gradient direction is more certain.

5. **LR was auto-scaled** — nanochat's scaling law code detected the 2× batch and multiplied LR by √2. This is the correct theoretical adjustment (linear scaling rule: LR ∝ batch size).

**Why 64 and 128 OOM'd:**

The culprit is the **lm_head** — a `(32768 vocab × 1536 dim)` linear layer. During forward pass, the output logits are `(batch×seq, vocab)`:
- batch=32: (65536, 32768) in fp32 = **8 GB** → total 93 GB ✅
- batch=64: (131072, 32768) in fp32 = **16 GB** → total 133 GB OOM ❌
- batch=128: (262144, 32768) in fp32 = **32 GB** → total 139 GB OOM ❌

The lm_head itself + its fp32 optimizer copy also consume ~400 MB × 2 = 800 MB, but the logit tensor is the killer.

**Bottom line:** Increasing batch from 16→32 gave us cleaner gradients and slightly higher MFU, but we hit the VRAM wall at 64. The H200 can't go higher with a 32K vocab and this model width. For the convergence bottleneck stage later (step ~10,000), we'll keep batch=32 — there's no room to scale up further on a single H200.
