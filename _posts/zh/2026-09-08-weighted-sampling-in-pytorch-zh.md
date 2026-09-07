---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch中的加权采样
translated: true
type: note
---

问题：`torch.multinomial` 在 PyTorch 中有什么作用？

答案：

`torch.multinomial` 根据权重张量定义的概率分布进行索引采样。可以把它想象成一个加权抽奖——权重越高的项被抽中的概率越大。

**函数签名：**
```python
torch.multinomial(input, num_samples, replacement=False, *, generator=None)
```

**参数：**

| 参数 | 说明 |
|---|---|
| `input` | 1D 或 2D 权重张量（不需要归一化求和为1） |
| `num_samples` | 需要抽取的索引数量 |
| `replacement` | 若为 `True`，同一索引可被多次抽取 |

**简单示例：**
```python
import torch

weights = torch.tensor([1.0, 2.0, 7.0])  # 索引2的概率最高
samples = torch.multinomial(weights, num_samples=5, replacement=True)
# 例如：tensor([2, 2, 1, 2, 0])  —— 索引2出现次数最多
```

**常见应用场景：**

- **语言模型** —— 根据 logit 概率采样下一个 token
- **强化学习** —— 从策略分布中采样动作
- **数据增强** —— 对数据点进行加权随机采样
- **蒙特卡洛方法** —— 从自定义分布中抽取样本

**二维输入（批处理模式）：**
```python
weights = torch.tensor([[1.0, 9.0],   # 第0行：强烈偏向索引1
                         [5.0, 5.0]]) # 第1行：等概率
samples = torch.multinomial(weights, num_samples=3, replacement=True)
# 形状：(2, 3) —— 每行独立采样
```

每行被视为独立分布，输出形状为 `(batch_size, num_samples)`。

参考资料：
- [torch.multinomial — PyTorch 官方文档](https://pytorch.org/docs/stable/generated/torch.multinomial.html)