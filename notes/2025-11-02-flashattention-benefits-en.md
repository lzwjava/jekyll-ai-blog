---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: FlashAttention Algorithm and Benefits
translated: false
type: note
---

# Deep explanation of FlashAttention (Tri Dao et al., 2022)

Short summary up front: FlashAttention removes the need to allocate the full \\(N\times N\\) attention matrix in GPU DRAM (HBM) by computing attention **block-by-block** inside on-chip SRAM (registers / shared memory), fusing the whole attention pipeline into a single kernel and using numerically correct blockwise softmax accumulation. That drastically cuts HBM traffic and memory from \\(O(N^2)\\) to effectively \\(O(N)\\), and in practice gives large wall-clock speedups on GPUs for long sequences. citeturn0search0turn0search9

---

## The problem: why standard attention is IO-bound
Transformer self-attention (scaled dot-product) is usually implemented with three steps:

1. compute scores \\(S = Q K^\top\\) (size \\(N\times N\\));
2. compute rowwise softmax \\(P = \mathrm{softmax}(S)\\);
3. compute output \\(O = P V\\).

Naively you materialize \\(S\\) (and often \\(P\\)) in GPU DRAM. For sequence length \\(N\\) this uses \\(O(N^2)\\) memory and leads to two IO problems:
- large DRAM footprint (often the first thing to blow GPU memory), and
- lots of reads/writes between DRAM (HBM) and on-chip SRAM/registers — and those HBM↔SRAM transfers are the real bottleneck on modern GPUs.

FlashAttention reframes attention as an **IO problem**, not just a FLOP problem, and targets reducing HBM accesses. citeturn0search0

---

## Core ideas (high level)
1. **Tile the matrices** \\(Q, K, V\\) into blocks that fit in on-chip SRAM (shared memory / registers).
2. **Process attention block-by-block**: for a given \\(Q\\)-tile and a streaming set of \\(K,V\\)-tiles, compute the partial contributions to the output and immediately accumulate them — never materialize the full \\(N\times N\\) score matrix in DRAM.
3. **Fuse everything into one kernel**: the kernel loads tiles into SRAM, computes \\(QK^\top\\) for that tile pair, applies softmax logic and multiplies by the \\(V\\)-tile, and writes partial outputs — all without round-trips of intermediate large matrices to DRAM. Kernel fusion reduces instruction and memory overhead.
4. **Blockwise numerically stable softmax accumulation**: because softmax across the whole row needs the global max and sum, FlashAttention uses a running max / running sum (log-sum-exp style) to combine softmax contributions from multiple \\(K\\)-tiles exactly and stably without storing the whole row of scores.
5. **Backward via recomputation**: instead of storing large intermediates for backward, recompute the forward attention for each block during the backward pass (trade extra FLOPs for much less DRAM IO). The saved DRAM IO usually yields net speedup since DRAM IO dominates. citeturn0search2turn0search10

These ideas together yield both memory reduction and wall-clock speed improvements. citeturn0search0

---

## Blockwise algorithm — step by step (forward)
Consider a single attention head with sequence length \\(N\\) and head dim \\(d\\). Choose a tile size \\(B\\) so a \\(B\times B\\) scores block and the corresponding \\(Q\\), \\(K\\), \\(V\\) tiles fit in SRAM.

For each query tile \\(Q_{i}\\) (rows \\(iB:(i+1)B\\)):

