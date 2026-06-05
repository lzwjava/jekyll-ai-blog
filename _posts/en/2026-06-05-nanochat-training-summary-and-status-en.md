---
audio: false
generated: true
image: false
lang: en
layout: post
title: NanoChat Training Summary and Status
translated: false
type: note
---

Now I have the full picture. Here's the comprehensive summary:

---

NANOCHAT TRAINING SUMMARY — TMUX SESSION 14
============================================

PROJECT
  nanochat is Karpathy's minimal LLM training harness. Covers tokenization,
  pretraining, SFT, eval, inference, and chat UI in one repo. The "speedrun"
  goal is to reach GPT-2 capability (CORE 0.2565) as fast as possible on
  8XH100. Current leaderboard record: 1.65 hours.

OUR TRAIN
  Run name:     rtx4070-d12-chinchilla (continued from fineweb-edu-d12)
  Started:      June 4, 2026 ~03:29 UTC
  Resumed from: step 10,000 (first run was 10k steps on fineweb-edu-d12)
  Current:      step 35,729 / 87,000 (41.07%)
  ETA:          ~16.8 hours from now (~1006 min remaining)
  Elapsed:      ~11.7 hours (700 min)

MODEL
  Architecture: GPT transformer, depth=12
  Parameters:   286,261,730 (~286M)
  Layers:       12, Heads: 6, KV heads: 6, Embed dim: 768, Head dim: 128
  Vocab:        32,768
  Seq length:   2,048
  FLOPs/token:  ~887M

TRAINING CONFIG
  Batch size:   65,536 tokens/step (device_bs=8, grad_accum=4)
  Iterations:   87,000
  Total tokens: 5.70B (Chinchilla-optimal for 286M params, ratio ~20x)
  LR:           matrix_lr=0.02, scaled by 0.3536 for batch 65536
  Warmup:       40 steps
  Warmdown:     65% of training
  Weight decay: 0.099 (scaled from 0.28 for depth 12)
  FP8:          No (RTX 4070 doesn't support it well)
  Flash Attn:   No (FA3 unavailable, using PyTorch SDPA fallback)

DATA
  Dataset:      NVIDIA ClimbMix (via nanochat)
  On disk:      374 GB, 177 parquet shards
  Available:    ~142.6B tokens total
  Consumed so far: ~2.34B tokens (shard 4/177, rg ~97)
  Will consume:    5.70B tokens (only 4% of available data!)

HARDWARE
  GPU:          RTX 4070, 12 GB VRAM, single GPU
  Speed:        ~55,660 tok/sec, ~1,177ms/step
  MFU:          Shows 0% (peak FLOPS undefined for this GPU)

VALIDATION LOSS TRAJECTORY
  Step      0:    val_bpb = 3.221
  Step  10,000:   val_bpb = 0.935  (best so far)
  Step  20,000:   val_bpb = 1.016
  Step  30,000:   val_bpb = 1.002
  Current train loss: ~3.16-3.20

REALITY CHECK — EXPECTED vs ACTUAL

  1. SCALE MISMATCH WITH LEADERBOARD
     The speedrun leaderboard targets depth=24-26 on 8XH100 (~1.6B params).
     We're running depth=12 (286M params) on a single RTX 4070. This is a
     GPT-1 scale model, not GPT-2 scale. GPT-2 capability requires ~1.6B
     params (depth ~24-26). Our model will NOT reach GPT-2 CORE score.

  2. CHINCHILLA OPTIMALITY
     5.7B tokens for 286M params = ratio ~20x. Chinchilla recommends ~20x,
     so this IS compute-optimal for this model size. Good.

  3. LOSS IS PLATEAUING
     val_bpb went from 0.935 (step 10k) to 1.002 (step 30k) — it actually
     got WORSE after step 10k. The train loss hovers ~3.14-3.22 and isn't
     decreasing meaningfully. This suggests the model may have already
     converged for its capacity, and further training yields diminishing
     returns or slight overfitting.

  4. WALL CLOCK TIME
     On 8XH100, the depth=24 speedrun takes ~1.65 hours. On our single
     RTX 4070, the depth=12 run takes ~28.5 hours. That's ~8x slower per
     GPU, and we're at 1/8 the GPUs, so roughly 64x less throughput than
     the speedrun setup. Realistic for consumer hardware.

  5. WHAT TO EXPECT AT COMPLETION
     - A ~286M param model that can generate coherent text
     - Comparable to early GPT-1 capability (not GPT-2)
     - Good enough for basic chat after SFT (steps 6-7 in the pipeline)
     - The model will hallucinate, struggle with reasoning, and have
       limited world knowledge — it's a kindergartener, not ChatGPT

  6. TRAINING SPEED IS STABLE
     No crashes, consistent ~55.6k tok/sec. 3 checkpoints saved so far
     (10k, 20k, 30k). No signs of divergence or NaN losses.
