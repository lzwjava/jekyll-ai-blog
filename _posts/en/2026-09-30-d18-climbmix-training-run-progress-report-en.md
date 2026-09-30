---
audio: false
generated: true
image: false
lang: en
layout: post
title: d18-climbmix Training Run Progress Report
translated: false
type: note
---

## Progress report

**No tmux session named `a` exists.** The live sessions are `0` and `1`, and both are attached to the same training terminal (`pts/10`), so they show identical output. The active run is:

### 🏃 Training run: `d18-climbmix` (nanochat)

- **Command:** `./.venv/bin/python -m scripts.base_train --depth=18 --max-seq-len=1024 --device-batch-size=2 --tracker=none --run=d18-climbmix`
- **Status:** Running (PID 1682358, started Sep 29, ~1632 min CPU time)

| Metric | Value |
| --- | --- |
| Progress | **step 1585 / 3712 (42.70%)**, epoch 1 |
| Loss | ~2.86 (declining steadily) |
| LR multiplier | 0.89 |
| Step time | ~58.2 s/step |
| Throughput | ~18,028 tok/sec |
| BF16 MFU | 127.6% |
| Total elapsed | ~1,528 min (~25.5 h) |
| **ETA remaining** | **~2,063 min (~34.4 h)** |

### 🎮 GPU (RTX 4070)

- **Utilization:** 100%
- **VRAM:** 11,072 / 12,282 MiB (90% used)
- **Temp:** 65°C
- **Power:** 193 W

### ⚙️ Background

- 32 Torch `_inductor` compile workers are spawned (normal for the compiled training loop).
- Everything looks healthy: GPU is pegged at 100%, loss is decreasing smoothly, and no errors in the output.

Want me to check the checkpoint/log files (e.g. latest saved checkpoint, eval metrics) under `/mnt/data/nanochat` for more detail?
