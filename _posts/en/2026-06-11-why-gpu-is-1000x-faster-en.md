---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why GPU is 1000x faster
translated: false
type: note
---

Great question. The ~1000x gap comes from fundamental hardware differences, not software issues.

CPU (i9 on 1.36):
  - Cores: ~24 (general-purpose, complex branch prediction, OoO execution)
  - Memory bandwidth: ~50-80 GB/s (DDR5)
  - Compute: scalar/vector (AVX-512 at best)
  - No tensor cores
  - Training in float32

RTX 4070:
  - CUDA cores: 5,888 (simple, massively parallel)
  - Memory bandwidth: 504 GB/s (GDDR6X)
  - Tensor cores: 184 (matrix multiply in hardware)
  - Training in float16/bfloat16 with mixed precision

The breakdown:

  1. Memory bandwidth (~10x)
     Transformer training is memory-bandwidth-bound. Each step moves 126M
     params (weights + activations + gradients) through memory. CPU reads at
     ~50 GB/s, GPU at 504 GB/s. That's 10x right there.

  2. Compute throughput (~20-50x)
     5,888 CUDA cores doing fused multiply-add vs 24 CPU cores doing AVX-512.
     Matrix multiplies parallelize perfectly on GPU. CPU does them sequentially
     in chunks.

  3. Tensor cores (~2-4x)
     RTX 4070 has 184 tensor cores that do 4x4 matrix multiply in a single
     instruction on fp16 data. CPU has no equivalent.

  4. Mixed precision (~2x)
     GPU trains in bf16/fp16 — half the memory, double the throughput.
     CPU is stuck in float32 (your NANOCHAT_DTYPE=float32).

  5. Fused kernels + CUDA graphs (~1.5-2x)
     PyTorch on GPU fuses operations (attention, layer norm, etc.) into single
     kernels. CPU executes each op separately with Python dispatch overhead.

  ~10 × ~30 × ~3 × ~2 × ~1.5 ≈ ~2,700x theoretical max
  Real-world: ~1,000x (kernel launch overhead, memory stalls, etc.)

The single biggest factor is memory bandwidth. A transformer step is basically: read all weights, compute matmuls, write activations, read again for backward. When your model fits in VRAM (126M params = ~500MB in fp16, easily fits in 12GB), the GPU's 504 GB/s bus is the highway. The CPU's 50 GB/s DDR5 is a country road.

Bottom line: CPU DDP at 57 tok/s is doing the same math the GPU would do — just through a straw instead of a firehose.
