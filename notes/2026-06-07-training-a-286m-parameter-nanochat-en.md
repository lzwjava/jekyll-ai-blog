---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training a 286M Parameter NanoChat
translated: false
type: note
---

Here's the full picture:

============================================================
               NANOKCHAT d12 TRAINING SUMMARY
============================================================

MODEL ARCHITECTURE (286M params)
  Type:              GPT (nanochat d12)
  Layers:            12
  Attention heads:   6 (no GQA)
  Embedding dim:     768
  Head dim:          128
  Vocab size:        32,768 (BPE)
  Context length:    2,048 tokens
  Window pattern:    "L" (full attention, no sliding window)
  Param breakdown:
    wte (token emb):     25.2M
    value_embeds:       151.0M
    lm_head:             25.2M
    transformer_weights: 84.9M
    scalars:                 50
  Total:            286,261,730 params
  FP32 checkpoint:  ~793MB (model) + ~1.2GB (optimizer)
  Peak VRAM:        ~9.4 GB

HARDWARE
  GPU:    NVIDIA RTX 4070 (12GB VRAM)
  DType:  BF16 (auto-detected, SM 89)
  FA3:    Not available, using PyTorch SDPA fallback
  MFU:    Undefined for RTX 4070 (consumer GPU)

TRAINING HYPERPARAMS
  Optimizer:         Muon (matrices) + AdamW (embeddings)
  Matrix LR:         0.02 (scaled by batch factor)
  Embedding LR:      0.3
  Unembedding LR:    0.008
  Scalar LR:         0.5
  Weight decay:      0.28 (scaled to 0.099 for d12)
  Warmup:            40 steps
  Warmdown:          65% of total steps (cosine decay)
  Final LR:          5% of initial
  Batch size:        65,536 tokens/step
    = 8 device_batch x 2048 seq_len x 4 grad_accum

============================================================
PHASE 1: 0 → 130,000 steps (COMPLETED)
============================================================
  Run name:      rtx4070-d12-130k
  Started from:  scratch (first run 0-87k, resumed 87k-130k)
  Steps:         130,000
  Tokens:        130,000 x 65,536 = 8,519,680,000 (~8.5B)
  Training time: 2,549.86 minutes (~42.5 hours)
  Loss:          2.78 → 2.63 → 2.60 (final smooth)
  LR decay:      0.47 → 0.31 → 0.20
  Final val bpb: 0.780026
  CORE metric:   0.1916
  Throughput:    ~55,700 tok/sec (~1.18s/step)
  Checkpoints:   14 saved (every 10k steps)
  Eval highlights:
    hellaswag (10-shot):  0.43
    winograd (0-shot):    0.62
    piqa (10-shot):       0.67
    boolq (10-shot):      0.585
    copa (0-shot):        0.63

============================================================
PHASE 2: 130,000 → 200,000 steps (RUNNING)
============================================================
  Run name:      rtx4070-d12-200k
  Resumed from:  step 130,000 checkpoint
  Steps:         70,000 remaining
  New tokens:    70,000 x 65,536 = 4,587,520,000 (~4.6B)
  ETA:           ~23 hours
  LR schedule:   Entering warmdown (65% of 200k = 130k)
                 Will cosine-decay from 0.02 → 0.001 (matrix)
  Initial loss:  2.57-2.61 (picked up cleanly)
  CORE metric:   0.1932 (at resume point)
  Val bpb:       0.810152 (at resume point)

============================================================
TOKEN BUDGET TOTALS
============================================================
  Phase 1:     8.5B tokens
  Phase 2:     4.6B tokens
  Combined:   13.1B tokens

  Params:     286M
  Token:Param ratio:  45.8:1 (Chinchilla optimal = 20:1)
  Total training FLOPs: ~1.16e19

============================================================
TIMELINE
============================================================
  Phase 1 start:  ~Jun 4 (estimated from checkpoint dates)
  Phase 1 end:    Jun 7, 03:21 (42.5 hours)
  Phase 2 start:  Jun 7, 18:08
  Phase 2 end:    ~Jun 8, 17:00 (estimated, ~23 hours)
  Total wall time: ~65.5 hours (2.7 days)

The model is being trained well past Chinchilla-optimal (45x vs 20x tokens/param). This is "overtrained" — intentional for inference efficiency (a smaller model trained longer is cheaper to serve than a larger model trained shorter).
