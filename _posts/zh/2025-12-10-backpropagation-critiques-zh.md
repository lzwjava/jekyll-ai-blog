---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 神经网络中反向传播的批判
translated: true
type: note
---

问题：关于神经网络中的反向传播有哪些不受欢迎或有争议的观点？

回答：

以下是关于反向传播 (backprop) 的一些真正不受欢迎或少数派观点，在主流深度学习圈子里很少被称赞：

- **反向传播在生物学上不合理，阻碍了受神经科学启发的 AI 发展**
  大多数神经科学家和一些机器学习研究员（例如，Geoffrey Hinton 近几年，David Marr 的继承者，Tai Sing Lee，Blake Richards）认为反向传播与大脑的工作方式截然不同：没有对称的反馈权重，没有锁定的前向/后向阶段，也没有全局误差信号向后传递。不受欢迎的观点是，继续依赖反向传播是在浪费时间，我们应该完全放弃它，转而采用局部、赫布（Hebbian）或预测编码（predictive-coding）式的学习规则。

- **反向传播是规模化定律和 AGI 的死胡同**
  少数人（François Chollet，一些“苦涩的教训”反运动者）声称，自 2012 年以来我们看到的惊人进步主要来自于规模 + 数据，而不是反向传播的神奇之处。如果我们转向进化策略（evolution strategies）、随机搜索（random search）或超网络权重生成（hypernetwork weight generation），或在足够规模下使用合成梯度（synthetic gradients），我们将以更少的麻烦（信度分配消失/爆炸等）获得相似或更好的结果。

- **反向传播的信度分配（credit-assignment）理由被高估了**
  一些研究人员（例如，Timothy Lillicrap 的“符号对称”或“反馈对齐”，Numenta 的 Subutai Ahmad）认为，你实际上不需要精确的梯度——随机反馈权重、符号一致性（sign-sign agreement），甚至零反馈通常也几乎同样有效。不受欢迎的结论是：反向传播中的链式法则导数部分大多是演戏；真正的魔力只是“大致朝着正确的方向推动层”。

- **反向传播有意使模型脆弱且不鲁棒**
  批评者如 Ali Rahimi（“炼金术”演讲）、Chris Olah 的电路线程怀疑论者和对抗性示例研究人员有时声称，反向传播在最小化 i.i.d. 数据损失方面的极端效率必然会产生尖锐的最小值和过度自信。不使用反向传播的替代方案（贝叶斯方法、基于能量的模型、扩散）天生就更鲁棒。

- **我们可以用前向传播方法取代反向传播，几乎不损失任何东西**
  Max Welling（forward-forward algorithm）、Hinton 最近再次提出以及一些平衡传播（equilibrium-prop）论文支持的极端版本：训练两个前向传播（正相和负相），而不是前向+后向。不受欢迎的说法是，经典的反向传播在十年后将看起来像是“用起重机搬动卵石”。

- **反向传播是我们缺乏持续学习/学会学习能力的原因**
  终身学习社区（例如，German I. Parisi，Vincenzo Lomonaco）的强烈观点：灾难性遗忘（catastrophic forgetting）是反向传播固有的，因为它使用 SGD 全局覆盖权重。局部学习规则或显式记忆重放是唯一的真正解决方案，而不是更多的反向传播技巧（EWC, SI 等）。

这些观点无疑是少数派观点——大多数从业者都喜欢反向传播，因为它有效且在 GPU 上效率极高——但它们由受尊敬的研究人员提出，并且随着该领域开始质疑 1986 年的方案是否能带领我们一路走向 AGI，这些观点正获得越来越多的关注。

参考文献：

- [Geoffrey Hinton’s Forward-Forward Algorithm (2022)](https://www.cs.toronto.edu/~hinton/FFA13.pdf)
- [Feedback Alignment works almost as well as backprop (Lillicrap et al., 2016)](https://www.nature.com/articles/ncomms13276)
- [Chollet’s “On the Measure of Intelligence” (2020) critiquing pure scaling](https://arxiv.org/abs/1911.01547)
- [Rahimi’s “Test of Time” NIPS 2017 talk (“Machine Learning has become Alchemy”)](https://www.youtube.com/watch?v=Qi1Yry33eDU)
