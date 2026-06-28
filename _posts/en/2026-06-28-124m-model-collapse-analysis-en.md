---
audio: false
generated: true
image: false
lang: en
layout: post
title: 124M Model Collapse Analysis
translated: false
type: note
---

Your 124M model is doing exactly what you'd expect at that scale/training budget: it nails the **in-distribution prefix** then collapses into **token-level degeneration**.

## What actually happened

The output has two distinct regimes:

**1. Coherent region (the BST):** This is your prompt continuation. The model produced syntactically perfect, idiomatic Java — correct `insertRec` recursion, proper null handling, balanced braces. This is *memorization-adjacent generalization*: BST implementations are extremely common in GitHub-Java training data, so the model is sampling from a sharp, low-entropy distribution. Nearly every next-token is high-probability. Easy mode.

**2. The collapse (starts at `boolean search`):** Look at the exact failure point:

```java
boolean search(int key) {
    return;        // ← first error: void return in a boolean method
}
```

Once it emits a *semantically invalid* token, the model is now conditioning on a context that **doesn't exist in training data**. No real Java file has `boolean search(int key) { return; }`. So the conditional distribution `P(x_t | x_<t)` flattens — the model has no sharp signal for what comes next because it's off-manifold. From there it's a feedback loop: garbage context → flat distribution → garbage token → more garbage context.

The `.S.S.S.S` repetition is the classic signature. With `top_k=200` and `temp=0.8`, once the distribution is flat, `.S` likely sits at a local probability peak (period + capital S is common in identifiers like `this.S...`), so the sampler keeps re-selecting into the same attractor basin. This is the degeneration Holtzman et al. described — it happens even with sampling, not just greedy decoding.

## Why this is the expected ceiling

At 124M params trained on a constrained code corpus, the model has enough capacity to learn:

- Local syntax (braces, keywords, common method shapes)
- High-frequency patterns (textbook algorithms)

But **not** enough to maintain:

- Long-range semantic consistency (return type ↔ return statement)
- Type coherence across a method body
- A stable representation that resists off-manifold drift

The forward pass has no mechanism to "back out" of a bad token once committed — autoregressive decoding is greedy in the sense that there's no lookahead or backtracking. GPT-2-small simply lacks the representational depth to keep the semantic state vector coherent past ~30-50 tokens of novel structure.

## What to actually do about it

**Diagnostic first — quantify the collapse.** Add per-token logprob/entropy logging to `sample.py`:

```python
# in model.py generate(), after computing logits
probs = F.softmax(logits, dim=-1)
entropy = -(probs * probs.clamp_min(1e-9).log()).sum(-1)
# log entropy[0].item() each step
```

Plot entropy vs. position. You'll see it spike right at the `return;` token. That spike *is* the model telling you it lost the plot. This is the single most useful thing to add.

**Then, levers in priority order:**

1. **Lower `top_k` / add `top_p`.** `top_k=200` is huge for code — it keeps 200 candidates alive even when only 2-3 are valid. Try `top_k=40` or nucleus `top_p=0.95`. This won't fix the underlying drift but cuts the tail tokens that *seed* the collapse.

2. **Repetition penalty.** nanoGPT doesn't ship one. Drop it into `generate()`:

```python
for tok in set(idx[0].tolist()):
    logits[0, tok] /= 1.15
```

This directly breaks the `.S.S.S` attractor.

3. **More training / more data.** The honest answer. Check your `train.py` loss curve — if val loss is still descending, you undertrained. 124M wants billions of code tokens to get past textbook-only competence. Your MI300X (192GB) can hold a much larger batch than the 4070 — push it there.

4. **Scale up.** This is fundamentally a capacity problem. 124M → 350M → 760M (your GPT-2 760M run) will extend the coherent window substantially. You already know this; the BST→garbage transition is the visceral demonstration of *why* you're training the 760M.

The interesting thing for your trajectory: this collapse is exactly what KV-cache + better sampling + scale are solving in production models. Watching your own model break this way is better intuition than any paper on it.

**References:**

- [The Curious Case of Neural Text Degeneration (Holtzman et al., 2020)](https://arxiv.org/abs/1904.09751)
- [nanoGPT sample.py](https://github.com/karpathy/nanoGPT/blob/master/sample.py)
