---
audio: false
generated: true
image: false
lang: en
layout: post
title: 326k Steps Training Journey
translated: false
type: note
---

Here's the full story of how we got to ~326k steps:

=== THE ZZ TRAINING JOURNEY ===

PHASE 1: DATA COLLECTION & TOOLING (May-June 2026)
The repo started as a dataset processing pipeline. You built scripts to:

- Download FineWeb (100B tokens, GPT-3 ablation shards) and Wikimedia dumps
- Use hf-mirror.com for China access, with resumable downloads (progress.json)
- Extract and tokenize data into uint16 .npy shards (GPT-2 BPE)

PHASE 2: FIRST SMALL RUNS (FineWeb, 125M model)
Early training on FineWeb data with a GPT-2 124M model:

- Config: 12 layers, 12 heads, 768 embed, lr=3e-4, 12k max iters
- Loss dropped from 10.87 → 3.53 in ~20k iters (train_log_fineweb.txt)
- Step time: ~3.9s/iter at ~11% MFU

PHASE 3: NANOCCHAT RUNS (286M model, June 4-6)
Bigger model (286M params, depth=12, n_embd=768, n_head=6) on fineweb-edu:

- 87k steps over ~28.4 hours on RTX 4070
- Val bpb: 0.934 → 0.866 (steadily improving)
- ~55,670 tok/sec throughput
- Finished cleanly at step 87,000

PHASE 4: 760M RUN (MI300X, briefly)
Attempted a 760M model run (logged in nanogpt_760m_train logs), likely on
a rented MI300X GPU.

PHASE 5: GITHUB-CODE 124M (CURRENT, running now)
Switched dataset to 282 .npy shards of GitHub code (27GB tokenized).
Config: GPT-2 124M, batch=4×1024×8 accum = 32,768 tok/step,
lr=6e-4, 427k max iters → 14B tokens total.

Progress:
  Step 0:    loss 10.87 (random init)
  Step 25k:  loss ~3.6  (learning fast)
  Step 325k: val loss 2.7892 (just evaluated at 325k)
  Current:   ~326,960 / 427,000 = 76.6% done

Step time started at ~3.9s but dropped to ~621ms after torch.compile warmed up.
MFU plateaued at 14.44%. At current pace, ~62k steps remaining × 621ms ≈ 10.7 hours left.

The checkpoint saves to /mnt/data/nanoGPT/out-github-code-124m/ (1.4GB).
