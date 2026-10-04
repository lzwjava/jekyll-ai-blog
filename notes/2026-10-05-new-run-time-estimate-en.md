---
audio: false
generated: true
image: false
lang: en
layout: post
title: New Run Time Estimate
translated: false
type: note
---

Here's the math, based on the observed run data:

**Baseline (old run, `device-batch-size=2`)**
- dt per step: **58.1s** (1143 min ÷ step 1188 ✓, eta math checks out)
- 3,712 steps × 58.1s = **~60h** pure training
- Plus ~16 val-evals (every 250 steps, 41.9M tokens each ≈ 10-15 min), 2 CORE evals, ~5 min compile → **~65-67h total (≈2.8 days)**

**New run (`device-batch-size=1`)**

| Component | Estimate |
|---|---|
| Per-step time | 58.1s → **~65-67s** (same FLOPs, but 1024 micro-steps of half size — GEMMs slightly less efficient, per-step overhead doubled; ~12-15% slower) |
| Training, 3,712 steps | **~67-69h** |
| Val evals ×16 | ~2× longer each now (eval batch halves too) → **~6-9h** total |
| CORE eval ×2 (max-per-task=50) | fast now, **<30 min** combined |
| torch.compile warmup | **~5 min** |

**Total: ~75-80h ≈ 3.1-3.3 days** (vs ~2.8 days before — you pay ~10-15% for the VRAM headroom, mostly in slower steps and evals)

**Milestones:**
- Step 250 (first checkpoint lands): **~4.5-5h** from launch
- Step 2000 (the spot that killed the old run): **~1.9 days** in — this is the moment of truth for the OOM fix
- Finish: **~3.2 days**

One way to claw back time later: `--eval-tokens=2097156` would cut those 16 val-evals from ~6-9h down to ~1h total (bpb curve just gets a bit noisier). Not needed to start, though.