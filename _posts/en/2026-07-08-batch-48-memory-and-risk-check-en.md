---
audio: false
generated: true
image: false
lang: en
layout: post
title: Batch 48 Memory and Risk Check
translated: false
type: note
---

Good thought. Let me analyze without killing the current run.

**batch=48 estimate:**

| Component | batch=32 (current) | batch=48 (estimate) |
| --- | --- | --- |
| **Microbatch tokens** | 32×2048 = 65,536 | 48×2048 = **98,304** |
| **Logit tensor** `(batch×seq, vocab)` | (65536, 32768) = **8 GB** | (98304, 32768) = **12 GB** |
| **Activations (embed + attn + MLP)** | ~30 GB | ~**45 GB** |
| **Model weights (fp8)** | ~1.4 GB | ~1.4 GB (same) |
| **Optimizer states (fp32)** | ~**16.5 GB** (1.38B × 12 bytes for Muon+AdamW) | ~16.5 GB (same) |
| **Gradients (fp8)** | ~1.4 GB | ~1.4 GB (same) |
| **Compiled graph memory** | ~**35 GB** (torch.compile caches) | ~35 GB (similar) |
| **Total estimate** | **~93 GB** | **~112 GB** |
| **H200 capacity** | 140 GB | 140 GB |
| **Headroom** | **47 GB free** | **~28 GB free** (probably fine) |

**Key question**: Does torch.compile recompile the graph for the new shape, using more memory temporarily? Yes — it allocates extra buffers during compilation that get freed after. During the first step (compilation), peak memory can spike 10-15 GB above steady state.

So real risk profile:

- **Steady state**: ~112 GB → 28 GB free → **likely safe** ✅
- **Compilation spike**: ~112 GB + ~15 GB = 127 GB → 13 GB free → **should still fit** ✅
- **Grad accum**: batch=48 with total-batch=1M means **grad_accum = 10-11**, which is fine

**Where it could fail**: if the compiled kernel for the attention forward pass allocates extra scratch space for FA3 with the `(48, 2048, 12, 128)` shape. That's a hot path allocation that isn't cached.

**My call**: 48 would **probably work**, but tight. The real question is whether it's worth the risk — you gain only ~$15\%$ throughput (bigger matmuls) but lose the current 22 minutes of training progress. The MFU gain from 32→48 would be marginal (maybe 65% → 66-67%).

Want me to try 48 after this run finishes (since we can't save checkpoints mid-run)? Or stay at 32 which is already running fine with 47 GB headroom?
