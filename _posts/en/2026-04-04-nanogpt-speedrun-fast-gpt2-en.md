---
audio: false
generated: true
image: false
lang: en
layout: post
title: "NanoGPT Speedrun: Fast GPT-2 Training"
translated: false
type: note
---

This is the **NanoGPT Speedrun** repo — a collaborative optimization challenge to train GPT-2 as fast as possible on 8x H100 GPUs. The goal: reach 3.28 cross-entropy loss on FineWeb validation. The current record is under 90 seconds (down from 45 minutes for the original baseline).

Key contents:

- `train_gpt.py` — Main training script for GPT-2 Small (~124M params). Contains the model definition, custom optimizers (Muon + Adam hybrid), and the full training loop.
- `train_gpt_medium.py` — Same idea but for GPT-2 Medium (~350M params).
- `triton_kernels.py` — Custom Triton GPU kernels for efficient matrix ops, fused ReLU², and softcapped cross-entropy.
- `data/` — Scripts to download/preprocess the FineWeb dataset (10B or 100B token versions), tokenized with GPT-2's tokenizer.
- `evals/hellaswag.py` — HellaSwag evaluation benchmark.
- `records/` — 89 experiment records for the Small track and 18 for Medium, documenting the progression of optimizations over time (June 2024 → March 2026).
- `run.sh` — Launcher using `torchrun` with 8 processes.

The optimizations are extensive: rotary embeddings, QK-Norm, ReLU² activations, FP8 matmul, Flash Attention 3 with sliding window, skip connections, sparse attention gates, bigram hash embeddings, batch size/sequence length scheduling, and more. Each `records/` entry documents what changed and the resulting speedup.
