---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training 760M Model on 12GB GPU
translated: false
type: note
---

Here's the analysis of this machine:

## Machine Specs

| Component | Details |
|-----------|---------|
| CPU | Intel i9-13900KF, 24 cores / 32 threads, 5.8GHz boost |
| RAM | 64GB (56GB available) |
| GPU | NVIDIA RTX 4070, 12GB VRAM, CUDA 13.0, driver 580.126.20 |
| Disk | /mnt/data = 1.8TB total, 972GB free (45% used) |
| PyTorch | 2.10.0+cu128, CUDA working |

## What's Already Here

You already have nanoGPT set up at `/mnt/data/nanoGPT/` with:

- **285GB of FineWeb-Edu data** in `data/fineweb/edu_fineweb100B/` (263GB of shards + 6.9GB train.bin)
- **A 760M config** at `config/train_fineweb_760m.py` — n_layer=24, n_head=24, n_embd=1536
- Previous training runs: out-fineweb, out-gpt2-200m, out-wikipedia, etc.

## The Problem: RTX 4070 has only 12GB VRAM

The 760M config was written for MI300X (192GB). On your RTX 4070 (12GB):

- Model weights (fp16): ~1.5GB
- Optimizer states (Adam): ~4.5GB
- Activations for bs=32, block=1024: **way over 12GB**

You'll hit OOM immediately with `batch_size=32`.

## Options

**Option A: Train on this GPU with reduced batch**

```
batch_size=2, gradient_accumulation_steps=16
```

This keeps effective batch at 32K tokens but processes 2 samples at a time. Will be slow (~weeks for 445K steps) but fits in 12GB.

**Option B: CPU-only training** — 64GB RAM is plenty for the model, but training would take months. Not practical.

**Option C: Use the MI300X remotely** — if you have SSH access to the MI300X machine, scp the data there and train. The 760M config is already tuned for it.

**Option D: Smaller model on this GPU** — train a 200M or 350M model that comfortably fits with bs=12+ on the 4070.

The data is already prepared — no downloads needed. Want me to adjust the config for Option A (760M on RTX 4070 with gradient accumulation) and do a smoke test?
