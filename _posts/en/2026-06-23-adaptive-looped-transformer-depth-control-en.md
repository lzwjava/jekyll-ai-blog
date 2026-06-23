---
audio: false
generated: true
image: false
lang: en
layout: post
title: Adaptive Looped Transformer Depth Control
translated: false
type: note
---

**Question:** What do you think about the idea of training a model that dynamically decides loop depth per token based on hidden state — essentially achieving 400M-equivalent performance with only 100M actual parameters — and what experiments could produce meaningful results?

**Answer:**

The paper you linked is **ALBERT-style parameter sharing taken to its logical extreme via adaptive computation** — this is the Universal Transformer / Looped Transformer line of work, and your instinct is correct that there's real untapped research here.

## Core Idea: Looped Transformers with Adaptive Depth

The key insight: instead of stacking N distinct transformer blocks (each with unique weights), you **loop a single block K times**, but let the model *decide K dynamically per token* based on hidden state. This is **ACT (Adaptive Computation Time)** meets **weight-tied depth**.

```
Standard 12L model:  x → L1 → L2 → ... → L12 → y     [12× params]
Looped model:        x → L → L → ... → L → y          [1× params, K loops]
Adaptive looped:     x → L^k(x) → y, where k = f(h_t) [per-token K]
```

Your target: **100M params, behaves like 400M** = 4× loop unrolling on average, but with variance per token/position.

---

## What the Paper Likely Shows

From the arxiv link (2604.21215 — Looped Transformers with adaptive compute):

The halting mechanism is probably a **learned scalar head** on hidden state:

```python
# Per-token halting (ACT-style)
def should_halt(h, step, halt_head):
    p = torch.sigmoid(halt_head(h))  # halting prob at this step
    return p  # accumulate until sum >= 1.0
```

The model learns *which tokens need more compute* — function words get 1-2 loops, complex reasoning tokens get 8-10.

---

## Experiments Worth Running on Your RTX 4070

### 1. Topic-wise Loop Depth Analysis

Train the model, then at inference time, **log average loop depth per token type**:

```python
import collections

topic_depths = collections.defaultdict(list)

for batch in eval_loader:
    tokens, topics = batch
    depths = model.get_loop_depths(tokens)  # your adaptive ACT output
    for token, topic, depth in zip(tokens, topics, depths):
        topic_depths[topic].append(depth)

# Compare: math tokens vs prose vs code vs dialogue
for topic, depths in topic_depths.items():
    print(f"{topic}: mean={np.mean(depths):.2f}, std={np.std(depths):.2f}")
```

**Hypothesis**: math/code tokens use 2-3× more loops than simple prose. This would be publishable comparison data.

### 2. Block Substitution Ablation

Swap out the loop body with different architectures and measure compute-efficiency tradeoff:

```
Experiment matrix:
- Base: standard MHA + FFN loop body
- Alt A: replace FFN with MoE (4 experts, top-2) → does routing interact with loop depth?
- Alt B: replace MHA with linear attention (Mamba-style SSM) → cheaper per loop, more loops?
- Alt C: add cross-attention to a compressed memory → "working memory" per token
```

This is a **2D sweep**: architecture × adaptive depth policy.

### 3. The 100M → 400M Equivalent Claim — How to Measure

You need an **iso-FLOPs comparison**, not iso-params:

```python
# FLOPs for looped model at inference
flops_looped = base_block_flops * avg_loop_depth * seq_len

# FLOPs for standard model
flops_standard = num_layers * base_block_flops * seq_len

# Claim: looped model matches standard model quality at same FLOPs budget
# but with 4x fewer parameters (better memory, better generalization)
```

Benchmark on: perplexity, BLiMP, MMLU-subset, and **your own domain** (code generation, since you have real use cases).

---

## What Makes This Tractable on 12GB VRAM

100M param model fits easily. The tricky part is the **ACT gradient flow** — halting decisions need to be differentiable. Use the standard ACT loss:

```python
def act_loss(ponder_steps, lambda_p=0.01):
    # Penalize unnecessary computation
    return lambda_p * ponder_steps.mean()

total_loss = task_loss + act_loss(ponder_steps)
```

Start with **fixed-depth looping first** (no adaptive), verify you match the parameter efficiency claim, then add adaptive halting. This is the correct experimental ladder.

---

## My Honest Take

The **adaptive loop depth per token** angle is genuinely interesting because:

1. It's a **free interpretability signal** — loop depth IS a measure of token complexity
2. The topic comparison experiment is low-cost, high-signal
3. 100M params on your 4070 trains in hours not days

The risk: ACT training is notoriously unstable. The halting distribution collapses (all tokens halt at step 1 or never halt). You'll need careful lambda tuning and probably a **minimum loop count** enforced during early training.

Start here:

```bash
# Minimal looped transformer — before adding adaptive compute
git clone https://github.com/karpathy/nanoGPT
# Modify: tie weights across all layers, train with loop_depth=4
# Verify: same perplexity as 4x-param model at same FLOPs
```

Then layer in the halting head once the base loop training is stable. The experiments that compare topic-wise depth usage would make a clean blog post or short paper — and it fits your "learn in public, ship fast" mode perfectly.
