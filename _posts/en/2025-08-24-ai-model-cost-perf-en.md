---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Model Cost and Performance Guide
translated: false
type: note
---

Here’s a clearer breakdown of the **benchmark scores** and **API pricing** for each model—Claude 4 Opus (also noted as Claude Opus 4), GPT‑5 (standard/full), GPT‑5 Mini, GPT‑5 Nano, plus o3 (OpenAI), and Claude 4 Sonnet—without using tables, to keep things neat and readable.

---

## Benchmark Performance (SWE-bench)

This reflects how well models perform on software engineering tasks:

* **Claude 4 Opus (May 14, 2025)**: 67.60
* **GPT‑5 (Aug 7, 2025, medium reasoning)**: 65.00
* **Claude 4 Sonnet (May 14, 2025)**: 64.93 ([SWE-bench][1])

**Takeaway**: Claude 4 Opus leads slightly in SWE-bench performance, followed closely by GPT-5 and Claude-Sonnet.

---

## API Pricing (per million tokens)

### **Claude 4 Opus**

* Input: **\$15**
* Output: **\$75** ([Anthropic][2], [LaoZhang AI][3], [Simon Willison’s Weblog][4])

### **GPT-5 (standard/full)**

* Input: **\$1.25**
* Cached input (when reused): **\$0.125**
* Output: **\$10** ([OpenAI][5])

### **GPT-5 Mini**

* Input: **\$0.25**
* Output: **\$2** ([OpenAI][5], [WIRED][6])

### **GPT-5 Nano**

* Input: **\$0.05**
* Output: **\$0.40** ([OpenAI][5], [WIRED][6])

### **o3-mini** (for context)

* Pricing available via o4‑mini reference:
* Input: **\$1.10**, Output: **\$4.40** ([Simon Willison’s Weblog][4])

### **Claude 4 Sonnet**

* Input: **\$3**, Output: **\$15** ([LaoZhang AI][3])

---

## Quick Comparison Highlights

* **Best performance**: Claude 4 Opus slightly outperforms both GPT-5 and Claude Sonnet in coding benchmarks.
* **Lowest cost per token**:

  * **GPT-5 Nano** is the cheapest by far—perfect for lightweight tasks like summarization.
  * **GPT-5 Mini** offers a balance of speed and affordability.
  * **GPT-5 standard** remains quite cost-effective, especially with cheap caches.
* **Claude models**, both Opus and Sonnet, are significantly more expensive per token but justify their pricing via stronger reasoning and agent capabilities.

---

## Summary (clear and concise):

* **Claude 4 Opus**: Top performance, high cost (\$15 in / \$75 out).
* **GPT-5 (full)**: Great performance (just behind Opus), much cheaper (\$1.25 in / \$10 out).
* **GPT-5 Mini**: Mid-tier budget-friendly option (\$0.25 in / \$2 out).
* **GPT-5 Nano**: Ideal for lightweight tasks or large-scale low-cost use (\$0.05 in / \$0.40 out).
* **Claude 4 Sonnet**: Middle-ground cost/performance (\$3 in / \$15 out), but benchmark slightly below the others.

---

Let me know if you’d like help estimating the **monthly cost** for a particular usage pattern, or need comparisons factoring in prompt caching and batch discounts!

[1]: https://www.swebench.com/?utm_source=chatgpt.com "SWE-bench Leaderboards"
[2]: https://www.anthropic.com/pricing?utm_source=chatgpt.com "Pricing"
[3]: https://blog.laozhang.ai/ai-tools/claude-4-pricing-guide-2025/?utm_source=chatgpt.com "Claude 4.0 Pricing Guide: Complete Cost Analysis & Best ..."
[4]: https://simonwillison.net/2025/Aug/7/gpt-5/?utm_source=chatgpt.com "GPT-5: Key characteristics, pricing and model card"
[5]: https://openai.com/api/pricing/?utm_source=chatgpt.com "API Pricing"
[6]: https://www.wired.com/story/openais-gpt-5-is-here/?utm_source=chatgpt.com "OpenAI Finally Launched GPT-5. Here's Everything You ..."
