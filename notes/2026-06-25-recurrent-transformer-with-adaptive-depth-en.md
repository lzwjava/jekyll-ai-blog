---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recurrent Transformer with Adaptive Depth
translated: false
type: note
---

**Question:** What is `Hippocrene/recurrent-transformer-0.1b-e0.4b` on HuggingFace?

**Answer:**

This is a clever research model that combines three classic ideas into one tight package. Here's the breakdown:

## Core Idea: Weight-Tied Recurrent Depth

Instead of stacking N *different* transformer layers (like GPT-2 does), this model has **one shared transformer block** that gets applied recurrently up to 8 times per token. Think of it as:

```
# Normal transformer (GPT-2 style)
x = layer_1(x)
x = layer_2(x)
...
x = layer_N(x)  # N distinct weight sets

# This model (Universal Transformer style)
for step in range(max_steps):
    x = shared_block(x)   # same weights every time
    if halting_head(x) > threshold:
        break              # ACT: stop early per token
```

## Architecture Details

| Property | Value |
|---|---|
| Stored params | **110M** |
| Compute-active block | ~46M |
| Max recurrence steps | 8 |
| Effective compute | ~0.4B (hence `e0.4b` in the name) |
| Hidden dim | 1280 |
| Attention | 20 heads × 64 head-dim |
| FFN | SwiGLU, 10240 |
| Context | Transformer-XL memory, up to **4096 tokens** |
| Tokenizer | GPT-2 (vocab 50257) |

## Three Papers Fused

1. **Universal Transformer** (Dehghani et al. 2018) — shared weights across depth
2. **Adaptive Computation Time / ACT** (Graves 2016) — per-token halting head; harder tokens get more recurrence steps
3. **Transformer-XL** (Dai et al. 2019) — segment-level memory for long context

The ACT piece is particularly interesting: the model measured code averaging **~6.3 recurrence steps** and hard prose hitting **~8 steps** — showing the halting is actually doing something meaningful.

## Training Stack

- Pretrained on **8.7B tokens**, 13-corpus mix (FineWeb, code, books, arXiv, wiki, dialogue, Pile)
- Trained in **native FP8** on a single RTX PRO 6000 Blackwell
- Long-context curriculum: 512 → 1024 → 2048 → 4096 tokens
- SFT on 707M tokens (Dolly, Alpaca, OpenOrca, OpenHermes)
- DPO on UltraFeedback

## Performance

- FineWeb PPL: **25.4** (vs 35.8 for a 6-layer baseline)
- Zero-shot macro-acc: **0.41** across LAMBADA/HellaSwag/ARC-Easy/Winogrande

## Why It's Interesting to You

Given your nanoGPT/nanochat work and interest in MoE + transformer internals — this is a different axis of model efficiency: **depth-adaptive compute** vs **width-sparse compute** (MoE). The idea that the same weights can be reused 8× is essentially **parameter efficiency via recurrence**, not via sparsity.

The halting head is just a small linear probe on the hidden state — trivially implementable. If you wanted to experiment with this pattern in nanochat, it's maybe 50 extra lines on top of a standard GPT block.

It's a **research/demo model**, not production-grade — but the architecture ideas are solid and underexplored compared to the MoE wave.

**References:**

- [Model card](https://huggingface.co/Hippocrene/recurrent-transformer-0.1b-e0.4b)
- [Universal Transformers (Dehghani 2018)](https://arxiv.org/abs/1807.03819)
- [ACT (Graves 2016)](https://arxiv.org/abs/1603.08983)
- [Transformer-XL (Dai 2019)](https://arxiv.org/abs/1901.02860)
