---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从博客到RoPE再到Kimi K3
translated: true
type: note
---

问题：阅读并总结/核查这篇关于苏剑林的中文传记文章——他从数学博客到RoPE，再到Kimi K3中的KDA和Attention Residuals的历程。

回答：

**去除文学框架后的叙述：**

苏剑林是数学自学出身（华南师范大学理学学士，中山大学基础数学硕士），从15岁起运营一个名为Scientific Spaces的博客。他没有读博，也没有出国。

关键技术里程碑：

- **2021年**：先在博客上发表了RoPE（旋转位置编码，Rotary Position Embedding），随后以RoFormer的形式在arXiv上发表。核心思想：将绝对位置编码为旋转矩阵，使得在query和key做点积时，只有*相对*旋转（角度差）保留下来——通过绝对编码方案，在注意力点积内部免费获得相对位置信息。这就是为什么它能与线性注意力完美结合（旋转只是保范线性映射），并且比学习式/绝对位置嵌入具有更好的外推能力。

- **2019–2022年**：在追一科技（公司处于收缩/裁员阶段）工作期间，编写了bert4keras、WoBERT/WoNEZHA——被广泛使用的中文NLP工具。

- **2023年**：加入Moonshot AI（Kimi），在广州远程办公。

- **2025年2月**：MoBA（Mixture of Block Attention，块注意力混合）——用于长上下文的稀疏注意力，在DeepSeek的NSA发布数小时后推出。

- **2025年**：QK-Clip，修复了将Muon优化器扩展到约100B参数以上时的"MaxLogit爆炸"问题，用于Kimi K2的15.5T token预训练，据报告实现了零loss spike的运行。

- **2025年11月**：Kimi Linear / KDA（Kimi Delta Attention）——一种门控DeltaNet变体，在公平比较中，在短上下文、长上下文*以及*RL扩展方面都击败了全注意力。我查了arXiv列表（2510.26692）——苏确实是约59位Kimi Team作者中的一位。

- **2026年3月**：Attention Residuals（AttnRes）——用对前层输出学习到的softmax注意力替代固定权重的残差求和。已在arXiv（2603.15031）上确认：苏与Guangyu Chen和Yu Zhang一同被列为最早期的合著者之一，一位17岁的高中生（Guangyu Chen）也是主要合著者。已通过GitHub（MoonshotAI/Attention-Residuals）和arXiv列表验证。

- **"杀死自己的RoPE"细节**：据报告，Kimi Linear使用NoPE——不进行显式位置编码——因为KDA的门控机制表达能力足够强，可以隐式学习位置结构。这是一个真实且值得注意的设计选择；根据Kimi Linear的公开文档，关于苏共同设计了某种使其此前著名发明过时的东西这一说法是成立的。

**关于Kimi K3本身**——我独立验证了：

- 2.8T总参数，MoE架构，896个专家，16个激活（约104B激活参数），1M上下文，基于KDA + AttnRes构建。Kimi K3是Kimi迄今为止最强大的旗舰模型，拥有2.8万亿参数，基于Kimi Delta Attention（KDA）——一种混合线性注意力机制——以及Attention Residuals构建，具备原生视觉理解和1M token上下文窗口，定位为全球首款3万亿参数级别的开源模型。

- 时间线：托管发布7月16日，开放权重2026年7月26–27日——权重于2026年7月26日美国东部时间约晚上7:30公开，比7月27日的目标提前了一天。

- 文章中的基准测试声称查证属实：在开发者盲测中，Arena在其Frontend Code评估中将K3排名第一，得分1,679分，领先于Fable 5，尽管Moonshot自己表示K3整体上仍落后于Claude Fable 5和GPT-5.6 Sol。

- 出口管制/制裁的支线情节是真实的：白宫OSTP指控Moonshot通过泰国使用受限芯片对Claude Fable 5进行蒸馏，财政部长Bessent警告可能实施制裁——这与今年夏天早些时候的Fable/Mythos出口管制事件相符。

**我认为无法验证/可能有润色的部分**："200家硅谷公司签署了反对制裁的信函"和"华尔街称之为DeepSeek 2.0"这两处——考虑到报道的语气，这是合理的，但我没有找到确定这些确切数字/引文的一手来源；将其视为渲染而非事实。

RoPE的数学本身，如果你想要实际的推导（块对角旋转矩阵，为什么`q_m^T k_n`只依赖于`m-n`），我可以带你过一遍——你可能已经在笔记中有了这些内容，但我也很乐意在讲解KDA的delta-rule门控与vanilla线性注意力有何不同的同时，做一遍前向传播版本。

参考资料：

- [Kimi K3 – Kimi API Platform](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)
- [Attention Residuals (arXiv 2603.15031)](https://arxiv.org/abs/2603.15031v1)
- [Kimi Linear (arXiv 2510.26692)](https://arxiv.org/abs/2510.26692)
- [MoonshotAI/Attention-Residuals GitHub](https://github.com/MoonshotAI/Attention-Residuals)
- [Tom's Hardware — Kimi K3对比Claude Fable 5](https://www.tomshardware.com/tech-industry/artificial-intelligence/moonshot-releases-2-8-trillion-parameter-kimi-k3)