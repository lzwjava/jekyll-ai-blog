---
audio: false
generated: true
image: false
lang: en
layout: post
title: Underserved AI Startup Directions
translated: false
type: note
---

**Question:** What are good AI startup directions right now, given how crowded the space is?

**Answer:**

You're right that it's crowded — but the crowding is *extremely uneven*. More than 70% of founders are building in markets already past saturation — the same handful of ideas keeps reappearing: AI writing tools, chatbots, logo generators, resume builders, repackaged with a different landing page each time. That's the noise. Here's where the signal is, filtered for someone with your profile.

---

## The Meta-Framework First

Before listing ideas: the question isn't "what AI startup" — it's **where do you have an unfair advantage + where is the market early**. For you specifically, that intersection is:

- You have: LLM API depth, agent-building experience, bank/fintech exposure, Chinese market context, full-stack + ML skills
- The market is early in: **agent infrastructure**, **vertical AI for regulated industries**, **AI eval/observability**, **inference optimization tooling**

---

## Directions That Are Actually Underserved

### 1. Agent Reliability Infrastructure
Many agent deployments still stumble on fundamentals: accessing live web data, maintaining organizational context, executing actions reliably, scaling compute efficiently, and preserving long-term memory. The companies solving this (Firecrawl, Mem0, Modal Labs) are gaining serious traction.

**Whitespace:** Agent *testing and reliability* — equivalent of Selenium/Cypress but for agentic workflows. Nobody has a great answer for "how do I CI/CD an agent." This is deeply technical, you'd understand the problem space from building `ww`/`iclaw`/`zz`.

### 2. AI Eval & Observability
Novel evaluation and observability present a critical infrastructure challenge that didn't exist in prior software development paradigms. Traditional monitoring tracks completion rates, latency, error codes — but AI agents need something fundamentally different.

**Whitespace:** LLM eval tooling for *domain-specific* outputs — finance, legal, code. General evals (MMLU etc.) are commoditized. Vertical eval platforms are not.

### 3. Vertical AI for "Boring" but High-Value Industries
Vertical SaaS for "boring" industries (HVAC, pest control, roofing) shows consistently low competition and high willingness to pay. But for you, given your bank background: **financial compliance automation** is less boring and more defensible.

**Whitespace:** AI for bank audit, AML narrative generation, regulatory report drafting. You've lived this problem. Harvey is doing it for legal ($100M+ ARR in 2 years) — the finance equivalent is wide open.

### 4. Inference Optimization Tooling
As AI agents and applications transition from prototype to production, inference workloads now rival training in both compute demand and economic importance. A new generation of infrastructure startups is attacking the inference stack.

**Whitespace:** Speculative decoding / KV cache optimization as a service, or MoE routing optimization. You already understand AMD MI300X and have hands-on training experience — that's rare context.

### 5. AI Skills / Agent Composition Layer
Skills replaced tool stuffing — the old way was to register every tool the agent might need at startup, eating context every turn. Most of the middle layer is now gone; the SDKs ship with the tools.

**Whitespace:** A marketplace or composition layer for agent skills/tools — like npm but for agent capabilities with eval scores attached. MCP registry is nascent and messy.

---

## What to Avoid (Saturated)

- AI writing tools / content generation
- Generic chatbots / customer support bots
- Resume builders, cover letter generators
- Wrapper apps around GPT-4o/Claude with no proprietary data or workflow

---

## My Take for You Specifically

Given your actual stack — you've trained GPT-2 scale models, you consume 1B tokens/month, you've built CLI agents, you work in a bank — the two most asymmetric bets for you are:

**A. Agent eval/testing infrastructure** — you feel the pain daily, it's deeply technical, nobody does it well
**B. Vertical AI for financial compliance / AML / audit** — you have insider knowledge, the TAM is enormous, regulation actually *creates* moats

Both of these require the kind of depth that filters out the "AI wrapper" founders. That's exactly your edge.

**References:**

- [AI Infrastructure Roadmap: Five frontiers for 2026 — Bessemer Venture Partners](https://www.bvp.com/atlas/ai-infrastructure-roadmap-five-frontiers-for-2026)
- [AI Startup Ideas 2026: 50 Ranked, 11 Worth Building](https://preuve.ai/blog/startup-ideas-2026)
- [How Building AI Agents Has Changed in 2026 — Pulumi](https://www.pulumi.com/blog/how-building-ai-agents-has-changed/)
- [5 Under-the-Radar AI Infrastructure Companies — TechPluto](https://www.techpluto.com/ai-infrastructure-companies-2026/)
