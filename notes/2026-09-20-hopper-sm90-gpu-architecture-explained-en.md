---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hopper SM90 GPU Architecture Explained
translated: false
type: note
---

Question: **Intro to NVIDIA Hopper (SM90) GPUs**

Answer:

NVIDIA Hopper is the **H100-generation GPU architecture**, introduced in 2022. For an engineer coming from CUDA / model-training work, the useful mental model is:

> **SM90 = Ampere SM80 + much more aggressive matrix compute + Tensor Memory Accelerator + asynchronous execution + FP8 + Transformer Engine.**

The flagship Hopper GPUs are **H100** (SXM5 / PCIe), with **H200** later adding HBM3e capacity/bandwidth while retaining the Hopper architecture.

![Image](https://images.openai.com/static-rsc-4/i2ChtU_Ei-R8cC7_jX7aV5UqmkVtCFubgqhCvYSMgLv2YNF-tFkcb2rcpuccCppiqBI9G_fob_Vz3v-Ra0TyWAbd6a5ofX8yp-5Ahy-lLm9q3Wc1GFX1zpD_XPkUChlSEUzF5mTD9GVwzDPjY8xqQOHfOXEMefMXCnt_yqk4jefg7f83Pzv3Am185v_hbOBp?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/LBGpZ6_9RieiVFziH2PdWcI1T6qu_0ySb-l-neyv-c7azYl6yomciGA1HtIaEfCWQAzhv1ULZaU51S23q5cSXSPPzE3KPRslJ8RyEw9ab5JuB3Hbg5zLLbXBg1GWHtMroteWV34W91p7Rp1YBEHqkr-bJnOBzXS8CG4Nwi_yZRUokR-0ACg8MFN3gPDRP_jn?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/L3xvT4LEQDY8-yVCzfpRKrY3qvJAHJYLHjt--2aykSHjVjMqkytuLUg2FH-_DqQlvSJT9DSYJ_kkb_N_IGDze-SNFBBSk4Vgkb26lt1hCJv33tNAfhsPqg-QEO27cvO2zUtMvKup4UwmFco47VvLFCGMl-lyaDXx27cJH_K6Ke6xc6pCJiYpS1UUipx5qj-e?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/DuW_N3O6qxuvSVaQeaEiYXXbbXh9gMwmc8Gm8MayhThrar8DCcirQ-qORw9PVEaxiPkViWkUaCb_j7_dYHKdx6Fl-UGZlzFvXseWtZ0yCxCLgCPpgISC7bBY_l8vxrH8Vue-ki_ODZTDpuArt60O9euuMl6e3me6VqaWPPDk86pqQ_3US_N74pLKTewbqps7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/EiOVEGRtg5SyASSNweD6qMlN62GfpvqcEJgNqznVYJ7Icybn6cBY54YJs8m89Y6Fjwzo6XMuQ5BrJLuCNSlHuhRpWlXZqGDeP7B_Dc2OJg4Fd51vj25LyCpSe3CORF9sflZXZXcRIGrShETU_IXtOolyhFsn6PIcCdoEcfCOvagK7pSjOIBqvaTrqvvYbpGV?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/tZUhItHBEHnbdrZREfVcJ0Z4wo6caI6wHJoeSNnHTkYqLaR50Q-Y7nUtGjbvRIywOZ81Kq4sMSEsPCBDp_OgTP-H_swHcGSnpKW1RNRiL5Mw4Z5sCHaMxBUwK3PCVJcUfsQENNIUjnSmHen4aqwtaibGos63FMR7bdt4GYgrb1u3VVvADExGWL65gepBHxHB?purpose=fullsize)

### 1. The hierarchy

The first thing to internalize is the hardware hierarchy:

```text
H100 GPU
│
├── 8 GPCs
│   │
│   ├── TPCs
│   │   └── SM
│   │       ├── CUDA cores
│   │       ├── Tensor Cores
│   │       ├── registers
│   │       ├── shared memory / L1
│   │       └── special-function / load-store units
│   │
│   └── ...
│
├── L2 cache
│
└── HBM
```

The key unit for CUDA programming is still the **SM (Streaming Multiprocessor)**.

On Hopper, this is **SM90**.

A CUDA kernel gets decomposed into thread blocks, and blocks are scheduled onto SMs:

```text
kernel
  ↓
grid
  ↓
thread blocks
  ↓
SM90 ── SM90 ── SM90 ── ...
  ↓
warps
  ↓
32 threads
```

The programming model hasn't fundamentally changed:

```cpp
__global__ void saxpy(float *x, float *y) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    y[i] = 2.0f * x[i] + y[i];
}
```

But Hopper dramatically changes **how much work can happen asynchronously inside one SM**.

---

## 2. H100's basic numbers

For H100 SXM:

| Property              | Hopper H100 |
| --------------------- | ----------: |
| Architecture          |      Hopper |
| Compute capability    |     **9.0** |
| SMs                   |     **132** |
| CUDA cores            |  **16,896** |
| Tensor Cores          |     **528** |
| HBM                   |        HBM3 |
| HBM capacity          |       80 GB |
| HBM bandwidth         |  ~3.35 TB/s |
| L2                    |       50 MB |
| FP8 Tensor            |         Yes |
| Transformer Engine    |         Yes |
| TMA                   |         Yes |
| Thread-block clusters |         Yes |

One important distinction:

**132 SMs ≠ 132 independent GPUs.**

Each SM is a fairly autonomous execution engine, and the GPU scheduler distributes blocks across them.

---

# 3. What's actually inside an SM90?

A useful simplified picture:

```text
                    SM90
 ┌──────────────────────────────────────────────┐
 │                                              │
 │  Warp schedulers / dispatch                  │
 │        │                                     │
 │        ├── CUDA cores                        │
 │        ├── Tensor Cores                      │
 │        ├── Load/Store                        │
 │        └── SFU                               │
 │                                              │
 │  Register File                               │
 │                                              │
 │  Shared Memory / L1                          │
 │                                              │
 │  Tensor Memory Accelerator (TMA)             │
 │                                              │
 │  Async execution machinery                   │
 │                                              │
 └──────────────────────────────────────────────┘
```

The most important Hopper additions are **Tensor Cores, TMA, and asynchronous execution**.

---

# 4. Tensor Cores are the real compute engine for ML

A CUDA core executes scalar/vector-ish arithmetic.

A Tensor Core executes **matrix multiply-accumulate**.

Conceptually:

```text
D = A @ B + C
```

For example:

```text
A: [M × K]
B: [K × N]
C: [M × N]

Tensor Core
     ↓
D: [M × N]
```

For transformer training/inference, this maps almost directly onto:

```text
Q @ Kᵀ
attention @ V
X @ W
W_up @ X
W_down @ X
```

That's why Tensor Core performance matters vastly more than raw CUDA-core count for LLMs.

---

# 5. Hopper's killer feature: FP8

Hopper introduced first-class **FP8 Tensor Core** execution.

The common FP8 formats are:

```text
E4M3
E5M2
```

Very roughly:

```text
FP32
 ↓
FP16 / BF16
 ↓
FP8
```

You sacrifice numerical precision/range for dramatically cheaper matrix computation and lower memory traffic.

For LLM workloads:

```text
weights / activations
        ↓
      FP8
        ↓
Tensor Core GEMM
        ↓
 higher throughput
```

The Hopper **Transformer Engine** dynamically helps choose numerical formats and scaling strategies for transformer workloads.

This is one of the architectural reasons H100 became so important for LLM training.

---

# 6. Hopper's other huge feature: TMA

If you're writing serious CUDA kernels, **TMA — Tensor Memory Accelerator — is probably the most important Hopper-specific feature to learn.**

Before Hopper, a common GEMM strategy looked like:

```text
global memory
     ↓
many threads perform loads
     ↓
registers
     ↓
shared memory
     ↓
Tensor Core
```

The threads themselves do a lot of address calculation and movement.

Hopper lets you describe a multidimensional tensor transfer and have dedicated hardware perform the movement:

```text
              TMA
global ─────────────────→ shared memory
         tensor transfer
```

Instead of every thread doing:

```cpp
for (...) {
    shared[...] = global[...];
}
```

you can essentially say:

```text
"Move this 2D/3D tensor region
 from global memory to shared memory."
```

and let the TMA machinery do it asynchronously.

This matters because a modern GEMM wants to overlap:

```text
        COMPUTE
          │
          ▼
       TensorCore
          │
          │
   ┌──────┴──────┐
   │             │
 LOAD tile    LOAD tile
   │             │
   └──────┬──────┘
          │
       next tile
```

while the Tensor Cores are still computing.

---

# 7. Hopper is fundamentally about asynchronous pipelines

A useful mental model is:

```text
          time →

Load tile 0 ────────┐
                    │
Compute tile 0      ├──────────
                    │
Load tile 1         └───────┐
                            │
Compute tile 1               ├──────────
                            │
Load tile 2                  └───────┐
                                     │
Compute tile 2                        ├──────
```

Instead of:

```text
LOAD
WAIT
COMPUTE
WAIT
LOAD
WAIT
COMPUTE
```

you want:

```text
LOAD ────────────────
      COMPUTE ───────────────
            LOAD ────────────────
                  COMPUTE ───────────
```

Hopper gives you substantially better primitives for constructing this pipeline.

Important pieces include:

* `cp.async`-style asynchronous memory movement
* **TMA**
* `mbarrier`
* asynchronous transaction management
* Tensor Core pipelines
* thread-block clusters

---

# 8. Thread-block clusters

Hopper also extends the execution hierarchy.

Previously, the useful mental model was:

```text
Grid
 └── Thread blocks
      └── Warps
           └── Threads
```

Hopper adds:

```text
Grid
 └── Cluster
      ├── Thread Block
      ├── Thread Block
      ├── Thread Block
      └── Thread Block
```

Blocks inside a cluster can cooperate more closely and use distributed shared-memory mechanisms.

This is useful when one computation needs cooperation beyond a single SM.

For many everyday CUDA kernels, you won't touch this.

For high-performance GEMM / attention / MoE kernels, it's increasingly relevant.

---

# 9. Memory hierarchy

For LLM kernels, think about memory like this:

```text
                    HBM
                 ~3.35 TB/s
                     │
                     ▼
                    L2
                 50 MB
                     │
                     ▼
              L1 / Shared
               per SM
                     │
                     ▼
                 Registers
```

Latency generally decreases as you move down the hierarchy, while capacity decreases too.

The fundamental optimization problem is:

> **Keep the expensive Tensor Cores busy while hiding HBM latency.**

For example, a naive implementation:

```text
HBM → Tensor Core → HBM
```

may spend much of its time waiting for memory.

A good implementation instead tries to do:

```text
                  ┌───────────────┐
HBM → shared ────→│ Tensor Cores  │
                  └───────────────┘
                       ↑
                  next tile loading
```

with the two sides running concurrently.

---

# 10. Why H100 is so good for transformers

Take a transformer linear layer:

```python
Y = X @ W
```

Suppose:

```text
X = [batch × sequence, hidden]
W = [hidden, 4 × hidden]
```

This is a huge GEMM.

Hopper can execute it approximately as:

```text
HBM
 │
 │ TMA
 ▼
Shared Memory
 │
 │
 ▼
Tensor Cores
 │
 │ FP8/BF16/FP16
 ▼
Accumulator
 │
 ▼
Output
```

The entire architecture is heavily optimized around making this pipeline efficient.

That's why frameworks like PyTorch, cuBLAS, CUTLASS, FlashAttention, and Transformer Engine are so important on Hopper: **the hardware is powerful enough that memory movement and kernel scheduling become first-order problems.**

---

# 11. SM90 vs SM80

If you've worked with A100, the clean comparison is:

```text
A100 / Ampere
SM80
 │
 ├── Tensor Cores
 ├── BF16
 ├── FP16
 └── cp.async
```

versus:

```text
H100 / Hopper
SM90
 │
 ├── much stronger Tensor Cores
 ├── FP8
 ├── Transformer Engine
 ├── TMA
 ├── mbarrier
 ├── thread-block clusters
 └── more sophisticated async execution
```

So don't think of Hopper merely as:

> "A100 but faster."

A better mental model is:

> **Hopper changes the kernel programming model toward explicitly pipelined asynchronous tensor computation.**

---

# 12. If you're writing CUDA on H100

Start with:

```bash
nvcc -arch=sm_90 kernel.cu
```

or, for PTX that can be JITed for Hopper:

```bash
nvcc -arch=compute_90 kernel.cu
```

Then inspect your kernel with:

```bash
ncu ./your_program
```

The questions I'd ask are:

```text
1. How much HBM bandwidth am I using?
2. How much Tensor Core utilization?
3. How much occupancy?
4. Register pressure?
5. Shared-memory bandwidth?
6. Are loads overlapping compute?
7. Are Tensor Cores stalled on memory?
8. How much instruction-level / warp-level parallelism?
```

For serious optimization, **Nsight Compute** becomes almost as important as the CUDA source itself.

---

# 13. The simplest Hopper mental model

If you remember only this:

```text
                    H100 / SM90

             ┌──────────────────────┐
             │       HBM3            │
             └──────────┬───────────┘
                        │
                       TMA
                        │
                        ▼
             ┌──────────────────────┐
             │   Shared Memory/L1   │
             └──────────┬───────────┘
                        │
                 async pipeline
                        │
                        ▼
             ┌──────────────────────┐
             │    Tensor Cores      │
             │                      │
             │   FP8 / FP16 / BF16  │
             │        GEMM          │
             └──────────┬───────────┘
                        │
                        ▼
                   Registers
```

**Hopper is a machine for feeding Tensor Cores.**

The performance game is:

```text
HBM
 ↓
move tiles efficiently
 ↓
shared memory
 ↓
feed Tensor Cores continuously
 ↓
overlap next memory transfer with current compute
 ↓
repeat
```

That's the foundation behind high-performance H100 kernels such as **FlashAttention, fused MLPs, MoE kernels, and optimized GEMMs**.

If you're coming from training large models, I'd learn Hopper in this order:

```text
SM90 execution model
    ↓
Tensor Core MMA
    ↓
shared memory + register tiling
    ↓
async pipeline
    ↓
TMA
    ↓
mbarrier
    ↓
warp-specialized kernels
    ↓
thread-block clusters
    ↓
CUTLASS / CuTe
    ↓
FlashAttention / Transformer Engine internals
```

That path gets you from **"I know CUDA" → "I can reason about why an H100 kernel is fast."**

I can also build a **minimal SM90 GEMM from raw CUDA → TMA → Tensor Core MMA**, showing the actual data movement and instruction-level pipeline.
