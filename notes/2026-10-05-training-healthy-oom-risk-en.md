---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training healthy, OOM risk
translated: false
type: note
---

Checked tmux session `1`. Here's the full status:

## Current run — healthy and training ✅

**Process:** `python -m scripts.base_train --depth=18 --max-seq-len=1024 --device-batch-size=1 --tracker=none --run=d18-climbmix --core-metric-max-per-task=50 --save-every=250` (PID 3976056, launched today 02:59)

| Metric | Value |
|---|---|
| Progress | step **544 / 3712** (~14.6%), epoch 1 |
| Loss | ~2.97 (down from 10.4 at init; recent range 2.82–3.07) |
| Speed | ~14,000 tok/s, ~75 s/step |
| MFU | ~99.1% (BF16) — steady |
| LR | still 1.00, no decay yet |
| ETA | ~3,955 min ≈ **66 h ≈ 2.7 days** (finish ~Oct 8) |
| GPU | RTX 4070: 100% util, **11.36 / 12.28 GB VRAM (92%)**, 60°C, 164 W |

**Checkpoints** (`/mnt/data/nanochat-cache/base_checkpoints/d18/`): step 250 (08:37) and step 500 (14:02) saved, ~6.8 GB each; next save at step 750.

## What happened before ⚠️

The scrollback shows an earlier run in this same session reached **step 1999/3712 (53.85%, loss ~2.68)** and passed the step-2000 validation (bpb 0.8279) + eval suite — then **crashed with `torch.OutOfMemoryError`** during the `boolq` eval task (`nanochat/gpt.py` logits softcap, tried to allocate 1.51 GiB with only 1.16 GiB free). That killed the old run, and you relaunched from scratch — which is why the current run is back at step 544.

## Risk flag

Training already uses **92% of VRAM**, and the eval at step 2000 runs on top of that — the same OOM will likely recur around **Oct 6 ~21:00** (step 2000). Before then, consider either:
- relaunching with `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` (the traceback's own suggestion), or
- patching the eval path to free training memory / eval in smaller chunks.

No action needed right now — training is progressing normally.