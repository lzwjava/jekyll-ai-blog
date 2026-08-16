---
audio: false
generated: true
image: false
lang: en
layout: post
title: MoE Pipeline in Mini-Sglang
translated: false
type: note
---

Here's how MoE works in mini-sglang, traced end-to-end from model to kernel.

## 1. Model level — router + experts (`models/utils.py`, `models/qwen3_moe.py`)

```python
class MoEMLP(BaseOP):
    def __init__(self, config):
        self.experts = MoELayer(num_experts=..., top_k=..., hidden_size=..., ...)
        self.gate = LinearReplicated(hidden_size, num_experts, has_bias=False)

    def forward(self, hidden_states):
        router_logits = self.gate(hidden_states)          # [num_tokens, num_experts]
        return self.experts(hidden_states, router_logits)  # MoE computation
```

Each decoder layer's MLP is a **router** (a replicated linear producing one logit per expert per token) plus a **MoE layer**. The router is `LinearReplicated`, meaning every TP rank computes identical logits — the routing decision is shared.

## 2. Layer level — expert weights (`layers/moe.py`)

`MoELayer` holds the expert weights as raw tensors (no `nn.Module` wrapping — these get sharded/loaded specially):

- `gate_up_proj`: `[num_experts, 2·intermediate_per_partition, hidden]` — the **fused gate+up projection** of SwiGLU
- `down_proj`: `[num_experts, hidden, intermediate_per_partition]`

**Tensor parallelism**: `intermediate_size` is split by `div_even(intermediate_size, tp_size)`, so each rank holds a slice of *every* expert. The forward calls the pluggable `ctx.moe_backend.forward(...)`, then does an `all_reduce` to combine the partial sums across ranks. (Note: this is **TP only — no expert parallelism**; all experts live on all ranks.)

## 3. Backend abstraction (`moe/`)

`BaseMoeBackend` is an ABC with a single `forward(...)`. The engine registers backends via a registry (`moe/__init__.py`), auto-selects `"fused"` for MoE models, and stashes it in the global ctx (`engine/engine.py`). Only `FusedMoe` ships — it wraps SGLang's `sgl_kernel` plus custom Triton kernels.

## 4. The fused pipeline (`moe/fused.py`) — the interesting part

`FusedMoe.forward` = **top-k routing → block-aligned dispatch → 2 fused GEMMs → sum-reduce**:

**a) `fused_topk`** — routing:
- `sgl_kernel.topk_softmax` computes the top-k expert indices and softmax-normalized weights per token over all experts.
- If `renormalize`, it re-normalizes so the *selected* k weights sum to 1 (standard MoE practice).
- Can mask padded tokens (`topk_ids = -1`) for ragged batches.

**b) `moe_align_block_size`** — dispatch layout:
- Flattens `topk_ids` (each token appears `top_k` times), **sorts token indices grouped by expert**, and pads each expert's token count to a multiple of `BLOCK_SIZE_M` (using `sgl_kernel.moe_align_block_size` with a cumsum buffer).
- This is the classic trick that lets a Triton GEMM process, per expert, a contiguous `[M_padded, K]` block — padding makes the block sizes consistent.

**c) `fused_experts_impl`** — the compute, in 3 kernel calls:

```
hidden [M, K]
  → fused_moe_kernel(w1=gate_up, mul_routed_weight=True)   # [M, topk, N]  (fused G+U)
  → silu_and_mul / gelu_and_mul                            # SwiGLU activation (splits 2N in half, elementwise-mul)
  → fused_moe_kernel(w2=down,  mul_routed_weight=False)    # [M, topk, hidden]
  → moe_sum_reduce_triton(sum over topk dim)               # [M, hidden]
```

Note the `apply_router_weight_on_input` flag is **flipped between the two kernel calls** (True → False), so the routed weight multiplies the result exactly once — on the gate-up output — before the top-k sum.

## 5. The Triton kernel (`kernel/triton/fused_moe.py`, `kernel/moe_impl.py`)

`fused_moe_kernel` is a grouped-GEMM with expert-indexed weight lookup:

- Each program computes a `[BLOCK_M, BLOCK_N]` tile of the (padded, sorted) token×expert GEMM.
- Token rows come from `sorted_token_ids[offs_token]`; since tokens are repeated `top_k` times in the sorted list, `offs_token // top_k` recovers the **original token row** in the input (`a_ptrs`). Padding tokens (`offs_token >= num_valid_tokens`) are masked out with `token_mask`.
- The expert weight slice is selected per block via `expert_ids[pid_m]` → `b_ptr + off_experts * stride_be`.
- K-dim loop accumulates in fp32, multiplies by the routed weight if `MUL_ROUTED_WEIGHT`, and writes into the `[M, topk, N]` cache.

`moe_sum_reduce_kernel` then sums the top-k contributions per token into the final hidden state.

## Summary diagram

```
router:  hidden [M,K] ──LinearReplicated──▶ logits [M,E]
                                              │ sgl_kernel.topk_softmax
                                              ▼
FusedMoe:  topk_weights [M,k] + topk_ids [M,k]
              │ moe_align_block_size (sort by expert + pad)
              ▼
          ┌─ fused_moe_kernel (w1: gate+up, ×weight) ─▶ [M,k,2N] ─ silu_and_mul ─▶ [M,k,N]
          │                                                                        │
          └─ fused_moe_kernel (w2: down, no weight) ◀──────────────────────────────┘
              │ moe_sum_reduce (sum over k)
              ▼
          [M, hidden] ── all_reduce (TP) ──▶ final
```

Key design points: **fused gate/up weights** (one GEMM instead of two), **grouped-GEMM dispatch** with expert-sorted padded blocks for efficient Triton matmuls, **TP-only sharding** (no EP), and a **pluggable backend** so SGLang's native `sgl_kernel` MoE path can be swapped in.