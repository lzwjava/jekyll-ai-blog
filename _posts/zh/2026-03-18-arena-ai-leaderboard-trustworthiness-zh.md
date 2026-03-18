---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Arena AI 排行榜可信度详解
translated: true
type: note
---

**问题：** arena.ai/leaderboard 是什么，它可靠吗？

**回答：**

## 什么是 Arena.ai Leaderboard？

Arena.ai 是一个平台，用户可以在其中并排与多个 AI models 聊天、比较响应，并投票选出最佳模型——通过真实世界的评估，众包 benchmarks 塑造了 LLMs、图像和代码 models 的公共 leaderboard。

您的投票通过 Bradley-Terry rating system 直接塑造模型排名——这是一种最初为成对比较实验开发的统计模型，类似于用于排名棋手的 Elo rating system。

Leaderboard 涵盖了许多类别：**Text、Code、Vision、Document、Text-to-Image、Image Edit、Search、Text-to-Video 和 Image-to-Video**，跟踪了来自 Anthropic、Google、OpenAI、Meta 等实验室以及许多其他实验室的数百个 models。

最初名为 LMArena，于 2026 年 1 月底更名为简称为“Arena”。2025 年 5 月，它独立成为一家获得风险投资支持的公司，以 6 亿美元估值筹集了 1 亿美元种子轮融资，随后在 2026 年初以 17 亿美元估值完成 1.5 亿美元 A 轮融资。

---

## 它如何运作

您输入一个 prompt，然后在“battle mode”中获得两个匿名 models。比较它们的响应并投票选出更好的那个后，模型身份才会揭示。这个过程会贡献于公共排名，并且一些反馈会分享给模型开发者。

---

## 它可靠吗？优势与批评

### ✅ 优势

- **基于人类偏好：** 排名基于真实用户偏好，而不仅仅是自动化 benchmarks。
- **大规模：** 数百万投票积累在众多类别中，使统计模式更具鲁棒性。
- **开放研究：** Arena 开源了世界上最大的生成模型有机人类偏好仓库，数据集免费开放访问，并在 ICML、NeurIPS 和 ICLR 发表了多篇同行评审论文。
- **匿名投票：** 投票期间模型保持匿名，以确保公平性和消除潜在偏见。

### ⚠️ 批评与已知问题

**1. 私有测试和选择性披露**

来自 Cohere Labs、AI2、Princeton、Stanford、University of Waterloo 和 University of Washington 的作者撰写的一篇 68 页论文《*The Leaderboard Illusion*》发现，未披露的私有测试实践有利于少数提供商，他们可以在公开发布前测试多个 variants，并在需要时撤回分数，导致由于选择性披露性能结果而产生的 Arena 分数偏差。

主要科技公司——包括 Meta、Google 和 OpenAI ——获得了特权访问权限，可以在 Chatbot Arena 上私下测试其 AI models 的多个版本。通过仅发布表现最佳的版本，这些公司能够提升其排名。例如，Meta 被指在 Llama 4 发布前测试了 27 个私有 variants。

**2. Llama 4 丑闻**

Llama 4 的发布陷入 leaderboard 丑闻：登顶 leaderboard 的模型并非公开发布的同一模型，这促使 Arena 发布了一份伪道歉。

**3. 刷分与 Goodhart's Law**

前 OpenAI 董事 Andrej Karpathy 指出，Arena 受到了“太多关注（部分是我的错？）”，导致实验室过度拟合它。换言之，models 可以针对 Arena 特定的动态（如格式风格、项目符号和答案长度）进行调优，而不是代表真正的真实世界质量。

在受控实验中，研究人员提交了同一模型的两个相同 checkpoints 但使用不同别名，结果在 leaderboard 上相差 17 分。同一模型的两个略有不同的版本在排名中相差近 40 分。

**4. 采样偏差**

出现的人群及其选择的 prompts 可能与您的用户不匹配。反刷分启发式和投票者人口统计数据未完全披露。

**5. 数据隐私**

您输入的任何 prompt 都会与 AI 提供商共享，并可能在研究数据集中公开。如果您测试敏感或专有信息，这一点很重要。

---

### Arena 的回应

Arena 对批评作出回应，称其模型测试政策公开可用，任何模型提供商都可以提交任意数量的公共和私有 variants。他们反驳了论文中的几项事实主张，并表示正在积极改进评估机制和透明度。

---

## 结论：有用，但需谨慎使用

Arena.ai leaderboard 是 **目前最有影响力和全面的人类偏好排名** 之一，用于 AI models。它作为方向性信号确实有用。然而，它 **不应** 被视为绝对、客观的真实依据。关于选择性测试、刷分和采样偏差的担忧是真实的。对于关键决策——尤其是任务特定、安全敏感或领域特定的决策——最好 **将 Arena 排名与其他 benchmarks 结合使用**，如 HuggingFace 的 Open LLM Leaderboard 或 Stanford 的 HELM，并理想情况下在您自己的真实用例中测试 models。

---

**参考文献：**

- [Understanding the recent criticism of the Chatbot Arena – Simon Willison](https://simonwillison.net/2025/Apr/30/criticism-of-the-chatbot-arena/)
- [Leaderboard illusion: How big tech skewed AI rankings – Computerworld](https://www.computerworld.com/article/3976355/leaderboard-illusion-how-big-tech-skewed-ai-rankings-on-chatbot-arena.html)
- [Gaming the System: Goodhart's Law in AI Leaderboard Controversy – Collinear AI](https://blog.collinear.ai/p/gaming-the-system-goodharts-law-exemplified-in-ai-leaderboard-controversy)
- [LMArena's Response to "The Leaderboard Illusion"](https://arena.ai/blog/our-response/)
- [Inside Arena, the unofficial scoreboard for the AI model wars – SmartCompany](https://www.smartcompany.com.au/artificial-intelligence/arena-ai-leaderboard-ranking-models-explained/)
- [Arena AI Model Evaluator Review – AI Founder Kit](https://aifounderkit.com/ai-tools/arena-ai-model-evaluator/)