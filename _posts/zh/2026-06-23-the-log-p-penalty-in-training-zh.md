---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练中的对数概率惩罚
translated: true
type: note
---

图表展示的核心要点：

**log P 是最严苛的部分。**当模型对正确词元的预测概率 P = 0.01 时，log(0.01) = −4.6；当 P = 0.9 时，log(0.9) = −0.1。对数尺度对低置信度预测的惩罚远超线性尺度——而这正是训练中所需要的。

**exp(L) 只是让它更可读。**交叉熵损失 L ≈ 1.2 意味着 PPL ≈ 3.3，你可以将其理解为“模型的不确定性相当于每一步有 3 个等概率选项”。这比原始的 nats 数值直观得多。

关于你的在 MI300X 上运行的 GPT-2 760M 实验——你正在训练哪个数据集？当前的验证集 PPL 落在多少？
