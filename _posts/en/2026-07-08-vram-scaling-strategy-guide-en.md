---
audio: false
generated: true
image: false
lang: en
layout: post
title: VRAM Scaling Strategy Guide
translated: false
type: note
---

Now let me check current VRAM usage to see what headroom we have:

**Current state at step ~996 (3.4%):**

- Loss: 10.4 → **3.0** (dropping fast — no bottleneck yet)
- VRAM: **54 GB / 144 GB (38%)** — only 54 GB used, 90 GB free!
- Step time: ~4.0s, MFU: 63%

---

## Batch Scaling Strategy

You have **90 GB free VRAM** — a huge advantage. Here's when and how to increase batch size:

| Training Phase | Steps | Loss Range | Batch Size | Why |
| --- | --- | --- | --- | --- |
| **Early** (now) | 0–20,000 | 10.4 → ~2.5 | 524K (current) | Learning fast, smaller batch = more exploration |
| **Mid** | 20,000–26,000 | ~2.5 → ~2.3 | **2M tokens** (4×) | Cleaner gradients near convergence |
| **Final** | 26,000–29,000 | ~2.3 → final | **4M tokens** (8×) | Polish the minimum |

**When to act**: The bottleneck starts around **step 20,000** (70%) when loss plateaus. Check every 5000-step eval — when loss stops dropping by more than 0.01 per 500 steps, it's time.

**On H200 with 90 GB free**, you can go from device_batch=16 up to **device_batch=64** (uses ~108 GB, still fits):

| Device Batch | Total Batch | VRAM Est. | What It Does |
| --- | --- | --- | --- |
| 16 (current) | 524K | 54 GB | Exploration mode |
| 32 | 1M | ~75 GB | Moderate smoothing |
| 48 | 2M | ~95 GB | Good convergence boost |
| 64 | 4M | ~115 GB | Max — final polish only |

### How to Implement

At step ~20,000, stop training (Ctrl+C in tmux), then:

```bash
tmux new -s train-d24-phase2
source .venv/bin/activate
export NANOCHAT_DATA_DIR=/workspace/zz/datasets/fineweb-edu/

python -m scripts.base_train \
  --depth=24 \
  --device-batch-size=48 \
  --total-batch-size=2097152 \
  --max-seq-len=2048 \
  --window-pattern SSSL \
  --fp8 \
  --resume-from-step=20000 \
  --num-iterations=22360 \
  --eval-every=200 \
  --save-every=1000 \
  --run=h200-d24-760m-phase2 \
  --tracker=wandb
```

The `--resume-from-step=20000` loads the saved checkpoint and dataloader state, and `--num-iterations` is recalculated so total token count stays the same.

### One catch

Larger batch at convergence can settle into **sharp minima** that generalize worse. To offset: reduce LR slightly (the code scales it automatically), or add a brief LR warmup after the batch change. The existing `--warmdown-ratio=0.65` handles the tail schedule.

Want me to set up a cron job that monitors the loss and alerts you when it's time to scale?
