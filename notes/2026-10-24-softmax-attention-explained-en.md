---
audio: false
generated: true
image: false
lang: en
layout: post
title: Softmax Attention Explained
translated: false
type: note
---

**Question:** What is Softmax Attention?

**Answer:**

Softmax Attention is the core attention mechanism used in Transformer models, introduced in the landmark 2017 paper *"Attention Is All You Need"*. It allows a model to dynamically focus on relevant parts of an input sequence when producing an output.

---

## The Core Formula

Given three matrices derived from the input — **Query (Q)**, **Key (K)**, and **Value (V)** — the attention output is:

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right) V$$

---

## Step-by-Step Breakdown

**1. Compute Raw Scores (Dot Products)**
Each query vector is compared against all key vectors via dot product:

$$\text{score}_{ij} = Q_i \cdot K_j$$

This measures how "relevant" position *j* is to position *i*.

**2. Scale**
Scores are divided by $\sqrt{d_k}$ (the dimension of the key vectors). Without this, large dot products push softmax into regions with near-zero gradients, making training unstable.

**3. Apply Softmax**
Convert raw scores into a probability distribution over positions:

$$\alpha_{ij} = \frac{e^{\text{score}_{ij}}}{\sum_k e^{\text{score}_{ik}}}$$

Each row now sums to 1 — this is the "attention weight" vector.

**4. Weighted Sum of Values**
Use the attention weights to take a weighted combination of value vectors:

$$\text{output}_i = \sum_j \alpha_{ij} \cdot V_j$$

---

## Why "Softmax"?

The softmax function is what makes attention *soft* (differentiable, gradient-friendly) rather than *hard* (argmax, non-differentiable). It assigns non-zero weight to all positions, letting the model blend information from multiple positions at once.

---

## Key Properties

| Property | Detail |
| --- | --- |
| **Quadratic complexity** | $O(n^2)$ in sequence length — the main bottleneck |
| **Permutation equivariant** | No inherent notion of order (positional encodings added separately) |
| **Multi-head** | Run $h$ attention heads in parallel, then concatenate |
| **Masking** | Causal mask (set future positions to $-\infty$ before softmax) for autoregressive models |

---

## Limitations (and Why Alternatives Are Being Explored)

- **Quadratic memory/compute** in sequence length $n$ makes long contexts expensive
- This has motivated alternatives like **Linear Attention**, **Flash Attention** (an efficient implementation), **GQA** (Grouped Query Attention), and **MLA** (Multi-head Latent Attention used in DeepSeek)

---

**References:**

- [Attention Is All You Need — Vaswani et al., 2017](https://arxiv.org/abs/1706.03762)
- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
- [Flash Attention — Efficient Exact Attention](https://arxiv.org/abs/2205.14135)
- [Lilian Weng — Attention? Attention!](https://lilianweng.github.io/posts/2018-06-24-attention/)
