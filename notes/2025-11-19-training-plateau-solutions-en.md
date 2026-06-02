---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Training Plateau Causes and Solutions
translated: false
type: note
---

The training log you posted shows a classic **severe plateau** in a small-scale nanoGPT run on FineWeb-edu data. The validation loss drops nicely at first (from ~10.9 → ~3.57 around iter 14k), but then completely flattens and even starts to **very slowly rise** after ~13-14k iterations.

Here are the real reasons why your model stopped improving (ranked by importance for this exact setup):

### 1. You are massively overfitting a single Parquet file
- Your run name: `125M-single-parquet-4070`
- You are training a 40M–125M model (the log says 40.56M params, probably the original GPT-2 small config) on **one single FineWeb parquet** (probably 10–15 GB → ~3–4 billion tokens at most, but likely much less after filtering).
- By iter 14 000 with batch_size=16, grad_accum=32, block_size=1024 you have already seen:
  14 000 iters × 524 288 tokens/iter ≈ **7.3 billion tokens**
- That means you have already done **2–3 full epochs** over the exact same data.
- FineWeb-edu is high-quality but still has a lot of near-duplicates and boilerplate. After 1.5–2 epochs on the same file(s), a 40M–125M model will memorize almost everything useful and loss plateaus hard.

### 2. Learning rate is now too high after the plateau
- You use `learning_rate = 1e-3`, cosine decay to `min_lr = 1e-4` over 20 000 iters.
- At iter 14 000 the LR is still ~2.5e-4 (cosine decay is slow at the beginning).
- Once the model has learned everything the data has to offer, keeping LR at hundreds of micro-lr units prevents it from fine-tuning further and actually starts hurting generalization → val loss slowly climbs.

### 3. Model size vs data diversity mismatch
A 125M (or even the 40M you actually initialized) model on a single parquet file is like giving a college student only one textbook and asking him to keep studying it for years. After a while he can recite it perfectly, but test-time performance on new text stops improving and even degrades slightly due to catastrophic forgetting of earlier patterns.

### 4. No regularization strong enough
- dropout = 0.1 is okay, but not enough when you overfit this hard
- weight_decay = 0.1 is standard, but still not sufficient for 2+ epochs on tiny data
- No gradient clipping (nanoGPT default is 1.0, but sometimes people set 0.5 or lower for small data)

### 5. Tokens seen vs real diversity
Even though you saw 7+ billion tokens, the **effective diversity** is maybe 1–1.5B unique high-quality tokens after dedup, boilerplate, low-edu-score samples, etc. That’s just not enough for a 125M model to keep improving past ~3.5–3.6 loss on this text distribution.

### Evidence from your own log

| Step   | Val loss | Comment                              |
|--------|----------|--------------------------------------|
| 0      | 10.87    | random                                       |
| 2000   | 4.03     | fast progress                            |
| 5000   | 3.76     | still good                                 |
| 8000   | 3.65     | slowing                                    |
| 11000  | 3.61     | almost flat                                |
| 13500  | 3.57     | **absolute lowest**                        |
| 14500  | 3.569    | already rising again → classic overfit sign |

### What you should do instead to actually get lower loss

1. Use way more data
   - Use the full 100+ GB FineWeb-edu sample (or at least 10–20 parquet files)
   - Or stream from HuggingFace datasets with multiple shards

2. Train for exactly 1 epoch (or slightly less) on diverse data
   - ~10B–15B tokens total is the sweet spot for 125M on FineWeb-edu
   - Llama-3/Phi-3 style: 15B tokens → ~3.0–3.2 val loss for 125M-class models

3. Lower final learning rate
   - Use `min_lr = 5e-5` or `3e-5` (common in recent small model runs)
   - Or switch to linear decay + longer zero-lr hold

4. Slightly larger model or better architecture tricks
   - The original nanoGPT is GPT-2 style (ALiBi absent, old RoPE, etc.)
   - Modern 125M models (Qwen2-0.5B, Phi-3-mini, Llama-3 8B scaled down) reach ~2.8–3.0 on the same data because of SwiGLU, RMSNorm, rotary embeddings, etc.

### TL;DR – Why your run plateaued at ~3.57 and will never go lower

You are training a 40–125M model for multiple epochs on one single FineWeb parquet file (~few billion tokens total). The model has already memorized everything useful by ~13k iters. Continued training with still-high LR just shuffles weights around → plateau + slight overfit degradation.

This is the #1 mistake people make when they first try nanoGPT on FineWeb: “I’ll just use one file to test” → ends up with exactly this loss curve.

Fix: either (a) use 10–50× more data and train for ~1 epoch total, or (b) accept that ~3.55–3.6 is the absolute floor for this model+data combination and stop training.

If you want a run that actually reaches ~3.0–3.2 loss with nanoGPT-style code, you need at least the full 100GB FineWeb-edu sample (or the newer FineWeb-Edu 2.0) and train for ~15B tokens max.
