---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 Small Trained on 10 Billion Tokens
translated: false
type: note
---

It's **GPT-2 small (124M)** — not medium.

- `n_layer=12, n_head=12, n_embd=768` → GPT-2 small (124M params)
- Batch: 4 × 1024 × 128 grad-accum = 524,288 tokens/step
- 19,073 iters × 524K ≈ **10B training tokens**
- Despite the filename `gpt3`, the architecture is GPT-2 small with GPT-3-style 10B-token training schedule

For reference (you're not running these):

- medium: 24L / 16H / 1024d (350M)
- large: 36L / 20H / 1280d (774M)
- XL: 48L / 25H / 1600d (1.5B)
