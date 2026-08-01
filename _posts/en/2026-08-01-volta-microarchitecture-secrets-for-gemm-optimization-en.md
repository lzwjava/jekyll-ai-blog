---
audio: false
generated: true
image: false
lang: en
layout: post
title: Volta Microarchitecture Secrets for GEMM Optimization
translated: false
type: note
---

Question: What's this Citadel paper (Jia, Maggioni, Staiger, Scarpazza 2018) about, and why does Aleksa Gordic cite it in a matmul-optimization blog post?

Answer:

It's a reverse-engineering report on the V100 (Volta) microarchitecture — no NVIDIA whitepaper gives you this level of detail, so the authors got it via microbenchmarks + SASS disassembly. Gordic cites it because writing a fast GEMM kernel (the whole point of his blog) requires exactly the stuff this paper exposes: register bank layout, instruction latency, and tensor core data movement — none of which is documented publicly.

**1. The motivating hook: register bank conflicts cost you real GFLOPS**

Volta divides its register file into 2 banks of 64 bits each, unlike the 4-bank 32-bit design on Pascal/Maxwell. An FFMA instruction can only read 64 bits per bank per cycle, so if all three source registers land in the same bank, the access serializes. Their motivational example is a naive register-blocked 8×8 outer-product GEMM inner loop:

```cuda
__shared__ float shr_A[8*512], shr_B[8*512];
float reg_A[8], reg_B[8], reg_C[64];
for (int k=0; k<512; k++) {
  for (int i=0;i<8;i++){ reg_A[i]=shr_A[i+k*8]; reg_B[i]=shr_B[i+k*8]; }
  for (int i=0;i<8;i++)
    for (int j=0;j<8;j++)
      reg_C[i*8+j] += reg_A[i]*reg_B[j];
}
```

NVCC 9.0's generated register mapping has bank conflicts on this pattern. Hand-patching the SASS to eliminate the conflicts and exploit register-reuse caches took performance from 132.05 to 152.43 GFLOPS/SM per warp of 128 threads — a +15.4% gain purely from register allocation. This is the "there's free performance on the table that cuBLAS-only-internal-teams know about" thesis of the whole paper.

**2. Memory hierarchy — the numbers you actually need for tiling decisions**

| Level | V100 (GV100) | Notes |
| --- | --- | --- |
| L1 data / shared mem (unified) | 32–128 KiB, hit latency 28 cyc | vs 82 cyc on Pascal — this is the big Volta win |
| L2 | 6,144 KiB, ~193 cyc, 2155 GB/s | 16-way, unified data/inst/const |
| Global (HBM2) | 900 GB/s theoretical, ~750 GB/s measured (83.3% efficiency) | best ratio of any gen they tested |
| Registers | 2 banks × 64-bit | bank = reg_index % 2 |
| Shared mem | up to 96 KiB/SM, 19-cycle no-conflict latency | 32 banks × 4B |

The paper measures global memory access latency with a pointer-chase (p-chase) technique: 28 cycles for an L1 hit, 193 for L1-miss/L2-hit, 375 for L2-miss/TLB-hit, and 1029 cycles for a full miss (L2 + TLB miss).

**3. How they actually microbenchmark (the method, code-first)**

Their latency-measurement trick, generalizable to any GPU you don't have docs for:

```
// fixed-latency instruction A:
// bracket with dependent instruction B, shrink A's "stall cycles"
// control-word field until B's result becomes wrong.
// the last correct stall count = A's true latency.

// variable-latency instruction A (loads, atomics):
// pair with known-latency B, force an artificial
// read/write dependency via control-word barriers,
// measure with CS2R (clock-to-register) instruction pair,
// subtract B's known latency.
```

Most Volta integer/FP32 instructions (IADD3, FFMA, FADD, ISETP...) have 4-cycle latency vs 6 on Pascal; DFMA/DADD are 8 cycles; half-precision HFMA2 is 6 cycles — down from the old FMA latency of 6, which is why Volta's scheduler-to-core ratio matters (it grew from 1:48 on Kepler to 1:16, letting instruction throughput scale with the shorter latency).

**4. Tensor cores — this is the part most relevant to modern matmul work**

A single wmma::mma_sync call compiles to 4 sets of 4 HMMA instructions each (16 total), operating on a 16×16×16 half-precision tile per warp. At runtime the 32 threads split into 8 groups of 4 (group = thread_id/4), each group computing a 4×8 chunk of the 16×16 output, with different HMMA sets contributing different accumulation steps. This is the actual data-parallel decomposition inside `mma_sync` that no NVIDIA doc shows you — it's why people wrote CUTLASS instead of hand-rolling WMMA. Measured tensor-core throughput hit 90.2% of theoretical peak, vs near-100% achievable in FP32/FP64 — the paper's own explanation is the register-loading and thread-mapping overhead they diagram in Fig 4.2–4.7.

**Why Gordic pulls this in:** his matmul blog is presumably walking through register-tiled / warp-tiled GEMM kernels (the CUTLASS-style hierarchy: block tile → warp tile → thread tile → instruction). This paper is the primary source for *why* those tile sizes and register mappings are chosen the way they are on Volta specifically — bank width, reuse cache, HMMA group semantics. It's essentially the "ground truth" citation for anyone building a from-scratch GEMM instead of trusting cuBLAS as a black box.

References:

- [Dissecting the NVIDIA Volta GPU Architecture via Microbenchmarking (arXiv:1804.06826)](https://arxiv.org/abs/1804.06826)
- [Full text PDF](https://arxiv.org/pdf/1804.06826)
- [Aleksa Gordic's matmul blog](https://www.aleksagordic.com/blog/matmul)
