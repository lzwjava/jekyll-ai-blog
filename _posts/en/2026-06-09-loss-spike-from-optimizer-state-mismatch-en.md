---
audio: false
generated: true
image: false
lang: en
layout: post
title: Loss Spike from Optimizer State Mismatch
translated: false
type: note
---

**Question:** Why did loss spike when resuming training with a flat learning rate schedule (after using a decaying schedule in the previous run)?

---

## Answer

You've diagnosed it correctly — this is an **optimizer state + schedule mismatch** issue. Here's the mechanics:

### Why the Spike Happens

Your optimizer's adaptive buffers (`v_t` in Adam, accumulated momentum in Muon) were calibrated under a *decaying* LR regime. Specifically:

1. **During first run** (steps 0 → 200,472):
   - LR started high, decayed over time
   - Adaptive factors (e.g., `1/sqrt(v_t)` in Adam) grew as a *compensation* for falling LR
   - Velocity buffers reached equilibrium *under the assumption* that LR would keep decaying

2. **At resume** (step 200,472 → 300,000):
   - LR is suddenly **flat and high** (you set `--warmdown-ratio=0`)
   - Velocity buffers don't reset — they still carry the accumulated history
   - The product: **same adaptive scaling × higher LR = larger effective step size**
   - Gradients hit harder → loss spikes as you overshoot minima

This is especially pronounced with **Muon** (if that's your optimizer), because Muon's scaling directly normalizes gradient norms. When LR context changes abruptly, the norm-based scaling becomes misaligned.

### Concrete Fix

Don't break the schedule continuity. Use one of these:

**Option A: Extend the decay** (recommended)

```bash
# Resume with natural schedule continuation
# Assume first run did: --warmup-steps=1000 --final-lr-ratio=0.1 or similar
# At step 200,472, effective LR was already lower
# Continue from there with the same decay law

python train.py \
  --resume checkpoint.pt \
  --warmup-steps=1000 \
  --final-lr-ratio=0.01 \
  --lr=3e-4 \
  # This keeps LR *decaying* for remaining 100k steps
  # Velocity buffers stay in sync with effective step size
```

**Option B: If you must go flat, do a micro-warmup**

```bash
# Temporary 5-10k step ramp to let adaptive factors re-equilibrate
python train.py \
  --resume checkpoint.pt \
  --warmup-steps=5000 \
  --final-lr-ratio=1.0 \
  # Ramps LR up slightly over 5k steps
  # Gives optimizer time to adjust v_t buffers
  # Then stays flat
```

**Option C: Inspect and validate schedules** (diagnostic)

```python
# Before resuming, check what effective LR you're about to apply
import json

# Load checkpoint
ckpt = torch.load('checkpoint.pt')
state_dict = ckpt['optimizer_state_dict']

# If using AdamW, check accumulated 'exp_avg_sq' (v_t)
# A healthy v_t should be order-of-magnitude consistent with current LR
# If v_t is tiny (from long decay), flat LR will cause spike

v_values = [v['exp_avg_sq'].mean().item() for v in state_dict['state'].values()]
print(f"Mean v_t: {sum(v_values)/len(v_values):.6f}")
```

### Why It Might Settle

It *may* converge back down over a few thousand steps because:

- Adaptive factors (v_t) will grow again with the new data
- The optimizer rebalances
- But you're losing convergence time and may land at a worse minimum

### My Recommendation

**Go with Option A** — extend the decay curve. Your first 200k steps tell you what LR schedule works for *this model on this data*. Don't flip the table midway. If you used linear decay `LR(t) = LR_init * (1 - t/T_total)`, just continue it:

```bash
# Conceptually:
# LR at step 200k was ~0.3e-4 (if you started at 3e-4)
# For remaining 100k steps, keep decaying toward 0.01e-4
```

This keeps momentum/velocity buffers aligned and avoids the transient loss spike entirely.

---

**Question for you:** What was your first run's `--warmup-steps` and `--final-lr-ratio`? If you paste those, I can write the exact resumed command.
