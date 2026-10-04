---
audio: false
generated: true
image: false
lang: en
layout: post
title: Device Batch Size 1 Fixes OOM
translated: false
type: note
---

Checked tmux `1` — confirmed: OOM at **step 0, `optimizer.step()`** (the Muon stacked buffer, 184 MiB), only 62 MiB physically free. The eval flag was fine; the problem is raw steady-state VRAM: params + grads + optimizer states (~7.5 GB) + activation peak + your desktop's 2.05 GB > 11.56 GB.

**The lever that reduces training VRAM: `--device-batch-size=1`**

This halves the activation peak (the biggest CLI-controllable memory block, ~680 MB → ~340 MB for d18/seq1024), giving the optimizer's stacked buffers room to breathe. Everything else stays identical — `total-batch-size` auto-computes to the same 1,048,576, so:

- grad-accum just goes 512 → 1024 micro-steps (same math, same LR scaling, same 3,712 iterations)
- steps get ~10-15% slower, that's the only cost

```bash
tmux attach -t 1
cd /mnt/data/nanochat
NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache \
./.venv/bin/python -m scripts.base_train \
    --depth=18 --max-seq-len=1024 \
    --device-batch-size=1 \
    --tracker=none --run=d18-climbmix \
    --core-metric-max-per-task=50 \
    --save-every=250
```

Notes:
- **Don't bother adding `PYTORCH_CUDA_ALLOC_CONF`** — I checked: `base_train.py:15` already sets `PYTORCH_ALLOC_CONF=expandable_segments:True` *before* torch is imported, and it takes priority over the CUDA variant anyway. The error message suggesting it is just PyTorch's generic boilerplate — memory was physically exhausted, not merely fragmented (only 62 MiB free).
- New estimate: ~8.3-8.6 GB process + 2.05 GB desktop ≈ **0.7-1 GB margin** on the 11.56 GB card.

If it *still* OOMs, next resort (in order):
1. `--eval-tokens=2097156` — shrinks each val-eval pass (default is a huge 41.9M tokens ≈ 7 min every 250 steps anyway; also speeds the run up)
2. `--eval-every=-1` — skip val bpb entirely, keep only the CORE metric

Want me to send this into tmux `1` now?