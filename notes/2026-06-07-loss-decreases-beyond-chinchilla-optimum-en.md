---
audio: false
generated: true
image: false
lang: en
layout: post
title: Loss decreases beyond Chinchilla optimum.
translated: false
type: note
---

**Question:** Why does loss continue to decrease even though you're training 45.8x past Chinchilla-optimal (13.1B tokens on 286M params vs. optimal 20:1)?

---

## Answer

You're conflating two different things: **compute-optimal scaling** (Chinchilla) and **when loss actually plateaus**. They're not the same.

### The Core Dynamics

**Chinchilla-optimal is about allocation, not saturation.** It answers: "Given a fixed compute budget, what model/data split is most efficient?" The answer is ~20:1 tokens/param. But that doesn't mean loss stops decreasing past that ratio — it means you're *spending compute less efficiently* (you could've trained a bigger model shorter).

Your model is still losing because:

#### 1. **Excess Model Capacity**

Your 286M model with 12 layers × 6 heads hasn't saturated. The learning curve looks roughly like:

```
loss = a / (tokens)^b + noise
```

where `b ≈ 0.08-0.10` for this scale (empirically, not analytically exact). The loss decreases *smoothly* — it doesn't hit a hard ceiling. At 8.5B tokens (Phase 1), you're still in the steep part of that curve.

The validation bpb at resume (0.810) tells you the model still has generalization capacity. If it was overfitting, val bpb would spike above train loss. It hasn't.

#### 2. **Data Diversity >> Model Capacity**

With BPE vocab (32K tokens), a 2K context window, and 8.5B raw tokens, even fully shuffled, the model encounters an effectively infinite distribution of patterns. You're training on:

```
unique patterns ≈ (vocab_size)^(context_length) >> 8.5B tokens
```

So the model is *still exploring* the data manifold. It's not "running out of things to learn."

#### 3. **Learning Rate Schedule is Still Active**

Look at your schedule:

- Phase 1: Warmup (40 steps), then cosine decay
- Final LR at 130k: **0.20** (20% of initial 0.02 for matrices)
- Phase 2: Entering warmdown at 65% of 200k = 130k steps

You're still in the **main cosine decay** (not yet at the long tail). The model is actively optimizing with meaningful gradient signal. Check your actual LR curve — the model's still training aggressively.

#### 4. **Batch Size Masks Gradient Noise**

With batch_size = 65,536 tokens (very large), gradient noise is low. The model sees cleaner optimization directions. Smaller batches would plateau earlier due to noise floor.

### Why Overfitting Hasn't Kicked In Yet

Overfitting typically emerges when:

1. Val loss > train loss significantly
2. Validation metrics plateau while train loss keeps dropping
3. You reach a hard data repetition limit

None of that's happening. Your CORE metric (0.1916 → 0.1932) and val bpb suggest generalization is still healthy.

### What You Should Expect

**Loss will keep decreasing until one of these hits:**

1. **Learning rate hits noise floor** (end of Phase 2, when LR → 0.001)
2. **Data repetition saturation** — you've seen most token n-grams from your dataset
3. **Overfitting emerges** — val metrics degrade relative to train
4. **Batch size floor** — gradient noise dominates

Given your setup, I'd expect:

- Phase 2 loss: 2.57 → ~2.45-2.50 (diminishing returns, not dramatic drops)
- Val bpb: ~0.78-0.82 (stable)
- By step 200k: loss plateaus, not because you're "overtrained," but because LR is negligible

---

### The Real Insight

Chinchilla says: **"Bigger model + less data = more efficient use of compute for a given budget."**

But it doesn't say: **"Stop training past 20:1; loss won't improve."**

You're training at 45:1 because:

- You want a **smaller, cheaper-to-serve model** (286M is production-grade for edge/mobile)
- You have GPU capacity to throw at it
- Loss still decreasing = return on investment is positive

This is the right call for inference-optimized models (think distillation, LoRA bases, or edge deployment).

---

**References:**

- Chinchilla paper: "Training Compute-Optimal Large Language Models" (Hoffmann et al., 2022) — defines the 20:1 law, but not when loss plateaus
- Empirically: OpenAI/DeepSeek findings show loss ∝ tokens^(-0.08) to ^(-0.10) — no hard saturation, just diminishing returns
- Your metrics: CORE 0.1916, val bpb 0.780 suggest healthy generalization, not overfitting
