---
audio: false
generated: true
image: false
lang: en
layout: post
title: GQA and MLA Explained
translated: false
type: note
---

**Question:** I understand attention is quadratic in context length (Q@Kᵀ matmul), which is slow and memory-hungry. Explain GQA and MLA. Also: how exactly does context length T enter the matmul dimensions, what does matrix multiplication mean at the CUDA level, how is it laid out in memory, and what's the parallel execution order?

**Answer:**

## 1. Where T appears — confirm your mental model

Your correction is right: **compute is quadratic, KV cache memory is linear** (per token), but the attention *score matrix* is quadratic. Shapes, nanoGPT-style:

```python
# B=batch, H=heads, T=seq_len, d=head_dim
q = x @ Wq   # (B, T, H*d) -> view -> (B, H, T, d)
k = x @ Wk   # (B, H, T, d)
v = x @ Wv   # (B, H, T, d)

att = q @ k.transpose(-2, -1)   # (B,H,T,d) @ (B,H,d,T) -> (B,H,T,T)  ← T² here
att = softmax(att / sqrt(d) + causal_mask)
out = att @ v                   # (B,H,T,T) @ (B,H,T,d) -> (B,H,T,d)  ← T² again
```

So T is **both** the M and N dimension of the matmul `(T×d) @ (d×T) → (T×T)`. FLOPs ≈ `2·B·H·T²·d`. Double the context → 4× attention compute, and the `(T,T)` score matrix is why naive attention OOMs (FlashAttention fixes the memory part by never materializing it, computing softmax in tiles — compute stays O(T²)).

Two regimes to keep separate:

- **Prefill**: full T×T → quadratic.
- **Decode** (one token at a time): q is `(B,H,1,d)`, K is cached `(B,H,T,d)` → each step is O(T), total generation O(T²). The bottleneck here is *memory bandwidth* — reading the KV cache every step. That's what GQA/MLA attack.

## 2. GQA — shrink the KV cache by sharing K/V across query heads

MHA: every query head has its own K and V head. GQA: **G query heads share one KV head**. Llama-3-70B: 64 query heads, 8 KV heads → KV cache is 8× smaller, decode reads 8× less memory. Quality loss is tiny because K/V representations are redundant across heads.

```python
# GQA in ~15 lines
n_head, n_kv_head, d = 32, 8, 128
group = n_head // n_kv_head  # 4 query heads per KV head

q = x @ Wq  # (B, T, n_head*d)    -> (B, n_head,    T, d)
k = x @ Wk  # (B, T, n_kv_head*d) -> (B, n_kv_head, T, d)   Wk is 4x smaller
v = x @ Wv  # (B, T, n_kv_head*d) -> (B, n_kv_head, T, d)

k = k.repeat_interleave(group, dim=1)  # broadcast to (B, n_head, T, d)
v = v.repeat_interleave(group, dim=1)  # (real kernels index, don't copy)
# ...then standard attention
```

KV cache per token per layer: MHA `2·n_head·d`, GQA `2·n_kv_head·d`. MQA is the extreme case (`n_kv_head=1`).

## 3. MLA — compress KV into a low-rank latent, cache only the latent

DeepSeek's move (V2/V3, and what you'll see in v4-family): instead of caching K and V at all, cache one small **latent vector** per token and reconstruct K/V from it on the fly.

```python
# MLA sketch (dropping RoPE details)
d_model, d_c = 5120, 512          # latent dim << 2*n_head*d

c_kv = x @ W_down                  # (B, T, d_c)   ← THIS is all you cache
k    = c_kv @ W_uk                 # (B, T, n_head*d)  reconstructed when needed
v    = c_kv @ W_uv                 # (B, T, n_head*d)
```

Cache per token: `d_c + d_rope` ≈ 512 + 64 = **576 values**, vs MHA with 128 heads × 128 dim = `2·128·128` = **32,768** — ~57× reduction. Two things make it actually work:

1. **Matrix absorption**: at inference you never materialize k. `qᵀk = qᵀ(W_uk · c) = (W_ukᵀ q)ᵀ c` — fold `W_uk` into the query projection and do attention directly against the cached latents. Same trick folds `W_uv` into the output projection.
2. **Decoupled RoPE**: RoPE is position-dependent so it can't be absorbed into a fixed matrix; MLA carries a small separate rotary sub-dimension per token (that's the +64).

Unlike GQA, MLA isn't just sharing — it's a learned low-rank bottleneck, and DeepSeek showed it *beats* MHA quality while caching far less. Good next read: DeepSeek-V2 paper §2.1, or the `mla` implementation in deepseek-ai/DeepSeek-V3's `model.py` (~100 lines).

