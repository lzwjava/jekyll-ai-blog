---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat的val/bpb指标解析
translated: true
type: note
---

**问题：** 在 nanochat 中，`val` 部分（包含 1 个图表）和 `val/bpb` 指标含义是什么？

**回答：**

你看到的是一个 wandb 指标命名空间。nanochat 使用 `/` 分隔的前缀记录指标 —— `train/…`、`val/…`、`core/…` —— wandb 将它们分组为可折叠的部分。因此 `val (1)` 仅表示：**验证**部分，包含 **1** 个图表，该图表就是 `val/bpb`。

`bpb` = **bits per byte**（每字节比特数），是一种与分词器无关的单位下的验证损失。Karpathy 会监控 val_bpb（以每字节比特数这种与词汇表大小无关的单位表示的验证损失）随训练步数的变化，以判断代码修改是否有所帮助，并且这是 nanochat 排行榜上的主要指标。

## 为什么不直接报告交叉熵损失？

因为原始 CE 是每个 *token* 的量，而 token 是分词器的人为产物。一个 65k 词汇量的分词器每个 token 大约对应 4-5 个字符；32k 词汇量的则更少。模型质量相同，但每个 token 的损失不同。每字节比特数通过每个 token 的字节数对损失进行归一化，使指标与分词器无关 —— 因此你可以公平地比较 d12 运行与 d26 运行的结果，或者你自己的自定义分词器实验与基准实验的结果。

从信息论的角度理解：它表示模型压缩未见文本的一个字节需要多少比特。对字节进行随机猜测 = 8.0 bpb。nanochat d20 大约达到 0.7–0.8 val bpb；前沿模型远低于此值。数值越低 = 压缩越好 = 下一个 token 预测越好。

## 数学推导

来自 `F.cross_entropy` 的交叉熵损失单位是 **nats per token**。转换公式：

$$
\text{bpb} = \frac{\sum_i \text{nll}_i}{\ln(2) \cdot \sum_i \text{bytes}(t_i)}
$$

其中 `bytes(t_i)` 是 token `t_i` 字符串的 UTF-8 字节长度。两步：nats → bits（除以 ln 2），per-token → per-byte（用每个 token 的字节数加权其 NLL 并除以总字节数）。

## 实际实现（约 20 行）

这是 nanochat 的 `evaluate_bpb` 核心（简化版）：

```python
import math, torch

@torch.no_grad()
def evaluate_bpb(model, loader, steps, token_bytes):
    # token_bytes: LongTensor [vocab_size]，每个 token 字符串的 UTF-8 字节长度
    total_nll, total_bytes = 0.0, 0
    for _ in range(steps):
        inputs, targets = next(loader)
        nll = model(inputs, targets, loss_reduction='none')  # [B, T] 每个 token 的 NLL（单位：nats）
        mask = targets >= 0                                  # 丢弃 ignore_index 填充
        nb = token_bytes[targets[mask]]                      # 每个目标 token 的字节数
        total_nll  += (nll[mask] * 1.0).sum().item() * 0 + (nll[mask]).sum().item()
        total_bytes += nb.sum().item()
    return total_nll / math.log(2) / total_bytes
```

注意其中的细微之处：精确版本通过将所有 token 的原始 NLL 相加并除以总字节数（等同于按字节加权平均）来正确加权。`token_bytes` 查找表由分词器一次性构建：`token_bytes[i] = len(tokenizer.decode([i]).encode('utf-8'))`。

快速验证，将结果与你已知的数字联系起来：如果你的分词器平均每个 token 对应 4.0 字节，验证损失为 2.2 nats/token，则 bpb ≈ 2.2 / ln(2) / 4.0 ≈ **0.79**。

## 为什么 Karpathy 将其作为主要调节指标

与基于任务的评估（如 CORE/MMLU）相比，val bpb 平滑且噪声低，后者在小规模下是阶梯函数。因此工作流程是：调整架构 → 重新运行 d12 → 在 wandb 中观察 `val/bpb` 随步数的变化（以及随挂钟时间/FLOPs 的变化）。CORE 运行稀疏（成本高）；bpb 是快速内循环信号。他的新版 `autoresearch` 仓库将 val_bpb 作为固定 5 分钟训练运行的唯一指标，正是因为它与词汇表大小无关，架构修改可以公平比较。

在自己的实验中需要注意一个细节：bpb 只有在评估相同的字节流时才完全可比。如果两个分词器将验证集分成不同的 token 序列，你仍然是在测量相同底层字节的压缩率——这正是其意义所在。

**参考：**

- [karpathy/nanochat — README](https://github.com/karpathy/nanochat)
- [nanochat walkthrough — Discussion #1](https://github.com/karpathy/nanochat/discussions/1)
- [BPB: a tokenizer-agnostic way to measure LLMs](https://dipkumar.dev/posts/llm/bits-per-byte/)
- [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
