---
audio: false
generated: true
image: false
lang: en
layout: post
title: Occam's Razor in Machine Learning
translated: false
type: note
---

**Question:** What is Occam's Razor (奥卡姆剃刀)?

**Answer:**

Occam's Razor is the principle: **prefer the simplest explanation that fits the evidence.**

Named after William of Ockham (14th century English friar/philosopher). The Latin formulation:

> *Entia non sunt multiplicanda praeter necessitatem*
> "Entities should not be multiplied beyond necessity."

In plain terms: if two hypotheses explain the data equally well, pick the one with fewer assumptions.

---

**Why it matters in ML/AI (your domain):**

- **Regularization** is literally Occam's Razor implemented mathematically — L1/L2 penalties punish model complexity, biasing toward simpler weight configurations that generalize better.
- **MDL (Minimum Description Length)** — the best model is the one that compresses the data most. Shorter description = simpler model = Occam wins.
- **Bayesian interpretation** — simpler models have higher prior probability. The evidence term (marginal likelihood) naturally penalizes over-parameterized models even without an explicit prior.
- **Bias-variance tradeoff** — Occam's Razor is the intuition behind why you shouldn't overfit: a complex model "explains" training noise as signal.

---

**It's a heuristic, not a law.** Neural nets violate the naive version — overparameterized models generalize surprisingly well (double descent). The razor applies to *hypotheses*, not raw parameter count.