---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: xAI 内部机密
translated: true
type: note
---

Question: Sulaiman Ghori 在播客中关于 xAI 说了什么？

Answer: 

xAI 的前 Member of Technical Staff，Sulaiman Ghori，参加了由 Ti Morse 主持的名为“Relentless”的播客，该集标题为“WTF is happening at xAI”，发布于 2026 年 1 月 15 日左右。在约 1 小时 11 分钟的访谈中，他提供了关于 xAI 文化、运营、项目以及与 Elon Musk 共事的罕见内部见解。他讨论的核心点包括：

- **公司文化与速度**：xAI 以极快的速度和高 agency 运作。工程师拥有极大的自主权——如果有好的想法，没有人会说“不”，当天就可以实施并展示反馈。公司结构扁平，仅分为三个层级：Individual contributors、Cofounders/managers 以及 Elon Musk。团队小而精（例如 iOS 团队仅 3 人，早期的 Macrohard 仅 2 人）。他强调了激进的自主权、自下而上的创新、快速迭代（例如 24 小时周期）以及带有高强度冲刺的“War room”文化，包括周末和超长办公时间。

- **入职与适应**：Ghori 于 2025 年 3 月加入 xAI，几乎没有指导——第一天只有一个笔记本电脑和工牌。他最初负责 Ask Grok，随后在多个项目间切换。

- **主要项目**：
  - **Macrohard**：一个关键项目，旨在构建“Human emulators”或数字人类模拟器，模仿人类的数字行为（如键盘/鼠标输入、屏幕决策），而无需特定的软件集成。目标是自动化任何数字人类任务，并在真实场景中部署 AI agents。他们在内部测试了虚拟 AI“员工”，有时会引起混乱（例如 Hallucinations 导致尴尬的互动，比如邀请同事在空座位处面谈）。长期目标：扩展到数百万个 emulators，潜在挑战如 Microsoft 等公司的工具。
  - **Grok 及相关功能**：讨论了 Grokipedia（可能是为 Grok 建立的以真相为核心的知识库），处理 Elon 在 X 上看到的 Grok 错误输出（Elon 会直接干预），以及探索 AI 中的“真相”（将其描述为一个与物理基础相关的、类似鸡生蛋蛋生鸡的难题）。

- **基础设施与硬件优势**：xAI 认为硬件/Compute 是实现 AGI 的真实瓶颈，而非软件。他们迅速建造了 Colossus 超级计算机（用时 122 天）。创新方法包括利用 Tesla 车辆的计算机（特别是 HW4）作为分布式 Compute（比云端 VM 资本效率更高）进行模拟和训练——本质上是“依托 Tesla 网络进行引导”。提到了使用移动发电机和电池组进行电力平衡。

- **Elon Musk 的风格**：Musk 会提前预测瓶颈，快速解决问题（如隔夜发布补丁），提供直接反馈，并乐于接受数据/实验证明他错误。轶事：Musk 承诺如果工程师（Tyler）能在 24 小时内完成 GPU 训练运行，就送一辆免费的 Cybertruck——该工程师成功了，现在那辆 Cybertruck 就停在办公室外面。

- **其他见解**：每个 Commit 的价值极高（约 250 万美元），通过 Hackathons 招聘，挑战假设和需求，实验高于等级制度，以及利用 Tesla 资源进行大规模硬件模拟以实现扩展（例如目标是需要同等算力的 100 万个 Human emulators）。

Ghori 对这种高度信任、无官僚主义的环境给予了正面评价，尽管他在访谈后不久离开了 xAI（2026 年 1 月 19 日宣布，并表示对团队只有“爱”），这引发了关于这次坦率的访谈导致他离职的猜测（虽未证实）。

References:  

- [YouTube: WTF is happening at xAI | Sulaiman Ghori](https://www.youtube.com/watch?v=8jN60eJr4Ps)
- [Business Insider: 10 quotes about xAI and Elon Musk from the engineer who is out days after giving a sweeping podcast interview](https://www.businessinsider.com/xai-engineer-sulaiman-ghori-leaves-company-relentless-podcast-elon-musk-2026-1)
- [Times of India: Read the full interview that got engineer Sulaiman Khan Ghori ‘fired’ from Elon Musk's xAI](https://timesofindia.indiatimes.com/technology/tech-news/read-the-full-interview-that-got-engineer-sulaiman-khan-ghori-fired-from-elon-musks-xai-in-less-than-a-year/articleshow/126776282.cms)
- [NextBigFuture: Inside xAI and Future of Millions of Emulated Humans](https://www.nextbigfuture.com/2026/01/inside-xai-and-future-of-millions-of-emulated-humans.html)