---
audio: false
generated: true
image: false
lang: en
layout: post
title: "FUNDA: AI-Native Equity Research Platform"
translated: false
type: note
---

Question: What is FUNDA (funda.ai)?

Answer: FUNDA is an AI-native equity research platform for institutional public-market investors — basically Bloomberg-terminal-meets-agentic-research-stack, sitting on four layers:

1. **In-depth Reports** (Judgment layer) — analyst-authored deep dives, earnings previews/reviews, thematic coverage. Their marquee case study: a Dec 2024 bullish call on LITE (via Google TPU optical strategy tied to Broadcom/Google/AMD ASIC coverage) is cited as +1474.8% since coverage.
2. **Research Agents** (Intelligence layer) — this is the AI-native part. "Proprietary plays" are prebuilt recurring workflows (e.g. a 573-stock/28-layer semiconductor supply chain sentiment tracker), plus a library of ~12 modular "research skills" (insider Form 4 analysis, 13-F institutional holdings, congressional trading disclosures, options IV/skew, Polymarket earnings-odds ingestion, macro/Fed tracking). There's also always-on ticker dashboards (e.g. NVDA) that fuse price action, curated news, sentiment, and auto-generated bull/bear "key debate" threads with timestamps and sourcing.
3. **Live Meetings** (Dialogue layer) — scheduled analyst access for institutional clients around earnings/catalysts, with explicit thesis-versioning ("what changed, v2").
4. **Expert Database** (Evidence layer) — 50,000+ vetted expert network + searchable transcript library from analyst-led calls, compliance-reviewed before being wired back into reports/dashboards as reusable evidence.

Positioning is "analyst-led, expert-backed, AI-native" — not a pure LLM-wrapper stock bot; it's explicitly trying to combine human analyst judgment + primary evidence (expert calls, filings) + agent workflows into one system, sold to institutional clients (demo-gated, not self-serve retail).

From a build perspective, the interesting technical bits for you: the "Research Agents" section looks like a skills/tools framework not unlike what you're doing with `ww`/`iclaw`/`zz` — templated agent workflows over a proprietary data layer (13-F, Form 4, options chain, Polymarket) rather than raw LLM chat.

References:

- [FUNDA — funda.ai](https://funda.ai)
- [FUNDA Research Agents](https://funda.ai/agent-chat)
- [FUNDA Reports](https://funda.ai/reports)
