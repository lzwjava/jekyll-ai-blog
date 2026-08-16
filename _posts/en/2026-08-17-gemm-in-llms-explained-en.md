---
audio: false
generated: true
image: false
lang: en
layout: post
title: GEMM in LLMs Explained
translated: false
type: note
---

Question: What is GEMM in the context of LLMs?

Answer: GEMM stands for **General Matrix Multiply** (also written as GEMM: `C = αAB + βC`), a core routine from the BLAS (Basic Linear Algebra Subprograms) library standard.

In LLMs, GEMM matters because:

- **Core computation**: Nearly all the heavy lifting in a transformer — linear layers, attention projections (Q/K/V), feed-forward networks — reduces to matrix multiplications, i.e., GEMM operations.
- **Performance bottleneck**: Since GEMMs dominate compute (FLOPs), how efficiently they run on GPUs/TPUs largely determines training and inference speed. Libraries like cuBLAS, cuBLASLt, and cuDNN provide highly optimized GEMM kernels.
- **Batched GEMM**: LLM workloads often use batched or strided GEMM (multiplying many small matrices at once), especially in attention computation across heads and batch elements.
- **Precision variants**: You'll see terms like FP16 GEMM, INT8 GEMM, or FP8 GEMM — referring to the numerical precision used, which trades off speed/memory vs. accuracy.
- **Optimization target**: Techniques like kernel fusion, tensor cores (on NVIDIA GPUs), and quantization all aim to make GEMM operations faster or cheaper, since they're the main cost driver in both training and inference.

In short, when people discuss LLM efficiency — "how many GEMMs per forward pass," "GEMM-bound vs. memory-bound," or "tensor core utilization" — they're talking about optimizing these matrix multiply operations that make up the bulk of the model's actual computation.
