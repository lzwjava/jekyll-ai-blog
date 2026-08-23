---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ICML 杰出论文 2023-2026
translated: true
type: note
---

**问题：** 近年来ICML的杰出论文有哪些？

**回答：**

以下是2023年至2026年ICML杰出论文奖获奖情况的全面概述。

---

## 🏆 ICML 2026（韩国首尔）

**杰出论文：**

- **《灵活性陷阱：重新思考扩散语言模型中任意顺序的价值》** — Zanlin Ni等。研究表明，基于置信度的扩散大语言模型任意顺序生成可能会绕过高不确定性的“分叉” token，从而减少解的多样性——这是一种非显而易见的失败模式。

- **《扩散模型与对数凹分布的高精度采样》** — Fan Chen, Sinho Chewi, Constantinos Daskalakis, Alexander Rakhlin。提出了一阶拒绝采样（FORS），将所需的去噪步数从多项式级别减少到关于1/ε的多对数级别。

**杰出立场论文：**

- **《立场：对齐社区正在无意间构建审查工具包》** — Sarah Ball, Phil Hackemann。认为对齐工具具有双重用途，并有助长审查的风险。

**时间检验奖：**

- **《深度强化学习的异步方法》**（ICML 2016）— Volodymyr Mnih等。开创了异步强化学习，是现代大语言模型后训练的基础。

---

## 🏆 ICML 2025（加拿大温哥华）

**杰出论文（主赛道）** — 从超过12,000篇投稿中选出6篇：

- **《CollabLLM：从被动响应者到主动协作者》** — Shirley Wu等（微软研究院）
- **《为最坏情况训练，为最佳情况规划：理解掩码扩散中的Token排序》** — Jaeyeon Kim, Kulin Shah等。在更难排序上训练的掩码扩散模型在推理时取得了显著更好的结果（数独准确率从6%提升至89%）。
- **《掷骰子与三思而后行：超越下一个Token预测的创造极限》** — Vaishnavh Nagarajan等。证据表明下一个Token预测限制了创造力，多Token方法能改善这一点。
- **《作为贝叶斯求积的共形预测》** — Jake Snell, Thomas Griffiths
- **《数据缺失情况下的分数匹配》** — Josh Givens, Song Liu, Henry Reeve
- **《识别最弱势群体的预测价值》** — Unai Fischer Abaigar等。表明有时扩大人类个案工作者的能力比构建更准确的预测模型更好。

**时间检验奖：**

- **《批量归一化》**（ICML 2015）— Sergey Ioffe & Christian Szegedy

---

## 🏆 ICML 2024（奥地利维也纳）

从超过9,400篇投稿中选出了10篇最佳论文。著名获奖者包括：

- **《立场：关于大规模公共预训练下差分隐私学习的考量》** — Tramèr, Kamath, Carlini。挑战了“公共预训练+私有微调能产生真正私有模型”这一假设。
- **《与更有说服力的大语言模型辩论能带来更真实的答案》** — Khan, Hughes等。
- **《Genie：生成式交互环境》** — Jake Bruce等（DeepMind）。一种从视频中创建交互式游戏环境的生成模型。

其他获奖者包括：

- **《通过估计数据分布的比率进行离散扩散建模》** — Aaron Lou, Chenlin Meng, Stefano Ermon
- **《立场：衡量数据集多样性，而非仅仅宣称》** — Dora Zhao等。
- **《窃取部分生产级语言模型》** — Nicholas Carlini等。

---

## 🏆 ICML 2023（美国夏威夷）

六篇论文获得杰出论文奖：

- **《通过D-Adaptation实现免学习率学习》** — Aaron Defazio, Konstantin Mishchenko。无需调整学习率即可实现最优收敛。
- **《大型语言模型的水印》** — Kirchenbauer, Geiping等（马里兰大学）。无需重新训练即可在LLM生成的文本中嵌入不可见、可统计检测的信号。
- **《未见数据的泛化、逻辑推理与度课程》** — Abbe, Bengio等。推进了对布尔函数分布外泛化的理解。
- **《零和不完美信息博弈中博弈树的适应》** — Fiegel, Menard等。为不完美信息博弈引入了近最优策略。
- **《一般图上的自排斥随机游走》** — Doshi, Hu, Eun。推进了具有最小方差的MCMC采样。
- **《频率派序贯学习的贝叶斯设计原则》** — Xu, Zeevi。引入了“算法信息比”来界定赌博机问题中的遗憾值。

---

**参考文献：**

- [ICML 2026奖项 — ICML博客](https://blog.icml.cc/2026/07/05/announcing-the-icml-2026-awards/)
- [ICML 2025杰出论文 — Jolt ML](https://joltml.com/icml-2025/awards/)
- [ICML 2024最佳论文 — 滑铁卢大学](https://uwaterloo.ca/computer-science/news/gautam-kamath-and-international-colleagues-win-best-paper-at-icml-2024)
- [ICML 2023杰出论文 — icml.cc](https://icml.cc/Conferences/2023/Awards)
