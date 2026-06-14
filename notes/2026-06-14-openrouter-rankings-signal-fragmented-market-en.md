---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenRouter Rankings Signal Fragmented Market
translated: false
type: note
---

**Question:** What does the OpenRouter LLM leaderboard this week reveal? Why are the token counts so close, and why is there no dominant leader?

**Answer:**

A few things stand out from this snapshot:

## What the Chart Shows

- **Token throughput per week** — not quality, not benchmark scores. This is raw usage volume routed through OpenRouter.
- **Week-over-week growth %** — the numbers next to each model (35%, 51%, 103%, etc.) show momentum, not absolute size.
- It's a **demand signal**, not a capability ranking.

## Why the Counts Are So Close

Several compounding reasons:

**1. The field genuinely fragmented this cycle**

There's no GPT-4-era monopoly anymore. DeepSeek V4 Flash, Hy3, MiniMax M3, MiMo — these are all competitive on price/performance. Users spread across them because each has a niche (speed, cost, context window, coding, Chinese language).

**2. OpenRouter's routing nature**

OpenRouter aggregates many API consumers — hobbyists, startups, CLI tools, agents. Each user picks differently. There's no single "enterprise default" pushing one model to 10x.

**3. Flash/free models cannibalize each other**

Notice most top models are Flash variants or have free tiers. Price-sensitive users (majority on OpenRouter) arbitrage between them constantly. No single free model dominates.

**4. Weekly window is too short**

A single week is noisy. A new model drops (MiniMax M3 at +103% WoW) and it spikes immediately. Next week it could be #8.

## Why No Clear Leader

**The "leader" changes by use case:**

| Use case | Who wins |
|---|---|
| Raw throughput / cost | DeepSeek V4 Flash |
| Chinese language | MiMo, GLM, Hy3 |
| Coding | Claude Opus 4.7/4.8 |
| Free tier | Nemotron 3 Ultra (+321% WoW!) |
| Multimodal | Gemini 3.x Flash |

**There's no GPT-4 moment happening right now.** Mid-2023 had a clear gap — GPT-4 was far ahead. Now the frontier is crowded at roughly the same capability band. The differentiator is price, latency, and specific task fit — not raw intelligence gap.

## What's Actually Interesting Here

- **Nemotron 3 Ultra free at +321% WoW** — 550B MoE from NVIDIA, free tier, massive growth. Worth watching.
- **Hy3 Preview from Tencent at #2** — a preview model at 4.26T tokens is unusual. Likely getting benchmarked by many developers simultaneously.
- **MiniMax M3 at +103% WoW** — fastest growing. New entrant getting trial traffic.
- **Claude Opus 4.8 already at #9** — newer than 4.7 but lower volume, suggesting 4.7 still has the production deployments.
- **DeepSeek V3.2 at 0% growth** — flat. Getting replaced by V4 variants.

## Bottom Line

This leaderboard measures **routing popularity**, not model quality. The closeness signals a genuinely competitive market — no one model is 10x better in a way that causes winner-take-all dynamics. For your use case (agent pipelines, high token volume), the signal is: **DeepSeek V4 Flash for cost-optimized throughput, Claude Opus 4.7/4.8 for quality-critical tasks** — which already matches your stack.

References:
- [OpenRouter Rankings](https://openrouter.ai/rankings)
