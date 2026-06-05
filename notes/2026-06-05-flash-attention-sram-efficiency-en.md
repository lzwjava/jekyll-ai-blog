---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flash Attention SRAM Efficiency
translated: false
type: note
---

Question: What is SRAM in Flash Attention, and why does it matter?

Answer:

SRAM in Flash Attention is the **on-chip, high-speed cache memory** on GPU streaming multiprocessors that the algorithm exploits to reduce expensive HBM (High Bandwidth Memory) accesses.

## GPU Memory Hierarchy (RTX 4070 / MI300X context)

```
L0 Cache (128 bytes/thread)  ← Ultra-fast, implicit
L1 Cache (128 KB per SM)
SRAM / Shared Memory (96-192 KB per SM)  ← Flash Attention lives here
L2 Cache (12 MB global, shared)
HBM (GDDR6/HBM3)  ← Slow! 750 GB/s (RTX 4070), but 192 GB/s per 100 cycles
```

SRAM bandwidth is **~10-100x faster** than HBM. On RTX 4070, SRAM bandwidth ≈ 5 TB/s vs HBM ≈ 576 GB/s. The latency gap is even worse.

## The Flash Attention Insight

Standard attention computes: `Attention(Q, K, V) = softmax(Q @ K^T / √d) @ V`

**Naive approach** (what NVIDIA did for years):

1. Load all Q, K, V from HBM → GPU registers/SRAM
2. Compute full `Q @ K^T` (N×N matrix) — **must live in HBM because it's too big for SRAM**
3. Compute softmax row-by-row, with O(N²) HBM accesses

**Flash Attention approach**:

1. Tile Q into blocks of size M = SRAM_size / (3 × d × sizeof(float))
2. For each Q block, loop through K, V blocks
3. **All intermediate computation stays in SRAM** — load, compute, accumulate, write back
4. Reduces HBM accesses from O(N²d) to O(Nd)

## The Math (Simplified)

Say you have:

- Sequence length N = 4096, d_model = 128
- SRAM available ≈ 96 KB for tensors
- Block size: M = 96_000 / (3 × 128 × 4) ≈ 62 tokens

For each block of 62 Q tokens:

```python
# Pseudocode
m = -inf  # row max (for numerically stable softmax)
l = 0     # row sum of exp
O = zeros(M, d)  # output accumulator

for block_k_v in range(0, N, block_size_kv):
    # Load K, V blocks into SRAM
    K_block = load_from_HBM(block_k_v)  # (block_kv, d)
    V_block = load_from_HBM(block_k_v)  # (block_kv, d)

    # Compute attention for this block in SRAM
    scores = Q_block @ K_block.T / sqrt(d)  # (M, block_kv)

    # Numerically stable softmax with running max/sum
    m_new = max(m, scores.max(axis=1))
    l = exp(m - m_new) * l + exp(scores - m_new).sum(axis=1)
    m = m_new

    # Accumulate output (crucial: done in SRAM)
    O += exp(scores - m[:, None]) @ V_block

# Final normalize
return O / l[:, None]
```

The key: **all of Q_block, K_block, V_block, scores, and O live in SRAM**. Only HBM -> SRAM and SRAM -> HBM transfers. No intermediate O(N²) matrix stored.

## Why This Matters for Your MI300X

On AMD MI300X (192 GB HBM3):

- HBM3 bandwidth: 5.2 TB/s (much better than RTX 4070)
- But SRAM bandwidth on MI300X is insane: cores can hit 100+ TB/s to local SRAM
- The efficiency gain is **smaller** (your gap is smaller), but still critical

For a 4B token model, Flash Attention saves ~4-10x HBM pressure depending on sequence length and d_model.

## Implementation Notes

If you're training nanoGPT-scale models:

- torch.nn.functional.scaled_dot_product_attention (PyTorch 2.0+) uses Flash Attention automatically when possible
- For manual CUDA, use `cutlass::gemm` for Q @ K^T and accumulate carefully
- The MI300X has 64 MB L3 cache per chiplet — even more room to tile aggressively

The paper (Dao et al., 2022) has the full algorithm including grad pass. The forward pass is straightforward; the backward is where the real wizardry happens (you need to recompute attention from blocks, not store it).

References:

- [Flash-Attention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135) (Dao et al., 2022)
- [GPU Memory Hierarchy & Roofline Model](https://people.eecs.berkeley.edu/~sameh/SC16/SC16_Roofline_Samuel_Williams.pdf)
