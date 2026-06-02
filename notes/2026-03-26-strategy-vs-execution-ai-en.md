---
audio: false
generated: true
image: false
lang: en
layout: post
title: Strategy Versus Execution in AI Development
translated: false
type: note
---

**Question:** Why do large corporations have many people who claim to have strategic insights but do nothing in actual coding or AI practice — and even figures like Kai-Fu Lee, who is great at strategy and narrative, still fall behind competitors like Kimi and MiniMax when running his own AI startup (01.ai)?

---

**Answer:**

This is a genuinely sharp observation that cuts to the heart of a well-documented phenomenon. Let's break it down systematically.

---

## 1. The "Strategy Class" Problem in Big Corporations

Large organizations structurally breed a class of people whose entire value is *narrative and positioning*, not execution. This happens for a few reasons:

**Incentive misalignment.** In big corps, visibility = promotion. Writing a deck about "AI strategy" and presenting it to a VP earns recognition. Grinding through an RLHF pipeline or debugging CUDA memory issues does not. The reward system punishes invisible engineering and rewards visible storytelling.

**The "visibility mirage."** Research found that 81% of business leaders are confident in their oversight of AI execution, yet 75% of practitioners believe leadership underestimates how hard AI execution really is. The consequence is that strategic decisions get made based on an optimistic version of reality that doesn't exist on the ground.

**Abstraction is safe.** Talking about NVIDIA, GPU compute trends, or LLM scaling laws is easy to say correctly at a high level. It requires no practical accountability. Nobody can blame you if the "strategy" turns out to be wrong — it was just a "vision."

**Size creates specialization silos.** In a 50,000-person company, it's perfectly viable for someone to spend years as a "Chief AI Strategy Officer" who has never trained a model, written a transformer attention block, or even run a fine-tuning job. The org is big enough to hide them.

---

## 2. Why Even Smart People Like Kai-Fu Lee Struggle in Execution

Kai-Fu Lee is genuinely brilliant at macro-level analysis. His book *AI Superpowers* (2018) was prescient about China's AI trajectory. He was the founding director of Microsoft Research Asia and served as president of Google China. His credentials are real.

But founding 01.ai revealed a fundamental gap between *strategic insight* and *competitive product execution*:

**01.ai leaned heavily on borrowed foundations.** His company, 01.AI, built its system using Meta's LLaMA model, which his team credits for reducing "the efforts required to build from scratch." This is not inherently bad, but it meant 01.ai was a fast-follower by design, not an original capability builder.

**Consumer traction lagged badly.** 01.ai's chatbot Wanzhi saw only 100,000 visits in September [2024], compared to over 20 million for rivals Baidu's ERNIE Bot and Moonshot's Kimi. Kimi specifically built a product-obsessed, user-feedback-driven culture that 01.ai could not match.

**He was forced to pivot away from frontier model training.** In January [2025], Lee announced 01.AI would abandon pre-training trillion-parameter models to prioritize smaller, faster, and commercially viable systems. This is a significant strategic retreat — essentially admitting that DeepSeek, Alibaba, and ByteDance have more raw compute and research depth.

**Lee himself predicted the consolidation.** Lee predicts China's AI sector will consolidate around three major AI model developers: DeepSeek, Alibaba, and ByteDance, with DeepSeek currently leading in momentum. Notably, 01.ai is not in that list.

---

## 3. Why "Insight" Does Not Transfer to Execution

Here's the core insight: **strategic pattern recognition and deep technical execution are entirely different cognitive and organizational muscles.**

Knowing that "China has strong AI engineers, low labor costs, and aggressive capital" (classic Kai-Fu Lee thesis) is valuable. But actually assembling a team that can:
- Design novel model architectures (like DeepSeek's MoE innovations)
- Optimize inference efficiency
- Build a sticky consumer product with fast iteration loops
- Compete on data flywheel effects

...requires a completely different kind of obsessive, ground-level execution culture.

Lee himself warned that "a lot of the LLM companies out there are run by researchers who care only about making a great model" — yet ironically, the companies that beat him (like DeepSeek) were exactly those technical-obsessive builders, not strategy-first leaders.

Kimi (Moonshot AI) and MiniMax were founded by young, deeply technical teams who iterated product at startup speed. The Kimi team was known as "the most AI-savvy," demonstrating an extreme pursuit of product polish. That kind of culture is hard to manufacture by someone whose primary skills are capital allocation, board relationships, and media narrative.

---

## 4. The Broader Pattern: Why This Is Structural

The disconnect has been called "the AI leadership gap" — the disconnect between executive optimism and the practical understanding needed to turn AI investment into measurable business outcomes. Research found that 58% of organizations have no clear ownership of AI initiatives and 75% lack comprehensive governance frameworks.

AI pilots fail not because of model limitations, but because integration, governance, and execution gaps overwhelm initial gains.

The uncomfortable truth is: **strategy is a commodity, execution is scarce.** Anyone can read an NVIDIA earnings call and extrapolate that GPU demand will explode. Almost nobody can build a team that ships a model better than OpenAI's at 1/10th the cost (DeepSeek did this). The market eventually prices this correctly — which is why 01.ai is fading, and DeepSeek dominates the 2025 narrative.

---

## Summary

| Trait | Strategy-Class Leaders | Execution-Class Builders |
|---|---|---|
| Core skill | Narrative, positioning | Coding, model training, product |
| Risk exposure | Low (ideas are unfalsifiable) | High (code either works or it doesn't) |
| Big corp value | High (visible, promotable) | Often invisible/undervalued |
| Startup success | Harder — no org to hide in | Stronger foundation |
| Examples | Many SVPs, some VCs, early 01.ai | DeepSeek, Kimi, early OpenAI |

The pattern you've identified is real and well-documented. The AI era is specifically brutal for strategy-only players because the product ships code, not slide decks — and the market can objectively benchmark one model against another.

---

**References:**

- [Kai-Fu Lee / 01.AI — Cornell Emerging Markets](https://business.cornell.edu/hub/2024/12/13/chinas-domestic-ai-competition-heats-up/)
- [01.AI vs Kimi usage data — Analytics India Magazine](https://analyticsindiamag.com/ai-news-updates/kai-fu-lees-ai-startups-01-ai-claims-to-have-surpassed-gpt-4o/)
- [01.AI abandons pre-training — TechNode](https://technode.com/2025/03/21/01-ai-founder-kai-fu-lee-predicts-the-endgame-of-chinas-ai-models-names-deepseek-as-frontrunner/)
- [AI Leadership Gap research — Innovation Visual](https://www.innovationvisual.com/knowledge-hub/knowledge/the-ai-leadership-gap)
- [Kai-Fu Lee warns of VC reckoning — Fortune](https://fortune.com/asia/2024/03/27/china-ai-kai-fu-lee-warns-investor-reckoning-unprofitable-ai-companies/)
- [China AI 2024 Year in Review — Recode China AI](https://recodechinaai.substack.com/p/top-10-chinas-ai-stories-in-2024)
