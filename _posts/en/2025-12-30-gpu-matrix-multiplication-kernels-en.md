---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: High-Performance GPU Matrix Multiplication Kernels
translated: false
type: note
---

Question: What does the content of the blog post at https://www.aleksagordic.com/blog/matmul say?

Answer: 

The blog post, titled **"Inside NVIDIA GPUs: Anatomy of high performance matmul kernels - From GPU architecture and PTX/SASS to warp-tiling and deep asynchronous tensor core pipelines"**, is written by Aleksa Gordić and was published on September 29, 2025.

It is a highly technical, in-depth exploration of how to implement state-of-the-art (SOTA) matrix multiplication (matmul) kernels on NVIDIA GPUs, with a primary focus on the Hopper architecture (e.g., H100 GPU). The post emphasizes that matmul is the most critical operation in transformers (used in linear layers, attention projections, etc.), consuming the majority of FLOPs during training and inference, making GPU optimizations extremely valuable.

### Structure and Main Sections

The post is divided into four major parts:

1. **NVIDIA GPU Architecture Fundamentals**  
   - Detailed explanation of the memory hierarchy: Global Memory (HBM/GMEM), L2 cache, L1 cache/shared memory (SMEM), and registers.  
   - Compute units: Tensor Cores, CUDA cores, load/store units, and warp schedulers.  
   - Concepts like parallelism vs. concurrency, "speed-of-light" (SoL) peak performance calculations, power throttling effects on clock speeds, and Tensor Memory Accelerator (TMA) in Hopper.

2. **GPU Assembly: PTX and SASS**  
   - Covers the compilation pipeline from CUDA C++ to PTX (virtual assembly) to SASS (native ISA).  
   - Shows how to inspect and influence low-level code generation for better performance.

3. **Synchronous Warp-Tiling Matmul Kernel**  
   - Introduces warp-tiling to boost arithmetic intensity by reducing global memory traffic.  
   - Explains tiling strategies, loading matrices A and B into shared memory (with transposition for vectorized loads), handling bank conflicts via swizzling, and computing partial results in registers.  
   - Includes code snippets for naive vs. tiled kernels and performance analysis.

4. **Asynchronous SOTA Matmul on Hopper**  
   - Leverages Hopper-specific features: asynchronous `wgmma.mma_async` instructions for Tensor Cores, TMA for async GMEM-to-SMEM transfers, and pipelining.  
   - Describes producer-consumer pipelines with circular buffers, warp-group collaboration (128 threads), swizzling to eliminate bank conflicts, persistent kernels, and advanced scheduling (e.g., Hilbert curves for better cache locality).  
   - Achieves massive performance gains (e.g., from ~32 TFLOP/s to ~317 TFLOP/s).

### Key Technical Insights

- **Why Optimize Matmul?** It's embarrassingly parallel and dominates transformer compute.
- **Performance Bottlenecks:** Memory-bound vs. compute-bound (roofline model), bank conflicts, uncoalesced accesses, occupancy, and wave/tile quantization.
- **Optimizations Highlighted:**  
  - Vectorized/coalesced loads.  
  - Shared memory tiling and outer-product formulation.  
  - Asynchronous operations to overlap compute and memory.  
  - Swizzling and multicasting in SMEM.  
  - Cluster-level coordination and persistent blocks.

The post includes numerous diagrams (e.g., memory hierarchies, bank conflict illustrations, pipeline stages), annotated code snippets (CUDA, PTX, SASS), mathematical derivations (e.g., peak FLOPs formulas), and performance metrics from tools like Nsight Compute.

### Conclusion/Takeaway

High-performance matmul requires intimate knowledge of GPU hardware and low-level programming. Pre-Hopper GPUs rely on warp-tiling for near-SOTA results, but Hopper's async features enable order-of-magnitude improvements. The author stresses that "computers can be understood" and teases future posts on Blackwell GPUs, multi-GPU setups, and more.

This post is aimed at advanced CUDA programmers and GPU kernel developers seeking to achieve peak performance.

References:  

- [Original blog post](https://www.aleksagordic.com/blog/matmul)