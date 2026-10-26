---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM演进的五个章节
translated: true
type: note
---

**问题：** LLMs 在近年来是如何演变的？

**答案：**

这个故事清晰地分为五个阶段：

**2022 — 觉醒。** 2022年末ChatGPT的出现普及了交互式对话，并引发了大规模采用。LLM演变的五个时代时间线从foundation（2017–2018），经过scaling（2019–2020）、scaling breakthroughs（2021–2022）、efficiency and democratisation（2022–2024），最后是multimodal and reasoning specialisation（2024–2026）。

**2023 — Open source 与 multimodal。** 2023年和2024年，LLaMA等open source项目以及专门化instruction tuning的兴起加速了进展，为更大规模的multimodal能力和更长的context windows铺平了道路。

**2024 — Reasoning 转折点。** 它始于OpenAI在2024年9月发布的o1-preview——首个公开的reasoning模型——其架构内部称为“Strawberry”。与此同时，小型模型表现出巨大的性能提升：4B参数模型最终将超越2024年的70B模型。

**2025 — DeepSeek时刻。** 2025年1月下旬，DeepSeek-R1因其性能与OpenAI、Anthropic和Google的顶级专有模型相当，且价格显著更低，而登上主流科技和金融新闻。与OpenAI的o1相比，DeepSeek R1的训练和部署成本约低95%，使其更易获得，并让高性能reasoning模型走向普及。

**2026 — 整合。** 我对时间线的解读是：模型的“核心”reasoning在2024年经历了最后一次大跃升。2026年是打磨harness的一年——即使基础智能几乎停滞，model+harness的组合也变得更加有能力。

脉络很清晰：从scale → alignment → multimodal → open-source → reasoning → agents。每一年的突破都重新定义了*下一个*突破必须是什么。

---

**参考资料：**
- [LLM演变五个时代 — arXiv LAAF论文](https://arxiv.org/pdf/2608.27102)
- [DeepSeek R1：梳理炒作 — IBM](https://www.ibm.com/think/topics/deepseek)
- [LLM历史里程碑2022–2026 — CloudInsight](https://cloudinsight.cc/en/blog/llm-guide)
- [2025年回顾 — Zvi Mowshowitz](https://thezvi.substack.com/p/2025-year-in-review)
- [LLMs + Agents = 足够有能力 — Akita on Rails](https://akitaonrails.com/en/2026/10/12/llms-agents-competent-enough/)