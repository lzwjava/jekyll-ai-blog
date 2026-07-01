---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Run Progress Assessment
translated: false
type: note
---

**Question:** Is the training run going well, and what can we infer from the current loss trajectory?

**Answer:**

Yes, this looks healthy. Here's a quick read on where you are:

**Progress sanity check**

- 70,700 / 427,000 steps = **16.6% done**
- Val loss dropped from 5.87 → 2.08 in that window — that's a clean 3.79 nats of descent, most of it happening in the early chaotic phase
- Still decreasing, no divergence, no plateau — you're in the "grinding down" phase now

**Where it'll likely bottom out**

Your prediction of ~1.8–1.9 is reasonable. For reference, code-trained models at this scale tend to converge around:

| Model | Data | Final val loss |
| --- | --- | --- |
| GPT-2 124M | WebText | ~2.85 |
| GPT-2 124M | FineWeb-Edu | ~3.0–3.2 |
| CodeParrot 110M | GitHub code | ~1.7–1.9 |
| Your run (760M) | GitHub code | **~1.6–1.8 est.** |

You're bigger (760M vs 110M), so you should beat CodeParrot's loss on the same data — expect the floor around **1.6–1.75** if training goes full distance.

**MFU at 14.4% — that's the thing to watch**

On MI300X with 192GB HBM3, 14.4% MFU is on the low side. Theoretical peak for MI300X is ~383 TFLOPS (bf16). At 14.4%, you're getting ~55 TFLOPS effective. For a 760M model:

- Are you using `torch.compile`?
- Flash attention enabled?
- Batch size large enough to saturate HBM bandwidth?

If not, you could potentially get MFU up to 35–45% with tuning, which would cut your ETA roughly in half. Worth profiling with `rocprof` or checking `roc-smi` utilization during a step.

**62 hours / 2.5 days remaining** — let it cook. The loss curve at 16% in still has meaningful room to drop. The real signal will be around 50% where you'll see if the curve is flattening prematurely or still descending cleanly.
