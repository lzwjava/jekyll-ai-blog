---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA vs Tensor Cores Explained
translated: false
type: note
---

**Question:** What's the difference between CUDA cores and tensor cores on a GPU like the RTX 4070?

**Answer:**

They're physically different execution units inside each Streaming Multiprocessor (SM), built for different granularities of math:

- **CUDA core** = a scalar FP32/INT32 ALU. One thread issues one fused multiply-add (FMA) per clock: `d = a * b + c` on *scalars*.
- **Tensor core** = a matrix-multiply-accumulate (MMA) unit. A whole *warp* (32 threads) cooperatively issues one instruction that computes `D = A @ B + C` on small *matrix tiles* (e.g. 16×16×16 in FP16) per instruction.

**Layout on your RTX 4070 (AD104, Ada):**

```
46 SMs
├── 128 CUDA cores / SM  → 5,888 total
└── 4 tensor cores / SM  → 184 total (4th gen)
```

**Why tensor cores are ~4x faster despite being 32x fewer**

Throughput math at ~2.48 GHz boost:

```python
# CUDA cores: 1 FMA = 2 FLOPs per core per clock
fp32 = 5888 * 2 * 2.48e9          # ≈ 29.2 TFLOPS

# Tensor cores: ~256 FP16 FLOPs per core per clock (dense)
fp16_tc = 184 * 256 * 2.48e9      # ≈ 116.8 TFLOPS
```

Each tensor core contains a hardwired grid of FP16 multipliers + an adder tree, so one instruction does the work of hundreds of scalar FMAs. It's the same trick as AVX-512 vs scalar on CPU, but for *matrices* instead of vectors, and an order of magnitude wider.

**What it looks like at the ISA level**

A CUDA core executes per-thread SASS like:

```
FFMA R4, R2, R3, R4 ;   // one scalar fp32 fma, one thread
```

A tensor core executes warp-wide PTX like:

```
mma.sync.aligned.m16n8k16.row.col.f32.f16.f16.f32
    {d0,d1,d2,d3}, {a0,a1,a2,a3}, {b0,b1}, {c0,c1,c2,c3};
```

That single `mma.sync` does a 16×8×16 matrix multiply — 2,048 multiply-adds — with the tile's fragments scattered across the 32 threads' registers. The "threads" stop being independent scalar lanes and become register storage for a collective matrix op.

**Programming them directly (WMMA API):**

```cpp
#include <mma.h>
using namespace nvcuda::wmma;

__global__ void tc_gemm(half *A, half *B, float *C) {
    fragment<matrix_a, 16, 16, 16, half, row_major> a;
    fragment<matrix_b, 16, 16, 16, half, col_major> b;
    fragment<accumulator, 16, 16, 16, float> acc;

    fill_fragment(acc, 0.0f);
    load_matrix_sync(a, A, 16);
    load_matrix_sync(b, B, 16);
    mma_sync(acc, a, b, acc);          // hits the tensor core
    store_matrix_sync(C, acc, 16, mem_row_major);
}
```

In practice you never write this — cuBLAS/cuDNN/CUTLASS do, and PyTorch routes through them.

**See it yourself on the 4070 workstation:**

```python
import torch, time

x = torch.randn(4096, 4096, device='cuda')

def bench(a, b, n=50):
    torch.cuda.synchronize(); t = time.time()
    for _ in range(n): a @ b
    torch.cuda.synchronize()
    return 2 * 4096**3 * n / (time.time() - t) / 1e12

print(f"fp32 (CUDA cores):   {bench(x, x):.1f} TFLOPS")
h = x.half()
print(f"fp16 (tensor cores): {bench(h, h):.1f} TFLOPS")
```

Expect roughly ~25 vs ~90+ TFLOPS (you won't hit peak due to memory bandwidth — AD104's 504 GB/s is often the real ceiling at this size).

**The catch — tensor cores only do matmul.** Everything else in a transformer forward pass — softmax, LayerNorm, GELU, residual adds, embedding lookups — runs on CUDA cores. This is why kernel fusion (FlashAttention fusing softmax into the MMA pipeline) matters so much: the elementwise ops on CUDA cores and the memory round-trips between them are what bottleneck you once the matmuls are on tensor cores.

One nuance relevant to your nanoGPT training: on GeForce cards (unlike H100/MI300X-class), FP16-with-FP32-accumulate runs at *half* the rate of FP16-with-FP16-accumulate. PyTorch AMP uses FP32 accumulation for stability, so your effective tensor core peak on the 4070 is ~58 TFLOPS, not ~117. BF16 has the same property. Your MI300X has no such handicap — its 1216 matrix cores do full-rate FP16/BF16 with FP32 accumulate (~1300 TFLOPS dense).
