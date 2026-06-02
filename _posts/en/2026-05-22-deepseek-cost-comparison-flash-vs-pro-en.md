---
audio: false
generated: true
image: false
lang: en
layout: post
title: "DeepSeek Cost Comparison: Flash vs Pro"
translated: false
type: note
---

**Question:** Is DeepSeek V4 Flash ~4x cheaper than DeepSeek V4 Pro on OpenRouter?

**Answer:**

Not exactly 4x — it's actually **~3.1x cheaper**, which is close but not quite 4x. Here's the exact breakdown:

| Model | Input ($/M tokens) | Output ($/M tokens) | Activated Params |
|---|---|---|---|
| DeepSeek V4 Pro | $0.435 | $0.870 | 49B |
| DeepSeek V4 Flash | $0.140 | $0.280 | 13B |
| **Ratio** | **3.1x** | **3.1x** | **3.8x** |

So the ratio is consistent at **3.1x** on both input and output. You were roughly right — "~4x" is a reasonable mental model, but the precise number is ~3x.

**What you're trading:**

- Flash: 284B total / **13B activated** — fast, cheap, good for coding assistants and agent loops
- Pro: 1.6T total / **49B activated** — heavier reasoning, better on hard math/code, 1M context with hybrid attention

For your use case — daily AI assistant, CLI agents, code iteration — Flash is a solid default. Reserve Pro for tasks where you actually need that extra reasoning headroom (complex multi-file refactors, hard algo problems, long-context analysis). You could likely cut your $8/day bill to ~$2.50/day just by routing 80% of traffic to Flash.

**References:**

- [DeepSeek V4 Pro on OpenRouter](https://openrouter.ai/deepseek/deepseek-v4-pro)
- [DeepSeek V4 Flash on OpenRouter](https://openrouter.ai/deepseek/deepseek-v4-flash)
