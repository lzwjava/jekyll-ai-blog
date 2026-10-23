---
audio: false
generated: true
image: false
lang: en
layout: post
title: KL Divergence Explained
translated: false
type: note
---

Question: What is KL divergence?

Answer:

**KL divergence** (Kullback–Leibler divergence) is a measure of how different one probability distribution is from another. It's also called **relative entropy**.

---

### Definition

For two distributions **P** (true/reference) and **Q** (approximate):

$$D_{KL}(P \| Q) = \sum_{x} P(x) \log \frac{P(x)}{Q(x)}$$

For continuous distributions, the sum becomes an integral.

---

### Key Properties

| Property | Detail |
| --- | --- |
| **Non-negative** | $D_{KL}(P \| Q) \geq 0$ always |
| **Zero iff identical** | $D_{KL}(P \| Q) = 0$ only when $P = Q$ |
| **Asymmetric** | $D_{KL}(P \| Q) \neq D_{KL}(Q \| P)$ — it is **not** a true distance metric |

---

### Intuition

Think of it as the **extra bits** needed to encode samples from **P** using a code optimized for **Q** instead. If Q is a bad approximation of P, you waste more bits → higher KL divergence.

---

### Why It Matters

- **Machine Learning**: minimizing $D_{KL}(P \| Q)$ is equivalent to maximizing log-likelihood — used in training language models, VAEs, etc.
- **Variational Inference**: approximates intractable posteriors by minimizing KL between the approximate and true posterior.
- **Reinforcement Learning from Human Feedback (RLHF)**: a KL penalty term keeps the fine-tuned model close to the base model (e.g., how ChatGPT/Claude are trained).
- **Information Theory**: quantifies information loss when using the wrong distribution.

---

### Forward vs. Reverse KL

| | $D_{KL}(P \| Q)$ | $D_{KL}(Q \| P)$ |
| --- | --- | --- |
| Name | Forward KL | Reverse KL |
| Behavior | **Mean-seeking** (Q spreads to cover all of P) | **Mode-seeking** (Q concentrates on one mode of P) |
| Used in | MLE, diffusion models | Variational inference |

---

### Quick Example

Suppose P = [0.9, 0.1] and Q = [0.5, 0.5]:

$$D_{KL}(P \| Q) = 0.9\log\frac{0.9}{0.5} + 0.1\log\frac{0.1}{0.5} \approx 0.531 \text{ nats}$$

Q is a uniform distribution — it's a poor model for the skewed P, so KL is noticeably above 0.

---

References:

- [KL Divergence — Wikipedia](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)
- [KL Divergence for Machine Learning — Towards Data Science](https://towardsdatascience.com/light-on-math-machine-learning-intuitive-guide-to-understanding-kl-divergence-2b382ca2b2a8)
- [Understanding KL Divergence (Lilian Weng's Blog)](https://lilianweng.github.io/posts/2017-08-20-flow-based-deep-generative-models/)
