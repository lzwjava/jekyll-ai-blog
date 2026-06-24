---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 先删除，再学习注意力
translated: true
type: note
---

**问题：** 你在简化 Transformer 和 attention 时的目标是什么——你实际上想剥离掉什么？所谓“比 nanoGPT 更简单”会是什么样子？

**回答：**

你的思路和 Karpathy 写 nanoGPT 时一样，但更进了一步。马斯克的原则：*先删，再证明需要加回来*。

以下是你真正瞄准的东西：

**nanoGPT 仍然有、但你可以删掉的部分：**

```python
# nanoGPT 包含了所有这些仪式：
- 学习率调度器（余弦预热）
- 梯度裁剪
- 权重衰减 / AdamW 调参
- Dropout
- Flash attention
- DDP 多 GPU
- 检查点保存/加载
- Wandb 日志
- 梯度累积
- 混合精度（fp16/bf16）
```

**你的“白粥”版本——绝对最小但仍然能学习：**

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# 所有内容约 100 行，没有配置文件，没有你不需要的类

B, T, C = 4, 64, 64  # batch, context, channels
vocab = 65  # Shakespeare chars

# 单注意力头——看清原始机制
def attention(q, k, v):
    T = q.size(-2)
    w = q @ k.transpose(-2, -1) / C**0.5          # (B, T, T)
    w = w.masked_fill(torch.triu(torch.ones(T,T), diagonal=1).bool(), float('-inf'))
    w = F.softmax(w, dim=-1)
    return w @ v                                   # (B, T, C)

# 一个 block——不用类，只用函数
def block(x, Wqkv, Wproj, W1, W2):
    B, T, C = x.shape
    qkv = x @ Wqkv                                # (B, T, 3C)
    q, k, v = qkv.split(C, dim=-1)
    x = x + attention(q, k, v) @ Wproj
    x = x + F.relu(x @ W1) @ W2                  # FFN
    return x

# 没有学习率调度——只有恒定学习率
# 没有梯度裁剪
# 没有 dropout
# 没有检查点
# 甚至用 SGD 代替 AdamW
```

**你真正想指出的洞见：**

nanoGPT 教的是 Transformer。你的版本应该教的是 *attention 为什么能工作*——唯一的问题：**“token i 如何看向 token j？”**

剥离到这一步。一个头。没有多头。甚至没有位置编码（让它失败，然后再加上）。观察损失曲线。这就是学习。

**删掉顺序 (deletion order):**

1. 多头注意力 → 单头注意力
2. AdamW → SGD
3. 学习率调度 → 恒定学习率
4. LayerNorm → 无（看看它如何崩溃）
5. 残差连接 → 无（看看它如何崩溃）
6. 多个 block → 一个 block
7. DataLoader → 内联 `x = data[i:i+T]`

每一次删除都会教你那部分东西实际 *做了什么*——而这正是自己动手搭建的全部意义。

你不是在造工具。你是在造显微镜。越简单越清晰。
