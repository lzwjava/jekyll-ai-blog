---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Math of Linear Attention
translated: false
type: note
---

Question: What's the history of linear attention in LLMs — the actual math evolution, not just names?

Answer:

**Core trick (Katharopoulos et al., ICML 2020, "Transformers are RNNs")**

Standard attention is O(N²) because you materialize the full `QKᵀ` matrix:

```
O_i = Σ_j softmax(q_i · k_j) v_j
```

Katharopoulos replaced `softmax(q·k)` with a separable kernel `φ(q)·φ(k)ᵀ` (they used `elu(x)+1`). Since matmul is associative, you can reorder:

```python
import torch

def causal_linear_attention(q, k, v, feature_map=lambda x: torch.nn.functional.elu(x) + 1):
    # q,k,v: [B, T, D]
    q, k = feature_map(q), feature_map(k)
    S = torch.zeros(q.shape[0], q.shape[-1], v.shape[-1])  # [B, D, D] running state
    z = torch.zeros(q.shape[0], q.shape[-1])                # [B, D] normalizer
    outs = []
    for t in range(q.shape[1]):
        S = S + torch.einsum('bd,be->bde', k[:, t], v[:, t])  # outer product write
        z = z + k[:, t]
        num = torch.einsum('bd,bde->be', q[:, t], S)
        den = torch.einsum('bd,bd->b', q[:, t], z).unsqueeze(-1) + 1e-6
        outs.append(num / den)
    return torch.stack(outs, dim=1)
```

That's the whole idea: attention becomes an **RNN with a matrix-valued state** `S ∈ R^{D×D}`, updated by rank-1 outer-product writes `k_t v_tᵀ`. O(N) time, O(1) memory per step (state size independent of T). Everything since 2020 is "what's the best update rule for `S`."

**Timeline**

- **2020 — Katharopoulos, "Transformers are RNNs"**: the kernel-trick reformulation above.
- **2020 — Performer (Choromanski et al.)**: FAVOR+, random Fourier features to *unbiasedly* approximate softmax rather than replace it with an arbitrary kernel.
- **2021 — Schlag et al., "Linear Transformers are Secretly Fast Weight Programmers"**: reframes the state update as a fast-weight memory and introduces a **delta-rule** write (`S += k(v - S k)ᵀ`, i.e. error-correcting instead of pure accumulation) — this becomes important again in 2024.
- **2023 — RetNet (Sun et al., MSRA)**: adds a fixed exponential decay to the state, `S_t = γS_{t-1} + k_t v_tᵀ`, and gives a **chunkwise-parallel** form (parallel within chunks, recurrent across chunks) so it's actually fast on GPUs, not just asymptotically better.
- **2023 — RWKV (Peng et al.)**: independently converges on the same decay-state idea (WKV), trained at real LLM scale as a pure RNN, no attention at inference.
- **2023 — Mamba (Gu & Dao)**: not literally kernelized attention, but a **selective SSM** where the decay/gates are input-dependent — same O(N) complexity class, becomes the sibling lineage.
- **Dec 2023 — GLA, Gated Linear Attention (Yang et al.)**: makes the decay *data-dependent* per-channel (not a fixed scalar like RetNet), plus a hardware-efficient chunked Triton kernel. This spawned the `flash-linear-attention` (fla) library that basically every later paper builds on.
- **2024 — DeltaNet (Yang et al., NeurIPS)**: resurrects Schlag's delta rule and shows how to parallelize it over chunks with matmuls — big jump in associative-recall quality vs. pure accumulation.
- **2024 — Mamba-2 (Dao & Gu)**: "State Space Duality" paper — formally proves SSMs and linear attention are the same computation viewed two ways.
- **Dec 2024 — Gated DeltaNet (Yang, Kautz, Hatamizadeh, NVIDIA)**: combines GLA's gating with DeltaNet's delta-rule write. State update: decay + error-corrected write.
- **2025 — RWKV-7 "Goose"**: generalizes the delta rule to a diagonal-plus-low-rank state transition matrix (more expressive than scalar decay).
- **2025 — MiniMax-01 (lightning attention)**: first big production LLM to ship linear attention at scale — hybrid, 7/8 linear-attention layers + 1/8 full softmax layers, because pure linear attention still loses on precise long-range retrieval.
- **2025 — DeltaProduct, Titans, Miras**: push further — multiple delta-rule steps per token, or replacing the linear state matrix with an MLP (nonlinear deep memory).

**Unifying view**: every model since 2023 is `S_t = A_t ⊙ S_{t-1} + k_t v_tᵀ` (or a delta-rule variant of the write), where the *only* differences are (1) whether `A_t` decay is scalar/diagonal/low-rank and data-dependent, and (2) whether the write is pure accumulation vs. error-corrected (delta rule). The recent "test-time training" framing (Sun et al. 2024) makes this explicit: the state update *is* an online-gradient-descent step on a `key→value` regression loss, and different papers are just picking different optimizers.

References:

- [Transformers are RNNs (Katharopoulos et al., 2020)](http://proceedings.mlr.press/v119/katharopoulos20a.html)
- [Linear Transformers are Secretly Fast Weight Programmers (Schlag et al., 2021)](https://arxiv.org/abs/2102.11174)
- [Retentive Network (Sun et al., 2023)](https://arxiv.org/abs/2307.08621)
- [Gated Linear Attention Transformers (Yang et al., 2023)](https://arxiv.org/abs/2312.06635)
- [Parallelizing Linear Transformers with the Delta Rule (Yang et al., 2024)](https://arxiv.org/abs/2406.06484)
- [Mamba-2 / State Space Duality (Dao & Gu, 2024)](https://arxiv.org/abs/2405.21060)
- [Gated Delta Networks (Yang, Kautz, Hatamizadeh, 2024)](https://arxiv.org/abs/2412.06464)
- [flash-linear-attention (fla) library](https://github.com/fla-org/flash-linear-attention)
- [MiniMax-01 lightning attention](https://arxiv.org/abs/2501.08313)
