---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Loss Bounce Explanation
translated: false
type: note
---

The bounce is baked into the data + architecture. Here's exactly why:

**1. Per-step training loss is a single minibatch sample, not eval loss**

The line `train_loss_f = train_loss.item()` grabs the loss from *one* global batch (65,536 tokens = ~32 code snippets). That's averaged over ~8 gradient accumulation microbatches, but it's still just data points. Eval loss tracks true convergence — this is a noisy proxy.

**2. The EMA window is tiny**

```python
ema_beta = 0.9  # line 563
smooth_train_loss = 0.9 * smooth_train_loss + 0.1 * train_loss_f
```

β=0.9 gives an effective window of ~10 steps. That means:
- A single bad batch contributes ~10% of the displayed loss for the next 10 steps
- A 0.12 range (1.25 ↔ 1.37) on a 10-step window implies raw per-batch variance is much larger — probably ±0.3 or more
- With cosine LR at 0.84, the gradient updates are small, so the loss per-batch is dominated by *which data happened to land in that batch*, not by the weight update

**3. Codeparrot data has high intrinsic variance**

54 parquet shards, each from different GitHub repos. A single 65K-token batch might contain:
- `print("hello world")` → near-zero loss
- Complex async generator with type annotations → high loss
- A docstring → moderate loss

These aren't evenly distributed across batches. The model hasn't memorized anything yet (286M params, 24.7B tokens total data), so each batch is essentially a different "test" and the scores vary.

**4. Gradient noise is real at 65K batch / 286M params**

With 8 microbatches × 4 sequences × 2048 tokens each = 65K tokens per step, the gradient is a noisy estimate of the true gradient on the full data distribution. At 46% through training, the loss is flat enough that gradient noise dominates the direction — the model is oscillating around a region rather than descending a steep slope.

**5. The smoothing doesn't hide it**

If Karpathy's nanoGPT used a wider SMA (say 100 steps) or eval-on-holdout, you'd see a smooth curve. But nanochat logs a ~10-step EMA of training loss. The bounce is just naked sampling noise.

**You can verify this yourself** — when eval runs (every 2K steps per `--eval-every=2000`), the eval loss will be much smoother and consistently lower than the bouncing training loss band. Check the next eval point to confirm.