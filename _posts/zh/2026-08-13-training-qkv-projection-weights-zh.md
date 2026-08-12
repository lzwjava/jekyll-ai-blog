---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练QKV投影权重
translated: true
type: note
---

问题：在Transformer注意力机制中，Q、K、V的形状和权重（`Wq`、`Wk`、`Wv`）是如何训练的？

回答：

是的，你的理解基本正确。我们来逐步看看实际的前向传播过程。

假设GPT风格的Transformer：

```
hidden_size = 768
num_heads = 12
head_dim = 64

12 * 64 = 768
```

输入的隐藏状态：

```
X shape = [sequence_length, hidden_size]

X = [T, 768]
```

例如，经过token嵌入和前面层之后，一个token有：

```
x = [768]
```

---

### 1. Q投影

模型有一个学习到的矩阵：

```
Wq = [768, 768]
```

这个矩阵在初始化时创建，并在训练过程中学习。

前向传播：

```
Q = X @ Wq
```

形状：

```
[T,768] @ [768,768]

= [T,768]
```

所以Q仍然具有hidden_size维度。

然后分割成多头：

```
Q -> [T, 12, 64]
```

或者：

```
q1 = [T,64]
q2 = [T,64]
...
q12 = [T,64]
```

每个头都有自己的Q切片。

---

### 2. K投影

同样的思路：

学习到的：

```
Wk = [768,768]
```

前向传播：

```
K = X @ Wk
```

结果：

```
K = [T,768]
```

分割：

```
K -> [T,12,64]
```

---

### 3. V投影

同样：

学习到的：

```
Wv = [768,768]
```

前向传播：

```
V = X @ Wv
```

结果：

```
V = [T,768]
```

分割：

```
V -> [T,12,64]
```

---

### 4. 注意力

对于单个头：

Query：

```
q = [T,64]
```

Key：

```
k = [T,64]
```

计算相似度：

```
scores = q @ k.T / sqrt(64)
```

形状：

```
[T,64] @ [64,T]

= [T,T]
```

这表示：

```
token i 关注 token j
```

然后：

```
attention = softmax(scores)
```

最后：

```
output = attention @ v
```

其中：

```
attention = [T,T]

v = [T,64]
```

所以：

```
[T,T] @ [T,64]

= [T,64]
```

合并12个头：

```
12 * 64 = 768
```

回到：

```
[T,768]
```

---

### Wq、Wk、Wv 是否被训练？

是的。

它们是普通的神经网络参数。

在训练过程中：

```
loss
 |
backprop
 |
grad(Wq)
grad(Wk)
grad(Wv)
 |
optimizer update
```

例如AdamW：

```
Wq = Wq - learning_rate * Adam(gradient)
```

模型学习：

* `Wq`：什么样的信息应该成为query
* `Wk`：什么样的特征应该被搜索/匹配
* `Wv`：什么样的信息应该被检索

---

一个有用的思维模型：

```
hidden state x
      |
      |
      +---- Wq ---> query space
      |
      +---- Wk ---> key space
      |
      +---- Wv ---> value space
```

`Wq`、`Wk`、`Wv` 是同一个隐藏表示经过三种不同学习到的投影。

它们初始是随机的，经过数十亿个样本的训练，变成了有用的变换。

有一个微妙之处：尽管Q/K/V来自同一个`X`，但经过投影后，它们**并不处于相同的语义空间**：

```
Q = XWq
K = XWk
V = XWv
```

因为：

```
Wq != Wk != Wv
```

模型为以下不同目的学习了不同的坐标系统：

* 提出一个问题（Q）
* 匹配一个问题（K）
* 提供信息（V）

这就是为什么注意力机制变成了一个**数据依赖的线性层**：训练后，矩阵`Wq/Wk/Wv`是固定的，但生成的注意力矩阵：

```
softmax(QK^T)
```

会随着每个输入序列而变化。
