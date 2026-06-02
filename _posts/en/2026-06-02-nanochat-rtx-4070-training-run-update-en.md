---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanochat RTX 4070 Training Run Update
translated: false
type: note
---

Nanochat is running on the RTX 4070:

  GPU:      RTX 4070 — 2.7 GB / 12 GB VRAM used, 99% utilization
  Model:    depth=8 (~40M params), bf16
  Throughput: ~103K tok/sec
  Loss:     7.73 → 6.22 (step 81/5000)
  ETA:      ~26 min pretraining, then SFT (~8 min), total ~35-40 min

Running in tmux session `nanochat` on the workstation. Log at `/mnt/data/nanochat/run_rtx4070.log`.

Note: only 2.7 GB VRAM used — you could easily bump to `--depth=12` or `--depth=16` for a bigger model if you want. The d8 is a quick demo run. Want me to let this finish, or restart with a larger model?
