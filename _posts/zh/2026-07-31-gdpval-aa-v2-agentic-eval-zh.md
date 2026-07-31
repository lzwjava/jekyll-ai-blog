---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GDPval-AA v2 代理评估
translated: true
type: note
---

Question: LLM 评估中的 GDPval-AA v2 是什么？

Answer: 这是 Artificial Analysis 在 OpenAI 原始 GDPval 数据集基础上构建的第二代测试框架。

**基础数据集 (OpenAI, 2025 年 10 月):** 包含 220 个任务，这些任务由行业专业人士的代表性工作构建而成，从业者平均拥有 14 年经验，覆盖了美国劳工统计局针对 44 个职业（分属美国 GDP 贡献最大的 9 个行业）所列出的绝大多数工作活动。

**AA 新增内容 (v2):** 他们并非仅根据评分标准打分——模型通过 agentic 循环（借助其“Stirrup”框架）获得 shell 访问权限和网页浏览能力来解决问题，并生成实际交付物——文档、幻灯片、图表、电子表格。评分采用盲法成对比较：两个模型的输出被匿名化，由 LLM 裁判选出胜者，结果汇总为 Elo 评分——思路与 LMArena/Chatbot Arena Elo 相同，但针对的是 agentic 知识工作输出而非聊天回合。

关键机制：
- Elo 以 **人类专家基线 ≈ 1000** 为锚点
- 这是一个动态排行榜——新模型的加入会改变所有人的 Elo，因为它是相对排名
- 在 v2 发布时（2026 年 6 月中旬），Claude Fable 5 / Opus 4.8 / GPT-5.5 位居前列；根据 datalearner 抓取的最新数据，目前 Kimi K3 和 Gemini 3.6 Flash 也位列其中——榜单变化很快，请查看下方实时链接，不要依赖任何快照。

为什么这对你的用例比 MMLU 类基准测试更重要：它是在工具使用场景下对 **基于文件的 agentic 输出**（电子表格、演示文稿、备忘录）进行评分，这比多项选择评估更接近你的 CLI agent（ww/iclaw/zz）实际需要擅长的能力。

参考资料：
- [GDPval-AA v2 排行榜 — Artificial Analysis](https://artificialanalysis.ai/evaluations/gdpval-aa)
- [GDPval 原始论文 (OpenAI, arXiv)](https://arxiv.org/abs/2510.04374)
- [GDPval-AA v2 基准测试说明](https://systems-analysis.ru/eng/GDPval-AA_v2)