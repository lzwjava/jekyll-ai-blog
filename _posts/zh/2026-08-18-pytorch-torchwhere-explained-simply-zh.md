---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch torch.where 简易讲解
translated: true
type: note
---

问题：解释PyTorch中的`torch.where`。

答案：

`torch.where` 基本上是 **element-wise if/else**。

```python
torch.where(condition, x, y)
```

意思是：

```python
result[i] = x[i] if condition[i] else y[i]
```

### 1. 简单示例

```python
import torch

x = torch.tensor([1, 2, 3, 4])
y = torch.tensor([10, 20, 30, 40])

condition = x > 2

torch.where(condition, x, y)
```

结果：

```text
tensor([10, 20,  3,  4])
```

因为：

```text
x > 2
 ↓
[False, False, True, True]

where：
False → y
True  → x

[10, 20, 3, 4]
```

这等价于：

```python
[
    x[i] if x[i] > 2 else y[i]
    for i in range(len(x))
]
```

但实现为在GPU上的tensor操作。

---

### 2. 非常常见的LLM用法

你经常会看到：

```python
mask = logits < threshold

logits = torch.where(
    mask,
    torch.tensor(float("-inf")),
    logits,
)
```

例如：

```python
logits = torch.tensor([
    1.0, 5.0, 2.0, 8.0
])

mask = logits < 3

result = torch.where(
    mask,
    torch.tensor(float("-inf")),
    logits,
)

print(result)
```

```text
tensor([-inf, 5., -inf, 8.])
```

概念上：

```python
if logits[i] < 3:
    result[i] = -inf
else:
    result[i] = logits[i]
```

这在**masking attention/logits**中非常有用。

---

### 3. Broadcasting

`torch.where` 遵循PyTorch的broadcasting规则。

```python
x = torch.tensor([
    [1, 2, 3],
    [4, 5, 6],
])

condition = torch.tensor([
    [True, False, True],
    [False, True, False],
])

torch.where(condition, x, 0)
```

结果：

```text
tensor([
    [1, 0, 3],
    [0, 5, 0],
])
```

这里 `0` 被broadcast到整个tensor。

所以：

```python
torch.where(condition, x, 0)
```

基本上就是：

```python
for every element i:
    if condition[i]:
        output[i] = x[i]
    else:
        output[i] = 0
```

---

### 4. `where(condition)` 有不同的含义

还有：

```python
torch.where(condition)
```

只有单个参数。

它返回**条件为真的索引**。

```python
x = torch.tensor([10, 20, 30, 40])

torch.where(x > 20)
```

给出类似：

```text
(tensor([2, 3]),)
```

意思是：

```text
x[2] = 30
x[3] = 40
```

对于2D tensor：

```python
x = torch.tensor([
    [1, 5],
    [7, 2],
])

torch.where(x > 3)
```

返回：

```text
(tensor([0, 1]), tensor([1, 0]))
```

意思是：

```text
x[0,1] = 5
x[1,0] = 7
```

---

### 5. 思维模型

把：

```python
torch.where(condition, A, B)
```

看作**tensor级别的三元运算符**：

```python
condition ? A : B
```

例如：

```python
y = torch.where(x > 0, x, 0)
```

本质上就是：

```python
y = max(x, 0)
```

逐个元素。

而：

```python
y = torch.where(mask, -torch.inf, logits)
```

意思是：

```text
mask=True  → -inf
mask=False → logits
```

这种模式在Transformer实现中随处可见：**causal masks, padding masks, attention masking, logit filtering, loss masking**等等。