1. Initialize an output accumulator \\(O_i \leftarrow 0\\).
2. Initialize running normalization state: `row_max` (per query row) to \\(-\infty\\), `row_sum` to 0. These track the numerically stable denom for softmax across multiple K-tiles.
3. For each key/value tile \\(K_{j}, V_{j}\\) (columns \\(jB:(j+1)B\\)):
   - Load \\(Q_i\\), \\(K_j\\), \\(V_j\\) into SRAM.
   - Compute the tile of raw scores \\(S_{ij} = Q_i K_j^\top / \sqrt{d}\\) (shape \\(B\times B\\) in vectorized form).
   - For each row in \\(S_{ij}\\), compute the local row max \\(m_{ij}\\) and exponentiated values \\(\exp(S_{ij} - m_{ij})\\).
   - Merge this tile’s exponentials into the running row normalization using the log-sum-exp trick:
     - Let \\(M = \max(\text{row\_max}, m_{ij})\\).
     - Update `row_sum` := `row_sum` · exp(row_max − M) + local_sum · exp(m_{ij} − M).
     - Set `row_max` := \\(M\\).
   - Compute the tile’s contribution to the accumulator with the appropriately scaled exponentials: accumulate \\(O_i \mathrel{+}= \text{(tile-softmax)} \times V_j\\). (All done inside SRAM.)
4. After streaming all K-tiles, finalize normalization using row_sum and row_max to produce correct softmax outputs; write \\(O_i\\) to DRAM.

Key point: no \\(N\times N\\) matrix is ever written to DRAM; only small tiles and final outputs are. The numerically-correct accumulation using running max + sum is what lets the per-tile softmax pieces combine exactly into the same result as a full softmax over the row. citeturn0search2turn0search10

---

## Why kernel fusion and SRAM tiling wins in practice
- **Lower HBM accesses:** Standard attention reads/writes \\(O(N^2)\\) elements to DRAM (scores, softmax). FlashAttention reads each \\(Q,K,V\\) element a constant number of times, and all temporary score/softmax values live only in SRAM. IO analysis in the paper shows fewer HBM accesses and ranges where FlashAttention is IO-optimal given SRAM size. citeturn0search0
- **Latency & bandwidth limits matter more than FLOPs:** GPUs are extremely fast at FP multiply-accumulate; when DRAM traffic dominates runtime, reducing DRAM transfers matters more than reducing FLOPs. Kernel fusion removes intermediate DRAM traffic and reduces kernel launch overhead. citeturn0search0
- **Backward pass tradeoff:** Recomputing forward blocks during backward increases FLOPs but avoids storing large intermediates in DRAM. Because recomputation happens in SRAM and limits DRAM traffic, it’s a net win for wall-clock time in many cases. citeturn0search10

Empirical results from the paper and follow-ups show multiple× speedups (e.g., 2–7× in their reported benchmarks depending on model and seq length) and large reductions in peak memory. citeturn0search0turn0search10

---

## Important implementation details & tradeoffs

- **Tile size selection:** Tile \\(B\\) must be chosen so the working set (tiles of Q, K, V, score buffers, partial accumulators, plus extra scratch) fits in on-chip SRAM per threadblock. Optimal \\(B\\) depends on head dimension, datatypes (FP16/FP32/FP8), and GPU architecture (amount of shared memory / registers). Too small reduces compute efficiency; too large won’t fit SRAM. citeturn0search2

- **Numerical stability:** The algorithm uses per-row running max and sum (log-sum-exp merging) to ensure the final softmax equals the full-matrix softmax. That is crucial: FlashAttention is **exact attention** (not an approximation) because of that stable accumulation. citeturn0search0

- **Masking & causality:** Causal masking (autoregressive) is handled by simply skipping or zeroing contributions from masked positions in the streamed tiles and updating the running normalization accordingly. The blockwise logic still works but may need careful tile ordering to ensure masked elements don’t contaminate accumulators. citeturn0search2

- **Backward pass and memory layout:** FlashAttention stores only minimal metadata (e.g., row_max/row_sum per block) and recomputes forward tile products during backward. Implementations carefully reorder work to maximize reuse and minimize register pressure. citeturn0search10

- **Precision & datatypes:** Using FP16/FP8 affects tile buffering and accumulation choices. Some later works (FlashAttention-2 / FlashAttention-3) add optimizations for mixed precision and newer GPU features (Hopper, H100) to push utilization and FP throughput further. citeturn0search4turn0search11

- **Parallelism mapping:** The kernel maps warps/CTA blocks to query tiles; within a CTA, warps cooperate in loading K/V tiles and computing tile matmul and reductions. Efficient warp-level reductions and use of fused multiply-add instructions are important for peak throughput. citeturn0search2

