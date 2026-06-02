---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: μ子优化器争议与批评
translated: true
type: note
---

问题：关于 Muon 优化器有哪些“非主流”观点？

回答：

Muon 优化器（MomentUm Orthogonalized by Newton-Schulz）是一种相对较新的神经网络优化技术，于 2024 年末推出，主要用于 transformers 等模型的隐藏层。它应用 Newton-Schulz 迭代来正交化基于动量的更新，旨在实现更高效的训练，同时降低计算开销（额外 FLOPs 不足 1%）并提高样本效率，优于 AdamW。尽管它在 CIFAR-10 和 NanoGPT 训练等任务中创下了速度记录，并为 Moonlight（一个 3B/16B MoE LLM）等模型提供了支持，但它并非没有争议。以下是一些从 ML 社区（例如 Reddit 的 r/MachineLearning 和 X 上的帖子）讨论中得出的“非主流”观点。这些观点挑战了人们的热情，往往强调实际限制而非理论收益。

### 关于 Muon 的非主流观点：
- **速度提升被过分夸大，主要归因于其他调整，而非 Muon 本身**：在速度赛跑基准测试中（例如在 3 分钟内训练一个 120M GPT 模型），Muon 仅贡献了总速度提升的约 10%——大部分来自架构更改、数据效率或实现优化。当 AdamW 等基线经过适当调优（例如，使用最佳学习率）后，Muon 仅带来适度的 10% 优势，而非论文中声称的革命性的 2 倍效率。

- **它并非真正的二阶或几何优越——那只是为了炒作而进行的“数学洗白”**：尽管声称是“谱范数下的最速下降”或流形优化，Muon 本质上是一种一阶方法（没有像 Hessian 这样的二阶统计量）。花哨的几何框架（在矩阵空间中保持“能量”的正交更新）被视为不必要的恐吓策略，旨在 T人或非专家，对精心调整的 Adam 变体没有真正的优越性。一位研究员称其“无关紧要”，并承诺发布一个 PSA 来揭穿其数学。

- **在训练过程中切换到 Muon（例如进行微调）弊大于利**：用 AdamW 预训练的模型不能很好地转移到 Muon，因为它们的归纳偏置不同——Muon 的正交约束产生“不同的思维”或结构，导致冲突，从而导致微调结果好坏参半或更糟（例如在 SFT 任务中）。整个过程都坚持 AdamW 更简单、更可靠，尤其是对于密集型与 MoE 架构。

- **AdamW 实际上是被低估的“主力”——Muon 只是昙花一现的“月度优化器”**：如果角色互换（Muon 是 2015 年的默认优化器，AdamW 在 2025 年问世），实验室会蜂拥而至 AdamW，因为它可以在 1M-GPU 集群之间“自由扩展”，没有额外的通信/计算，并且可以在奇怪的架构上即插即用，可靠性高。Muon 的利基（例如，仅限 2D 隐藏权重）使其通用性较差，通过使比较复杂而减缓了研究。

- **它产生可能过于严格的“极简主义”解决方案**：通过正交化更新（有效地在参数空间中“限制到球体”），Muon 倾向于紧凑、深奥的知识吸收（例如，为什么 Kimi K2 “知识渊博”却比 GPT-4 小）。但这可能会限制创造力或广泛泛化，使模型在狭窄领域过于精确，而牺牲了鲁棒性——本质上是用表达能力换取效率。

- **开销和不稳定性使其在前沿规模上不切实际**：早期版本在大型 LLMs 中导致 logit 爆炸，需要 MuonClip 等hack。即使修复了，它在巨大规模下也已“死亡”（例如，仅在小型模型中表现出 >10% 的优势），Newton-Schulz 步骤增加了微妙的错误或调优麻烦。根据罕见的严格消融研究，“如果你很好地调整基线，Adam 仍然非常好。”

总的来说，这些意见突出了一种分歧：Muon 在受控的速度赛跑中表现出色，但在实际规模和集成方面的混乱中却步履维艰。支持者赞扬其理论上的优雅，但怀疑者认为它只是进化而非革命——这与围绕 Lion 或 Shampoo 等过去优化器的争论遥相呼应。

参考文献：
- [Muon: An optimizer for hidden layers in neural networks](https://kellerjordan.github.io/posts/muon/)
- [Muon is Scalable for LLM Training (arXiv)](https://arxiv.org/abs/2502.16982)
- [r/MachineLearning: [P] Understanding Muon](https://www.reddit.com/r/MachineLearning/comments/1m2y23l/p_understanding_muon_a_revolutionary_neural/)
- [r/LocalLLaMA: Kimi.ai released Moonlight](https://www.reddit.com/r/LocalLLaMA/comments/1ivrprb/kimiai_released_moonlight_a_3b16b_moe_model/)
- [r/MachineLearning: [R] Muon is Scalable](https://www.reddit.com/r/MachineLearning/comments/1ixzj26/r_muon_is_scalable_for_llm_training/)
- [X Post: Jason Lee on Muon not being second-order](https://x.com/jasondeanlee/status/1986102152574767308)
- [X Post: Simo Ryu on Adam vs. Muon](https://x.com/cloneofsimo/status/1963670853574705413)
- [X Post: James MMatrix on lab adoption](https://x.com/JamesWhate89993/status/1998190303669342530)
