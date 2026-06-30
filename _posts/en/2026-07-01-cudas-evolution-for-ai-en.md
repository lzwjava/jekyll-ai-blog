---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA's Evolution for AI
translated: false
type: note
---

Question: How has CUDA evolved over the years?

Let me get the current state right before laying out the timeline.Question: How has CUDA evolved over the years — what are the major architectural and programming-model shifts across its history?

Answer:

CUDA's evolution tracks two intertwined arcs: the **hardware** (each GPU architecture adding capabilities) and the **programming model** (how you express parallelism). Here's the throughline from a model-trainer's perspective — what actually changed for the code you write and the FLOPs you get.

## The big picture

```
2006  CUDA 1.0      SIMT model born — threads, blocks, grids, shared memory
2008  CUDA 2.x      double precision (Tesla), atomics
2010  CUDA 3.x      Fermi: real L1/L2 cache, ECC, unified address space
2012  CUDA 5.x      Kepler: dynamic parallelism, GPUDirect
2014  CUDA 6.x      Unified Memory (cudaMallocManaged)
2016  CUDA 8.x      Pascal: NVLink, FP16, page-migration UM
2017  CUDA 9.x      Volta: TENSOR CORES, independent thread scheduling, cooperative groups
2018  CUDA 10.x     Turing: INT8/INT4 tensor cores, RT cores
2020  CUDA 11.x     Ampere: TF32, BF16, sparsity, async copy (cp.async), CUDA graphs mature
2022  CUDA 12.x     Hopper: FP8, TMA, thread-block clusters, wgmma, distributed shared mem
2025  CUDA 13.x     Blackwell: FP4/FP6, tile programming model (cuTile), drops pre-Turing
```

The single most important inflection for AI was **Volta (2017) introducing Tensor Cores** — dedicated matmul units. Everything since is about feeding them better.

## The programming-model shifts that matter for ML

**1. SIMT (2006–today): the foundation**

You write a kernel from the perspective of one thread; the hardware runs warps of 32 in lockstep. This is the mental model you used training GPT-2.

```cuda
__global__ void saxpy(int n, float a, float* x, float* y) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;  // global thread index
    if (i < n) y[i] = a * x[i] + y[i];
}
// launch: saxpy<<<(n+255)/256, 256>>>(n, 2.0f, d_x, d_y);
```

**2. Tensor Cores (Volta, 2017): the AI pivot**

Instead of one FMA per thread, a warp cooperatively issues a matrix-multiply-accumulate. The `wmma` API (then `mma`, then `wgmma` on Hopper) exposes this. This is why an H100 does ~1000 TFLOPS BF16 vs a few dozen on the CUDA cores — your transformer's `Q @ K^T` lives here.

```cuda
#include <mma.h>
using namespace nvcuda::wmma;
fragment<matrix_a, 16, 16, 16, half, row_major> a_frag;
fragment<matrix_b, 16, 16, 16, half, col_major> b_frag;
fragment<accumulator, 16, 16, 16, float> c_frag;
fill_fragment(c_frag, 0.0f);
load_matrix_sync(a_frag, a, 16);
load_matrix_sync(b_frag, b, 16);
mma_sync(c_frag, a_frag, b_frag, c_frag);   // 16x16x16 MMA on tensor core
store_matrix_sync(c, c_frag, 16, mem_row_major);
```

**3. Async + the memory hierarchy (Ampere→Hopper, 2020–2022)**

The bottleneck became *feeding* tensor cores, not the math. So CUDA added:
- `cp.async` (Ampere): copy global→shared without going through registers, overlapping with compute. This is the heart of FlashAttention's pipelining.
- **TMA** (Hopper): a hardware DMA engine that does bulk async tensor copies with a single instruction — the programmer hands it a descriptor instead of computing per-thread addresses.
- **Thread-block clusters + distributed shared memory** (Hopper): blocks on the same SM-cluster can read each other's shared memory.

**4. Lower precision (the relentless march down)**

