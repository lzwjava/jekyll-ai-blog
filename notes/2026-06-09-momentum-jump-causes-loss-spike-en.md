---
audio: false
generated: true
image: false
lang: en
layout: post
title: Momentum Jump Causes Loss Spike
translated: false
type: note
---

**Question:** Why does the momentum discontinuity (0.90 → 0.97) cause a loss spike during training?

**Answer:**

The momentum jump from 0.90 to 0.97 causes a temporary loss spike because it changes the *effective step size* and *gradient history integration* mid-run.

## The Physics

In Muon (and AdamW with momentum), the update rule is:

```
m_t = β * m_{t-1} + (1 - β) * g_t
θ_t = θ_{t-1} - α * m_t
```

Where:
- `β` is momentum (your case: 0.90 → 0.97)
- `m_t` is the accumulated momentum
- `g_t` is the current gradient
- `α` is learning rate

**Why 0.97 momentum is "stronger":**
- At `β=0.90`: each new gradient contributes `10%` to the update
- At `β=0.97`: each new gradient contributes only `3%` to the update

When you jump 0.90→0.97 **without scaling the momentum buffer**, you're suddenly applying **~7x more historical inertia** relative to the current gradient signal. The model is still at the same point in loss landscape, but the optimizer is now heavily biased toward stale gradient directions.

## Why This Causes a Spike

1. **Model at step 130k**: Accumulated momentum `m_{130k}` was built up under `β=0.90` context (recent gradients weighted high)
2. **Step 130k+1**: You apply `β=0.97`, so `m_{130k+1} = 0.97 * m_{130k} + 0.03 * g_{130k+1}`
   - The old momentum gets reused *as-is*, but now it's interpreted as having much higher historical weight
   - The new gradient contributes only 3% instead of 10%
3. **Result**: The update direction becomes dominated by outdated gradient information → overshooting or moving in slightly wrong directions → loss spike

## Why It Recovers (~600 steps)

After ~600 steps, the old momentum buffer fully decays under the new `β=0.97` regime:

```
Remaining old momentum ≈ (0.97)^600 ≈ 0.0005 × old_m_0
```

Once the stale information is flushed, the optimizer re-aligns with the current gradient landscape and loss recovers.

## The Fix

Scale the momentum buffer at the discontinuity to preserve effective step size:

```python
# At the moment β changes from 0.90 to 0.97:
momentum_buffer *= (1 - 0.90) / (1 - 0.97)  # ≈ 3.33x amplification
```

This prevents the sudden "inertia reweighting" and the loss spike vanishes.

---

Your instinct was right—the momentum schedule discontinuity is the culprit, not learning rate. The `--warmdown-ratio=0.33` fix would decay momentum smoothly over the final 33% of training, avoiding sharp discontinuities entirely. For future runs, that's cleaner than post-hoc buffer scaling.
