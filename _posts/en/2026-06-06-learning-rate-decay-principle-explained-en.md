---
audio: false
generated: true
image: false
lang: en
layout: post
title: Learning Rate Decay Principle Explained
translated: false
type: note
---

**Question:** Why does the learning rate decay during the later phase of training? What's the principle behind LR scheduling in nanoGPT-style training?

**Answer:**

Learning rate decay is **optimization landscape management**. Here's the principle:

### The Two Phases of Training

**Early phase (high LR, e.g., 0.47):**

- Loss surface is rough, full of suboptimal valleys. Large steps help you *traverse* quickly and escape poor local minima.
- Model is far from convergence, so large updates are safe — you're not risking oscillation around a good solution.
- The noise from large updates helps exploration.

**Late phase (low LR, e.g., 0.30–0.31):**

- You're entering the convergence basin — close to a decent solution.
- Large steps now *overshoot* good minima and add noise around the solution.
- Smaller steps = finer adjustments, settling into lower loss valleys.
- Lower LR stabilizes training and reduces oscillation.

This is **simulated annealing applied to deep learning**: start hot (explore), cool down (exploit).

### The Code: Cosine Annealing (What nanoGPT Uses)

```python
def get_lr(it, warmup_iters, max_iters, lr_max=0.47, lr_min=0.1):
    """Cosine annealing with linear warmup."""
    # Linear warmup
    if it < warmup_iters:
        return lr_max * it / warmup_iters

    # Cosine decay
    progress = (it - warmup_iters) / (max_iters - warmup_iters)
    return lr_min + 0.5 * (lr_max - lr_min) * (1 + math.cos(math.pi * progress))

# At step 107,319 / 130,000:
# progress ≈ 0.825
# lr ≈ 0.1 + 0.5 * (0.47 - 0.1) * (1 + cos(π * 0.825))
# lr ≈ 0.1 + 0.185 * (1 + cos(2.59)) ≈ 0.1 + 0.185 * (1 - 0.85) ≈ 0.13
```

Wait, your log shows 0.30–0.31, which suggests a different schedule. Likely a **linear decay** or **warmup + polynomial decay**:

```python
def get_lr_linear_decay(it, warmup_iters, total_iters, lr_max=0.47):
    if it < warmup_iters:
        return lr_max * it / warmup_iters
    else:
        decay_progress = (it - warmup_iters) / (total_iters - warmup_iters)
        return lr_max * (1 - decay_progress)  # Simple linear decay

# At 82.55% of training:
# decay_progress ≈ 0.825
# lr ≈ 0.47 * (1 - 0.825) ≈ 0.082  # Hmm, still lower than observed
```

Your schedule might be **cosine with a higher `lr_min`** or use a **warmup + step-based decay**. The exact coefficients matter.

### Why This Matters Empirically

From Andrej Karpathy's nanoGPT and GPT-2/3 papers:

1. **Fixed high LR** → training oscillates and diverges late
2. **Fixed low LR** → slow convergence, gets stuck in early poor minima
3. **Decaying LR** → fast early progress + smooth late convergence

Your loss curve confirms this: dropping from 2.78→2.71 as LR decayed shows the schedule is working. The decay lets you settle into better loss regions without overshooting.

### The Deeper Insight

Decay is really about **matching step size to the curvature of the loss landscape**:

- Early: flat, noisy terrain → large steps OK
- Late: sharp, narrow minima (Hessian eigenvalues are larger) → small steps required

Modern schedulers (cosine, polynomial) are **soft proxies** for this curvature. A "smarter" approach would use adaptive methods (Adam, AdamW), but those have their own tradeoffs.

For nanoGPT-scale training, **cosine annealing with warmup** is the gold standard because it's:

- Simple (no tuning)
- Empirically proven (GPT-2 used it)
- Theoretically sound (covers exploration → exploitation)

---

Your training looks healthy — 0.1 drop in loss over 5 hours at 82% progress is solid. The decay is doing its job. Post your final checkpoint loss?
