---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解 PyTorch 中的 torch.roll
translated: true
type: note
---

问题：`torch.roll` 是什么意思？

答案：

`torch.roll` 会**沿指定维度循环移动张量元素**。当元素移出一端时，会从另一端绕回。

可以将其想象为旋转数组。

语法：

```python
torch.roll(input, shifts, dims=None)
```

* `input`：张量
* `shifts`：移动的步数
* `dims`：沿哪个维度移动

### 一维示例

```python
import torch

x = torch.tensor([1, 2, 3, 4, 5])

torch.roll(x, shifts=2)
```

输出：

```
tensor([4, 5, 1, 2, 3])
```

解析：

```
原数组：
[1, 2, 3, 4, 5]

向右移动2步：
        <- 绕回
[4, 5, 1, 2, 3]
```

最后两个元素移动到了最前面。

---

### 负向移动

```python
torch.roll(x, shifts=-2)
```

输出：

```
tensor([3, 4, 5, 1, 2])
```

向左移动2步：

```
[1, 2, 3, 4, 5]
       ↓
[3, 4, 5, 1, 2]
```

---

### 二维示例

矩阵：

```python
x = torch.tensor([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
```

向下移动行：

```python
torch.roll(x, shifts=1, dims=0)
```

输出：

```
[
 [7, 8, 9],
 [1, 2, 3],
 [4, 5, 6]
]
```

向右移动列：

```python
torch.roll(x, shifts=1, dims=1)
```

输出：

```
[
 [3, 1, 2],
 [6, 4, 5],
 [9, 7, 8]
]
```

---

### 深度学习为什么使用 `torch.roll`？

常见用途：

### 1. 视觉模型 / 图像平移

用于数据增强或比较相邻像素：

```python
shifted = torch.roll(image, shifts=(1,1), dims=(1,2))
```

沿垂直和水平方向移动图像像素。

---

### 2. 自监督学习

示例：比较特征图与其平移版本：

```python
loss = (x - torch.roll(x, 1, dim=1)).abs().mean()
```

衡量局部平滑度。

---

### 3. Transformer / 大语言模型研究

用于位置操作、旋转位置编码实验、循环注意力模式等。

示例：

```python
q_shifted = torch.roll(q, shifts=1, dims=1)
```

如果：

```
q shape = [batch, seq_len, hidden]
```

那么：

```
移动前：

token0 token1 token2 token3

经过 roll(1) 后：

token3 token0 token1 token2
```

这创建了平移后的 token 关系。

---

### 与 NumPy 的关系

基本等同于：

```python
numpy.roll()
```

对应关系：

```python
torch.roll(x, 2)
```

≈

```python
np.roll(x, 2)
```

---

实现思路：

```python
def simple_roll(x, shift):
    return torch.cat([
        x[-shift:],
        x[:-shift]
    ])
```

`torch.roll` 只是这种循环索引操作的高效 C++/CUDA 实现。