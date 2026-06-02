---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: FlashAttention Solves Transformers Memory Bottleneck
translated: false
type: note
---

### Background: The Challenges of Standard Attention in Transformers

Transformers, the backbone of models like GPT and BERT, rely heavily on the self-attention mechanism to process sequences. In self-attention, given input sequences represented as query matrix \\(Q\\), key matrix \\(K\\), and value matrix \\(V\\) (each of shape \\(N \times d\\), where \\(N\\) is the sequence length and \\(d\\) is the head dimension, typically 64-128), the attention output \\(O\\) is computed as:

\\[
S = QK^T \in \mathbb{R}^{N \times N}, \quad P = \softmax(S) \in \mathbb{R}^{N \times N}, \quad O = PV \in \mathbb{R}^{N \times d},
\\]

where \\(\softmax\\) is applied row-wise, and \\(S\\) is often scaled by \\(\tau = 1 / \sqrt{d}\\) for stability. Additional operations like causal masking (for autoregressive models) and dropout are common.

This formulation is elegant but computationally expensive. The intermediate matrices \\(S\\) and \\(P\\) are \\(N \times N\\), leading to **quadratic time and memory complexity** \\(O(N^2)\\) in sequence length \\(N\\). For long contexts (e.g., \\(N = 4096\\) in GPT-2 or up to 128k in modern LLMs), this becomes a severe bottleneck:

- **Memory Hunger**: On GPUs, high-bandwidth memory (HBM) is the primary storage, but materializing \\(S\\) and \\(P\\) can exceed available HBM (e.g., 40-80 GB on A100/H100). At \\(N=4096\\), \\(d=64\\), this alone consumes ~1-2 GB just for intermediates, plus inputs/outputs/activations, often causing out-of-memory (OOM) errors.
- **Speed Limitations**: Attention is memory-bound, not compute-bound. Modern GPUs (e.g., NVIDIA A100) have ~1.5 TB/s HBM bandwidth but ~19 TFLOPS compute—yet operations like softmax require reading/writing the full \\(N^2\\) matrix multiple times (e.g., 4-6 HBM accesses per element in forward/backward passes). This results in wall-clock times scaling quadratically: e.g., forward pass ~36 ms at \\(N=4096\\) in PyTorch, backward ~88 ms.
- **Training/Generation Barriers**: During training, gradients require storing \\(P\\) for the backward pass, doubling memory. For inference, long contexts (e.g., 64k tokens) are infeasible without approximations like sparse attention or low-rank methods (e.g., Reformer, Linformer), which trade exactness for efficiency but often underperform due to ignoring I/O costs.

FlashAttention (introduced in 2022 by Tri Dao et al.) addresses these by rethinking the algorithm to be **I/O-aware**, leveraging GPU memory hierarchy (fast SRAM ~20 MB vs. slow HBM) without approximations.

### Core Ideas: Tiling, Kernel Fusion, and Online Softmax

FlashAttention computes **exact** attention (no approximations) by:

1. **Tiling**: Instead of materializing the full \\(N \times N\\) matrices, it divides \\(Q, K, V\\) into small blocks that fit in SRAM. \\(Q\\) is split into \\(T_r = \lceil N / B_r \rceil\\) row-blocks of size \\(B_r \times d\\) (e.g., \\(B_r \approx 64-256\\)), and \\(K, V\\) into \\(T_c = \lceil N / B_c \rceil\\) column-blocks of size \\(B_c \times d\\) (e.g., \\(B_c \approx 128-1024\\)). Block sizes are chosen dynamically based on SRAM capacity \\(M\\) (e.g., \\(B_c \approx M / (4d)\\)) to maximize reuse.

2. **Kernel Fusion**: All operations (matmul for \\(S\\), masking, softmax, dropout, matmul for \\(O\\)) are fused into a single CUDA kernel. This avoids writing intermediates to HBM, reducing I/O by ~50-70%. The kernel loads blocks from HBM to SRAM, computes on-chip, and writes only partial sums back—e.g., one HBM read/write per block instead of per element.

