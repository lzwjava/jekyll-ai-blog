---
audio: false
generated: true
image: false
lang: en
layout: post
title: Adam Optimization Algorithm Explained
translated: false
type: note
---

**Question:** What is the Adam optimization algorithm, as described in the original paper?

**Answer:**

## Overview

Adam (Adaptive Moment Estimation) is an algorithm for first-order gradient-based optimization of stochastic objective functions, based on adaptive estimates of lower-order moments. It is computationally efficient, has little memory requirements, is invariant to diagonal rescaling of gradients, and is well suited for problems that are large in terms of data and/or parameters.

The name "Adam" is derived from **Ada**ptive **M**oment estimation. The method combines the advantages of two previously popular methods: AdaGrad, which works well with sparse gradients, and RMSProp, which works well in non-stationary settings.

---

## Core Idea: Two Moments

Adam tracks **two moving averages** of the gradients at each step *t*:

| Symbol | Name | What it tracks |
|--------|------|----------------|
| **mₜ** | 1st moment | Exponential moving average of the gradient (mean) |
| **vₜ** | 2nd moment | Exponential moving average of the squared gradient (variance) |

The moving averages are estimates of the 1st moment (mean) and 2nd raw moment (uncentered variance) of the gradient. The hyper-parameters β₁ and β₂ ∈ [0, 1) control the exponential decay rates of these moving averages.

---

## The Algorithm Step-by-Step

At each timestep *t*:

1. **Compute gradient:** `gₜ = ∇f(θₜ₋₁)`
2. **Update 1st moment:** `mₜ = β₁·mₜ₋₁ + (1−β₁)·gₜ`
3. **Update 2nd moment:** `vₜ = β₂·vₜ₋₁ + (1−β₂)·gₜ²`
4. **Bias correction:**
   - `m̂ₜ = mₜ / (1 − β₁ᵗ)`
   - `v̂ₜ = vₜ / (1 − β₂ᵗ)`
5. **Update parameters:** `θₜ = θₜ₋₁ − α · m̂ₜ / (√v̂ₜ + ε)`

Good default settings are **α = 0.001**, **β₁ = 0.9**, **β₂ = 0.999**, and **ε = 10⁻⁸**.

---

## Why Bias Correction?

The moving averages are initialized as vectors of zeros, leading to moment estimates that are biased towards zero — especially during the initial timesteps and especially when the decay rates are small (i.e., βs are close to 1). This initialization bias is counteracted by dividing by `(1 − β₁ᵗ)` and `(1 − β₂ᵗ)` to yield bias-corrected estimates m̂ₜ and v̂ₜ.

This is a key difference from RMSProp, which lacks this correction. Not correcting the bias with β₂ close to 1 leads to very large stepsizes and often divergence.

---

## Intuition: Why Does It Work?

The update rule `m̂ₜ / √v̂ₜ` can be thought of as a **signal-to-noise ratio**:

- **m̂ₜ** = the direction we want to move (mean gradient)
- **√v̂ₜ** = how uncertain we are about that direction (gradient variance)

With a smaller SNR the effective stepsize will be closer to zero — a desirable property, since a smaller SNR means greater uncertainty about whether the direction of m̂ₜ corresponds to the true gradient. As optimization approaches an optimum, the SNR tends toward 0, leading to smaller effective steps: a form of automatic annealing.

---

## Convergence

Adam achieves an **O(√T)** regret bound, comparable to the best known results under the online convex optimization framework. The average regret R(T)/T = O(1/√T), meaning `lim T→∞ R(T)/T = 0`.

---

## Extension: AdaMax

AdaMax is a variant of Adam based on the infinity norm. Rather than dividing by the L2-norm-based v̂ₜ, it uses `uₜ = max(β₂·uₜ₋₁, |gₜ|)`, a simpler recursion that does not require bias correction. The bound on parameter updates becomes simply `|Δₜ| ≤ α`.

---

## Summary Diagram

```
Gradient gₜ
    ↓
1st moment mₜ  →  bias-corrected m̂ₜ  ─┐
                                         ├─→  θ update = α · m̂ₜ / (√v̂ₜ + ε)
2nd moment vₜ  →  bias-corrected v̂ₜ  ─┘
```

Adam essentially gives **each parameter its own adaptive learning rate**, scaling fast-changing parameters with smaller steps and slow-changing ones with larger steps — making it very robust across diverse architectures.

---

**References:**

- [Adam: A Method for Stochastic Optimization (Kingma & Ba, 2015)](https://arxiv.org/pdf/1412.6980)
