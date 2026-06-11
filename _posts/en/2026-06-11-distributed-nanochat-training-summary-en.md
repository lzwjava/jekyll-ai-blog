---
audio: false
generated: true
image: false
lang: en
layout: post
title: Distributed NanoChat Training Summary
translated: false
type: note
---

Here's the full picture.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  NANOCHAT 2-NODE CPU DDP — COMPREHENSIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ARCHITECTURE
  Protocol: PyTorch DDP (DistributedDataParallel) via Gloo backend
  Transport: TCP (static rendezvous, no Etcd/C10d)
  Rendezvous: master:29500 (TCPStore)
  Data transport: Gloo over Ethernet (ephemeral ports, bidirectional)

MACHINES
  MASTER — lzw@192.168.1.36
    OS:       Ubuntu 24.04 (MSI MS-7E01)
    CPU:      i9 (many cores, ~62 GB RAM)
    GPU:      RTX 4070 12 GB (unused — CPU-only training)
    Role:     rank 0, hosts TCPStore on :29500, runs MLflow tracker
    Interface: enp4s0
    tmux:     nanochat-master
    Script:   /mnt/data/nanochat/run_dist_cpu_master.sh

  WORKER — xiaoxin@192.168.1.28
    OS:       Linux Mint (USB Ethernet adapter)
    RAM:      ~16 GB
    Role:     rank 1, connects to master's TCPStore
    Interface: enx00e04c362f89
    tmux:     nanochat-worker (empty pane — output goes to background proc)
    Script:   ~/projects/nanochat/run_dist_cpu_worker.sh
    Firewall: user opened ports (was blocking Gloo ephemeral ports before)

MODEL
  Name:        d8 (nanochat architecture)
  Params:      125,829,354 (~126M total, not 80M as labeled)
  Breakdown:
    wte (token embeddings):     16.8M
    value_embeds:               67.1M  ← bulk of params
    lm_head:                    16.8M
    transformer_matrices:       25.2M
    scalars:                    42
  Config:
    sequence_len:  1024
    vocab_size:    32,768
    n_layer:       8
    n_head:        4
    n_kv_head:     4
    n_embd:        512
    window_pattern: SSSL (sliding window, PyTorch SDPA fallback — no flash-attn)

TRAINING CONFIG
  Device:          CPU (float32, NANOCHAT_DTYPE=float32)
  Batch:           2 (device) × 1024 (seq) × 2 (ranks) = 4,096 tokens/step
  Grad accum:      1 (no accumulation needed)
  Iterations:      5,000
  Total tokens:    20,480,000 (~20.5M)
  Tokens/param:    0.16 (very low ratio — expect underfitting)
  FLOPs estimate:  5.6 × 10^15
  OMP threads:     8 (master), 4 (worker)

HYPERPARAMETERS (auto-scaled)
  LR scaling:      ×0.0884 for batch 4096 (ref 524,288)
  Weight decay:    0.064965 (scaled from 0.28 for depth 8)
  AdamW LR scale:  ×1.224745 (∝ 1/√(512/768))
  Tracker:         MLflow (master only), experiment "nanochat-d8"

CURRENT STATUS (as of this snapshot)
  Step:       4 / 5,000 (0.08%)
  Loss:       10.392623 (down from 10.398023 at step 0)
  Val bpb:    3.209475 (step 0)
  Speed:      55-57 tok/s
  Step time:  ~72-73 seconds
  ETA:        5000 × 72s ≈ 98-100 hours ≈ 4.1 days

ISSUES ENCOUNTERED & RESOLVED

  1. EADDRINUSE (port 29500) — stale processes from earlier attempt held the
     port. Fixed: fuser -k 29500/tcp + pkill
  2. Gloo connection timeout — master→worker on ephemeral ports blocked by
     worker's firewall. Worker had no sudo. Fixed: user opened firewall.
  3. Stale orphan processes — old background runs left orphaned base_train
     processes (PPID=1). Fixed: kill -9 by PID.
  4. Log capture — script/tee buffering hid stderr output. Used tmux
     capture-pane instead.

KNOWN LIMITATIONS

- PyTorch SDPA fallback (no flash-attn) — no sliding window support
- CPU-only — 57 tok/s vs ~60 tok/s single-node (minimal parallelism gain)
- Gloo all-reduce over Ethernet is the bottleneck, not compute
- Worker tmux pane shows no output (backgrounded process)
- Tokens/param ratio 0.16 is very low — model will underfit

MONITORING
  Latest step:
    ssh lzw@192.168.1.36 "tmux capture-pane -t nanochat-master -p | tail -3"
  Attach master:
    ssh -t lzw@192.168.1.36 "tmux attach -t nanochat-master"
  MLflow UI:
    <http://192.168.1.36:5000>
  Kill training:
    ssh lzw@192.168.1.36 "tmux kill-session -t nanochat-master"
    ssh lzw@192.168.1.36 "ssh xiaoxin@192.168.1.28 'tmux kill-session -t nanochat-worker'"
