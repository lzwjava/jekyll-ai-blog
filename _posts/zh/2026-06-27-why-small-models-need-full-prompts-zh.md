---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么小模型需要完整提示
translated: true
type: note
---

是的，你的观察是正确的，而且有一个具体的机制原因。让我比“小模型笨”这一层深入一点。

## 为什么 124M 模型需要完整段落

一个 124M 的模型（GPT-2 small：12 层，768 隐藏维度，12 个注意力头）存储先验（priors）的能力非常有限。大模型将海量的世界知识和任务结构压缩到权重中，因此一个简短的提示（“修复这个 bug”）就能激活丰富的潜在任务表征。而 124M 模型根本没有记住那些任务→行为的映射。因此它几乎完全依赖**上下文信息**，而非参数化知识。

用 transformer 术语来说：模型的输出分布是

```
P(next | context) = softmax(W_unembed · h_L)
```

其中 `h_L` 是最后一层的残差流。对于大模型，即使上下文很短，`h_L` 也能携带强烈的任务条件信号，因为注意力头和 MLP 已经学会了“补全”隐含的任务。对于 124M，残差流主要由 token 的字面内容驱动——没有丰富的先验可供插值。**短提示 = 薄弱的残差 = 通用的续写。**

这就是为什么 few-shot 和冗长的提示在小规模下效果格外好：你在外部提供了模型权重无法提供的条件信号。

## 你提到的规模效应部分

随着模型规模扩大，有两件事会解决这个问题，它们是可分离的：

1. **预训练规模**——上下文学习（in-context learning）能力的涌现。ICL 能力随规模急剧提升；在约 1B 参数以下，few-shot 的提升微弱且不稳定。这属于 Kaplan/Wei 的“涌现能力”区间。你的 124M 模型位于该曲线拐点之下。

2. **后训练（你问到的部分）**——SFT + RLHF/DPO 将“需要一段话”转变为“遵从 3 个词的指令”。指令微调（instruction tuning）实际上是在训练模型将简洁的指令映射到行为。但关键的是——**对 124M 模型进行指令微调收益小得多**，因为模型缺乏可供调用的基础能力。你无法通过 RLHF 创造出模型在预训练中从未学会的能力。InstructGPT 表明对齐（alignment）更多是恢复/引导已有的能力，而不是创造能力。

所以你的直觉可以清晰地分解：
- “行业有其他后训练方法” → 正确，但它们主要帮助那些已经拥有潜在能力的模型。
- “随着模型增大而解决” → 正确，而且对于 124M 模型这是主导因素。在这里，没有任何后训练技巧能完全替代规模。

## 对你 nanoGPT/nanochat 工作的实际意义

对于 124M 模型，按优先级排序，最高杠杆率的方法是：

1. **缩小领域。** 一个只做一件事（比如只做 Python 补全）的 124M 模型，远比一个通用型 124M 模型要好。限制预训练/微调的数据分布。
2. **大量使用显式的指令→输出对的 SFT**，并且格式要与推理时的提示完全一致。小模型对格式极其敏感——提示模板本身就是任务表征的一部分。训练时和测试时的格式不匹配会不成比例地破坏小模型的表现。
3. **推理时保持提示的冗长和 few-shot 风格。** 这不仅是正确的做法，也不是失败——你是在用上下文补偿缺失的参数化先验。不要与之对抗。
4. **考虑知识蒸馏（distillation）**，从大模型进行 logit/序列级别的 KD——在固定的 124M 预算下，蒸馏模型胜过从头训练的 SFT，因为目标输出携带了大模型的任务条件信号。

一句话总结：在 124M 规模下，行为是**上下文主导而非权重主导**，所以冗长的提示不是变通方案——它就是这个机制的运行模式。后训练有帮助，规模化帮助更大，而让“简洁提示生效”的最廉价途径是缩小任务领域，而不是改进提示本身。

参考文献：

- [Language Models are Few-Shot Learners (GPT-3)](https://arxiv.org/abs/2005.14165)
- [Training language models to follow instructions (InstructGPT)](https://arxiv.org/abs/2203.02155)
- [Emergent Abilities of Large Language Models](https://arxiv.org/abs/2206.07682)
- [Scaling Laws for Neural Language Models (Kaplan et al.)](https://arxiv.org/abs/2001.08361)
- [Distilling the Knowledge in a Neural Network (Hinton et al.)](https://arxiv.org/abs/1503.02531)