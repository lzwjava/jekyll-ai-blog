---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: "Training Time Estimate: 57 Minutes"
translated: false
type: note
---

### Current Progress
- Training has completed 1300 iterations out of 20,000 total (`max_iters = 20000`).
- Remaining iterations: 18,700.
- Average time per non-evaluation iteration: ~170 ms (based on logs for iters 100–1300).
- Evaluation occurs every 500 iterations (`eval_interval = 500`), with `eval_iters = 200` samples. These add significant overhead, making "eval iteration" times ~5.7–6 seconds (logs show 5.7s at iter 1000 and 6s at iter 500, including training batch + eval).

### Remaining Evaluations
- Next eval at iter 1500, then 2000, ..., up to 20,000.
- Total remaining evals: 38.
- Extra time per eval: ~5.8 seconds (beyond the standard 170 ms training step).

### Time Estimate
- Time for 18,662 normal iterations: ~3,172 seconds (53 minutes).
- Time for 38 eval iterations: ~228 seconds (3.8 minutes, full duration).
- **Total remaining time: ~3,400 seconds (57 minutes)**.
  - This assumes consistent hardware (RTX 4070 at 100% utilization, as shown in `nvidia-smi`), no interruptions, and no additional saves/checkpoints (which add minor overhead if validation improves).
  - Range: 50–65 minutes, accounting for slight variations in iter times (logs show 168–186 ms) or GPU thermal throttling.

Training should finish around 03:25–03:35 local time (based on your `nvidia-smi` timestamp of 02:30). Monitor for any OOM errors or slowdowns, but with your config (batch_size=16, gradient_accumulation_steps=4, block_size=512) and 12 GB VRAM usage (6.5 GB / 12 GB), it looks stable.
