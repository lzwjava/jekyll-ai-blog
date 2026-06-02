---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Jeff Dean 与 Noam Shazeer AI 对谈录
translated: true
type: note
---

Question: Noam Shazeer 在 YouTube 视频 https://www.youtube.com/watch?v=v0gjI__RyCY&t=4s 中说了什么？

Answer:

该视频是一段时长超过 2 小时的播客访谈，标题为“Jeff Dean & Noam Shazeer — 25 years at Google: from PageRank to AGI”，由 Dwarkesh Patel 主持（2025 年 2 月上传）。视频邀请了 Google Chief Scientist Jeff Dean 和 Noam Shazeer（Transformer 架构、Mixture of Experts 以及其他关键 AI 技术的共同发明人），探讨他们在 Google 的职业生涯、AI 系统的演变、Hardware 趋势、Scaling laws、Large Language Models 的未来以及通往 Artificial General Intelligence (AGI) 的路径。

Noam Shazeer 在整个对话中进行了大量的发言，与 Jeff Dean 轮流回应主持人的提问。他的贡献包括个人轶事、技术见解以及对 AI 发展的远见。

Noam Shazeer 谈到的核心话题和部分语录包括：

- **加入 Google 及早期的 AI 兴趣**：他描述了在 1999 年招聘会上看到 Google 的情景，因为其搜索查询量的指数级增长而申请入职，最初计划在那短暂工作以资助独立的 AI 研究。“我觉得它是我最喜欢的搜索引擎……看起来是一群聪明人在做有意义的事情。他们有一个非常漂亮的蜡笔图……每日搜索查询量……看起来非常符合指数增长。”

- **Hardware 与 Moore's Law**：他指出从通用 CPU 向 TPU 等专用 Accelerator 的转变。“最近，基于通用 CPU 的机器 Scaling 效果已经没那么好了……但我们看到了更多专门的计算设备，比如 Machine Learning Accelerators、TPUs……这使得我们实际上能够获得极高的性能。”

- **Mixture of Experts (MoE) 与模块化**：作为现代 MoE 技术的发明者，他主张使用 Sparse Models，由不同的 Expert 处理不同的任务，从而实现 Continual Learning 和更好的 Interpretability。“我一直是 Sparse Models 的忠实粉丝……模型的不同部分擅长不同的事情……我认为我们应该拥有更具有机性的结构。”

- **Distillation 与模型效率**： “Distillation 是一个非常有用的工具……你可以将模型转换成不同的形式……在模块级别……这是一个持续的过程，每个模块都有几种不同的表示。”

- **Inference Scaling 与更长的 Context**：他讨论了在 Inference 阶段提升模型性能以及处理海量 Context 的问题。“你希望系统能积极探索一系列不同的潜在解决方案……拥有一个拨盘，让你通过增加 Inference Time Compute 来让模型给出更好的答案。” 此外，“如果模型能处理数万亿个 Tokens 就太好了……它能否在获得我许可的情况下，处理整个互联网……以及你所有的个人信息。”

- **Interpretability**： “实际上，在过去，我发现 Experts 相对容易理解……这个 Expert 负责指代圆柱形物体的单词。而这个则非常擅长日期。”

- **Sample Efficiency 与训练目标**：对比人类学习：“一个人看过十亿个 Tokens……他们就在很多事情上表现得非常出色。” 他建议改变超越 Next-token Prediction 的目标。

视频从开头附近开始（t=4s 基本上是开场），主持人介绍了嘉宾，Noam 随后说道：“谢谢。非常激动能来到这里。”

如需获取 Noam Shazeer 发言的完整详细记录，请参阅视频描述中链接的官方 Transcript。

References:

- [YouTube Video](https://www.youtube.com/watch?v=v0gjI__RyCY)
- [Full Transcript](https://www.dwarkeshpatel.com/p/jeff-dean-and-noam-shazeer)