3. **Online Softmax with Statistics**: Softmax can't be computed partially without the full row, so FlashAttention uses an **associative decomposition** for incremental computation. For a row split into blocks \\(x = [x^{(1)}; x^{(2)}]\\), track running statistics:
   - Row-max \\(m_i = \max_j S_{ij}\\),
   - Row-sum of exponentials \\(\ell_i = \sum_j \exp(S_{ij} - m_i)\\).

   Updating for a new block \\(x^{(t)}\\) with local stats \\(\tilde{m}_t, \tilde{\ell}_t\\):
   \\[
   m_i^{\new} = \max(m_i, \tilde{m}_t), \quad \ell_i^{\new} = e^{m_i - m_i^{\new}} \ell_i + e^{\tilde{m}_t - m_i^{\new}} \tilde{\ell}_t.
   \\]
   The partial softmax is then \\(\tilde{P}_{ij} = \exp(S_{ij} - m_i^{\new})\\), and output accumulates as \\(O_i \leftarrow \frac{\ell_i}{\ell_i^{\new}} e^{m_i - m_i^{\new}} O_i + \frac{\tilde{\ell}_t}{\ell_i^{\new}} e^{\tilde{m}_t - m_i^{\new}} \tilde{P}_{ij} V_j\\).

   This is numerically stable (matches fused softmax) and exact, as proven inductively: after all blocks, \\(O = \softmax(S) V\\).

These ideas reduce **memory to \\(O(N)\\)** (inputs + output + \\(O(N)\\) stats like \\(m, \ell\\)) and **HBM accesses to \\(O(N^2 d / M)\\)**—sub-quadratic, as each \\(K/V\\) element is read once, and \\(Q/O\\) is read \\(T_c \approx N d / M\\) times.

### Forward Pass: Block-by-Block Computation

