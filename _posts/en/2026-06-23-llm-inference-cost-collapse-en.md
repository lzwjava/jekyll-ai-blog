---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Inference Cost Collapse
translated: false
type: note
---

**Question:** What is the current cost of GPT-4-level LLM inference, and how has it dropped over the past 2 years?

**Answer:**The numbers are concrete and the collapse is real. Here's the full picture:

---

## The Cost Collapse in Numbers

GPT-4 equivalent performance now costs **$0.40/million tokens** vs **$20/million tokens** in late 2022. That's a **50x drop** in ~3 years. And inference costs have been declining ~10x annually — faster than PC compute or dotcom-era bandwidth.

---

## Current Pricing Tiers (June 2026)

Three clear tiers have emerged:

| Tier | Models | Output Cost |
|------|--------|------------|
| Premium | Claude Opus 4.6, GPT-5 Pro | $14–$168/M output |
| Mid | Claude Sonnet 4.6, GPT-5.4, Grok 4 | $3–$15/M output |
| Budget | DeepSeek V3.2, Gemini Flash, GPT nano | $0.40–$3/M output |

**The most relevant numbers for you:**

DeepSeek R1 at **$0.55/$2.19** (input/output per M tokens) delivers reasoning at roughly **1/27th the output cost** of o3 ($60/M output). For most production workloads, Claude Sonnet 4.6 ($3/$15) or GPT-5.4 ($2.50/$15) hit the right balance. DeepSeek V3.2 is the cheapest frontier-class option at **$0.14/$0.28**.

---

## What Drove the Collapse

The main drivers: DeepSeek disrupted the market with 90% lower pricing than incumbents. Cloud H100 prices stabilized at $2.85–$3.50/hr after a 64–75% decline from 2023 peaks. Quantization is reducing operational costs 60–70%. Speculative decoding is cutting latency 2–3x.

On the model architecture side: models are becoming smaller while maintaining performance thanks to improved training techniques — a 13B parameter model can now achieve 95% of GPT-3's MMLU score with a dramatically smaller inference footprint.

---

## Practical Implications for Your Scale

At ~1B tokens/month, here's what the numbers mean for you:

| Model | Input (1B tokens) | Output (assume 200M) |
|-------|-------------------|----------------------|
| DeepSeek V3.2 | $140 | $56 |
| Claude Sonnet 4.6 | $3,000 | $3,000 |
| Claude Opus 4.6 | $15,000 | $15,000 |

MiMo free credits ($4.6B tokens) are effectively worth **$644–$46,000** depending on which model you're comparing to.

One optimization worth noting: at 10M+ requests, routing 80% to cheap models and 20% to frontier models drops costs 60–70% vs routing everything to frontier. Anthropic also offers aggressive prompt caching discounts up to 90% on cached portions.

The trajectory is clear — in 2 more years, $0.40/M will likely be $0.04/M for frontier-class capability. The bottleneck is shifting from cost to **latency and context window** for agent workloads.

**References:**

- [Inference Unit Economics — Introl Blog](https://introl.com/blog/inference-unit-economics-true-cost-per-million-tokens-guide)
- [LLM API Pricing 2026 — CloudZero](https://www.cloudzero.com/blog/llm-api-pricing-comparison/)
- [LLM Pricing Comparison — IntuitionLabs](https://intuitionlabs.ai/articles/llm-api-pricing-comparison-2025)