## 4. What matmul *is*, and how CUDA does it

Definition: `C[i,j] = Σₖ A[i,k] · B[k,j]` — row i of A dotted with column j of B. That's it. `(M×K) @ (K×N) → (M×N)`, `2·M·N·K` FLOPs.

**Memory layout**: there is no 2D memory. A `(M,K)` row-major matrix is a flat array where `A[i][k]` lives at `A[i*K + k]`. Row elements are contiguous; column elements are strided by K. This is why reading B column-wise is slow and why transposes/tiling matter.

Naive kernel — one thread per output element:

```cuda
__global__ void matmul_naive(const float* A, const float* B, float* C,
                             int M, int N, int K) {
    int i = blockIdx.y * blockDim.y + threadIdx.y;  // row
    int j = blockIdx.x * blockDim.x + threadIdx.x;  // col
    if (i >= M || j >= N) return;
    float acc = 0.0f;
    for (int k = 0; k < K; k++)
        acc += A[i*K + k] * B[k*N + j];   // B access: stride N -> bad reuse
    C[i*N + j] = acc;
}
```

This works but each element of A and B gets re-fetched from global memory ~N or ~M times. Arithmetic intensity is terrible → memory-bound. Fix: **tiling in shared memory**:

```cuda
#define TILE 32
__global__ void matmul_tiled(const float* A, const float* B, float* C,
                             int M, int N, int K) {
    __shared__ float As[TILE][TILE], Bs[TILE][TILE];
    int i = blockIdx.y * TILE + threadIdx.y;
    int j = blockIdx.x * TILE + threadIdx.x;
    float acc = 0.0f;
    for (int t = 0; t < K; t += TILE) {
        // cooperative load: 32x32 threads each grab one element.
        // threadIdx.x varies fastest -> consecutive threads read consecutive
        // addresses -> one coalesced 128-byte transaction per warp.
        As[threadIdx.y][threadIdx.x] = A[i*K + (t + threadIdx.x)];
        Bs[threadIdx.y][threadIdx.x] = B[(t + threadIdx.y)*N + j];
        __syncthreads();                       // wait for tile to land
        for (int k = 0; k < TILE; k++)
            acc += As[threadIdx.y][k] * Bs[k][threadIdx.x];  // SRAM, ~fast
        __syncthreads();
    }
    C[i*N + j] = acc;
}
```

Each global-memory value is now reused TILE(=32) times from shared memory. Real kernels (cuBLAS/CUTLASS) go further: each thread computes an 8×8 register tile, warps drive tensor cores on 16×16×16 fragments, double-buffered async loads. But tiling is the core idea — and it's the same idea FlashAttention applies to the `(T,T)` score matrix.

**Parallel execution order — the part people get wrong:**

- **Across blocks**: order is *undefined*. The GPU schedules blocks onto SMs in whatever order; you cannot assume block 0 runs before block 5. Correctness must not depend on it. Blocks can only sync via kernel boundaries (or cooperative groups).
- **Within a block**: `__syncthreads()` is your only ordering barrier.
- **Within a warp**: 32 threads execute in lockstep (SIMT).
- **Within one thread**: the k-loop accumulation is sequential, left to right, in that thread's register. So a basic tiled matmul is deterministic. Nondeterminism appears when a *reduction is split across threads* — split-K matmuls with `atomicAdd`, some backward kernels — because float addition isn't associative: `(a+b)+c ≠ a+(b+c)`. That's why `torch.use_deterministic_algorithms(True)` disables certain kernels.

## 5. Try it on your 4070

```bash
nvcc -O3 matmul.cu -o matmul && ./matmul          # your kernels
python -c "import torch; ..."                      # vs torch.matmul (cuBLAS)
ncu --set full ./matmul                            # Nsight Compute: see coalescing, occupancy
```

Benchmark naive → tiled → cuBLAS at M=N=K=4096. Expect roughly ~300 GFLOPs → ~3 TFLOPs → ~25+ TFLOPs (fp32) on the 4070. Watching that 100× gap close is the fastest way to internalize why memory layout is the whole game. Then read the FlashAttention paper — it'll feel obvious.

**References:**

- [DeepSeek-V2: MLA paper](https://arxiv.org/abs/2405.04434)
- [GQA paper (Ainslie et al.)](https://arxiv.org/abs/2305.13245)
- [Simon Boehm — How to Optimize a CUDA Matmul Kernel](https://siboehm.com/articles/22/CUDA-MMM)
- [FlashAttention](https://arxiv.org/abs/2205.14135)
- [karpathy/llm.c — attention & matmul kernels in plain CUDA](https://github.com/karpathy/llm.c)
