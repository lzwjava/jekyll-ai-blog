---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chinchilla Training Token Guidelines
translated: false
type: note
---

**Question:** For a ~200M parameter custom GPT-2 model, using the Chinchilla 20× tokens-per-parameter rule, do we need 4 billion tokens to train it optimally?

**Answer:**

Yes, your math is exactly right.

## The Chinchilla Scaling Law

The Chinchilla paper (Hoffmann et al., 2022) found the optimal compute ratio is roughly:

> **tokens = 20 × parameters**

So for a 200M model:

```
20 × 200,000,000 = 4,000,000,000 = 4 billion tokens
```

That is correct.

---

## Putting It in Context

| Model | Params | Chinchilla-optimal tokens |
|---|---|---|
| GPT-2 small | 124M | ~2.5B tokens |
| **Custom middle** | **200M** | **~4B tokens** |
| GPT-2 medium | 350M | ~7B tokens |

Note: OpenAI's original GPT-2 was trained on ~40B tokens for all sizes — that was actually *over*-trained by Chinchilla standards, which is why modern reproductions (like Karpathy's llm.c) use 10B tokens for 124M and 30B tokens for 350M — those are *more* than Chinchilla-optimal, intentionally, because a slightly over-trained smaller model is often more useful at inference time (better loss per parameter at serving cost).

---

## What 4B Tokens Means Practically

**Dataset:** FineWeb or FineWeb-Edu (100B tokens total) — you only need 4% of it. This is very manageable.

**Training steps at 0.5M tokens/step:**
```
4,000,000,000 / 500,000 = 8,000 steps
```

Compare to 124M nanoGPT which runs ~19,073 steps to see 10B tokens. At Chinchilla-optimal (2.5B tokens), that's only ~5,000 steps for 124M.

**Wall-clock on RTX 4070:**

If your 200M model does roughly ~0.5–0.8 sec/step at `batch_size=2, grad_accum=240`:

```
8,000 steps × ~0.7 sec = ~5,600 sec ≈ 1.5 hours
```

Wait — that seems shockingly fast. The catch: **Chinchilla-optimal is compute-optimal, not loss-optimal.** It tells you the best model to train for a *fixed compute budget*, not the lowest possible loss. To reach a good val loss (~2.9x), you will want to train longer — closer to 10–30B tokens — just like Karpathy does.

---

## Summary

| Question | Answer |
|---|---|
| Is 4B tokens the Chinchilla-optimal amount? | **Yes, exactly** |
| Is 4B tokens enough to get a good model? | **Barely — you'd want 10B+ for quality** |
| Is 4B tokens feasible on a 4070? | **Yes, very manageable** |
| Does more tokens beyond 4B hurt? | **No — over-training improves inference-time efficiency** |

So 4B tokens is your *minimum target*. Aim for **10B tokens** (what Karpathy uses for 124M) as a practical baseline — at 200M that is 2× over-trained by Chinchilla, which is perfectly fine and gives a noticeably better model.