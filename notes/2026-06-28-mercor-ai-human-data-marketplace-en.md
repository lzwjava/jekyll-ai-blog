---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Mercor: AI Human-Data Marketplace"
translated: false
type: note
---

Question: What is Mercor, the AI company?

Answer:

Let me search for current information.Answer:

Mercor is an American AI company that provides experts to train AI models and chatbots. It's essentially a human-data marketplace sitting between AI labs and domain experts — the "new oil" play on high-quality RLHF/expert data rather than data centers or models.

**The basics:**
- Founded in 2023 by Brendan Foody, Adarsh Hiremath, and Surya Midha — three Bay Area high school friends from the Bellarmine debate team who dropped out of college and got Thiel Fellowships. HQ in San Francisco.
- Originally an AI recruiting startup — it began connecting freelance programmers in India with US companies, with an AI platform to interview and match them. Then it pivoted to data labeling / expert contractor matching for AI companies like OpenAI.
- Customers include OpenAI and Anthropic. It manages ~30,000 contractors as of October 2025 — engineers, lawyers, doctors, bankers, journalists.

**The money:**
- $3.6M seed (2023, General Catalyst) → $32M Series A (2024, Benchmark, $250M valuation) → $100M Series B (Feb 2025, Felicis, $2B valuation).
- $350M Series C in October 2025 at a $10B valuation — making the then-22-year-old founders the youngest self-made billionaires. Backers include Peter Thiel, Jack Dorsey, and Adam D'Angelo.

**Relevant to your world (benchmarks):**
Mercor produces **APEX-Agents**, an open-source benchmark of 480 tasks across investment banking, management consulting, and corporate law — with tool implementations, rubrics, and grading workflows. Frontier models cluster tightly on it: GPT-5.4 at 33.3%, Claude Opus 4.6 at 33.0%, Gemini 3.1 Pro Preview at 32.0% — the top three separated by just 1.3 percentage points. They also built **APEX-SWE** with Cognition, where every frontier model fails on nearly 60% of real production software engineering tasks. Worth a look if you're benchmarking agents on professional knowledge work.

**The controversy:**
- In late March 2026, Mercor was hit by a supply-chain attack involving the LiteLLM package, potentially exposing up to 4 TB of internal data and contractor PII — leading to class-action lawsuits and a temporary pause from clients including Meta. (Notable for you specifically — LiteLLM is widely used as an LLM proxy/router.)
- Contractors interviewed by The Verge, NY Magazine, and Wired reported a stressful environment, poor management, and declining pay.
- Some critics argue the "AI interviews" are partly a data-harvesting funnel for training rather than pure hiring.

The thesis Foody pushes: if AI automates 90% of the economy, humans become the bottleneck on the remaining 10%, giving 10x leverage on every unit of human economic output. Mercor positions itself as the marketplace allocating that scarce human expertise to AI training.

References:

- [Mercor - Wikipedia](https://en.wikipedia.org/wiki/Mercor)
- [Mercor raises $100M at $2B valuation - TechCrunch](https://techcrunch.com/2025/02/20/mercor-an-ai-recruiting-startup-founded-by-21-year-olds-raises-100m-at-2b-valuation/)
- [Mercor | LinkedIn (APEX-Agents benchmarks)](https://www.linkedin.com/company/mercor-ai)
- [What is Mercor AI? - eesel AI](https://www.eesel.ai/blog/mercor-ai)
