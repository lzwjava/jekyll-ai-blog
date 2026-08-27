---
audio: false
generated: true
image: false
lang: en
layout: post
title: China’s Second-Tier AI Model Boom
translated: false
type: note
---

**Question:** Are "second-tier" Chinese companies like Weibo and Ant Group (with its Ling model) joining the AI model race — even though Alibaba already has Qwen?

**Answer:**

You're spot on — it really is a golden age of proliferation. Both Weibo and Ant Group are very much in the game, and independently of Qwen.

**Weibo — VibeThinker series**

Weibo's AI division released the open-source VibeThinker-1.5B, a 1.5B parameter LLM fine-tuned from Alibaba's Qwen2.5-Math-1.5B, available under MIT license on Hugging Face, GitHub, and ModelScope. The notable twist: the post-training cost was only $7,800, far less than what similar models typically require. They kept going — VibeThinker-3B scored 94.3 on AIME 2026, placing it alongside DeepSeek V3.2 and its 671 billion parameters, built on top of Qwen2.5-Coder-3B as its base architecture.

So interestingly, Weibo is *building on top of* Qwen rather than competing with it head-on — using Qwen as a foundation and differentiating with their post-training recipe.

**Ant Group — Ling / Ring / Ming family**

Ant Group (Alipay's parent) is going much bigger and more independently. In February 2026, Ant Group released Ling-2.5-1T, its newest trillion-parameter LLM, and Ring-2.5-1T, claimed to be the world's first hybrid linear-architecture thinking model — both available under open licenses on Hugging Face and ModelScope. The family has three lines: the Ling non-thinking models, the Ring thinking models, and the multimodal Ming series. The efficiency story is compelling: Ling-2.5-1T matches frontier reasoning models on AIME 2026 while using only ~5,890 tokens, versus the 15,000–23,000 tokens comparable systems require.

**The Qwen question**

Yes, Alibaba has Qwen and Ant Group is technically an Alibaba affiliate — but they operate quite separately and have their own R&D teams and strategic motivations. Ant needs AI for fintech use cases (compliance, fraud, customer service) and clearly wants its own stack. As for Weibo, they lean on Qwen as a base, which actually validates Qwen's role as a platform for the ecosystem rather than being undermined by it.

The broader dynamic you're pointing to is real: the cost of building competitive specialized models has dropped so dramatically that even social media platforms and fintech firms can field credible research teams. It's less "everyone building from scratch" and more "everyone fine-tuning and post-training with novel techniques on cheap compute" — which is arguably even more interesting.

**References:**

- [Weibo's VibeThinker-1.5B (VentureBeat)](https://venturebeat.com/ai/weibos-new-open-source-ai-model-vibethinker-1-5b-outperforms-deepseek-r1-on)
- [VibeThinker-3B matches DeepSeek V3.2 (CryptoBriefing)](https://cryptobriefing.com/sina-weibo-vibethinker-3b-matches-top-ai-models/)
- [Ant Group releases Ling-2.5-1T and Ring-2.5-1T (BusinessWire)](https://www.businesswire.com/news/home/20260215551663/en/Ant-Group-Releases-Ling-2.5-1T-and-Ring-2.5-1T-Evolving-Its-Open-Source-AI-Model-Family)
- [Ant Group Ling-2.6-Flash (BusinessWire)](https://www.businesswire.com/news/home/20260422256825/en/Ant-Group-Unveils-Ling-2.6-Flash-A-Major-Leap-in-AI-Efficiency)
