---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fineweb Training Progress Update
translated: false
type: note
---

## Training status

**Config:** `train_fineweb.py` — 124M params, max_iters=12000

**Latest progress:** iter 6800 / 12000 (~57% done)

- train loss: 3.4861, val loss: 3.4225 (at step 6500, last eval)
- loss dropping smoothly: 10.99 → 3.48 over the run
- ~9.34s per iter, mfu ~13–15%

**Time to finish:** 5200 iters left × ~9.34s/iter ≈ **13.5 hours** → should end roughly **9–10 PM HKT today** (Apr 30).

**Checkpoint:** `/home/lzw/projects/nanoGPT/out-fineweb/ckpt.pt` — **1.4 GB**, last saved at 06:42 (step 6500). It's overwritten every 500 iters when val loss improves.

Note: both tmux sessions 0 and 1 show identical output — only one `train.py` PID (980082) is actually running, attached to pts/4. The other session is likely just viewing the same log.
