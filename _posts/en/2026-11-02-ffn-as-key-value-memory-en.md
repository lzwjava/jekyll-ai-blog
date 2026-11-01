---
audio: false
generated: true
image: false
lang: en
layout: post
title: FFN as Key-Value Memory
translated: false
type: note
---

**Question:** How to understand FFN as Key-Value Memory in Transformers?

**Answer:**

Let's build the intuition step by step.

---

## Step 1: Recall the FFN math

```
FFN(x) = ReLU( x · W₁ᵀ ) · W₂
```

- `x` = input token vector (dim: `d_model`)
- `W₁` = first weight matrix (dim: `d_hidden × d_model`)
- `W₂` = second weight matrix (dim: `d_model × d_hidden`)

---

## Step 2: Think of W₁ as a set of "keys"

Each **row of W₁** is a vector in the same space as `x`.

The operation `x · W₁ᵀ` is just computing the **dot product** between the input `x` and every row of W₁.

```
x · W₁ᵀ = [x·k₁, x·k₂, x·k₃, ..., x·kₙ]
```

This is literally asking: **"How similar is my input x to each key kᵢ?"**

A large dot product = key matched. A small dot product = key not matched.

After ReLU, only the **matching keys fire** (negative = 0, positive = kept).

---

## Step 3: Think of W₂ as a set of "values"

Each **column of W₂** is a value vector `vᵢ`.

After ReLU gives you activation scores `[a₁, a₂, ..., aₙ]`, the second step:

```
output = a₁·v₁ + a₂·v₂ + ... + aₙ·vₙ
```

This is a **weighted sum of value vectors** — exactly like a soft lookup table.

---

## Step 4: Concrete analogy

Imagine a dictionary inside the model:

```
"The Eiffel Tower is in ___"
        ↓
Key pattern: [city after landmark, French context, ...]
        ↓ matches neuron #4721
Value vector #4721: points toward "Paris" in vocab space
        ↓
Output: adds "Paris" signal to the prediction
```

Each key correlates with textual patterns in the training examples, and each value induces a distribution over the output vocabulary.

In a sentence ending with '...no substitutes', a specific FFN key activates. If we don't know this key correlates to the pattern 'substitutes at end of sentence' and its value predicts the next likely token, we cannot explain why the model outputs a specific word next.

---

## Step 5: It's a "soft" lookup, not hard lookup

Unlike a hash map where you either find a key or not, this is **differentiable / soft**:

| Hard dictionary | FFN (soft) |
| --- | --- |
| Exact key match | Dot product similarity |
| Returns one value | Returns weighted mix of many values |
| Fixed entries | Learned during training |

The activation `m = f(x · Kᵀ)` can be viewed as a vector that contains the unnormalized coefficient of each memory entry in the FFN block. As a result, the output of the FFN block is a **weighted mixture of memory values**.

---

## Summary diagram

```
Input x
   │
   ▼
x · W₁ᵀ  ←── "Which keys match my input?"
   │           (W₁ rows = keys)
   ▼
ReLU       ←── "Suppress non-matches"
   │
   ▼
scores · W₂ ←── "Retrieve weighted values"
   │             (W₂ columns = values)
   ▼
Output     ←── "Knowledge retrieved"
```

Each row of W₁ is a key (pattern detector), and each column of W₂ is a value used to compose the output. The second projection acts as the corresponding "values" — each column is a contribution that gets added to the output proportional to how strongly its key fired.

---

## Why does this matter?

The output of a feed-forward layer is a **composition of its memories**, which is subsequently refined throughout the model's layers via residual connections to produce the final output distribution.

This means factual knowledge (e.g., "capital of France = Paris") is literally **encoded in the weights of W₁ and W₂** — which is why you can sometimes "edit" a model's factual knowledge by modifying specific FFN weight entries.

**References:**

- [Geva et al. (2021) — Transformer Feed-Forward Layers Are Key-Value Memories](https://arxiv.org/abs/2012.14913)
- [ZeroEntropy — Feedforward Network explainer](https://www.zeroentropy.dev/concepts/feedforward-network/)
- [Geva et al. (2022) — Transformer Feed-Forward Layers Build Predictions by Promoting Concepts](https://arxiv.org/abs/2203.14680)
