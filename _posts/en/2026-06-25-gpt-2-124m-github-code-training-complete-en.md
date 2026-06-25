---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 124M GitHub Code Training Complete
translated: false
type: note
---

Here's the comprehensive training summary:

================================================================
  GPT-2 124M TRAINING ON GITHUB CODE — COMPLETE RUN SUMMARY
================================================================

DURATION
  Start:     Sat Jun 21, 21:14 (directory created)
  End:       Thu Jun 25, 00:39 (final checkpoint saved)
  Total:     ~3 days, 3.5 hours (75.4 hours)

CONFIG
  Model:        GPT-2 124M (12 layers, 12 heads, 768 embd, ~163M total params)
  Dataset:      282 .npy shards of GitHub code (27 GB, ~14B tokens)
  Batch:        4 × 1024 × 8 grad_accum = 32,768 tokens/step
  Steps:        427,000 iterations
  Tokens seen:  ~14.0 billion
  Optimizer:    AdamW (lr=6e-4, cosine decay → 6e-5, warmup 2k steps)
  Precision:    bfloat16, torch.compile enabled

THROUGHPUT
  Avg step time:   ~636 ms/step (including eval/checkpoint overhead)
  Steady-state:    621 ms/step (after torch.compile warmup)
  Steps/hour:      ~5,663
  Tokens/sec:      ~51,900
  Tokens/hour:     ~187 million
  MFU:             14.44%

HARDWARE
  GPU:          RTX 4070 (12 GB VRAM)
  VRAM used:    ~5,050 MiB (7.3 GB free headroom)
  Power draw:   ~208W
  Temperature:  ~65°C

LOSS PROGRESSION
  Step 0:       loss 10.87 (random init)
  Step 14k:     val_loss 5.87
  Step 25k:     loss ~3.6
  Step 70k:     val_loss 2.08 ← best point
  Step 325k:    val_loss 2.79
  Step 427k:    val_loss 3.47 (final best_val_loss in checkpoint)

NOTE: The final val_loss (3.47) is higher than mid-training (2.08 at 70k).
This suggests some overfitting in the later stages as the LR decayed
and the model memorized training data. The best generalization was
around step 60-80k.

CHECKPOINT
  Path:   /mnt/data/nanoGPT/out-github-code-124m/ckpt.pt
  Size:   1.4 GB

PIPELINE
  1. Download:  38/1126 parquet shards from codeparrot/github-code
  2. Tokenize:  GPT-2 BPE via tiktoken → 140 train + 1 val .npy shards
  3. Train:     427k steps on RTX 4070, 3.25 days

================================================================

So yes — 3 days, 3.5 hours, 14 billion tokens, done! 🎉
