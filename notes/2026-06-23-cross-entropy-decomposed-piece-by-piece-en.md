---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cross-Entropy Decomposed Piece by Piece
translated: false
type: note
---

**Question:** Break down the cross-entropy formula H(p, q) = −Σₓ p(x) log q(x) = 𝔼_{x∼p}[−log q(x)] piece by piece.

**Answer:**

## Cross-Entropy: Layer by Layer

### What the formula is saying

```
H(p, q) = −Σₓ p(x) log q(x)
```

You have **two distributions**:

- `p(x)` — the **true** distribution (labels, ground truth)
- `q(x)` — the **predicted** distribution (model output, softmax logits)

The formula asks: **on average, how many bits does it take to encode samples drawn from `p`, using a code optimized for `q`?**

---

### Piece-by-piece decomposition

**`−log q(x)`** — the surprisal (self-information) under q

This is the cost of encoding event `x` if you designed your codebook assuming `q`. If your model says `q(x) = 0.01` but `x` actually happens, you pay `−log(0.01) = 6.64 bits`. If `q(x) = 0.99`, you pay almost nothing.

**`Σₓ p(x) · [−log q(x)]`** — weighted average over the true distribution

You're not sampling uniformly. You weight each event's cost by how often it *actually occurs* under `p`. Rare true events contribute little even if your model is wrong about them. Frequent true events dominate.

**`𝔼_{x∼p}[−log q(x)]`** — same thing, expectation notation

Exactly equivalent. Draw `x` from the real world (`p`), then measure surprise under your model (`q`). This is the cleaner way to read it: **expected surprise of model q, under reality p**.

---

### Connection to KL divergence

```
H(p, q) = H(p) + D_KL(p || q)
```

Where:

- `H(p) = −Σₓ p(x) log p(x)` — entropy of true distribution (irreducible)
- `D_KL(p || q) = Σₓ p(x) log [p(x)/q(x)]` — extra cost from using wrong model

When you minimize cross-entropy loss in training, `H(p)` is constant (labels don't change), so you're **purely minimizing KL divergence** — pushing `q` toward `p`.

---

### In classification (the concrete case)

For one-hot labels, `p` is a spike: `p(y=k) = 1`, all others = 0. The sum collapses:

```
H(p, q) = −log q(y_true)
```

That's it. Just the negative log probability the model assigned to the correct class. This is why PyTorch's `CrossEntropyLoss` is:

```python
loss = -torch.log(softmax(logits)[true_class])
# or equivalently:
loss = F.cross_entropy(logits, targets)  # fused for numerical stability
```

---

### Numerical stability note (relevant for your nanoGPT work)

Never compute `log(softmax(x))` in two steps. Use `log_softmax` which computes:

```python
log_softmax(x_i) = x_i - log(Σ exp(x_j))
# = x_i - (max_x + log(Σ exp(x_j - max_x)))  # logsumexp trick
```

In nanoGPT this is exactly `F.cross_entropy` which calls `log_softmax` internally via CUDA kernels — no overflow from `exp(large_logit)`.

---

### One-line intuition

> Cross-entropy measures how **surprised** your model is, on average, by what actually happens. Minimize it → model stops being surprised → model has learned the true distribution.
