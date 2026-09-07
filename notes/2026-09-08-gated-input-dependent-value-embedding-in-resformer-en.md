---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gated Input-Dependent Value Embedding in ResFormer
translated: false
type: note
---

Now I have all the details needed. Let me write a clear, well-structured answer.

---

**Question:** What is ResFormer, and why does the gating mechanism make the Value Embedding (VE) input-dependent — rather than a fixed per-token addition?

**Answer:**

**ResFormer Background**

ResFormer (Zhou et al., 2024) is a Transformer architecture that enhances information flow through deep networks by adding a *value residual connection*: a direct shortcut from the first layer's value projection V₁ to all subsequent layers, in addition to the standard hidden-state residuals.

The core motivation is that low-level lexical, structural, and token-specific features computed in early layers can become difficult to recover deeper in the network, as the residual stream is repeatedly transformed through depth.

The ResFormer formula for layer n > 1 is:

> **V'ₙ = λₙ₁ · V₁ + λₙ₂ · Vₙ**

where V₁ is the value representation from the first layer, and λ values are learned layer-wise scalar coefficients. A variant called SVFormer takes this further — all layers share the same value embedding from the first layer, reducing KV cache size by nearly half with only a small performance penalty.

**Why the Fixed λ (Static VE) is Limiting**

In the original ResFormer, λ is a single scalar per layer. This means the same amount of V₁ is applied to every token and every attention head within a layer — it is completely *input-agnostic*. The problem is that the usefulness of the first-layer value embedding varies: a token that needs early lexical information benefits from accessing V₁, while another may not need it at all. A per-layer scalar cannot express this variation.

**What the Gate Does (SATFormer's Extension)**

SATFormer replaces the static scalar λₙ with a per-token, per-KV-head gate computed as a single linear projection of the current normalized hidden state, passed through a ReLU activation. Concretely:

> **αₜ,ⱼ⁽ⁿ⁾ = ReLU( xₜ⁽ⁿ⁾ · Wα⁽ⁿ⁾ )ⱼ**
> **V'ₜ,ⱼ,ᵣ = Vₜ,ⱼ,ᵣ + αₜ,ⱼ⁽ⁿ⁾ · Vₜ,ⱼ,ᵣ⁽¹⁾**

This is what makes VE **input-dependent**:

- **Per-token**: different tokens get different amounts of V₁ mixed in, depending on what the current hidden state "says" about that token.
- **Per-head**: different attention heads can specialize — some can lean heavily on V₁, others can ignore it entirely.
- **Exact-zero possible**: the ReLU gate can shut off access to V₁ completely when early information is not useful for that token/head combination.

Non-negativity keeps the pathway interpretable as additive reuse of the first-layer value stream, while exact zeros allow the model to fully disengage from V₁ when early information is unhelpful.

**What the Gate Learns in Practice**

Gate analyses reveal sparse, depth-dependent, head-specific, and token-specific access patterns. Early layers show little access to V₁, while a subset of later-layer heads activates sharply, indicating that the model uses the early-value pathway selectively rather than uniformly.

In short: the gate turns the fixed per-token VE addition of ResFormer into a *context-aware query* — each token, at each head, in each layer, decides how much of the first layer's value representation it needs, based on its current state.

---

**References:**

- [Value Residual Learning (ResFormer) — arXiv 2410.17897](https://arxiv.org/abs/2410.17897)
- [Transformers with Selective Access to Early Representations (SATFormer) — arXiv 2605.03953](https://arxiv.org/abs/2605.03953)
- [MoVE: Mixture of Value Embeddings — arXiv 2601.22887](https://arxiv.org/html/2601.22887v1)
