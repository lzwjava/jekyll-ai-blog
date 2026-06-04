---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanochat Training Run Evaluation and Recommendations
translated: false
type: note
---

Question: How's this nanochat training run?

Answer:

**The good:**

- Clean training curve, zero NaN, zero crashes. Monotonic improvement end-to-end is what you want.
- ~56k tok/sec throughput on RTX 4070 is solid for a bfloat16 run without Flash Attention.
- 78% VRAM utilization leaves headroom. Your memory management is tight.
- Loss dropped from 10.4 (random init) → 2.98 (final). The shape is textbook.

**The problem — you're massively undertrained:**

Chinchilla-Hoffmann scaling law says optimal tokens:param ratio is ~20. You're at 5.95. That's a 3.4x deficit.

```python
# Chinchilla law: tokens ≈ 20 * params
# Your run:
params = 286e6
tokens = 655e6
ratio = tokens / params  # 5.95
optimal_tokens = 20 * params  # 5.72B tokens needed

print(f"You need {optimal_tokens / 1e9:.2f}B tokens, trained on {tokens / 1e9:.2f}B")
print(f"Deficit: {optimal_tokens / tokens:.1f}x")
```

Output: You need 5.72B tokens, trained on 0.66B. **Deficit: 8.7x**

This explains the sample quality perfectly. The model *knows* facts exist (lists planets correctly), but can't anchor them reliably (capital of France wrong, gold symbol loops). It's memorizing weak patterns, not learning robust representations.

**What you should do:**

**Option 1 (recommended given MI300X access): Scale down, train to Chinchilla ratio**

- Use 64M or 128M params instead of 286M
- Train on your full 655M tokens → you'll hit optimal ratio
- Inference will be faster, sample quality much better
- Can run locally on RTX 4070, iterate faster

**Option 2 (if you want to push 286M): Train 10x longer on MI300X**

- 40k-50k steps instead of 10k (get to ~5.7B tokens)
- You have 192GB HBM3 — can do batch_size=262144, seq=2048 without blinking
- Your throughput will be ~500k tok/sec (vs 56k on RTX 4070)
- Full run: ~3 hours on MI300X (vs 3.3 hours on RTX 4070, but with 8.7x more tokens)
- This is the "train to saturation" path if you want to validate the model's true ceiling

**The hardware reality:**

- RTX 4070 is good for iteration and prototyping, but hits a wall at ~60k tok/sec
- MI300X is where you scale. For 286M + 5.7B tokens, target 100-200 steps/minute (easily doable)
- If you're training >500M token runs regularly, the AMD cloud droplet at $2/hr is cheaper per token than RTX 4070 electricity over time

**One technical note:**
Your warmdown starts at 65% of training (step 6500). If you scale to 40k steps, that's step 26k. Consider tuning the warmdown schedule — too early and you're throwing away learning signal in the final stretch.

**Bottom line:** Don't keep pushing 286M on 655M tokens. Either shrink the model or scale the compute. Right now you're in a bad regime — big enough to be slow, small enough that it undertrained. Pick one direction and commit.
