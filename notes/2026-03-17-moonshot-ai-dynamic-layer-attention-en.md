---
audio: false
generated: true
image: false
lang: en
layout: post
title: Moonshot AI’s Dynamic Layer Attention
translated: false
type: note
---

**Question:** What is a comprehensive introduction to Kimi's Attention Residual (from Moonshot AI)?

**Answer:**

**Attention Residuals (AttnRes)** is a novel architectural innovation introduced by Moonshot AI (the team behind Kimi) in March 2026. It replaces the traditional fixed residual connections in transformer models with a **learned, input-dependent attention mechanism over previous layers**.

This change addresses long-standing limitations in how deep networks aggregate information across depth.

### Traditional Residual Connections – The Baseline

In a standard transformer (post-LN or pre-LN), each layer updates the hidden state like this:

```
x_{l} = x_{l-1} + F_l(x_{l-1})
```

(or in pre-LN: LayerNorm → sub-layer → add)

- The skip connection always adds the previous layer's output with weight **1.0**.
- This is **fixed**, **uniform**, and **input-independent**.
- As depth increases → signal dilution, exploding/vanishing magnitudes, uneven gradient flow.

### Core Idea of Attention Residuals

Instead of blind addition of the immediate previous layer, each layer attends over **all (or many) previous layers** using softmax attention.

Simplified mathematical view:

Let the outputs of previous layers be {h₁, h₂, ..., h_{l-1}}

For layer l:

- Learn a **pseudo-query vector** qₗ (one vector per layer, typically small dimension or shared)
- Compute attention scores over previous hidden states:  
  α_{l,i} = softmax( qₗ · h_i ) for i = 1…l-1
- The new input to layer l becomes a **weighted sum**:

```
x_l^{pre} = ∑_{i=1}^{l-1} α_{l,i} ⋅ h_i
```

- Then apply the normal sub-layer (attention + FFN) → add & norm as usual.

Key insight: depth is treated analogously to **time** in sequence models → attention over depth instead of fixed recurrence.

### Main Benefits

- **Selective retrieval** — layers can focus on useful earlier representations (bypassing diluted middle layers).
- **Mitigates representational dilution** — hidden states stay more stable in magnitude across very deep models.
- **More uniform gradient flow** — gradients distribute better across layers (less vanishing).
- **Better scaling behavior** — especially helpful when pushing model depth or when using PreNorm (which suffers more from dilution).

### Practical Implementation: Block Attention Residuals

Full attention over every previous layer would be quadratic in depth (very expensive at 100+ layers).

Moonshot uses **block-wise** grouping:

- Group layers into blocks (e.g., every 4–8 layers)
- Perform attention only over block summaries (or block outputs)
- Keeps memory & compute roughly linear in depth
- Inference overhead is very small (~1–2%)

Reported results show:

- ~1.25× effective compute advantage during pre-training
- Negligible inference slowdown
- Better downstream performance in several settings

### Integration Example: Kimi Linear

Moonshot integrated Attention Residuals into their **Kimi Linear** model (hybrid linear-attention + MLA architecture, 48B total / 3B active params, trained on 1.4T tokens).

It helps mitigate PreNorm issues and contributes to strong scaling behavior.

### Summary – Why It Matters

Attention Residuals is one of the cleanest and most elegant updates to the **core transformer block** since the original "Attention is All You Need" paper (2017).

It completes the "attention-ification" transition:

- Tokens already attend over other tokens (self-attention)
- Now layers attend over other layers (depth-wise)

Many researchers view it as a natural evolution that was surprisingly overlooked for almost a decade.

For the full technical details, refer to the official paper released by Moonshot AI.

**References:**

- [Moonshot AI Attention Residuals announcement](https://www.linkedin.com/posts/kimi-ai-linkedin_introducing-%F0%9D%91%A8%F0%9D%92%95%F0%9D%92%95%F0%9D%92%86%F0%9D%92%8F%F0%9D%92%95%F0%9D%92%8A%F0%9D%92%90%F0%9D%92%8F-%F0%9D%91%B9%F0%9D%92%86%F0%9D%92%94%F0%9D%92%8A%F0%9D%92%85-activity-7439188677697679360-p-gw)
- [MarkTechPost coverage of Attention Residuals](https://www.marktechpost.com/2026/03/15/moonshot-ai-releases-%F0%9D%91%A8%F0%9D%92%95%F0%9D%92%95%F0%9D%92%86%F0%9D%92%8F%F0%9D%92%95%F0%9D%92%8A%F0%9D%92%90%F0%9D%92%8F-%F0%9D%91%B9%F0%9D%92%86%F0%9D%92%94%F0%9D%92%8A%F0%9D%92%85)
- [GitHub repo with paper (Attention_Residuals.pdf)](https://github.com/MoonshotAI/Attention-Residuals/blob/master/Attention_Residuals.pdf)
- [Reddit discussion on replacing residuals with attention](https://www.reddit.com/r/LocalLLaMA/comments/1rv7ige/residual_connections_havent_changed_for_10_years)