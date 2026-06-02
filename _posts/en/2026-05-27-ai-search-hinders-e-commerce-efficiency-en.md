---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Search Hinders E-commerce Efficiency
translated: false
type: note
---

**Question:** Is JD.com's AI search feature (DeepSeek-powered) in their mobile app actually worse for users than traditional keyword search? Would users be better off using a dedicated chat AI for research, then switching to JD.com with conventional keyword queries?

**Answer:**

Yes, and this is a well-understood product design failure pattern. Here's why JD.com's AI search is suboptimal and why your instinct is correct:

## Why AI Search in E-commerce Apps Fails

**Misaligned objective functions.** JD.com's AI search isn't optimized for *your* best answer — it's optimized for GMV (gross merchandise value). The DeepSeek model is fine-tuned or prompted to surface products that convert, not to give you neutral, accurate product research. Every AI answer is a funnel, not an oracle.

**Context window ≠ product catalog intelligence.** A general LLM like DeepSeek doesn't have deep structured knowledge of SKU-level specs, real user reviews at scale, or cross-category comparison reasoning baked in. It's essentially doing RAG over JD's product data, which is noisy and merchant-biased.

**Hallucination risk on specs.** If you ask "which graphics card has the best price-performance under 3000 CNY," the AI might confidently give you outdated benchmark comparisons or wrong TDP numbers. Traditional search returns the actual product pages where you verify specs yourself.

**The UI/UX forcing function.** AI search answers are a dead end — you read the answer, maybe click one recommended product. Traditional keyword search gives you a results grid where your eye can scan 20 products, sort by price, filter by brand, check ratings count. Information density is higher with keyword search for shopping tasks.

## The Right Mental Model: Two-Phase Research

Your described workflow is actually optimal:

```
Phase 1: Research (ChatGPT / Claude / Perplexity)
  → "Compare RTX 4070 vs RX 7800 XT for ML inference workloads"
  → "Best mechanical keyboard switches for programming under 500 CNY"
  → Get structured, unbiased analysis

Phase 2: Execute (JD.com with keywords)
  → Search "RTX 4070 Ti ASUS" — already know exactly what you want
  → Sort by price + filter by JD self-operated (京东自营)
  → Check ratings count and recent reviews manually
```

This separation works because **research is a generative task** (LLMs are good at this) and **shopping execution is a retrieval + filtering task** (structured search is good at this).

## Why JD Won't Fix This

JD's incentive is to keep you *inside the app* and reduce comparison shopping. AI search that gives you a confident answer discourages you from checking Taobao or PDD. The AI feature is partly a retention mechanism, not a pure user value play.

DeepSeek integration is also likely a **cost signal** — cheap inference, fast deployment, and a marketing story ("AI-powered"). Product quality for the user is secondary to the narrative.

## The General Principle

**AI search is good when:** the query is ambiguous and needs interpretation, the corpus is well-structured and curated (e.g., enterprise knowledge bases), and there's no conflict of interest between the platform and the user.

**AI search is bad when:** the platform has a financial stake in what you find, the underlying data is merchant-generated (biased), and you need to *compare* across many options rather than *describe* one.

JD.com's case hits all three "bad" conditions. Your two-app workflow is the correct response to a poorly aligned product.
