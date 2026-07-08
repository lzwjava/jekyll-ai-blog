---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 批次48：保留还是回退？
translated: true
type: note
---

## batch=48 正在运行！🎉

**Current state at step 15/9280:**

| Metric | batch=32 | batch=48 | Δ |
| -------- | ---------- | ---------- | --- |
| **VRAM** | 93 GB (65%) | **135 GB (93.5%)** | +42 GB |
| **Headroom** | 47 GB | **9.4 GB** (tight) | ↓ |
| **Tok/sec** | 135K | **137K** | +1.5% |
| **MFU** | 65% | **66.3%** | +1.3% |
| **Step time** | 7.8s | **11.5s** | +47% |
| **Total steps** | 14,500 | **9,280** | -36% |
| **ETA** | ~31h | **~29.5h** | -1.5h |
| **LR scale** | ×1.414 | **×1.732** | ↑ |

It fits but **barely** — only 9.4 GB free. A single CUDA graph recompile could push it over the edge. The gain is marginal: ~1.5h saved (~5%) for running at 93% memory pressure.

Want to keep it at 48 (risking OOM on any recompile) or fall back to 32 (safe, 47 GB headroom, only 1.5h slower)?
