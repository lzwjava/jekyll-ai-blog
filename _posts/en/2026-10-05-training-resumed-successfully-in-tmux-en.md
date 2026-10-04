---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Resumed Successfully in Tmux
translated: false
type: note
---

Checked — the job **restarted successfully** in tmux `1` at 02:05. ✅

**Process running:**
```
./.venv/bin/python -m scripts.base_train --depth=18 --max-seq-len=1024 
    --device-batch-size=2 --tracker=none --run=d18-climbmix 
    --core-metric-max-per-task=50 --save-every=250
```

**Status:**
- **GPU:** 5,330 MiB / 12,282 MiB used — much healthier headroom than before (old run was pushing 9.35 GiB at eval time)
- **Config identical to the crashed run:** d18, 701M params, 3,712 iterations, 1,048,576 tokens/step, 512 grad-accum steps
- **Phase:** startup done — it's now in (or just finishing) the `torch.compile` warmup, then step 0 begins

**What to expect:**
- ~58s/step → first checkpoint at **step 250** in ~4 hours (`/mnt/data/nanochat-cache/base_checkpoints/d18/`)
- The dangerous CORE eval now runs with `max-per-task=50` instead of 500 — much smaller eval batches, should clear the OOM at step 2000 and the final step
- Total ETA: **~2.4 days** for all 3,712 steps

To watch it later: `tmux attach -t 1`