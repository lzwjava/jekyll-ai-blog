---
audio: false
generated: true
image: false
lang: en
layout: post
title: Muon Optimizer for LLMs
translated: false
type: note
---

Question: What is the Muon optimizer in the context of LLMs?

Answer:

The **Muon optimizer** is a recently developed gradient-based optimizer designed to improve training efficiency and performance for large language models. Here's a breakdown:

**Core Idea**

Muon stands for **MomentUm Orthogonalized by Newton-schulz**. It applies an orthogonalization step to the momentum buffer before using it as a gradient update — meaning the weight updates are made approximately orthogonal, which helps maintain stable, well-conditioned gradient steps.

**How It Works**

1. Compute momentum (like standard SGD with momentum)
2. Apply a **Newton-Schulz iteration** to orthogonalize the momentum matrix
3. Use the orthogonalized update as the effective gradient step

This is mathematically related to steepest descent under the **spectral norm** rather than the L2 norm, giving it better curvature-awareness without needing to compute or store a full Hessian.

**Why It Matters for LLMs**

- **Better than AdamW in some regimes** — several experiments have shown Muon can match or outperform AdamW with fewer tokens or lower loss at the same compute budget
- **More stable updates** — orthogonal updates avoid redundant or collinear gradient steps
- **Memory efficient** — no need to store second-moment estimates like Adam does

**Limitations**

- Best suited for **matrix-shaped parameters** (attention/MLP weights); bias and embedding layers still typically use Adam
- Relatively new — less battle-tested at the very largest scales
- Hyperparameter sensitivity is still being studied

**Who's Using It**

It gained attention from Keller Jordan's work and has been explored by teams at various labs as a potential AdamW replacement, especially in mid-scale LLM training runs.

References:
- [Muon: An optimizer for hidden layers in neural networks (Keller Jordan)](https://kellerjordan.github.io/posts/muon/)
- [Muon Optimizer – GitHub](https://github.com/KellerJordan/Muon)
- [Newton-Schulz Iteration – Wikipedia](https://en.wikipedia.org/wiki/Polar_decomposition#Algorithms)