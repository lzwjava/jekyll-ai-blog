---
audio: false
generated: true
image: false
lang: en
layout: post
title: "FFN: GPT's Computation and Memory"
translated: false
type: note
---

**Question:** What is the role of the Feed-Forward Network (FFN) in GPT?

**Answer:**

In GPT (and Transformers generally), each layer has two sub-components:

1. **Multi-Head Self-Attention** — figures out *which* tokens to pay attention to
2. **Feed-Forward Network (FFN)** — processes *what* to do with that information

---

### Structure of FFN

A standard FFN is just two linear layers with a non-linearity in between:

```
FFN(x) = ReLU(x · W₁ + b₁) · W₂ + b₂
```

In GPT-style models, the hidden dimension is typically **4× the model dimension**:
- If model dim = 768, FFN hidden dim = 3072

---

### Key Roles of FFN

| Role | Explanation |
|---|---|
| **Non-linearity** | Attention is mostly linear; FFN introduces the non-linear capacity the model needs to learn complex functions |
| **Per-token processing** | FFN operates on each token **independently** (unlike attention which mixes tokens). It refines each token's representation in isolation |
| **Knowledge storage** | Research (Geva et al., 2021 *"Transformer FFN are Key-Value Memories"*) shows FFN layers act as **factual memory** — storing world knowledge in their weights |
| **Feature transformation** | After attention aggregates context, FFN *transforms* that context into useful higher-level features for the next layer |

---

### Intuition

Think of it this way:

- **Attention** = "look around and gather relevant context from other tokens"
- **FFN** = "now *think* about what you've gathered and update your own representation"

The FFN is where much of the model's **parametric knowledge** lives — studies have shown that factual recall (e.g., "Paris is the capital of France") is largely stored and retrieved through FFN weights.

---

### FFN as Key-Value Memory

Each FFN neuron in the first layer acts as a **"key"** that detects a pattern, and the second layer provides the **"value"** to emit. This makes FFN layers function like a soft lookup table over learned associations.

```
Key layer (W₁):  detects input patterns
Value layer (W₂): emits stored "knowledge" when pattern matches
```

---

In summary, the FFN is the **computation and memory engine** of each transformer block — while attention routes information between tokens, the FFN is where the actual "thinking" and knowledge retrieval happens.

**References:**
- [Geva et al. (2021) — Transformer Feed-Forward Layers Are Key-Value Memories](https://arxiv.org/abs/2012.14913)
- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762)
