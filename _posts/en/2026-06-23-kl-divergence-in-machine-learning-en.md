---
audio: false
generated: true
image: false
lang: en
layout: post
title: KL Divergence in Machine Learning
translated: false
type: note
---

**Question:** What is KL divergence?

**Answer:**

KL divergence (Kullback-Leibler divergence) measures how much one probability distribution differs from another. It's the backbone of modern LLM training — shows up in cross-entropy loss, RLHF, DPO, and VAEs.

## Definition

$$D_{KL}(P \| Q) = \sum_x P(x) \log \frac{P(x)}{Q(x)}$$

For continuous distributions:

$$D_{KL}(P \| Q) = \int P(x) \log \frac{P(x)}{Q(x)} dx$$

Read as: **"how much extra bits does Q cost you, when the true distribution is P?"**

## Intuition

Think of it as the *surprise penalty* when you use the wrong distribution:

- If Q = P exactly → KL = 0
- If Q assigns low probability where P assigns high → KL blows up
- **Asymmetric**: $D_{KL}(P \| Q) \neq D_{KL}(Q \| P)$

## Connection to Cross-Entropy

This is the key insight for LLM training:

$$H(P, Q) = H(P) + D_{KL}(P \| Q)$$

Cross-entropy = entropy of true distribution + KL divergence. Since $H(P)$ is constant (you don't control the data), **minimizing cross-entropy loss = minimizing KL divergence from model Q to data distribution P**.

That's why language model training works.

## Forward vs Reverse KL

| | $D_{KL}(P \| Q)$ | $D_{KL}(Q \| P)$ |
|---|---|---|
| Name | Forward KL / "I-projection" | Reverse KL / "M-projection" |
| Behavior | Q spreads to cover all of P ("mean-seeking") | Q collapses onto one mode of P ("mode-seeking") |
| Used in | MLE / cross-entropy training | VAE encoder, RL PPO KL penalty |

## In RLHF / PPO

The KL term in PPO prevents the policy from drifting too far from the reference model:

$$\mathcal{L} = \mathbb{E}\left[r(x, y)\right] - \beta \cdot D_{KL}(\pi_\theta \| \pi_\text{ref})$$

`β` controls the tradeoff between reward maximization and staying close to the SFT model. Too low → reward hacking. Too high → no learning.

## In DPO

DPO implicitly optimizes KL without an explicit RL loop — the closed-form solution to the PPO objective with KL constraint is exactly what DPO's loss computes.

## Minimal Python

```python
import numpy as np

def kl_divergence(p, q):
    # P is true, Q is approximate
    p, q = np.array(p), np.array(q)
    # Clip to avoid log(0)
    return np.sum(p * np.log(p / (q + 1e-10) + 1e-10))

p = [0.4, 0.4, 0.2]   # true distribution
q = [0.3, 0.4, 0.3]   # model's distribution

print(kl_divergence(p, q))   # ~0.026 nats
print(kl_divergence(q, p))   # ~0.027 nats — different!
```

## In PyTorch (what you actually use)

```python
import torch
import torch.nn.functional as F

# Both in log-space for numerical stability
log_q = F.log_softmax(logits, dim=-1)
p = target_distribution  # soft labels

# PyTorch's KLDivLoss expects log-probabilities for input
loss = F.kl_div(log_q, p, reduction='batchmean')
```

Note: PyTorch's `kl_div` takes `log(Q)` as input and `P` as target — easy gotcha.

## Why It's Non-Symmetric

$$D_{KL}(P \| Q) = 0.026, \quad D_{KL}(Q \| P) = 0.027$$

Small here but catastrophic when distributions have disjoint support. In VAEs, the reverse KL $D_{KL}(Q \| P)$ pushes the encoder posterior toward the prior — it *ignores* regions where Q=0, leading to posterior collapse in some architectures.

## Practical Summary

| Context | Which KL | Why |
|---|---|---|
| LLM cross-entropy loss | $D_{KL}(P_{data} \| P_{model})$ | MLE = forward KL |
| PPO penalty | $D_{KL}(\pi_\theta \| \pi_{ref})$ | Reverse, prevents drift |
| VAE | $D_{KL}(q_\phi(z\|x) \| p(z))$ | Reverse, regularizes latent |
| Distillation | $D_{KL}(P_{teacher} \| P_{student})$ | Forward, match teacher |
