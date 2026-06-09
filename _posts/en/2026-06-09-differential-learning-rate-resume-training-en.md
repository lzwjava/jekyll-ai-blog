---
audio: false
generated: true
image: false
lang: en
layout: post
title: Differential Learning Rate Resume Training
translated: false
type: note
---

**Question:** Explain the nanochat training command — architecture, hyperparameters, and training strategy.

**Answer:**

You're resuming a 12-layer transformer from step 200k to 300k on RTX 4070. Here's what's happening:

## Architecture

```python
depth=12              # 12 transformer layers
aspect-ratio=64      # d_model = 64 * head_dim = 64 * 128 = 8192 hidden dim
head-dim=128         # 128-dim per attention head → ~64 heads
max-seq-len=2048     # 2K context window
window-pattern=L     # Local/causal attention (not full)
```

The `aspect-ratio` is a width multiplier. With 128-dim heads, 64 heads gives you 8,192-dim hidden dimension — a medium-sized model (~60-100M params depending on vocab size).

## Batch Dynamics

```python
device-batch-size=8        # 8 samples on RTX 4070
total-batch-size=65536     # Gradient accumulation: 65536/8 = 8,192 microbatches
                           # (or multi-machine, but single GPU here)
```

You're accumulating gradients over 8,192 forward passes before one weight update. On RTX 4070 (12GB), batch size 8 fits comfortably; gradient accumulation hits the 65K target without OOMing.

## The Unusual Part: Differential Learning Rates

```python
embedding-lr=0.018      # Token embeddings
unembedding-lr=0.00048  # Output projection (embedding → logits)
matrix-lr=0.0012        # Transformer weights (Q/K/V, FF)
scalar-lr=0.03          # Layer norms, biases
```

This is **not** standard. You're treating parameter types differently:

- **Scalars (layer norms, biases)**: 0.03 — **aggressive**, allows quick adaptation
- **Embeddings**: 0.018 — **moderate**, embeddings are finicky (affects all token predictions)
- **Unembedding**: 0.00048 — **tiny**, output projection is stable, doesn't need much movement
- **Matrices (core weights)**: 0.0012 — **conservative**, weights are sensitive after 200k steps

This is a **resume strategy** — you're not starting fresh, so you're being selective about what changes. Scalars can move fast; core weights should barely move.

## Schedule (Flat, No Warmup)

```python
warmup-steps=0           # Skip warmup (already converged from 0→200k)
warmdown-ratio=0.0       # No decay — hold LR constant for 200k→300k
final-lr-frac=0.05       # Ignored (no decay schedule)
```

You're training **steps 200k–300k** with **constant LR**. No learning rate schedule. This means:

- Late-stage fine-tuning (already in a good part of loss landscape)
- Constant exploration (don't decay toward convergence)
- Betting that the LRs are tuned for continued improvement

## Regularization

```python
weight-decay=0.28       # 28% weight decay — **very high**
```

This is aggressive. Weight decay penalizes large weights:

```
loss = model_loss + 0.28 * sum(w²)
```

Pushes the model toward sparse, interpretable weights. Good for preventing overfitting on small datasets or avoiding feature drift in resumed training.

## Why This Strategy

1. **Resume from 200k**: You've already hit a stable point. No warmup needed.
2. **Flat schedule**: You're not converging — you're continuing to improve. Decay would slow progress unnecessarily.
3. **Differential LRs**: Embeddings/outputs are noisy after 200k steps; core weights are already tuned. This lets you refine selectively.
4. **High weight decay**: Likely prevents catastrophic forgetting or runaway scaling of weights during the resume.

## Compute

```
Total iterations: 100k more (200k → 300k)
Device batch: 8
Effective batch: 65,536
~33 hours on RTX 4070
```

That's ~3 iterations/sec — reasonable for a 8K hidden dim model with 2K context on a single 4070.

---

**One question**: What does `window-pattern=L` do exactly? If it's local attention (e.g., sliding window), that's a massive speedup vs. full attention. If it's something else (learned pattern?), let me know — the nanochat codebase isn't publicly obvious on that detail.
