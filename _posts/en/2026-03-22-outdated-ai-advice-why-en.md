---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why AI Models Give Outdated Advice
translated: false
type: note
---

**Question:** Why do AI chatbots like Grok or Claude fail to recommend newer, preferred contact methods (such as HSBC HK's "Chat with Us" feature) and instead default to older methods like calling, and what is the root cause of this limitation?

**Answer:**

You have identified a very real and well-understood structural problem with general-purpose LLMs applied to real-world institutional contexts. Here is a thorough breakdown:

---

## The Core Problem: Knowledge Cutoff + Token Frequency Bias

LLMs are trained on large sums of data only up to a certain date. If you ask a question about something that happened recently — after the training cutoff — the model likely will not have an accurate answer. This also means the AI might not have available knowledge to answer very specific and technical questions about newer features.

This is exactly the situation with HSBC HK's **"Chat with Us"** feature. HSBC HK actively promotes this in-app messaging service, encouraging customers to go to the Support tab and tap "Chat with Us" to get help instantly, with no more waiting on the phone for answers. But a general-purpose LLM trained before this feature became prominent — or before HSBC HK started pushing it as the preferred channel — simply won't know to recommend it.

Beyond the cutoff, there is a second problem: **token frequency/pattern bias**. LLMs generate responses based on what patterns were most common in their training data. Since "call the hotline" has been the dominant customer service advice for decades across billions of web pages, the model statistically gravitates toward suggesting phone calls — even when newer, better options exist. It is not following HSBC HK's current institutional preferences; it is echoing the statistical weight of old text.

---

## Why This Is Particularly Bad for Banking Contexts

LLMs may face difficulties executing or referencing tasks that require interaction with external systems — such as processing payments, updating databases, or handling complex workflows. The limited availability of robust integrations hampers LLMs' capacity to facilitate seamless end-to-end transactions, diminishing their suitability for customer support scenarios.

In banking, this is compounded because:

- **Institutional instructions are not public training data.** HSBC HK's internal policy to prefer "Chat with Us" over phone calls is not something scraped from the internet and put into a training corpus.
- **New features launch faster than models retrain.** In the dynamic environment of customer service, company policies, product specifications, and operational procedures constantly evolve. Maintaining the freshness of an AI's knowledge base isn't just a technical task — it's a critical business imperative. Outdated or inaccurate information fed to a customer service AI can lead to incorrect responses, customer dissatisfaction, and a negative impact on brand credibility.
- **Hallucination risk.** LLMs are prone to hallucinations — they are capable of making up fake information and have a tendency to fill in gaps in a strikingly confident and assertive manner.

---

## The Right Solution: RAG (Retrieval-Augmented Generation)

The standard industry fix for this is **RAG — Retrieval-Augmented Generation**:

RAG is a powerful technique that requires no additional training of the LLM. It provides more up-to-date information and mitigates LLM hallucinations by selecting and providing relevant, current knowledge at query time.

When a customer query comes in, the RAG system first searches internal knowledge bases — documents, databases, policies, FAQs — for relevant information. This retrieved, factual information is then provided to the LLM as context alongside the customer's query, so the LLM uses specific context to generate an accurate, relevant, and grounded response. Essentially, RAG gives the LLM access to the company's collective, up-to-date brain.

For HSBC HK specifically, a properly built system would:

1. Have an always-updated knowledge base that explicitly states **"Chat with Us" is the preferred first contact method for payment and general queries**.
2. Feed that policy to the LLM at inference time via RAG.
3. Add **guardrails** so the model cannot default to phone-call suggestions when a digital chat option is available and preferred.

---

## Summary Table

| Problem | Root Cause | Fix |
| --- | --- | --- |
| LLM recommends calling instead of "Chat with Us" | Knowledge cutoff — feature didn't exist or wasn't prominent in training data | RAG with live HSBC policy docs |
| LLM defaults to old patterns statistically | Token frequency bias toward "call the hotline" in training corpus | Explicit system-prompt instructions + guardrails |
| LLM ignores HSBC HK's institutional preferences | General LLMs are not trained on internal bank SOPs | Fine-tuning or RAG on HSBC-specific knowledge base |
| New features not reflected in answers | Static training snapshot vs. rapidly evolving product features | Continuous knowledge base refresh pipeline |

---

Your observation is correct: **general-purpose LLMs are structurally unsuited to give accurate, policy-compliant customer service guidance for institutions like HSBC HK without being grounded in live, institution-specific knowledge.** The model is not "wrong" by its own logic — it is simply optimizing on stale, generic training signals rather than following HSBC HK's current and evolving service preferences.

**References:**

- [HSBC HK Contact Us – Chat with Us](https://www.hsbc.com.hk/help/contact/)
- [Limitations of Generative AI for Customer Service – Ada](https://www.ada.cx/blog/getting-around-the-limitations-of-generative-ai-for-customer-service/)
- [RAG and LLMs in Customer Service – deepsense.ai](https://deepsense.ai/blog/ai-in-customer-service-how-rag-and-llms-are-transforming-support-at-scale/)
- [LLM Limitations and Risks – Master of Code](https://masterofcode.com/blog/generative-ai-limitations-risks-and-future-directions-of-llms)
