---
audio: false
generated: true
image: false
lang: en
layout: post
title: Distributed CPU DDP Setup Complete
translated: false
type: note
---

Done. Here's the final state:

```
FINAL SETUP SUMMARY
===================

Data: 201 parquet shards (18GB) on both machines
  1.36: ~/.cache/nanochat/base_data_climbmix/  (201 files)
  1.47: ~/.cache/nanochat/base_data_climbmix/  (201 files, rsync'd)

Launch scripts:
  1.36: /mnt/data/nanochat/run_dist_cpu_master.sh
  1.47: ~/projects/nanochat/run_dist_cpu_worker.sh

How to run:
  Terminal 1 (master):  bash /mnt/data/nanochat/run_dist_cpu_master.sh
  Terminal 2 (worker):  bash ~/projects/nanochat/run_dist_cpu_worker.sh

Firewall: ufw allow from 192.168.1.0/24 (already applied)

Env vars (in scripts):
  NANOCHAT_FORCE_SDPA=1    — FA is CUDA-only
  NANOCHAT_DTYPE=float32   — bf16 auto-detects from GPU, slow on CPU
  GLOO_SOCKET_IFNAME=...   — bind to LAN interface

Code patches (4 files):
  common.py      — Gloo backend for CPU DDP
  flash_attention.py — NANOCHAT_FORCE_SDPA env var
  optim.py       — _AsyncWorkWrapper for Gloo get_future() compat
  dataset.py     — NANOCHAT_DATA_DIR env var
```

Both machines now have identical full datasets, identical code, and ready-to-run scripts. The multi-node CPU DDP pipeline is fully operational — Gloo connected, gradients synced, checkpoints saved.
