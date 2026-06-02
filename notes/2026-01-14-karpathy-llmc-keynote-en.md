---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Andrej Karpathy on llm.c CUDA Keynote
translated: false
type: note
---

Question: What does the YouTube video at https://www.youtube.com/watch?v=aR6CzM0x-g0 say?

Answer:

The video is a keynote talk titled **"CUDA Mode Keynote | Andrej Karpathy | Eureka Labs"** by Andrej Karpathy, presented at the first CUDA Mode IRL hackathon event organized by Accel.

In it, Karpathy explains the creation and details of his project **llm.c** — a from-scratch implementation to train language models (specifically recreating GPT-2 style training) purely in C/CUDA, with almost no external dependencies (except optionally cuBLAS for FlashAttention).

### Main points he covers:
- **Motivation**: While making educational YouTube videos about training LLMs, he became frustrated with PyTorch bugs (especially torch.compile issues during eval/inference). He decided to rewrite everything in plain C to regain full control, transparency, and understanding.
- **Implementation approach**:
  - Starts by manually writing forward + backward passes in pure C using simple float arrays (no high-level abstractions).
  - All memory is pre-allocated in one big blob at startup → deterministic behavior, no malloc during training.
  - Progressively moves parts to CUDA kernels, optimizing step-by-step (multiple kernel versions, reaching "Kernel 6").
  - Uses techniques like shared memory, warp-level primitives, cache-aware loading, bfloat16, FlashAttention, kernel fusion, gradient checkpointing/recomputation, stochastic rounding, packed data structures, etc.
  - Later adds multi-GPU/multi-node support via NCCL and optimizer state sharding.
- **Results**:
  - Trains a GPT-2 (124M or up to ~1.6B scale) model faster than equivalent PyTorch version in some settings.
  - Achieves ~50% Model FLOPs Utilization (MFU) on H100 GPUs.
  - Runs GPT-2 124M training in ~24 hours on a single H100 node for roughly $600.
  - Uses noticeably less memory and is competitive or faster than PyTorch for this specific workload.
- **Philosophy & call to action**:
  - llm.c is intentionally kept clean and readable (~3,000 lines of C).
  - It serves as a minimal, understandable **reference architecture** for how a full LLM training stack works.
  - Encourages others to build similar reference implementations that fit inside an LLM's context window, so future powerful coding LLMs can directly read, understand, and improve such code.
  - Speculates that as LLMs get much better at coding, they could eventually generate custom CUDA kernels or even replace high-level frameworks for many use cases.

He also mentions community contributions that helped optimize the code, challenges learning modern CUDA (outdated resources), and future plans like adding Llama 3.1 support and FP8.

The talk is technical but accessible if you're familiar with deep learning basics; it's in English, roughly 45–60 minutes long, and includes slides with code snippets.

Karpathy also wrote a detailed accompanying Twitter/X thread breaking it down further.

References:
- [YouTube Video](https://www.youtube.com/watch?v=aR6CzM0x-g0)
- [Andrej Karpathy's X thread on the keynote](https://x.com/karpathy/status/1841536804073439268)
- [Accel event page with more context](https://www.accel.com/noteworthy/6-keynotes-from-the-first-cuda-mode-irl-hackathon)
