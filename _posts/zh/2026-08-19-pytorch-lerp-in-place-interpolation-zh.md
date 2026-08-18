---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch lerp_ 原地插值
translated: true
type: note
---

问题：PyTorch 中的 `lerp_` 是什么意思？

回答：

`lerp_` 表示 **就地线性插值（in-place linear interpolation）**。

名称分解如下：

* `lerp` = **线性插值（linear interpolation）**
* `_` 后缀 = **就地修改张量（modify the tensor in-place）**

核心运算为：

\[
\text{out} = a + w(b-a)
\]

或等价地：

\[
\text{out} = (1-w)a + wb
\]

在 PyTorch 中：

```python
a = torch.tensor([0., 10.])
b = torch.tensor([10., 20.])

a.lerp_(b, 0.25)

print(a)
# tensor([ 2.5, 12.5])
```

由于是 `_`，**`a` 本身被修改**。

### `lerp` 与 `lerp_` 的区别

```python
a = torch.tensor([0., 10.])
b = torch.tensor([10., 20.])

c = torch.lerp(a, b, 0.25)

# a 保持不变
# c = [2.5, 12.5]
```

对比：

```python
a.lerp_(b, 0.25)

# a 现在为 [2.5, 12.5]
```

### 为什么在 ML 代码中会看到 `lerp_`

一个非常常见的用途是 **EMA / 指数移动平均（exponential moving average）**：

```python
ema.lerp_(model, decay)
```

假设：

```python
ema = [1, 1]
model = [5, 9]
decay = 0.1
```

那么：

```text
ema ← ema + 0.1 * (model - ema)
```

得到：

```text
[1, 1] + 0.1 * ([5, 9] - [1, 1])
= [1.4, 1.8]
```

这基本上等价于一种简洁写法：

```python
ema = (1 - decay) * ema + decay * model
```

但 `lerp_` 是 **就地** 操作，避免了创建另一个张量。

一个重要细节：**第三个参数是一个权重（weight）**，在语义上不一定是“衰减”（decay）。所以：

```python
torch.lerp(start, end, weight)
```

意思是：

```text
start + weight * (end - start)
```

* `weight = 0` → `start`
* `weight = 1` → `end`
* `weight = 0.5` → 中点
* `weight = 2` → 外推到 `end` 之外

参考：

* [PyTorch torch.lerp 文档](https://docs.pytorch.org/docs/stable/generated/torch.lerp.html?utm_source=chatgpt.com)
