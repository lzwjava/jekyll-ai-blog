---
audio: false
generated: true
image: false
lang: en
layout: post
title: MoE Layer Forward Pass Explained
translated: false
type: note
---

**Question:** In DeepSeek V3/V4's MoE architecture, what are the shapes at each step of the simplified MoE forward pass, and how does it work?

**Answer:**

Let me annotate the shapes precisely and explain the full picture.

## Setup / Notation

```
B   = batch size
T   = sequence length
d   = model hidden dim (DeepSeek V3: 7168)
n   = total routed experts (256 in V3/V4)
k   = top-k experts selected (8 in V3/V4)
d_e = expert intermediate dim (2048 in V3/V4, much smaller than dense FFN)
```

---

## Shape-annotated Forward Pass

```python
# x: [B*T, d]  — flattened tokens, each is a d-dim hidden state
# router_weight: [n, d]  i.e. [256, 7168]

router_logits = x @ router_weight.T
# x:             [B*T, d]
# router_weight.T: [d, n]
# result:        [B*T, n]  = [B*T, 256]
# Each row = one token's affinity score over all 256 experts

topk_ids = router_logits.topk(k=8).indices
# shape: [B*T, 8]
# Each token selects 8 expert indices out of 256

topk_weights = router_logits.topk(k=8).values.softmax(-1)
# shape: [B*T, 8]  — normalized gating weights (sum to 1 per token)

output = sum(expert[i](x) for i in topk_ids)
# Each expert[i](x): [B*T, d]  (only computed for tokens routed to it)
# Weighted sum:       [B*T, d]
```

Final output shape: **`[B*T, d]`** — same as input, just like a normal FFN.

---

## What Each Expert Actually Does

Each expert is a small FFN (SwiGLU in DeepSeek V3):

```python
# Inside expert[i]:
# gate_weight: [d_e, d]  = [2048, 7168]
# up_weight:   [d_e, d]
# down_weight: [d, d_e]  = [7168, 2048]

def expert_forward(x):  # x: [B*T, d]
    gate = x @ gate_weight.T   # [B*T, d_e]
    up   = x @ up_weight.T     # [B*T, d_e]
    act  = F.silu(gate) * up   # [B*T, d_e]  — SwiGLU
    out  = act @ down_weight.T # [B*T, d]
    return out
```

But in practice only a **subset of tokens** get sent to each expert — this is the dispatch/gather mechanism.

---

## Realistic Dispatch (what actually happens in code)

The naive loop `for i in topk_ids` is wrong in practice. Real implementation:

```python
# [B*T, 8] → flatten to get (token_idx, expert_idx) pairs
# For each expert e, gather only the tokens assigned to it

expert_outputs = torch.zeros(B*T, d)

for e in range(n_experts):  # 256 experts
    # which tokens route to expert e?
    mask = (topk_ids == e).any(dim=-1)         # [B*T] bool
    tokens_for_e = x[mask]                      # [n_e, d], n_e << B*T
    
    if tokens_for_e.shape[0] == 0:
        continue
    
    out_e = expert[e](tokens_for_e)             # [n_e, d]
    
    # get the weight for this expert for each routed token
    weight_e = topk_weights[mask, (topk_ids[mask] == e).nonzero()...]
    expert_outputs[mask] += weight_e.unsqueeze(-1) * out_e

# final: [B*T, d]
```

In real CUDA kernels (and Triton), this is done via **token permutation** — tokens are sorted by expert assignment, batched per expert, then un-permuted.

---

## DeepSeek V3 Specific: Shared Experts + Routed Experts

V3 doesn't just have 256 routed experts. It has **1 shared expert** (always fires) + **256 routed** (top-8 selected):

```
V3 MoE layer:
  shared_expert(x)           → [B*T, d]   always active
+ sum of top-8 routed experts → [B*T, d]
= final FFN output            → [B*T, d]
```

The router only selects from the 256 **routed** experts; shared expert bypasses routing entirely.

---

## Key Numbers: V3 Param Budget

| | Dense equivalent | MoE V3 |
|---|---|---|
| FFN hidden dim | ~18K (for 671B dense) | 2048 per expert |
| Active experts per token | all | 8 + 1 shared |
| Total expert params | — | 256 × small FFN |
| Active params per token | ~671B | ~37B |

The router matrix itself is tiny: `256 × 7168 = 1.8M params` — negligible.

---

## Load Balancing (V3 innovation: no auxiliary loss)

V3 uses **auxiliary-loss-free load balancing** — a bias term added to router logits per expert, updated dynamically to keep expert utilization uniform:

```python
router_logits_biased = router_logits + expert_bias  # [B*T, 256]
topk_ids = router_logits_biased.topk(8).indices     # routing decision

# But gating WEIGHTS use unbiased logits:
topk_weights = router_logits.gather(-1, topk_ids).softmax(-1)
```

This is the key V3 trick vs V2 which used an explicit auxiliary loss term.

---

## Summary Table

| Tensor | Shape |
|---|---|
| `x` (input) | `[B*T, d]` = `[B*T, 7168]` |
| `router_weight` | `[256, 7168]` |
| `router_logits` | `[B*T, 256]` |
| `topk_ids` | `[B*T, 8]` |
| `topk_weights` | `[B*T, 8]` |
| per-expert input | `[n_e, 7168]` where `n_e` ≪ `B*T` |
| per-expert output | `[n_e, 7168]` |
| final output | `[B*T, 7168]` |

**References:**

- [DeepSeek-V3 Technical Report (arXiv)](https://arxiv.org/abs/2412.19437)
- [DeepSeek-V3 GitHub](https://github.com/deepseek-ai/DeepSeek-V3)
- [Mixture of Experts Explained — Hugging Face](https://huggingface.co/blog/moe)