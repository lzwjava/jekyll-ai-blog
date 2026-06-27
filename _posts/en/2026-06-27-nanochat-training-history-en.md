---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanochat Training History
translated: false
type: note
---

Here's the full picture of your previous nanochat training:

=== TRAINING HISTORY SUMMARY ===

You ran multiple training experiments. Here's what happened:

--- 1. d8 base model (2-node CPU distributed, Jun 2) ---
   - Model: depth=8, 512 dim, 4 heads, seq_len=1024
   - Trained: step 1000 on CPU (2 nodes), val_bpb = 1.64
   - Continued to step 5000 on RTX 4070, val_bpb = 0.99
   - Total training time: ~26 min (RTX 4070 portion)

--- 2. d12 base model (RTX 4070, Jun 7-10) ---
   - Model: depth=12, 768 dim, 6 heads, seq_len=2048
   - Resumed from step 130,000, trained to step 200,000
   - Best val_bpb: 0.7800 (at step 130k)
   - Final val_bpb: 0.8534 (at step 200k)
   - Total training time: ~65 hours on RTX 4070
   - Batch size: 65,536 tokens, LR: 0.001 (Muon), embedding LR: 0.015

--- 3. d12-fresh-fa2 (RTX 4070, Jun 10) ---
   - Fresh d12 with Flash Attention 2, seq_len=2048
   - Trained 5000 steps, val_bpb = 0.928
   - Total time: ~1.6 hours (short test run)

--- 4. d4 base model (2-node CPU, Jun 11) ---
   - Tiny model: depth=4, seq_len=512, only 20 steps
   - val_bpb = 4.23 (barely trained, just a test)

--- 5. d8 SFT (RTX 4070, Jun 2) ---
   - Fine-tuned the d8 model with SFT
   - Trained 188 steps, val_bpb = 0.822 (SFT loss)
   - ChatCORE metric: 0.0037 (essentially random)

=== RESULTS ANALYSIS ===

The d12 model was your main training effort. Results:

  CORE metric (d8, step 5k):  0.0815  (very weak, random is ~0)
  Target (GPT-2):             0.2565

The d12 model reached val_bpb=0.78 which is decent for a 12-layer model,
but it was still far from GPT-2 capability (CORE 0.2565). The d8 model
was too small to be useful. The SFT on d8 produced a ChatCORE of 0.0037,
essentially random - the base model wasn't good enough for SFT to help.

For reference, Karpathy's speedrun uses depth=24 with 8xH100 and reaches
GPT-2 level in ~2 hours. Your RTX 4070 (12GB VRAM) can only fit smaller
models. The d12 on RTX 4070 took 65 hours and still didn't reach GPT-2 level.

Want to try fine-tuning the d12 checkpoint with SFT, or train a new model?
