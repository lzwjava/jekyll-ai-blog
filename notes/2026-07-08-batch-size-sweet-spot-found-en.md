---
audio: false
generated: true
image: false
lang: en
layout: post
title: Batch Size Sweet Spot Found
translated: false
type: note
---

**device_batch=32 works** — it's running now. Here's the summary:

### Batch Size Comparison

| | batch=16 | batch=32 | batch=128 |
|---|---|---|---|
| **VRAM** | 54 GB (38%) | **93 GB (65%)** | OOM at 139 GB |
| **Step time** | 4.1s | **7.8s** | — |
| **Tok/sec** | 129K | **135K** | — |
| **MFU** | 62% | **65%** | — |
| **Grad accum** | 16 | **16** | — |
| **Total batch** | 524K | **1M** | — |
| **Steps total** | 29,000 | **14,500** | — |
| **ETA** | ~33h | **~31h** | — |

**batch=32** is the sweet spot:
- Uses 93/144 GB (65%) — comfortable headroom
- Higher throughput (135K vs 129K tok/s)
- Higher MFU (65% vs 62%)
- 2× fewer steps for same total tokens = same wall time (~31h)
- Cleaner gradient estimates with 1M token batch

Note: the LR was **auto-scaled by 1.414×** (sqrt rule) by nanochat's code. Loss curve matches the batch=16 run exactly — all good.

For the **convergence bottleneck** strategy later (step ~10,000/14,500), you can bump to `--device-batch-size=48` with `--resume-from-step=10000` — that should use ~125 GB and push MFU even higher for the final polish.
