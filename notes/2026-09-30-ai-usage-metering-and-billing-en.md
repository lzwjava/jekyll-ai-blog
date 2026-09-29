---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Usage Metering and Billing
translated: false
type: note
---

**Question: Companies doing AI/software consultancy or platforms that meter usage (tokens/API usage) per client/project?**

There are a few categories. Most are not pure "software consultancy billed by token", but they operate the same economic model: **client/project isolation + usage metering + AI infrastructure billing**.

### AI usage metering / billing infrastructure

* Helicone

  * AI gateway that tracks LLM requests, tokens, costs, latency.
  * Common setup: one customer/project key → usage dashboard → billing.

* Langfuse

  * Tracks traces, generations, token usage, model costs.
  * Used by AI teams building client-facing applications.

* Lago

  * Metering infrastructure for usage billing.
  * Supports charging customers based on events (tokens, API calls, credits).

* OpenMeter

  * Built specifically for usage-based pricing.
  * Common pattern: event stream → usage aggregation → invoice.

* OpenRouter

  * Provides unified access to multiple models and tracks usage/costs.

---

### AI consulting / implementation companies likely to use this model

* Bain & Company (AI practice)
* BCG X
* Accenture AI
* Slalom

Large firms usually bundle AI usage into managed-service contracts rather than exposing token-level billing.

---

### Smaller AI-native companies closer to your described model

* Relevance AI

  * Builds AI workforce/agent systems.
  * Usage-based economics are common in this category.

* Lindy

  * AI agents with usage-based pricing.

* Dust

  * Enterprise AI assistants/agents.

* Retool

  * Internal tools + AI workflows, often tied to usage.

---

The **closest match to "one project, one client API key, measure tokens, invoice client"** is usually not a famous consultancy. It is more often a small AI agency using a stack like:

```
Client
  |
  | project API key
  v
Helicone / Langfuse
  |
  v
OpenAI / Anthropic / Gemini
  |
  v
Lago / Stripe metering
  |
  v
Monthly invoice
```

A lot of AI consultancies are still doing this privately rather than marketing "token billing" as their business model. The market is still early.
