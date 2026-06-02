---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Tri Dao FlashAttention 3 Keynote Summary
translated: false
type: note
---

Question: What does the YouTube video at <https://www.youtube.com/watch?v=_B6ZbRbxiMY> say?

Answer:

The video is a technical keynote presentation titled **"CUDA Mode Keynote | Tri Dao | Together.ai"** uploaded by the Accel channel on October 3, 2024.

It features Tri Dao (Assistant Professor at Princeton and Chief Scientist at Together AI), the inventor of FlashAttention, presenting **FlashAttention 3**, the latest version of his highly efficient attention mechanism for transformers.

**Main points covered in the talk:**

- Explains why efficient attention is critical for handling very long sequences (millions of tokens) in large language models and other transformer-based applications (NLP, vision, audio, video, medical imaging, etc.).
- Discusses performance bottlenecks in standard attention implementations, especially as context length grows (e.g., sharp drop in throughput beyond ~2K tokens on A100 GPUs).
- Introduces **FlashAttention 3**, optimized specifically for NVIDIA Hopper GPUs (like H100), building on FlashAttention 2.
- Key technical innovations include:
  - Use of new hardware features: **warp group matrix multiply-accumulate (MMA)** instructions and **Tensor Memory Accelerator (TMA)** for faster, asynchronous memory loading with less register pressure.
  - **Asynchrony** techniques (warp specialization, ping-pong scheduling, intra-warp-group overlapping) to hide latencies and overlap matrix multiplies with softmax operations, addressing the slow exponential computation in softmax.
  - **Low-precision FP8** computation to double throughput, combined with orthogonal transformations (e.g., Hadamard transform) to maintain numerical stability and reduce errors from outlier features in LLMs.
- Performance results: FlashAttention 3 achieves 1.6–3× speedup over FlashAttention 2, reaching up to ~750 TFLOPs (at head dimension 256) and ~1.3 PFLOPs in FP8 — close to the raw speed of matrix multiplication on H100.
- This enables training and inference with 2–3× longer sequences using the same hardware budget, leading to faster training and better long-context models.
- Mentions collaboration with Together AI, Meta, NVIDIA, and use of CUTLASS 3 for async programming.
- Concludes that asynchrony and low precision are essential for efficient long-sequence modeling beyond chat applications, extending into science and other domains.
- FlashAttention 3 is described as a fast and accurate attention primitive for Hopper GPUs, with future plans to support AMD GPUs, TPUs, Blackwell, etc.

The talk is highly technical, aimed at GPU programmers, ML researchers, and people working on high-performance transformer implementations. It includes slides with benchmarks, kernel diagrams, and code-level explanations.

References:

- [CUDA Mode Keynote | Tri Dao | Together.ai](https://www.youtube.com/watch?v=_B6ZbRbxiMY)
- [Accel event page mentioning the talk](https://www.accel.com/noteworthy/6-keynotes-from-the-first-cuda-mode-irl-hackathon)
