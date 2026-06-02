---
audio: false
generated: true
image: false
lang: en
layout: post
title: Naming a GPT-2 Style Model
translated: false
type: note
---

**Question:** Should I call this model GPT-2 or GPT-3?

**Answer:**

Call it **GPT-2 760M** (or "GPT-2 style 760M").

Here's the precise distinction:

## Architecture vs. Training Recipe

| Dimension | GPT-2 | GPT-3 |
|---|---|---|
| Architecture | Transformer decoder | Same (near-identical) |
| Paper | Radford et al. 2019 | Brown et al. 2020 |
| Largest model | 1.5B | 175B |
| Training tokens | ~10B (WebText) | ~300B |
| Batch size | Small (~512K tokens) | Massive (~3.2M tokens) |
| Optimizer tweaks | Basic Adam | β2=0.95, grad clip, cosine LR decay |
| Training data | WebText (Reddit outlinks) | CommonCrawl + Books + Wiki |

## What your config actually is

Your config uses **GPT-3 hyperparameters** (β2=0.95, weight_decay=0.1, cosine decay with min_lr, large warmup) but a **GPT-2-scale architecture** (760M sits between GPT-2 Medium 345M and GPT-2 XL 1.5B — not an official GPT-2 checkpoint size, but architectural family).

This is exactly what **nanoGPT** calls it — see Karpathy's own naming in the repo: the model class is `GPT`, config presets are `gpt2`, `gpt2-medium`, `gpt2-large`, `gpt2-xl`. He uses GPT-3 training hyperparameters but calls the architecture GPT-2.

## Practical naming

```
GPT-2 760M (trained on FineWeb-Edu, GPT-3 hparams)
```

Or if you want to be cheeky/accurate:

```
GPT-2 arch, GPT-3 training recipe, 760M params, 14.6B tokens
```

**Don't call it GPT-3** — that implies 175B to most engineers. **Do** credit the GPT-3 paper for your optimizer settings if you write this up.

## One note on your param count

Your comment says `~760M` but let me verify:

```python
# Embedding: vocab * n_embd = 50257 * 1536 = 77.2M
# Transformer blocks: n_layer * (attn + ffn)
#   attn: 4 * n_embd^2 = 4 * 1536^2 = 9.44M per layer
#   ffn:  8 * n_embd^2 = 8 * 1536^2 = 18.87M per layer  (4x hidden, 2 matrices)
#   per layer total: ~28.3M
# 24 layers: 24 * 28.3M = 679M
# + embeddings (shared with lm_head if weight tying): 77M
# Total: ~756M ✓
```

So ~756M — close enough, "760M" is fine as a label.
