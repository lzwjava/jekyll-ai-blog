---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 长短期记忆网络实为旋转残差网络
translated: true
type: note
---

在获得NeurIPS 2024时间检验奖的演讲中，Ilya Sutskever回顾了2014年《使用神经网络进行序列到序列学习》论文中的关键见解与失误。他在“我们当初错在哪里”部分指出，LSTM（长短期记忆网络）的过度复杂化及其最终局限性是重要问题——正是LSTM推动了早期序列建模的突破，如机器翻译。

### 关于LSTM的核心误解

我们曾将LSTM视为专门为序列数据定制的全新复杂架构，认为这种“特殊”结构需要深度学习研究者精心设计以处理时间依赖、梯度消失和递归问题。但Sutskever解释道，LSTM的实际本质远比这简单：**它们本质上就是旋转了90度的ResNet（残差网络）**。

- **ResNet**（2015年提出）通过添加跨层直连的跳跃连接（残差），使信息能直接流动，从而在不引发训练不稳定的情况下实现更深的网络，彻底改变了图像处理领域
- LSTM（1997年提出）在*时间维度*上实现了类似功能：其门控机制和细胞状态就像残差连接，允许梯度和信息在长序列中传播而不会衰减。这与ResNet原理相同——只是从空间堆叠（如图像像素）“旋转”到了时间堆叠（如句子中的单词）

Sutskever打趣道：“对不熟悉的人来说，LSTM是Transformer出现前可怜深度学习研究者们的无奈之举。它本质上就是个旋转了90度的ResNet...而且出现得更早，就像个稍复杂的、带有积分器和乘法运算的ResNet。”这个类比强调LSTM并非革命性创新，而是残差思想在循环网络中的早期优雅实践。

### 此事为何重要（以及问题出在哪里）

- **辉煌成就**：LSTM在当时展现出惊人的扩展能力，使seq2seq模型在翻译任务上击败传统统计方法。其残差设计使深度循环网络可训练，正如后来对前馈网络的改变
- **认知误区（及LSTM的衰落）**：我们低估了LSTM顺序处理特性对扩展性的制约。与可并行化的ResNet或Transformer不同，LSTM需逐步处理数据，导致其难以应对海量数据集或长上下文场景。其冗余复杂度（如多重门控机制）也被Transformer中的注意力机制简化。到2017年，Transformer的出现暴露了这些局限，推动领域转向具有更好并行性和长程依赖能力的自注意力机制

回望过去，错误不在于发明LSTM——它们曾是里程碑式的过渡方案——而在于我们将其视为序列建模的终极方案，未能及时认识到残差连接是通用工具，也未更快转向并行架构。

这一视角将LSTM重新定义为理解跳跃连接如何解锁多维度深度网络的关键基石，而非过时技术。

[序列到序列学习十年回顾：演讲实录与视频](https://kingy.ai/news/sequence-to-sequence-learning-with-neural-networks-what-a-decade-transcript-video/)
[Ilya Sutskever NeurIPS 2024完整演讲](https://www.youtube.com/watch?v=1yvBqasHLZs)
[从Ilya的NeurIPS 2024演讲获得的启示](https://dlyog.com/papers/one_internet_v1)
