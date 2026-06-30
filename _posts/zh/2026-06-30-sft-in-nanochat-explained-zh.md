---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat中的SFT详解
translated: true
type: note
---

问题：nanochat 中的 SFT 是什么？

回答：

nanochat 中的 SFT（监督微调）是指通过使用聊天特殊标记格式化的完整对话训练基础预训练模型，将其转变为对话助手的阶段。在 Karpathy 的流程中（`scripts/chat_sft.py`），它介于基础预训练/中间训练和 RL 之间。

核心思想：与预训练相同的下一个词元交叉熵损失，但作用于渲染后的对话，且损失**仅掩码到助手词元**——你不需要训练模型预测用户轮次或系统提示，只需生成助手的回复。

nanochat 的 SFT 与中间训练的不同之处：

- **按行步长，而非文档拼接。** 预训练将许多文档打包成固定长度的序列。SFT 则每行取一个对话，进行填充，这样模型看到的示例领域与推理时匹配（一次一个对话）。Karpathy 指出这减少了训练/测试不匹配。
- **通过渲染进行损失掩码。** 对话使用特殊标记（`<|user_start|>`, `<|assistant_start|>` 等）进行词元化，并通过掩码标记哪些位置是助手生成的。只有这些位置贡献损失。
- **简短且廉价。** 在精选数据上进行少量迭代——`SmolTalk`（通用对话）、`MMLU` 辅助多项选择、`GSM8K`（结合 Python 解释器的数学/工具使用）等。在 8×H100 机器上运行只需几分钟。

掩码损失的最小化草图，这是整个概念核心：

```python
# logits: (B, T, V), targets: (B, T), mask: (B, T) 其中 1 表示助手词元
loss = F.cross_entropy(
    logits.view(-1, logits.size(-1)),
    targets.view(-1),
    reduction="none",
).view_as(targets)
loss = (loss * mask).sum() / mask.sum().clamp(min=1)
```

SFT 之后得到 `chatsft` 检查点，Web UI/CLI 默认提供这些检查点——RL（`scripts/chat_rl.py` 中基于 GSM8K 的 GRPO）也在此基础上构建。

参考：

- [karpathy/nanochat](https://github.com/karpathy/nanochat)
- [nanochat walkthrough（Karpathy 讨论）](https://github.com/karpathy/nanochat/discussions/1)
