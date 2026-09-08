---
audio: false
generated: true
image: false
lang: en
layout: post
title: No Direct Expert Logits in MoE
translated: false
type: note
---

Question: **In a Mixture-of-Experts (MoE) model, when computing the final logits, which expert's logits do we use?**

Answer: **None of the experts' logits directly.** The experts operate on the hidden states, and their outputs are **weighted and combined before the model's final LM head produces logits**.

For one token, the forward pass is roughly:

```text
x
│
├── Router(x) → scores
│              ↓
│         top-k experts
│        /     |      \
│      E1      E3      E7
│       │       │       │
│       └───────┼───────┘
│          weighted sum
│              ↓
│        MoE output
│              ↓
│       residual + norm
│              ↓
│         hidden state h
│              ↓
│       LM Head / Linear
│              ↓
│          logits
│              ↓
│         softmax → P(token)
```

### Concrete example

Suppose the router selects 2 experts:

```python
x = hidden_state

router_logits = router(x)              # [num_experts]
weights, expert_ids = topk(router_logits, k=2)

y1 = expert_3(x)
y2 = expert_7(x)

moe_output = (
    weights[0] * y1 +
    weights[1] * y2
)

h = residual + moe_output

logits = lm_head(norm(h))
```

So **Expert 3 does not produce vocabulary logits**, and Expert 7 doesn't either.

They produce something like:

```text
Expert 3:
hidden dimension = 4096
        ↓
      [4096]

Expert 7:
hidden dimension = 4096
        ↓
      [4096]
```

The weighted combination remains a hidden vector:

```text
0.7 * Expert3(x) + 0.3 * Expert7(x)
              ↓
           [4096]
```

Then the shared LM head maps it to vocabulary space:

```text
[4096]
   ↓
Linear(4096 → 128k)
   ↓
[128000]   ← logits
```

### Why this matters

An MoE layer is essentially:

$$
y = \sum_{i \in TopK(x)} g_i(x) E_i(x)
$$

where:

* \\(E_i(x)\\) = output of expert \\(i\\)
* \\(g_i(x)\\) = router weight
* \\(TopK(x)\\) = selected experts

Then later:

$$
\text{logits} = W_{lm}h
$$

where \\(h\\) is the **combined hidden state** after the MoE layer and subsequent transformer layers.

So if you have:

```text
8 experts
top-k = 2
```

for a particular token:

```text
Expert 1 ──┐
Expert 5 ──┤
            ↓
       weighted sum
            ↓
       transformer
            ↓
         LM head
            ↓
         logits
```

**You don't choose "Expert 1's logits" or "Expert 5's logits."**

The router chooses **which experts contribute to the hidden representation**, not which expert generates the vocabulary distribution.

One useful next step would be to walk through the actual **DeepSeek/Qwen-style MoE PyTorch code**, including the exact tensor shapes `[batch, seq, hidden] → router → topk → expert output → logits`.