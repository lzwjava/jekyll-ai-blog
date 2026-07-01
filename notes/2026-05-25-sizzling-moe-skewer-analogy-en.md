---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sizzling MoE Skewer Analogy
translated: false
type: note
---

**Question:** Explain MoE (Mixture of Experts) structure using the BBQ skewer analogy — each skewer is an expert, each piece of meat is a token/logit. Is the simplified forward pass correct?

**Answer:**

The skewer analogy is solid. Let me extend it precisely and then fix your code.

---

## 🍢 羊肉串 MoE Analogy

```
Each SKEWER  = one Expert FFN          (e.g., 64 skewers total)
Each CHUNK OF MEAT = one token         (one position in the sequence)
The GRILL CHEF = the Router            (decides which skewers to cook each chunk on)
TopK selection = only 8 skewers get the meat, 56 sit idle
```

A token (chunk of meat) gets **routed to only 8 skewers** out of 64. The other 56 experts don't fire — this is why MoE is compute-efficient at inference.

---

## Your Code — Almost Right, One Bug

```python
# Simplified MoE forward
router_logits = x @ router_weight.T        # [B*T, n_routed_experts]
topk_ids = router_logits.topk(k=8).indices # select 8 experts
output = sum(expert[i](x) for i in topk_ids)  # ❌ missing routing weights
```

**The missing piece: routing weights (gating scores).** You're summing expert outputs equally — but each expert should contribute **proportionally to its router score**. The meat on skewer #3 might be 60% done, skewer #7 only 40% — you weight by that.

---

## Correct Forward Pass

```python
import torch
import torch.nn.functional as F

# x: [B*T, d_model]  — one token per row (one chunk of meat)
router_logits = x @ router_weight.T          # [B*T, n_experts]  — score each skewer
router_probs  = F.softmax(router_logits, -1) # normalize scores

topk_vals, topk_ids = router_probs.topk(k=8, dim=-1)
# topk_vals:  [B*T, 8]  — how much each selected expert contributes
# topk_ids:   [B*T, 8]  — which 8 skewers got the meat

# Re-normalize among the 8 selected (important!)
topk_vals = topk_vals / topk_vals.sum(dim=-1, keepdim=True)  # [B*T, 8]

# Weighted sum over selected experts
output = torch.zeros_like(x)
for k in range(8):
    expert_idx   = topk_ids[:, k]          # which expert for each token
    expert_score = topk_vals[:, k]         # its weight   [B*T]

    # Each token goes to its assigned expert
    # (in real impl, tokens are batched per expert for efficiency)
    for b in range(x.shape[0]):
        expert_out = experts[expert_idx[b]](x[b])          # FFN forward
        output[b] += expert_score[b] * expert_out          # weighted add
```

---

## The Full Picture in Skewer Terms

```
Token (chunk of meat)
        │
        ▼
   Router (chef)
   scores all 64 skewers
        │
   softmax → probabilities
        │
   topk(8) → pick 8 skewers
        │
   ┌────┴────────────────────┐
   │  skewer 3  (w=0.35)     │  FFN_3(x) * 0.35
   │  skewer 17 (w=0.28)     │  FFN_17(x) * 0.28
   │  skewer 42 (w=0.15)     │  FFN_42(x) * 0.15
   │  ... 5 more ...         │
   └────────────────────────┘
        │
   weighted sum → output token
```

56 skewers = **cold, idle, zero FLOPS**. That's the MoE win.

---

## DeepSeek-V3 / Qwen MoE Reality Check

| Thing | Value |
| --- | --- |
| Total experts | 64–256 |
| Activated per token | 8 (DeepSeek-V3 uses 8 of 256) |
| Active params per token | ~37B of 671B total |
| Router type | linear + softmax (sometimes sigmoid) |
| Load balancing loss | auxiliary loss to prevent expert collapse |

**Expert collapse** is the main training hazard — without the aux loss, the router learns to always send meat to the same 3 skewers and the other 61 starve. DeepSeek-V3 also adds **shared experts** (skewers that get every chunk of meat, always on) on top of the routed ones.

---

## DeepSeek-V3 Exact Formula

```
output = FFN_shared(x) + Σ_{i ∈ topk} g_i · FFN_i(x)

where g_i = softmax(router_logits)[i]  (among selected k only, renormalized)
```

Your intuition was right — it's a weighted sum. You just needed the `g_i` weights in there.
