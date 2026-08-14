---
audio: false
generated: true
image: false
lang: zh
layout: post
title: view -1 自动推断维度
translated: true
type: note
---

问题：在 `logits.view(-1, logits.size(-1))` 中，`-1` 是最后一个索引的意思吗？

答案：**不是。** 在 PyTorch 的 `view()` 中，`-1` 表示**“自动推断该维度”**，而不是“最后一个索引”。

例如，假设：

```python
logits.shape
# [B, T, V]
# [2, 10, 50000]
```

那么：

```python
logits.view(-1, logits.size(-1))
```

就变成了：

```python
logits.view(-1, 50000)
```

PyTorch 会计算：

```text
2 × 10 × 50000
---------------- = 20
     50000
```

因此结果是：

```python
[20, 50000]
```

这在语言模型的损失计算中非常常见：

```python
logits = model(x)
# [batch, seq_len, vocab_size]

logits = logits.view(-1, logits.size(-1))
# [batch * seq_len, vocab_size]

targets = targets.view(-1)
# [batch * seq_len]

loss = F.cross_entropy(logits, targets)
```

其核心思想是：

```text
[B, T, V]
   ↓
[B*T, V]
```

你是在**将 batch × sequence 的位置展平**，同时保留词表维度不变。

### `-1` 与负索引

这两个是不同的概念：

```python
x[-1]       # indexing: last element
x.view(-1)  # reshape: infer dimension
```

所以：

```python
logits.size(-1)
```

**确实**表示“最后一个维度的大小” → `V`。

但是：

```python
logits.view(-1, ...)
```

表示“自动推断这个维度。”