---
audio: false
generated: true
image: false
lang: en
layout: post
title: "AdaGrad: Adaptive Subgradient Methods Paper"
translated: false
type: note
---

**Question:** What is the paper at https://jmlr.org/papers/volume12/duchi11a/duchi11a.pdf?

**Answer:** This is the original **AdaGrad** paper — one of the most influential papers in machine learning optimization. Published in the *Journal of Machine Learning Research* in 2011, it introduced the **Adaptive Subgradient** method, better known as **AdaGrad** (Adaptive Gradient Algorithm).

**Authors:** John Duchi (UC Berkeley), Elad Hazan (Technion), and Yoram Singer (Google).

**Core Idea:**
Standard gradient descent uses the same learning rate for every parameter. AdaGrad instead adapts the learning rate *per feature*, based on the historical magnitude of gradients for that feature:

- **Frequently updated features** get a *smaller* learning rate
- **Rarely updated features** get a *larger* learning rate

This is especially powerful for sparse, high-dimensional data (e.g., NLP tasks), where some features appear rarely but carry strong predictive signal — the "needle in a haystack" problem the authors describe.

**Key Contributions:**

1. **Diagonal AdaGrad** — scales each coordinate's learning rate by the inverse square root of the sum of squared past gradients for that coordinate. Efficient and practical in high dimensions.
2. **Full-matrix AdaGrad** — uses the full outer product matrix of gradients for richer geometry, at higher computational cost.
3. **Theoretical regret bounds** — proves the algorithm achieves provably good regret guarantees, competitive with the best fixed proximal function chosen in hindsight.
4. **Practical algorithms** — derives concrete update rules for common regularizers (ℓ₁, ℓ₂, ℓ∞) and domain constraints.

**Why it matters:** AdaGrad was a foundational step toward modern adaptive optimizers. It directly inspired **RMSProp**, **Adam**, and **AMSGrad**, all of which are widely used to train deep neural networks today.

**References:**
- [AdaGrad Paper — JMLR](https://jmlr.org/papers/volume12/duchi11a/duchi11a.pdf)
