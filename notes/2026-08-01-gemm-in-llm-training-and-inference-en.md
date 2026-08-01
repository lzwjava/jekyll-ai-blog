---
audio: false
generated: true
image: false
lang: en
layout: post
title: GEMM in LLM Training and Inference
translated: false
type: note
---

Question: What is GEMM and where does it show up in LLM training/inference?

Answer:

GEMM = **General Matrix Multiply**: `C = alpha * A@B + beta * C`, shapes `(M,K) @ (K,N) -> (M,N)`. It's the BLAS-3 primitive (cuBLAS/cutlass/rocBLAS) everything else is built on.

**Where it lives in a transformer layer:**

Every `nn.Linear` is a GEMM. Per layer:
- QKVO projections: 4 GEMMs, each `(seq, d_model) @ (d_model, d_model)`
- MLP up/down: 2 GEMMs, `(seq, d_model) @ (d_model, 4*d_model)` and back
- Attention scores `Q@K^T` and `attn@V`: batched GEMM over heads

This is why the Kaplan/Chinchilla `C ≈ 6ND` FLOPs approximation exists — GEMM FLOPs (`2*M*N*K` each) dominate total compute; softmax/layernorm/RoPE are FLOP-negligible, just latency/memory noise.

```python
# naive GEMM, O(M*N*K)
def gemm_naive(A, B):
    M, K = A.shape
    K2, N = B.shape
    C = [[0.0]*N for _ in range(M)]
    for i in range(M):
        for j in range(N):
            s = 0.0
            for k in range(K):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C

flops = lambda M,N,K: 2*M*N*K  # multiply-add = 2 flops
```

Real GEMM kernels tile A/B into shared-memory/register blocks matched to tensor core shapes (e.g. 16x16x16 for fp16 on Ampere+) to maximize arithmetic intensity and hit peak TFLOPS. That's what cuBLAS/cutlass/Triton do — the naive triple loop above is ~1000x slower than a tiled tensor-core kernel.

**The insight that actually matters for you (inference/agent serving):** GEMM assumes `M > 1`. During autoregressive **decode** with batch size 1, you're doing `(1, d) @ (d, d)` — that's a **GEMV** (matrix-vector), not GEMM. GEMV is memory-bandwidth bound (you load the whole weight matrix per token, do almost no reuse), while GEMM is compute-bound (reuse rows/cols across the M and N dims). This is *the* reason continuous batching / vLLM-style serving exists: batching decode requests together turns many small GEMVs into one big GEMM, moving you from bandwidth-bound to compute-bound and multiplying throughput.

Rough arithmetic intensity check:
```
AI = FLOPs / bytes_moved
GEMM (M,K,N large):  AI ~ O(min(M,N,K))  -> compute bound
GEMV (M=1):          AI ~ O(1)           -> memory bound, GPU starves
```

This is also why **MFU (Model FLOPs Utilization)** — actual FLOPs/s achieved divided by GPU peak FLOPs/s — is the metric you track when training your 760M GPT-2 on MI300X. Low MFU almost always means your GEMMs aren't shaped/batched to be compute-bound (bad tile sizes, small batch, unfused ops causing extra memory traffic between GEMMs).

References:
- [Data Movement Is All You Need (GEMM/memory-bound analysis)](https://arxiv.org/abs/2007.00072)
- [NVIDIA cuBLAS GEMM performance guide](https://docs.nvidia.com/cuda/cublas/)
- [vLLM PagedAttention paper (continuous batching motivation)](https://arxiv.org/abs/2309.06180)
