---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hugging Face的崛起
translated: true
type: note
---

**问题：** Hugging Face 的故事是什么——它何时诞生，如何成长，由谁创立，以及团队如何演变？

---

## Hugging Face 的故事

### 起源：三个法国人、一个聊天机器人和艾伦·莫里塞特的翻唱

故事始于 2016 年的巴黎。朱利安·肖蒙在 Stupeflix 担任软件工程师时，与他在工程学校认识的老朋友托马斯·沃尔夫重新联系上了——他们曾一起组摇滚乐队，翻唱艾伦·莫里塞特的歌曲。两人与肖蒙早已认识的克莱芒·德朗格一起，三人共同创立了 Hugging Face。

创始人的背景从一开始就互补：

- 克莱芒·德朗格带来商业头脑，朱利安·肖蒙提供工程技能，托马斯·沃尔夫拥有研究背景。
- 托马斯·沃尔夫拥有物理学博士学位，并发表过机器学习领域的研究论文。

最初的产品：一个面向青少年的 AI 驱动聊天机器人——他们并非要打造 AI 革命的基础设施，只是想做些有趣的东西。

### 2016–2018 年：消费者聊天机器人阶段

团队在获得美国投资者 Betaworks 的 20 万美元种子投资并进入其聊天机器人加速器项目后，搬到了纽约。他们在法国绝对无法凭这种 pitch 融到资——这强烈表明，当时法国创业生态系统尚未准备好押注消费者 AI。

在开发出最初的聊天机器人理念后，创始人参加了 Betaworks 加速器项目，该项目提供了早期种子资金，并帮助公司在美国站稳脚跟。

### 2018 年：BERT 时刻——真正的转折点

这是 HF 历史上的关键事件。2018 年底，谷歌发布 BERT 成为重要转折点。Hugging Face 团队在一周内快速制作并开源了 BERT 的 PyTorch 实现。肖蒙表示，这一时刻明确了公司方向，促使 Hugging Face 在 2019 年正式转型，从消费者聊天机器人转向构建开源 ML 基础设施。

那个周末的冲刺——在一周内推出 BERT 的 PyTorch 移植版——常被引为定义公司未来方向的那一刻。

洞察：创始人意识到，虽然人们喜欢他们的聊天机器人，但开发者需要的是工具。

### 2019 年：Transformers 库 + A 轮融资

从聊天机器人转型为以开发者为中心的公司后，Hugging Face 在 2019 年发布 Transformers 库，该库统一了对 BERT、GPT-2 及其他先进模型的访问，推动了爆炸式增长。

融资：2019 年 12 月，Hugging Face 在由 Lux Capital 领投的 A 轮融资中筹集了 1500 万美元，参投方包括 A.Capital、Betaworks、理查德·索彻（Salesforce 首席科学家）、格雷格·布罗克曼（OpenAI 联合创始人兼 CTO）、凯文·杜兰特及其他天使投资人。早期天使投资人包括格雷格·布罗克曼，这是一个强烈的信号——OpenAI 网络早早看到了这笔赌注。

### 2020–2021 年：规模化与 B 轮融资

到 2020 年中，团队在巴黎和纽约两地扩张，从 Google Research 和 FAIR 招募人才，月下载量达到约 100 万次。融资和产品扩展加速，涉足视觉、音频和生物领域。

2021 年 3 月，由 Addition VC 领投的 B 轮融资筹集了 4000 万美元。

此时收入：Hugging Face 在 2021 年实现了 1000 万美元收入。

### 2022 年：C 轮融资——估值 20 亿美元，ML 界的 GitHub

2022 年 5 月，Hugging Face 在由 Lux Capital 领投的 C 轮融资中筹集了 1 亿美元，以 20 亿美元估值加入双独角兽俱乐部。投资者包括 Sequoia、Coatue、Addition。

收入：2022 年 1500 万美元。

这也是其“ML 界的 GitHub”定位得以巩固的时候。该平台现在拥有 100 万月活跃用户，肖蒙将其描述为“机器学习的 GitHub”。

### 2023 年：D 轮融资——估值 45 亿美元，获所有主要科技公司支持

Hugging Face 的最新估值为 45 亿美元，基于 2023 年 D 轮融资筹集 2.35 亿美元，较此前 20 亿美元估值翻了一倍多。

D 轮投资者包括 Salesforce Ventures（领投）、谷歌、英伟达、亚马逊——几乎所有超大规模云服务商都在为开源 ML 中心下注。截至 2023 年，年化收入约为 5000 万美元，超过 10,000 家公司使用该平台。

---

## 时间线总结

| 年份 | 事件 |
|------|------|
| 2016 | 在纽约成立（法国创始人），面向青少年的消费者聊天机器人，Betaworks 种子轮 20 万美元 |
| 2018 | BERT 发布 → HF 在 1 周内推出 PyTorch 移植版 → 决定转型 |
| 2019 | Transformers 库发布，A 轮融资 1500 万美元（Lux Capital，格雷格·布罗克曼天使投资） |
| 2020 | 月下载量达 100 万，团队从 Google Research 和 FAIR 招聘人员扩张 |
| 2021 | B 轮融资 4000 万美元，收入 1000 万美元，Hub 上线 |
| 2022 | C 轮融资 1 亿美元，估值 20 亿美元（Sequoia、Coatue），收入 1500 万美元 |
| 2023 | D 轮融资 2.35 亿美元，估值 45 亿美元，年化收入约 5000 万美元，谷歌/英伟达/亚马逊成为投资者 |
| 2026 | 约 731 名员工，Hub 上模型超 100 万个 |

---

## 为什么能成功

战略核心是：**免费提供库，通过基础设施赚钱**。团队和组织使用付费工作空间，每位用户每月 20 美元；大型客户按使用量付费使用推理端点，CPU 实例每小时 0.033 美元起。企业版计划增加了自定义基础设施、SSO、审计日志。

这是经典的开源策略——Redis、MongoDB、Elastic——但执行时机恰到好处，正值 Transformer 革命让每个团队都能使用 ML。Transformers 库成为了标准抽象层。如果你控制了抽象层，你就拥有了整个生态。

对你个人而言：HF 的故事与你正在构建的东西有相似之处。他们通过最快实现 BERT 并将其开源而获胜——速度 + 开源 + 开发者信任，而非精致的成品。他们早期的护城河与你的应该相同：深厚的技术可信度，而非市场营销。

---

**参考资料：**

- [Hugging Face 业务解析与创立故事 — Contrary Research](https://research.contrary.com/company/hugging-face)
- [在美国融资与新兴创始人工厂 — Sifted](https://sifted.eu/articles/hugging-face-interview-julien-chaumond)
- [从开源到十亿美元估值 — WeAreFounders](https://www.wearefounders.uk/from-open-source-to-billion-dollar-valuation-the-hugging-face-founders/)
- [HuggingFace 统计数据 — Originality.AI](https://originality.ai/blog/huggingface-statistics)
