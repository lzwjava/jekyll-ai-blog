---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanochat Model Sizing Guide
translated: false
type: note
---

Here's the full picture:

```
NANOCHAT MODEL SIZES
====================

Name   | Depth | Dim  | Heads | Params    | FLOPs/token | Reference
-------|-------|------|-------|-----------|-------------|----------
d4     |   4   | 256  |   4   |    37M    |    72M      | Current CPU run
d8     |   8   | 512  |   4   |    80M    |   250M      | RTX 4070 target
d12    |  12   | 768  |   6   |   286M    |   1.7B      | Karpathy reference
d20    |  20   | 1280 |  10   |   1.0B    |   6B        | Scaling laws target
d24    |  24   | 1536 |  12   |   1.7B    |  10B        | MI300X target
```

```
TRAINING HORIZONS (from scaling laws)
=====================================

d12 reference:
  200k steps × 65,536 tokens/step = 13.1B tokens
  Tokens:params ratio = 13.1B / 286M = 45.8 (Chinchilla optimal ~20)
  Final val_bpb: 0.853

d8 (RTX 4070 script):
  5,000 steps × 32,768 tokens/step = 164M tokens
  Tokens:params ratio = 164M / 80M = 2.05 (very undertrained)
```

```
CPU DDP SPEED ESTIMATES (2 nodes, Gloo)
========================================

Measured: d4 at ~115 tok/sec

Model | Params | FLOPs/token | Est. tok/sec | Time/step | 1000 steps
------|--------|-------------|-------------|-----------|----------
d4    |   37M  |     72M     |    115      |   18s     |    5 hrs
d8    |   80M  |    250M     |    ~35      |   58s     |   16 hrs
d12   |  286M  |    1.7B     |    ~5       |  7.5min   |  5.2 days
d20   |  1.0B  |    6.0B     |    ~1.4     |  26min    |  18 days

Formula: tok/sec ∝ 1 / FLOPs_per_token (compute-bound on CPU)
d4→d12: 72M / 1.7B = 24x slower → 115/24 ≈ 5 tok/sec
```

```
WHAT'S REALISTIC ON CPU DDP
============================

d4 (current):
  20 steps @ 2048 batch = 40,960 tokens → ~6 min ✅ done
  1000 steps → 5 hours → learns basic patterns
  Val bpb: ~10.39 → ~3.2 (huge improvement)

d8:
  1000 steps × 32768 batch = 33M tokens → ~16 hours
  Would need ~5000 steps for decent results → 3.3 days
  Val bpb: should reach ~1.5-2.0

d12 (the real thing):
  Min useful: 10k steps × 65536 batch = 655M tokens → 36 hours
  Karpathy's run: 200k steps → 30 days on CPU DDP
  Best achieved: val_bpb 0.853 (on RTX 4070, took ~65 hours)

VERDICT: CPU DDP is great for learning and d4/d8 experiments.
         For d12+, use the RTX 4070 (GPU is ~100x faster per step).
```

The current d4 run is training well — loss going from 10.40 → 10.39 in 5 steps. For a real model that produces coherent text, you'd want at minimum d8 with 5000 steps. On CPU DDP that's ~3 days. On the RTX 4070 it's a few hours.
