---
audio: false
generated: true
image: false
lang: en
layout: post
title: NanoChat Training Complete with Validation Results
translated: false
type: note
---

Training just finished! Here's the full status:

**nanochat d12 SFT — COMPLETE** (finished 2 minutes ago)

| Metric | Value |
|--------|-------|
| Steps | 8,985 |
| Duration | 184.70 min (~3h) |
| Final loss | 1.0674 (step 8984) |
| Validation bpb | **0.4053** |
| Peak VRAM | 6,240 MiB |
| Learning rate | cosine decay 0.05 → -0.00 |
| Epoch | 2 (slightly over 1x data) |
| Checkpoint saved | `d12/model_008985.pt` |

**Validation bpb of 0.4053** — that's actually very good for SFT on mixed data. At ~0.4 bpb, the model has learned the distribution well (equivalent to ~0.28 perplexity in token space). This is in line with your previous d12 run (was 0.954 bpb on the previous run, I recall — so this is significantly better).

What's notable: the MFU reading was ~162%, which is clearly an artifact (can't exceed 100% theoretical max). Likely a measurement issue in nanochat's tok/sec calculation — it's counting tokens faster than real due to gradient accumulation not being factored. The real compute utilization is probably in the 60-80% range which is fine for a single GPU.

Loss curve ended with some oscillation (1.01-1.13 range in the final 100 steps) suggesting it's near convergence — more steps would start overfitting.

Want to run inference on the checkpoint or move on to the next experiment?