The forward pass (pseudocode in the paper's Algorithm 2) iterates over column-blocks of \\(K, V\\):

- Initialize \\(O = 0^{N \times d}\\), \\(m = -\infty^N\\), \\(\ell = 0^N\\) in HBM.
- For each column-block \\(j = 1\\) to \\(T_c\\):
  - Load \\(K_j, V_j\\) to SRAM (reuse across rows).
  - For each row-block \\(i = 1\\) to \\(T_r\\):
    - Load \\(Q_i, O_i, m_i, \ell_i\\) to SRAM.
    - Compute local \\(S_{ij} = \tau Q_i K_j^T\\) (\\(B_r \times B_c\\)).
    - Mask: \\(S_{ij}^{\masked} = \mask(S_{ij})\\) (e.g., causal: lower triangle to \\(-\infty\\)).
    - Local softmax stats: \\(\tilde{m}_{ij} = \rowmax(S_{ij}^{\masked})\\), \\(\tilde{P}_{ij} = \exp(S_{ij}^{\masked} - \tilde{m}_{ij})\\), \\(\tilde{\ell}_{ij} = \rowsum(\tilde{P}_{ij})\\).
    - Update global stats and output using the formulas above, applying dropout to \\(\tilde{P}_{ij}\\).
    - Write updated \\(O_i, m_i, \ell_i\\) to HBM.

This fuses everything: total FLOPs remain \\(O(N^2 d)\\), but I/O drops dramatically (e.g., 9x fewer accesses than standard). For causal attention, masking is cheap (vectorized). Dropout uses a shared RNG state \\(R\\) saved for backward.

### Backward Pass: Gradient Computation via Recomputation

The backward pass (Algorithm 4) is trickier, as gradients depend on \\(P\\):

\\[
dP = dO \cdot V^T, \quad dS = P \odot (dP - \rowsum(dO \odot O)), \quad dQ = dS \cdot K, \quad dK = Q^T \cdot dS, \quad dV = P^T \cdot dO.
\\]

Storing \\(P\\) would be \\(O(N^2)\\), so FlashAttention **recomputes blocks on-the-fly** (selective recomputation, like checkpointing but tiled):

- Iterate similarly: for each \\(j\\), load \\(K_j, V_j\\); initialize local \\(dK_j, dV_j = 0\\).
- For each \\(i\\): recompute \\(S_{ij}, P_{ij}\\) using saved \\(m_i, \ell_i\\); regenerate dropout mask from \\(R\\).
- Compute local gradients: \\(dV_j += P_{ij}^{dropped^T} dO_i\\), \\(dP_{ij} = dO_i V_j^T \odot Z_{ij}\\) (dropout mask), \\(dS_{ij} = P_{ij} \odot (dP_{ij} - D_i)\\) where \\(D_i = \rowsum(dO_i \odot O_i)\\).
- Accumulate \\(dQ_i += \tau dS_{ij} K_j\\), \\(dK_j += \tau Q_i^T dS_{ij}\\).

This uses another \\(O(N^2 d)\\) FLOPs but only \\(O(N)\\) extra memory (no \\(P\\) storage). Total forward + backward: ~2-3x the FLOPs of standard but 2-4x faster due to I/O savings.

### I/O-Awareness and GPU Optimizations

GPUs have a hierarchy: registers/SRAM (fast, small) >> HBM (slow, large). Standard attention thrashes HBM with \\(\Theta(N^2)\\) accesses per pass. FlashAttention's tiling ensures:
- \\(K, V\\) loaded once (\\(O(N d)\\)).
- \\(Q, O\\) loaded \\(T_c \approx N / B_c \approx N d / M\\) times (\\(O(N^2 d / M)\\)).
- Lower bound: No exact algorithm beats \\(\Omega(N^2 d^2 / M)\\) for mid-range \\(M\\).

Empirical: On A100, HBM stalls dominate runtime; FlashAttention reduces them by 50-80%, hitting compute-bound regime. It supports block-sparsity (skip zero-mask blocks) for even more gains (2-4x over dense).

### Benefits: Speed, Memory, and Downstream Impact

- **Memory**: Linear \\(O(N d)\\), enabling 64k+ sequences on single GPUs (vs. 2k-4k standard). E.g., 13 GB at \\(N=65k\\) vs. 200+ GB standard.
- **Speed**: 2-4x end-to-end on GPT/BERT training; up to 7x on raw attention. E.g., combined fwd/bwd: 0.43 ms at \\(N=128\\) to 9s at \\(N=65k\\) (vs. PyTorch OOM).
- **Quality**: Exact, so no perplexity drop. Enables longer contexts: 0.7-point perplexity gain on GPT-2 at 4x length; state-of-the-art on long-doc tasks (e.g., 63% on Path-256 at 64k seqs).
- **Extensions**: FlashAttention-2 (2023) adds better parallelism (up to 2x faster); FlashAttention-3 (2024) uses asynchrony/low-precision for H100 (50% faster).

### PyTorch Integration: Seamless Usage

PyTorch 2.0+ integrates FlashAttention natively via `torch.nn.functional.scaled_dot_product_attention(q, k, v)`, which auto-dispatches to the fused kernel if conditions met (e.g., contiguous tensors, supported dtypes). No custom CUDA needed:

```python
import torch
from torch.nn.functional import scaled_dot_product_attention

q, k, v = torch.randn(1, 8, 1024, 64, device='cuda')  # batch, heads, seq, dim
with torch.backends.cuda.sdp_kernel(enable_flash=True, enable_math=False):
    out = scaled_dot_product_attention(q, k, v, attn_mask=mask, dropout_p=0.1)
```

This handles masking/dropout; falls back to math kernel if unsupported. For custom models, it's a drop-in replacement for manual attention loops, yielding 2-3x speedups out-of-box.

FlashAttention revolutionized long-context training, powering models like Llama-2 (4k→70B) and beyond.

[FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135)
[PyTorch 2.2: FlashAttention-v2 Integration](https://pytorch.org/blog/pytorch2-2/)
[GitHub: Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention)
