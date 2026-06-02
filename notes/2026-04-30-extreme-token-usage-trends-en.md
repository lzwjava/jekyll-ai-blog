---
audio: false
generated: true
image: false
lang: en
layout: post
title: Extreme Token Usage Trends
translated: false
type: note
---

Question: Is it currently possible to spend more than 100 million tokens per day, what is the trend, and how many people (e.g., 100k engineers) are able to reach that level?

Answer:

### 1. Is **>100 million tokens/day** possible?

Yes — and it’s already happening, but mostly in **extreme or automated setups**, not normal usage.

* A real example: one engineer used **~234 million tokens/day equivalent** via heavy automation (AI agents) ([Business Insider][1])
* Companies like Meta reportedly consume **tens of trillions of tokens monthly** at scale ([Business Insider][2])

👉 Key insight:

* Humans alone rarely reach that level
* **Agent systems (multi-agent loops, autonomous workflows)** are what push usage into 100M+/day territory

---

### 2. Is this common?

No — it’s still **very rare at the individual level**.

From available data and discussions:

* Typical heavy individual engineer:

  * ~10M–100M **per month**, not per day
* Extreme individual users (rare):

  * Hundreds of millions to billions **per month**
* Hitting **100M/day consistently**:

  * Requires:

    * automation (agents)
    * large-scale pipelines
    * or intentional “token-maxing”

Even in companies:

* Only **top power users** hit these levels
* One dataset showed thousands of employees, but only a **tiny fraction dominate usage** ([Business Insider][1])

👉 So your “100k engineers doing this?”
**No — not even close.**
More realistic:

* Probably **hundreds to a few thousand globally** (rough estimate)
* Mostly:

  * AI infra engineers
  * agent framework builders
  * well-funded startups

---

### 3. Trend (this is the important part)

There *is* a clear trend toward massive token usage:

#### (1) Prices are collapsing

* Token cost dropped **~80–95% since 2023** ([LLM Versus][3])

#### (2) But total spending is rising

* Because usage explodes faster than price drops
* Especially due to:

  * agents
  * long context
  * iterative workflows

#### (3) “Token-maxxing” is emerging

* Some startups explicitly encourage high token usage
* Seen as:

  * productivity multiplier
  * replacement for hiring engineers ([Business Insider][4])

#### (4) Agents change everything

* A single human → thousands of AI calls/day
* That multiplies token usage by **10x–1000x**

---

### 4. Practical intuition

To understand scale:

* 1M tokens ≈ ~750,000 words ([LLM Versus][3])
* 100M tokens/day ≈
  → ~75 million words/day
  → equivalent of **~100 books/day**

That’s clearly not human-driven — it’s **machine loops**.

---

### 5. Bottom line

* ✅ Possible today: **Yes**
* ⚠️ Common: **No (extreme outliers only)**
* 📈 Trend: **Rapid growth, driven by agents**
* 👥 People at that level:

  * Not 100k
  * Likely **<< 1% of engineers**
  * Concentrated in top AI-heavy orgs

---

### 6. The deeper reality (important insight)

The industry is shifting from:

> “How smart is the model?”

to:

> “How many tokens can your system effectively use?”

This is why:

* Token usage is becoming a **new productivity metric**
* But also a **cost + efficiency trap**

---

If you want, I can break down:

* what workflows actually consume 100M+/day
* or how to design systems that scale tokens efficiently without wasting money

[1]: https://www.businessinsider.com/how-disney-tech-employees-are-using-ai-claude-cursor-tokens-2026-4?utm_source=chatgpt.com "One Disney employee calls Claude 51,000 times a day. Internal docs reveal how the Mouse House is using AI."
[2]: https://www.businessinsider.com/disney-ai-adoption-dashboard-tokens-tokenmaxxing-claude-cursor-josh-damaro-2026-4?utm_source=chatgpt.com "Disney staffers have an 'AI Adoption Dashboard.' One Claude user invoked the chatbot 460,000 times in 9 days."
[3]: https://www.llmversus.com/blog/llm-token-pricing-explained?utm_source=chatgpt.com "LLM Token Pricing Explained: What You're Actually Paying For | LLMversus Blog | LLMversus"
[4]: https://www.businessinsider.com/startups-tokenmaxxing-token-quotas-2026-4?utm_source=chatgpt.com "Some startups are tokenmaxxing. Others tell us it's a 'stupid' trend that will die out."
