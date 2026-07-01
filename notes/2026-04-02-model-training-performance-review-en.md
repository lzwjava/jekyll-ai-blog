---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Training Performance and Issue Review
translated: false
type: note
---

Here's the training review:

## 📊 Training Trajectory (950 iters / 10K target)

| Iter | Train Loss | Val Loss |
| ------ | ----------- | ---------- |
| 0 | 11.05 | 11.06 |
| 250 | 5.93 | 5.93 |
| 500 | 5.07 | 5.06 |
| 750 | 4.26 | 4.22 |
| 950 | 4.00 | — |

**~640M tokens seen** (950 × 1M × gradient_accumulation effect). 10B target is 10× more.

## ⚠️ Issues

1. **Step time stuck at 21s even after compile** — should be 1-3s. Something's wrong. Either:
   - Data loading bottleneck (disk I/O)
   - Inductor workers still running
   - CPU preprocessing on critical path

2. **MFU 150%+** — impossible on single H200. This is a torch.compile measurement artifact, not real utilization.

3. **Loss spike at iter 600** (4.91 vs 4.85 before and 4.43 after) — could be a bad batch or LR scheduling hiccup. Not concerning if it recovers.

4. **ckpt iter = 0** — checkpoint saves model weights but `iter` counter isn't being stored properly in this checkpoint. That's a nanoGPT bug/feature.

## ✅ Good

- Loss dropping consistently (11 → 4 in 950 steps)
- Val loss tracks train loss closely — no overfitting yet
- Model at 4.0 loss is already usable for basic generation
- Checkpoint at 18GB saved correctly

## Verdict

At 21s/step × 9050 remaining iters = **~53 hours** left. That's too slow. The data pipeline is likely the bottleneck. But the model itself is learning fine. If you can fix the speed (maybe use `block_size=512`), you'd finish in hours not days. 🦞
