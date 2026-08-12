---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解PyTorch中的X.mT
translated: true
type: note
---

问题：这里的 `X.mT` 是什么意思，整体计算是否与你写的等价？

答案：是的。在 PyTorch 中，**`.mT` 表示矩阵转置**。

对于二维张量：

```python
X.mT
```

等价于：

```python
X.transpose(-2, -1)
```

所以如果：

```python
X.shape == (n, d)
```

那么：

```python
X.mT.shape == (d, n)
```

你的代码可以理解为：

```python
X = X / (X.norm(...) * 1.01 + 1e-6)

A = X.mT @ X
B = b * A + c * (A @ A)

X = a * X + X @ B
```

我们来看一下形状。

假设：

```text
X: (n, d)
```

其中 `n` = 向量/令牌的数量，`d` = 隐藏维度。

### 1. 归一化 X

```python
X = X / (X.norm(...) * 1.01 + 1e-6)
```

这会将 `X` 按某种基于范数的因子进行缩放。

忽略广播细节：

```text
X: (n, d)
```

仍然为 `(n, d)`。

### 2. `X.mT @ X`

```python
A = X.mT @ X
```

表示：

```text
(d, n) @ (n, d)
       ↓
     (d, d)
```

所以：

```text
A = XᵀX
```

这本质上是一个**维度/特征的格拉姆矩阵/相关矩阵**。

例如：

```text
X = [
  x₁
  x₂
  x₃
]
```

其中每个 `xᵢ ∈ Rᵈ`。

那么：

```text
XᵀX
```

表示**X 的不同维度在 n 个样本之间的相关性**。

### 3. `A @ A`

```python
A @ A
```

就是：

```text
A²
```

因为 `A` 是 `(d, d)`：

```text
(d, d) @ (d, d)
        ↓
      (d, d)
```

因此：

```python
B = b * A + c * (A @ A)
```

数学上表示为：

```text
B = bA + cA²
```

所以 `B` 是 `XᵀX` 的**多项式函数**：

```text
B = b XᵀX + c (XᵀX)²
```

### 4. `X @ B`

最后：

```python
X = a * X + X @ B
```

其中：

```text
X: (n, d)
B: (d, d)

X @ B: (n, d)
```

所以结果可以加回到 `X` 中。

展开全部：

```text
X_new
= aX + X[bXᵀX + c(XᵀX)²]
```

或者：

```text
X_new
= aX
+ bXXᵀX
+ cX(XᵀX)²
```

这是一种理解该操作的好方法：**`X` 构建特征空间矩阵 `XᵀX`，将其转化为多项式变换 `B`，然后将这种学习到的/数据相关的变换应用于 X。**

重要的是，这**不是**：

```text
X = X / X
```

`X.mT` 特指**转置最后两个维度**，而不是某种特殊的乘法运算。

如果 `X` 是三维的，例如 `(batch, seq, hidden)`，`.mT` 得到 `(batch, hidden, seq)`，这正是 PyTorch 的 `.mT` 在批量矩阵乘法中特别方便的原因。