---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deep AI Engineering in 500 Hours
translated: false
type: note
---

**Question:** How should I allocate my ~4 hours/day over the next 3 months to maximize AI engineering skill compounding?

**Answer:**

Your situation: bank contractor by day, AI engineer by trajectory. 4 hours/day is ~500 hours over 3 months. That's enough to go deep on one thing or shallow on five. The mistake most people make is spreading it thin. Here's how I'd structure it for you specifically.

---

## The Core Constraint

You're not skill-zero. You've trained GPT-2 760M, built CLI agents, consumed 2B tokens. The gap between you and Karpathy isn't breadth — it's **depth on internals** and **shipped artifacts that prove it**. Those 500 hours should close that gap.

---

## Allocation Framework (per week ~28 hrs)

### Block 1 — Deep Technical (12 hrs/week, ~2 hrs/day on weekdays)

**Goal:** One core AI engineering domain per month, studied to implementation depth.

| Month | Focus | Concrete Deliverable |
|-------|-------|----------------------|
| 1 | Transformer internals → attention, KV cache, sampling | Implement MHA + KV cache from scratch in ~200 lines of Python. Beat your nanoGPT notes. |
| 2 | Training loop mastery → LoRA, DPO, GRPO | Fine-tune a 1B model on your RTX 4070 with LoRA. Log every loss curve. |
| 3 | Inference optimization → quantization, speculative decoding, batching | Run DeepSeek-V4 locally or via API with custom inference harness. Benchmark throughput. |

This is Karpathy-style: one thing, all the way down, working code.

### Block 2 — Ship Something (8 hrs/week, weekend-heavy)

**Goal:** One public artifact per month. Not blog posts — tools with GitHub stars or paying users.

Candidates ranked by leverage for you:

1. **An opinionated LLM eval harness** (CLI-first, wraps OpenRouter) — scratches your own itch, useful to others
2. **A LoRA fine-tuning CLI** (wrappers around transformers/unsloth, one command) — high star potential
3. **A nanochat-derived chatbot** trained on your own blog/notes — living proof of your skill stack

Ship → get feedback → iterate. This is your startup validation runway.

### Block 3 — Reading/Synthesis (4 hrs/week, ~30 min/day)

**Not** passive consumption. Active reading = paper → annotate → implement one key idea.

Prioritized reading list for next 3 months:

- Flash Attention 2 paper → implement naive vs. flash attention, benchmark
- DeepSeek-V4 MoE paper (technical report) → understand expert routing
- Chinchilla laws → understand why you'd train 760M vs 7B given compute budget

Skim your own notes first. If it's already at lzwjava.github.io/notes-en, go one layer deeper.

### Block 4 — Eliminate (0 hrs)

Based on your own playbook: WeChat noise, non-compounding networking, passive video watching, anything that doesn't feed Block 1 or 2. Track for one week, then cut.

---

## Daily Time Architecture

```
6:00–8:00   Deep technical (Block 1) — before brain is taxed by work
Evening
19:00–21:00 Ship/build (Block 2 on weekends, light reading Block 3 on weekdays)
```

Morning is non-negotiable. Bank work drains context. You want transformer internals in your working memory before the daily standup, not after.

---

## The 3-Month Output Test

At the end of 90 days, you should be able to say:

- "I implemented attention + KV cache from scratch and can explain every line"
- "I fine-tuned a model with LoRA and DPO and have loss curves to show it"
- "I shipped a tool that has >100 GitHub stars or earns any CNY"

If you can't say all three, the allocation drifted. Recalibrate at the 30-day mark.

---

## One Tactical Suggestion

Use your bank job's AI assistant quota (top 6% globally) as a forcing function. Every task at the bank that touches data, automation, or tooling — extract a pattern, abstract it, add it to your tooling. Don't waste the access.

The mortgage clock is running. These 500 hours are the compression mechanism.
