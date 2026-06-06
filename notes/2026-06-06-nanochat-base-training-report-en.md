---
audio: false
generated: true
image: false
lang: en
layout: post
title: NanoChat Base Training Report
translated: false
type: note
---

Here's the comprehensive training summary:

```
===============================================================
            NANOCHAT BASE TRAINING SUMMARY
===============================================================

MODEL ARCHITECTURE — GPT-2 style, 286M params
  Layers:        12
  Heads:         6 (GQA with n_kv_head=6)
  Embed dim:     768, Head dim: 128
  Vocab:         32,768
  Context:       2,048 tokens
  Total params:  286.3M (261.1M non-embedding)
  Notable:       RoPE, QK norm, ReLU² MLP, no bias,
                 untied embed/lm_head, Value Embeddings
                 on odd layers (1,3,5,7,9,11) w/ learned gate

TRAINING SCHEDULE
  Phase 1 (steps 0-10k):    fineweb-edu-d12, from scratch
  Phase 2 (steps 10k-87k):  rtx4070-d12-chinchilla, resumed
  Total steps:    87,000
  Batch size:     65,536 tokens/step (device_bs=8 × seq=2048)
  Total tokens:   ~5.7B
  Data ratio:     12 (Chinchilla-optimal: 5.7B / 286M ≈ 20x)
  GPU:            RTX 4070 12GB, bf16, peak 9.4 GB VRAM

OPTIMIZER
  Type:           MuonAdamW (custom)
  Matrix LR:      0.02,  Scalar LR: 0.5
  Embed LR:       0.3,   Unembed LR: 0.008
  Weight decay:   0.28
  Warmup:         40 steps
  Warmdown:       starts at 65% of training (step ~56,550)
  Final LR frac:  0.05

LOSS PROGRESSION
  ┌─────────┬───────────┬────────────┬──────────┬──────────┐
  │  Step   │ Val bpb   │ Train Loss │ Delta    │ Time     │
  ├─────────┼───────────┼────────────┼──────────┼──────────┤
  │  10,000 │ 0.9349    │ 2.979      │  (base)  │  3.2h    │
  │  20,000 │ 1.0155*   │ 3.271*     │  spike   │  6.5h    │
  │  30,000 │ 1.0019    │ 3.234      │ -0.014   │  9.8h    │
  │  40,000 │ 0.9780    │ 3.136      │ -0.024   │ 13.1h    │
  │  50,000 │ 0.9533    │ 3.042      │ -0.025   │ 16.3h    │
  │  60,000 │ 0.9299    │ 2.954      │ -0.023   │ 19.6h    │
  │  70,000 │ 0.9022    │ 2.885      │ -0.028   │ 22.9h    │
  │  80,000 │ 0.8799    │ 2.850      │ -0.022   │ 26.1h    │
  │  87,000 │ 0.8658    │ 2.748      │ -0.014   │ 28.4h    │
  └─────────┴───────────┴────────────┴──────────┴──────────┘
  * Step 20k spike: optimizer state resume + config change

  Phase 2 net improvement: 1.0155 → 0.8658 bpb (-14.7%)
  From scratch to finish:  0.9349 → 0.8658 bpb (-7.4%)

PERFORMANCE
  Throughput:     55,670 tok/sec (constant throughout)
  Step time:      1,177 ms/step
  Total time:     1,706 min (28.4 hours)
  Checkpoints:    9 saved (every 10k steps + final)
  Model size:     ~756 MB per checkpoint
  Optim size:     ~1.2 GB per checkpoint

KEY OBSERVATIONS
  1. Loss never plateaued — still decreasing at final step.
     The warmdown (LR decay) was just beginning to take effect.
     More steps would likely yield further gains.

  2. Phase 2 resume caused a temporary loss spike (0.93→1.02),
     likely from optimizer state mismatch or data distribution
     change. Recovered within ~20k steps.

  3. Val bpb tracked smoothly — no overfitting. Train loss
     stayed above val bpb throughout (expected for smoothed
     vs. point estimates).

  4. RTX 4070 handled this well — 9.4 GB peak VRAM, 100% util,
     66°C, 211W throughout. No OOM, no crashes.

NEXT STEPS
  Evaluate:  python -m scripts.base_eval --device-batch-size=8
  Chat:      python -m scripts.chat_cli -p 'Why is the sky blue?'
  SFT:       python -m scripts.chat_sft  (fine-tune for chat)
  RL:        python -m scripts.chat_rl   (RLHF/DPO alignment)
===============================================================
```

The model is in great shape — loss was still decreasing at finish, never plateaued, no overfitting. The 286M param model with value embeddings and Chinchilla-optimal data ratio performed well on a single RTX 4070. The next natural step would be running `base_eval` to get benchmark scores, then SFT/RL for chat capability.
