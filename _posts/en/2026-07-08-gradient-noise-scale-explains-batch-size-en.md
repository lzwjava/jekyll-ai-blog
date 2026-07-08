---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gradient Noise Scale Explains Batch Size
translated: false
type: note
---

Question: What's the mechanism behind the trick "if you have large VRAM, increasing batch size during the convergence-bottleneck phase gives better results" — why does this work?

Answer:

## The core idea: gradient noise scale grows as loss decreases

The gradient noise scale is essentially a measure of the signal-to-noise ratio of gradients across training examples, and it can approximately predict the largest efficient batch size for a wide range of tasks. The critical finding from McCandlish et al. (OpenAI, 2018): the noise scale increases as the loss decreases over a training run, and depends on the model size primarily through improved model performance.

This directly explains your observation. Early in training, a small batch is data-efficient because per-example gradients are highly correlated (redundant). As you approach a plateau/bottleneck, per-example gradients start disagreeing more relative to the shrinking "true" gradient signal — so a small batch becomes a noisy, low-SNR estimate of the direction you should actually move. Increasing batch size averages out that noise and gives you a cleaner descent direction, letting you make real progress again instead of the optimizer randomly walking near the plateau.

## The math

Take a second-order (quadratic) expansion of the loss around the current point $\theta$, with true minimum $\theta^*$ and Hessian $H$:

$$L(\theta) \approx L^* + \tfrac{1}{2}(\theta-\theta^*)^T H (\theta-\theta^*)$$

The **true gradient**: $g_{\text{true}} = H(\theta - \theta^*)$

A **minibatch gradient** estimate of size $B$: $\hat g = g_{\text{true}} + \epsilon$, where $\epsilon \sim \mathcal{N}(0, \Sigma/B)$ and $\Sigma$ is the per-example gradient covariance (roughly constant, determined by the dataset — not by how close you are to the optimum).

- As you approach the minimum, $\theta \to \theta^*$, so $\|g_{\text{true}}\| \to 0$.
- But $\Sigma$ (the noise from sample-to-sample variance) doesn't shrink at the same rate.
- **SNR = $\|g_{\text{true}}\|^2 / \text{tr}(\Sigma)/B$ collapses** near convergence for a fixed $B$.

McCandlish's simplified noise scale (well-conditioned Hessian assumption), essentially a measure of how large the gradient is compared to the noise:

$$B_{\text{noise}} = \frac{\text{tr}(\Sigma)}{\|G\|^2}$$

where $G$ is the true (population) gradient. This is literally the "critical batch size" — McCandlish et al. (2018) suggest that a critical batch size (CBS), below which training will not substantially degrade loss, can be estimated based on the gradient noise scale during training. And this correspondence between the CBS and the gradient noise scale is the variance of the per-example gradients from the training distribution.

Since $B_{\text{noise}} \propto 1/\|G\|^2$ and $\|G\| \to 0$ near the loss plateau, **the useful/critical batch size mechanically grows as loss decreases**. That's the whole trick, formalized.

## Why this manifests as "convergence bottleneck → bump batch size helps"

Less noisy gradient estimates allow SGD-type optimizers to take larger steps, leading to convergence in a smaller number of iterations. Concretely, during a plateau:

1. Small-batch gradient direction is dominated by per-example noise, not curvature signal.
2. Optimizer effectively "vibrates" around a local basin rather than descending it — you see loss oscillate or crawl.
3. Increasing $B$ (via larger actual batch, or gradient accumulation if VRAM-bound only on activations) shrinks $\Sigma/B$, restoring SNR, restoring effective progress per step.
4. You *don't* need to keep raising LR proportionally at this stage the way early-training linear-scaling rules suggest — the point is variance reduction, not step-size scaling.

This is why GPT-3 style training ramps batch size over the course of training (32K → 3.2M tokens) rather than fixing it — it tracks the growing critical batch size instead of guessing one number up front.

## Practical estimator (usable in your own MI300X/nanochat runs)

You don't need the full Hessian. McCandlish's simple estimator uses two batch sizes and the variance-of-gradient-norm trick:

```python
import torch

def per_example_grads(model, loss_fn, x, y):
    """Returns list of per-sample gradient vectors (flattened)."""
    grads = []
    for i in range(x.size(0)):
        model.zero_grad()
        loss = loss_fn(model(x[i:i+1]), y[i:i+1])
        loss.backward()
        g = torch.cat([p.grad.flatten() for p in model.parameters() if p.grad is not None])
        grads.append(g.clone())
    return torch.stack(grads)  # [B, D]

def noise_scale_estimate(model, loss_fn, x, y, b_small, b_big):
    """
    Two-batch-size estimator (McCandlish et al. 2018, Appendix A).
    Run this periodically (e.g. every N steps) during training.
    """
    g_all = per_example_grads(model, loss_fn, x[:b_big], y[:b_big])  # [b_big, D]

    g_small = g_all[:b_small].mean(dim=0)
    g_big   = g_all.mean(dim=0)

    norm_small_sq = g_small.pow(2).sum().item()
    norm_big_sq   = g_big.pow(2).sum().item()

    # unbiased estimates of true grad^2 (G2) and noise scale (S)
    G2 = (b_big * norm_big_sq - b_small * norm_small_sq) / (b_big - b_small)
    S  = (norm_small_sq - norm_big_sq) / (1.0 / b_small - 1.0 / b_big)

    B_noise = S / G2
    return B_noise, G2, S
```

Track `B_noise` alongside your loss curve. When you see it climbing sharply near a plateau (i.e. `B_noise` approaching or exceeding your current effective batch size), that's your empirical signal to bump `B` — either the real micro-batch (you have room on 192GB HBM3) or gradient accumulation steps. This is more principled than eyeballing "the loss looks stuck, let's throw more batch at it."

## One caveat worth internalizing before you over-apply this

While their method has been adopted in practice, e.g., when training GPT-3, strong assumptions are required to justify gradient noise as a proxy for the CBS, which makes it unclear whether their approach should be trusted in practice, limiting its applicability. A 2025 NeurIPS paper revisits this and proposes a more direct empirical CBS estimator rather than trusting the noise-scale proxy blindly — worth reading if you're tuning this for DeepSeek v4 MoE-scale runs where per-expert gradient statistics are messier than the dense-model case McCandlish studied.

References:

- [An Empirical Model of Large-Batch Training (McCandlish et al., 2018)](https://arxiv.org/abs/1812.06162)
- [Critical Batch Size Revisited (NeurIPS 2025)](https://arxiv.org/html/2505.23971v1)
