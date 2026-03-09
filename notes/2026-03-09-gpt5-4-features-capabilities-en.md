---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-5.4 Features and Capabilities Explained
translated: false
type: note
---

Question: What is a comprehensive introduction to the GPT-5.4 model?

Answer:

## GPT-5.4: A Comprehensive Introduction

### Overview

GPT-5.4 is OpenAI's most capable and efficient frontier model for professional work, released on March 5, 2026. It is available in ChatGPT (as GPT-5.4 Thinking), the API, and Codex. It brings together the best of OpenAI's recent advances in reasoning, coding, and agentic workflows into a single frontier model.

It is the first mainline reasoning model that incorporates the frontier coding capabilities of GPT-5.3-Codex, and OpenAI named it GPT-5.4 to reflect that significant capability jump and to simplify the choice between models when using Codex.

---

### Model Variants

There are three main variants of GPT-5.4:

**1. GPT-5.4 (Standard / API)**
Available through the API as `gpt-5.4`, rolling out gradually across ChatGPT and Codex.

**2. GPT-5.4 Thinking (ChatGPT)**
In ChatGPT, GPT-5.4 Thinking can now provide an upfront plan of its thinking, so users can adjust course mid-response while it is working, and arrive at a final output more closely aligned with what they need. This variant is available to Plus, Team, and Pro users in ChatGPT, while Enterprise and Edu customers can enable early access.

**3. GPT-5.4 Pro**
GPT-5.4 Pro is a version that uses more compute to think harder and provide consistently better answers. It is available in the Responses API only, to enable support for multi-turn model interactions before responding to API requests, and other advanced API features. GPT-5.4 Pro is available through the API as `gpt-5.4-pro` and to Pro and Enterprise plan users in ChatGPT.

---

### Key Capabilities

**Reasoning & Efficiency**
GPT-5.4 is OpenAI's most token-efficient reasoning model yet, using significantly fewer tokens to solve problems compared to GPT-5.2 — translating to reduced token usage and faster speeds.

**Coding**
GPT-5.4 incorporates the industry-leading coding capabilities of GPT-5.3-Codex, improving how the model works across tools, software environments, and professional tasks involving spreadsheets, presentations, and documents.

**Native Computer Use**
In Codex and the API, GPT-5.4 is the first general-purpose model released with native, state-of-the-art computer-use capabilities, enabling agents to operate computers and carry out complex workflows across applications. It achieves 75% on the OSWorld-Verified Computer Use benchmark.

**Long Context Window**
GPT-5.4 supports up to 1 million tokens of context, allowing agents to plan, execute, and verify tasks across long horizons. Prompts exceeding 272K input tokens are priced at 2x input and 1.5x output for the full session.

**Tool Search**
GPT-5.4 improves how models work across large ecosystems of tools and connectors with a new feature called Tool Search, helping agents find and use the right tools more efficiently without sacrificing intelligence.

**Professional Knowledge Work**
On GDPval — which tests agents' abilities to produce well-specified knowledge work across 44 occupations — GPT-5.4 achieves a new state of the art, matching or exceeding industry professionals in 83.0% of comparisons, compared to 70.9% for GPT-5.2.

---

### Hallucination & Accuracy Improvements

GPT-5.4 is OpenAI's most factual model yet. On a set of de-identified prompts where users flagged factual errors, GPT-5.4's individual claims are 33% less likely to be false, and its full responses are 18% less likely to contain any errors, relative to GPT-5.2.

---

### Safety Features

OpenAI published new safety research on monitoring how models reason, including an open-source evaluation designed to test whether systems can conceal their reasoning. The research found that GPT-5.4 Thinking showed a low ability to obscure its reasoning, which the company characterized as a positive safety signal.

OpenAI kept the same high cyber-risk classification used for GPT-5.3-Codex and deployed additional protections, including expanded cyber safety systems, monitoring tools, trusted access controls, and request blocking for higher-risk activity on Zero Data Retention surfaces.

---

### Pricing (API)

The standard `gpt-5.4` model is priced at **$2.50 per million input tokens** and **$15 per million output tokens**. The `gpt-5.4-pro` model is priced at **$30 per million input tokens** and **$180 per million output tokens**.

---

### Model Snapshot / Version

The current snapshot is `gpt-5.4-2026-03-05`. Snapshots allow developers to lock in a specific version of the model so that performance and behavior remain consistent over time.

---

### Legacy Model Retirement

GPT-5.2 Thinking will remain available for three months for paid users in the model picker under the Legacy Models section, after which it will be retired on June 5, 2026.

---

### Summary Table

| Feature | GPT-5.4 | GPT-5.4 Pro |
|---|---|---|
| Context Window | 1.05M tokens | 1.05M tokens |
| Computer Use | Native (first general-purpose) | Native |
| Reasoning Effort | none, low, medium, high, xhigh | medium, high, xhigh |
| API Price (Input) | $2.50 / 1M tokens | $30 / 1M tokens |
| API Price (Output) | $15 / 1M tokens | $180 / 1M tokens |
| ChatGPT Access | Plus, Team, Pro | Pro & Enterprise |

References:

- [Introducing GPT-5.4 | OpenAI](https://openai.com/index/introducing-gpt-5-4/)
- [GPT-5.4 Model | OpenAI API Docs](https://developers.openai.com/api/docs/models/gpt-5.4)
- [GPT-5.4 Pro Model | OpenAI API Docs](https://developers.openai.com/api/docs/models/gpt-5.4-pro)
- [OpenAI launches GPT-5.4 | TechCrunch](https://techcrunch.com/2026/03/05/openai-launches-gpt-5-4-with-pro-and-thinking-versions/)
- [OpenAI announces GPT-5.4 | Neowin](https://www.neowin.net/news/openai-announces-gpt54-its-most-powerful-model-that-excels-at-professional-tasks/)
- [GPT-5.4 safety & release | Help Net Security](https://www.helpnetsecurity.com/2026/03/06/openai-chatgpt-gpt%E2%80%915-4-model-release/)