```
FP32 → TF32 (Ampere) → FP16/BF16 → FP8 (Hopper) → FP4/FP6 (Blackwell)
```

Each halving roughly doubles throughput and halves memory. DeepSeek-v3/v4 training in FP8 is only possible because Hopper made FP8 tensor cores first-class. Blackwell's FP4 is what's driving the current inference-cost collapse.

**5. CUDA Graphs (11.x): kill launch overhead**

For tiny kernels (common in LLM decode, where each token is a sequence of small ops), per-launch CPU overhead dominates. Graphs capture a sequence once and replay it as a single submission — major win for inference.

**6. Tile programming (CUDA 13.1, 2025): the newest shift**

The most recent change is conceptually the biggest since SIMT. CUDA has, from the beginning, embraced a thread-parallel model using SIMT; with CUDA 13.0 NVIDIA laid the foundation for a complementary tile-based programming model. CUDA 13.1 launched CUDA Tile — a tile-based programming model for abstracting away specialized hardware including tensor cores, along with a Python DSL (cuTile) and a new tile IR.

The motivation: SIMT gives maximum control but requires considerable effort to write code that performs well, especially across multiple GPU architectures. Tile programming flips it — you specify chunks of data (tiles) and the computations on those tiles, and the compiler and runtime handle the element-by-element execution mapping onto hardware. It's the NumPy/Triton mental model brought natively into CUDA. Where PTX ensures portability for SIMT programs, CUDA Tile IR extends the platform with native support for tile-based programs. This is NVIDIA's direct response to Triton eating mindshare.

## What recent versions dropped (relevant to your hardware)

CUDA 13.x raised the floor: offline compilation and library support for Maxwell, Pascal, and Volta were removed in CUDA Toolkit 13.0 — you can still build for them with 12.x toolkits, but newer toolkits can't target them. CUDA 13.0 supports Turing through Blackwell, including GB200/GB300 NVL72 and the RTX 5000 series. Driver floor moved to ≥580.65.06 on Linux; for CUDA 12 you stay between 525 and under 580.

Your **RTX 4070 (Ada, SM 8.9)** is fully supported on both 12.x and 13.x — Ada sits comfortably in the Turing→Blackwell window. Your **MI300X** is a different stack entirely (ROCm/HIP), but the conceptual arc is parallel: tensor-equivalent matrix cores, low precision, async copy.

## The throughline

If you compress 20 years into one sentence: **CUDA started by exposing raw SIMT control, then progressively added specialized matmul hardware (tensor cores) and the async memory machinery to feed it, while steadily descending the precision ladder — and is now adding a higher-level tile abstraction so you stop hand-writing the feeding logic.** Triton and cuTile are the same bet: most people writing GPU kernels for ML want to think in tiles, not threads.

For your trajectory, the leverage points are: understand the **memory hierarchy + async copy** (this is 80% of why FlashAttention is fast), understand **tensor core tile shapes** (why matmuls want dims as multiples of 16/64), and watch **cuTile vs Triton** — that's where kernel-authoring is heading.

References:

- [What's New and Important in CUDA Toolkit 13.0 — NVIDIA](https://developer.nvidia.com/blog/whats-new-and-important-in-cuda-toolkit-13-0/)
- [NVIDIA CUDA 13.1 Powers Next-Gen GPU Programming with CUDA Tile — NVIDIA](https://developer.nvidia.com/blog/nvidia-cuda-13-1-powers-next-gen-gpu-programming-with-nvidia-cuda-tile-and-performance-gains/)
- [NVIDIA Announces CUDA Tile with CUDA 13.1 — TechPowerUp](https://www.techpowerup.com/343740/nvidia-announces-cuda-tile-with-cuda-13-1)
- [NVIDIA CUDA Toolkit 13.0 Is Out — ServeTheHome](https://www.servethehome.com/nvidia-cuda-toolkit-13-0-is-out/)
- [CUDA Toolkit 13.0 Release Notes — NVIDIA](https://docs.nvidia.com/cuda/archive/13.0.3/cuda-toolkit-release-notes/index.html)
