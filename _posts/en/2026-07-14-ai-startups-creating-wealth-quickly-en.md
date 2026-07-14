---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Startups Creating Wealth Quickly
translated: false
type: note
---

Question: What are Sierra and OpenEvidence? Why are they examples of AI creating wealth quickly?

Answer:

These are two interesting **AI application-layer startups**. They are different from OpenAI/Anthropic (foundation models), but they use LLMs to attack specific high-value markets. ([Sierra][1])

## 1. Sierra

Sierra

**What it does:**

* Builds AI agents for enterprise customer service.
* Instead of a chatbot that only answers FAQs, the goal is an autonomous agent that can:

  * understand customer requests
  * access company systems
  * execute actions (refund, change subscription, book service, etc.)
  * escalate to humans when needed

Example:

```
Customer:
"I want to cancel my airline ticket and get a refund."

Traditional chatbot:
"Here is our refund policy."

Sierra-style agent:
- verify identity
- check booking
- calculate refund
- issue refund
- send confirmation
```

Founded by:

* Bret Taylor
* Clay Bavor

Bret Taylor is already a famous Silicon Valley executive (Google Maps, Facebook CTO, Salesforce co-CEO), so Sierra had strong founder-market fit. ([Sierra][1])

The interesting part: Sierra reached a very high valuation very quickly because investors believe **AI agents may replace parts of traditional enterprise software**. ([Sierra][2])

---

## 2. OpenEvidence

OpenEvidence

**What it does:**

* AI assistant for doctors.
* Similar idea to "ChatGPT for doctors", but specialized:

  * medical literature search
  * diagnosis support
  * treatment information
  * clinical reasoning assistance

Example:

```
Doctor:
"65-year-old patient,
chest pain,
high troponin,
ECG abnormal.
What are possible diagnoses?"

OpenEvidence:
- retrieves medical evidence
- summarizes guidelines
- suggests differential diagnosis
- cites sources
```

Founded by:

* Daniel Nadler
* Zachary Ziegler

The company focuses on healthcare because medicine has:

* huge economic value
* expensive expert labor
* information overload
* strong need for AI assistance

([Wikipedia][3])

---

Your observation is correct: **AI is compressing the time from startup → billionaire-scale outcome.**

Old pattern:

```
1995 Google:
search engine
↓
10+ years
↓
huge company
```

AI pattern:

```
2023 startup
↓
excellent founders + LLM wave
↓
2-3 years
↓
multi-billion valuation
```

Why?

Because AI has three accelerators:

### 1. Existing foundation models

A startup does not need to spend $1B training GPT-5.

They can build:

```
GPT/Claude/open models
        +
domain data
        +
workflow integration
        =
valuable product
```

---

### 2. Software has near-zero scaling cost

A traditional company:

```
10,000 customers
=
10,000 employees
```

AI company:

```
10,000 customers
=
same model infrastructure
+
more GPUs
```

---

### 3. Domain experts become much more powerful

A doctor + AI can become like:

```
one doctor
+
100,000 medical papers
+
AI reasoning assistant
```

A programmer + AI:

```
one engineer
+
codebase understanding agent
+
testing agent
+
deployment agent
```

This is why people who were worth "only" millions before AI can suddenly create billion-dollar companies.

The important lesson for builders: the biggest opportunities are probably not only "train a bigger model". Many fortunes may come from:

```
foundation model
        ↓
vertical agent
        ↓
real workflow replacement
        ↓
business value
```

Sierra = enterprise agents.
OpenEvidence = medical agents.

Both are examples of the same AI-native company pattern. ([Sierra][1])

References:

* Sierra official overview ([Sierra][1])
* Sierra AI agent funding/valuation coverage ([TechCrunch][4])
* OpenEvidence overview ([Wikipedia][3])

[1]: https://sierra.ai/about?utm_source=chatgpt.com "About Sierra | Sierra"
[2]: https://sierra.ai/blog/theres-an-agent-for-that-and-it-runs-on-sierra?utm_source=chatgpt.com "There's an agent for that, and it runs on Sierra | Sierra"
[3]: https://en.wikipedia.org/wiki/OpenEvidence?utm_source=chatgpt.com "OpenEvidence"
[4]: https://techcrunch.com/2025/09/04/bret-taylors-sierra-raises-350m-at-a-10b-valuation/?utm_source=chatgpt.com "Bret Taylor's Sierra raises $350M at a $10B valuation | TechCrunch"
