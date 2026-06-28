---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mid-2026 AI Technical Frontier
translated: false
type: note
---

Question: What will the world look like over the next 6 months (roughly July–December 2026)?

Answer:

I can't predict the future, and anyone who gives you a confident forecast is selling something. What I can do is give you a grounded read on trajectories already in motion as of mid-2026, scoped to what actually matters for your AI engineering trajectory. I'll skip geopolitics/markets (noise for your goals) and focus on the technical frontier.

**LLM/model landscape**

- MoE scaling continues to dominate. DeepSeek v4's flash/pro split (which you're already running) reflects the broader pattern: sparse activation, aggressive expert routing, cheaper inference per quality unit. Expect the open-weight gap to keep closing — the interesting question for you is whether v4-class MoE recipes get cleanly reproducible at nanochat scale.
- Inference cost per token keeps falling roughly an order of magnitude/year. Your 2B-tokens/month habit gets cheaper, not more expensive.
- Long-context + KV cache optimization (paged attention, quantized KV, cross-layer sharing) stays the active battleground for serving efficiency.

**Agents**

- The shift from chat to agentic execution is the dominant theme. Tool use, planning loops, and multi-agent orchestration move from demos to production. This is exactly where your CLI agents (ww, iclaw, zz) sit — you're building in the right lane.
- Expect consolidation around agent protocols/standards (MCP-style tool interfaces) rather than everyone rolling bespoke glue.

**Training/hardware**

- AMD (your MI300X work) keeps gaining inference share; ROCm tooling maturity is the bottleneck, and it improves quarterly.
- Small-model training (your GPT-2 760M from-scratch work) stays a great learning vehicle but the frontier moves toward distillation and synthetic-data pipelines.

What's *not* knowable: which specific labs ship what, regulatory moves, whether any architecture genuinely breaks the transformer paradigm. If you want a forecast on something specific — a model release, a benchmark, a hardware roadmap — name it and I'll search for current signals rather than hand-wave.

What were you actually trying to plan around?