---

## FlashAttention vs. approximate long-attention methods
FlashAttention keeps **exact** attention semantics (same numerical result as full attention up to floating-point rounding), whereas many long-attention methods approximate attention (sparsity, low-rank, FAVOR+, etc.) and trade quality for memory/time. FlashAttention instead reduces memory/IO cost while preserving the exact computation, so model quality is unchanged while throughput/memory improve. That’s why it’s widely attractive: no accuracy tradeoff, just a better low-level kernel. citeturn0search0

---

## Practical availability & ecosystem
- The authors released an implementation (CUDA) and a maintained repo with FlashAttention and later FlashAttention-2. Many frameworks (Hugging Face Transformers, XLA/PyTorch forks, Triton-based implementations) either call the flash-attn operator or provide similar fused kernels. You can use the `flash_attn` operator or libraries that expose it; in PyTorch, recent versions include memory-efficient attention primitives too, and third-party `flash_attn` packages give a drop-in speed/memory improvement for many workloads. Check the official repo for installers and API examples. citeturn0search9turn0search4

Caveat: “No need for custom kernels” is only partly true — FlashAttention *is* a custom fused kernel (the work in the repo) that frameworks call. Modern PyTorch versions may internally ship comparable fused kernels or delegate to vendor libraries, but the core idea requires a fused kernel implementation (whether in CUDA, Triton, or vendor code). The important lesson: you (as a model user) don’t have to write those kernels yourself — use the provided operator. citeturn0search9turn0search7

---

## Extensions and follow-ups
- **FlashAttention-2 (2023):** improves parallelism, work partitioning, and multicore scaling to get even better GPU utilization and throughput. citeturn0search4
- **FlashAttention-3 and other engineering work (2024+):** further tweaks for new hardware (Hopper/H100), FP8, and even higher TFLOP utilization. These continue the trend of hardware-aware fused attention kernels. citeturn0search11

---

## When FlashAttention helps most (rules of thumb)
- **Long sequences** (multiple thousands) or large batch/head sizes — saves most memory and gives biggest speedups.
- **When DRAM bandwidth is the bottleneck** — e.g., large models with large \\(N\\) where naive attention would thrash DRAM.
- **Training with large contexts** since recomputation-friendly backward reduces peak memory (permits bigger batch/context). citeturn0search0

---

## Quick pseudocode (conceptual)
```
for each query tile Qi:
    row_max = -inf (per row)
    row_sum = 0    (per row)
    out_acc = 0    (B x d_v)
    for each key/value tile Kj, Vj:
        load Qi, Kj, Vj into SRAM
        S = Qi @ Kj.T / sqrt(d)
        m = max_row(S)
        expS = exp(S - m)      # local exponentials
        local_sum = sum_row(expS)
        # merge normalizers stably:
        M = max(row_max, m)
        row_sum = row_sum * exp(row_max - M) + local_sum * exp(m - M)
        row_max = M
        # accumulate partial output with scaled expS:
        out_acc += (expS / (row_sum after merge)) @ Vj
    write out_acc to DRAM
```
(Implementation stores more metadata and arranges exact scaling carefully; above is conceptual.) citeturn0search2

---

## References / where to read next
- Original FlashAttention paper (Tri Dao et al., 2022) — algorithm, IO analysis, benchmarks. citeturn0search0turn0search2
- Official GitHub with CUDA kernels and PyTorch bindings. citeturn0search9
- FlashAttention-2 paper (Tri Dao, 2023) and engineering notes on later versions. citeturn0search4turn0search11

---

If you want, I can:
- show a line-by-line comparison of a naive attention loop vs. blockwise FlashAttention pseudocode (no wide tables),
- sketch CUDA/Triton kernel organisation and register/shared-memory budgeting for a concrete example (e.g., head dim 64, tile 128), or
- point you to the exact PyTorch API call and an example snippet to replace `torch.nn.functional.scaled_dot_product_attention` with FlashAttention. Which would be most useful next?
