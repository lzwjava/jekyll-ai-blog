---
audio: false
generated: true
image: false
lang: zh
layout: post
title: KV缓存：2与层乘数
translated: true
type: note
---

**问题：** 为什么 KV 缓存公式中会出现 `2` 这个系数，又为什么要乘以 `num_layers`？

**回答：**

`2` 和 `num_layers` 是**两个独立的乘数**，并非组合因子。下面我来详细解释：

```
KV 缓存大小 = batch_size × seq_len × hidden_dim × 2 × num_layers × bytes
                                                     ↑                  ↑
                                              K + V 张量       每层一个
```

## 系数 `2`：键和值张量

在多头注意力机制中，包含 **Q、K、V**：

```python
Q = input @ W_q  # 查询：每一步重新计算
K = input @ W_k  # 键：在后续所有步骤中复用
V = input @ W_v  # 值：在后续所有步骤中复用
```

在推理阶段，只缓存 **K 和 V**，而不缓存 Q。原因如下：

- **Q 仅从当前词元计算得出**，因此数据量小且是临时的
- **K 和 V 必须为序列中所有之前的词元存储**，因为：

  ```
  attention(Q_new, K_all, V_all) = softmax(Q_new @ K_all.T / sqrt(d)) @ V_all
  ```

  当预测第 100 个词元时，需要用到第 1-99 个词元的 K 和 V。因此，`2` 这个系数代表同时缓存了 K 和 V。

## `× num_layers`：每个注意力层都有自己的缓存

一个 Transformer 模型包含多个层（例如，13B 模型有 40 层），**每个层都有独立的 K 和 V 缓存**：

```
第 1 层：K_cache_1 (batch, seq_len, hidden_dim)
         V_cache_1 (batch, seq_len, hidden_dim)
第 2 层：K_cache_2 (batch, seq_len, hidden_dim)
         V_cache_2 (batch, seq_len, hidden_dim)
...
第 40 层：K_cache_40 (batch, seq_len, hidden_dim)
          V_cache_40 (batch, seq_len, hidden_dim)
```

总计 = `2 * 40 = 80` 个缓存张量。

## 具体示例

对于一个 **13B 模型**（通常 hidden_dim 约为 5120，约 40 层）：

```python
batch_size = 32
seq_len = 4096
hidden_dim = 5120
num_layers = 40
bytes = 2  # fp16

# 每层：batch × seq × hidden = 32 × 4096 × 5120 = 6.71亿 个元素
# 每层 K 缓存：6.71亿 × 2 字节 = 1.3 GB
# 每层 V 缓存：6.71亿 × 2 字节 = 1.3 GB
# 每层两者合计：2.6 GB
# 总 × 40 层：104 GB
```

所以，当你看到 **52 GB**（我之前的例子）时，它实际上指的是所有层在单个批次下的完整 KV 缓存大小。

## 为什么这很重要

这就是为什么 KV 缓存会成为推理过程中**批次大小的硬性限制**：

```python
最大批次大小 ≈ 可用内存 / (2 × num_layers × seq_len × hidden_dim × bytes)
```

在 MI300X（192 GB）上：

```
最大批次大小 ≈ 192GB / (2 × 40 × 4096 × 5120 × 2 字节)
             ≈ 192GB / 每个词元位置 3.3GB
             ≈ 完整序列时约 58 的批次大小
```

这就是 **MQA（多查询注意力）** 和 **GQA（分组查询注意力）** 发挥作用的原因——它们会减小缓存中的 `hidden_dim`：

```
# 标准 MHA：K 和 V 是 (batch, seq, hidden_dim)
# GQA：K 和 V 是 (batch, seq, hidden_dim // num_groups)
# MQA：K 和 V 是 (batch, seq, hidden_dim // num_heads)  [极端情况]
```

将缓存大小减小 8-12 倍，可以让你容纳更大的批次。
