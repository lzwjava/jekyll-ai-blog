---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 克里斯·奥拉与机械解释性研究
translated: true
type: note
---

问题：Chris Olah 和他的团队的工作是什么，Anthropic 在解释性研究领域做了什么？

答案：

## Chris Olah：Mechanistic Interpretability 的先驱

### Chris Olah 是谁？

Chris Olah 是一位机器学习研究员和 Anthropic 的联合创始人。他以神经网络解释性工作闻名，特别是 mechanistic interpretability，以及可视化神经网络内部表示的研究和工具。

在加入 Anthropic 之前，他在 Google Brain 工作了四年，开发工具来可视化神经网络内部发生的事情。他参与了 2015 年 DeepDream 的推出，并开创了 feature visualization、activation atlases，并合著了论文 "Concrete Problems in AI Safety"。

---

## 什么是 Mechanistic Interpretability？

Mechanistic interpretability（通常缩写为 mech interp）是可解释 AI 中的一个研究子领域，旨在通过分析神经网络计算中存在的机制来理解其内部工作原理。该术语由 Chris Olah 创造，用于描述他在 circuit analysis 中的工作。Circuit analysis 试图完全表征模型中的单个特征和电路，而更广泛的领域则倾向于基于梯度的 saliency maps 等方法。

核心目标本质上是**逆向工程神经网络**——将 AI 模型视为软件工程师处理编译后的汇编代码：将其分解为可理解的逻辑。

---

## Olah 团队的关键研究里程碑

### 1. Circuits Framework（2020–2021）

Chris Olah 在 Anthropic 领导的一个团队于 2021 年首次在 transformer 中发现了具体、可理解的算法。他们识别出“induction heads”——一种专用的注意力机制，用于识别重复模式。当模型看到“Harry Potter went to Hogwarts. Hermione Granger went to…”时，induction head“知道”在“Hermione Granger went to”之后很可能跟着“Hogwarts”——不是通过模糊的统计，而是通过一个具体的算法来复制早期的模式。这具有革命性：研究人员首次能够指向特定机制并说“这个精确执行这个计算”。

### 2. Superposition 和 Polysemanticity 问题

Anthropic 的研究团队在 2022 年发现，单个神经元并不代表单一概念。这是一个转折点：它解释了为什么神经网络如此紧凑和高效，但也解释了解释性如此困难。同时，它揭示了解决方案的路径：Sparse Autoencoders (SAEs) 可以解混这些叠加的特征，使其再次可解释。

### 3. Towards Monosemanticity & Sparse Autoencoders（2023）

Anthropic 的研究使用 sparse autoencoders 将 transformer 激活分解为更可解释的特征。他们的方法——使用 16× 扩展的 dictionary learning，在 80 亿 residual-stream 激活上训练——提取了近 15,000 个潜在方向，其中人类评估者发现 70% 清晰映射到单一概念，如 Arabic script 或 DNA motifs。

Sparse autoencoders (SAEs) 用于大型语言模型解释性，由 Anthropic 引入。

### 4. Scaling Monosemanticity & “Golden Gate Bridge” 实验（2024）

2024 年 5 月，Olah 在 Anthropic 的团队通过将这些策略应用于其最前沿的大型语言模型之一取得了突破。他们发现可以识别模型中对应不同概念和活动的神经元组，如识别偏见或识别诈骗邮件。切换这些神经元组的开关可以改变模型行为，为 AI 研究人员提供新工具，使 AI 更少危险。

通过 Sparse Autoencoders，他们在 Claude Sonnet 中识别了超过 3400 万个此类特征，从“sarcasm”到“DNA sequences”再到“conspiracy theories”。最著名的例子是“Golden Gate Bridge Neuron”——一个专门对 Golden Gate Bridge 反应的特征。当研究人员人为放大此特征时，Claude 开始痴迷于谈论这座桥，即使是完全不相关的主题如烹饪食谱。

### 5. Circuit Tracing & Attribution Graphs（2025 年 3 月）

2025 年 3 月，Anthropic 引入了一种重大新技术 circuit tracing，将几种早期方法结合成统一框架。该方法用 cross-layer transcoders (CLTs) 替换模型的 MLPs——一种新型 sparse autoencoder，从一层 residual stream 读取但可向所有后续 MLP 层提供输出。这产生了一个可解释的“replacement model”，其中构建块是 sparse、人可读的特征，而不是 polysemantic 神经元。然后系统构建 attribution graphs：针对单个提示的计算图，其中节点代表活跃特征，边代表它们之间的线性依赖。

在一篇配套论文中，他们将 attribution graphs 应用于 Claude 3.5 Haiku。其中发现：模型在写诗时提前规划输出——在开始写每一行之前，模型识别潜在的押韵词，这些词可能出现在行尾。

---

## 更广泛的影响和愿景

Olah 强调还有很多工作要做，但他对他目前的研究成果持乐观态度：“如果我们真的能理解这些系统，这将需要大量进步，我们或许能够判断这些模型是否真正安全——还是只是看起来安全。”

MIT Technology Review 将 mechanistic interpretability 评为 2026 年突破性技术，Anthropic 开源了 circuit tracing，标志着从“有趣的研究方向”转向“实用工程学科”。

Anthropic 的解释性团队还开始探索将这些方法应用于生物学——protein language models 和 DNA foundation models——表明解释性工具最终可能作为“显微镜”，从训练于生物数据的 AI 模型中提取科学理解。

---

## 总结表格

| 年份 | 里程碑 |
| ------ | -------- |
| 2015 | DeepDream 和早期神经网络可视化 (Google Brain) |
| 2020 | Circuits framework — 视觉模型中的特征和电路 |
| 2021 | Transformer 中发现 induction heads |
| 2022 | Superposition 假设得到证实 |
| 2023 | 用于 monosemanticity 的 sparse autoencoders |
| 2024 | 在 Claude Sonnet 中扩展到 3400 万特征；Golden Gate Bridge 实验 |
| 2025 | Circuit tracing + attribution graphs；开源工具；生物学应用 |

参考文献：

- [Chris Olah - Wikipedia](https://en.wikipedia.org/wiki/Chris_Olah)
- [Mechanistic Interpretability - Wikipedia](https://en.wikipedia.org/wiki/Mechanistic_interpretability)
- [Chris Olah - TIME100 AI 2024](https://time.com/collections/time100-ai-2024/7012873/chris-olah/)
- [Interpretability Dreams (transformer-circuits.pub)](https://transformer-circuits.pub/2023/interpretability-dreams/index.html)
- [On the Biology of a Large Language Model (Anthropic, 2025)](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)
- [Circuits Updates - July 2025 (transformer-circuits.pub)](https://transformer-circuits.pub/2025/july-update/index.html)
- [Understanding Mechanistic Interpretability in AI Models - IntuitionLabs](https://intuitionlabs.ai/articles/mechanistic-interpretability-ai-llms)
- [Monosemanticity Research Summary - Galileo AI](https://galileo.ai/blog/anthropic-ai-interpretability-breakthrough)
