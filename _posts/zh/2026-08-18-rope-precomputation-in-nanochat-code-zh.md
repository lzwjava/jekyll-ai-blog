---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RoPE预计算在NanoChat代码中
translated: true
type: note
---

**问题：解释 nanochat 代码中的 RoPE 实现。**

**答案：**

这段代码是**旋转位置编码（RoPE）的预计算部分**。它创建了后续用于旋转 Query 和 Key 向量的 `cos` 和 `sin` 表格。

让我们从数学 → 张量形状 → 代码逐步分析。

---

## 1. 首先：RoPE 需要什么

对于每个令牌位置 `t` 和每一对嵌入维度，RoPE 需要一个角度：

[
\theta_{t,i}=t \cdot \frac{1}{base^{2i/d}}
]

其中：

* `t` = 令牌位置
* `i` = 维度对索引
* `d` = 注意力头维度
* `base` = 通常为 10000，此处为 100000

然后：

[
cos(\theta_{t,i})
]

和

[
sin(\theta_{t,i})
]

被用来旋转 Q/K。

---

## 2. 计算注意力头维度

```python
head_dim = self.config.n_embd // self.config.n_head
```

示例：

GPT：

```
嵌入大小 = 768
注意力头数 = 12
```

那么：

```
head_dim = 768 / 12 = 64
```

注意力机制分割：

```
隐藏状态

[768]

        分割成注意力头

注意力头0 [64]
注意力头1 [64]
...
注意力头11[64]
```

RoPE 在每个注意力头**内部**工作，而不是在整个嵌入上。

---

## 3. 预计算旋转表格

```python
cos, sin = self._precompute_rotary_embeddings(
    self.rotary_seq_len,
    head_dim
)
```

假设：

```
最大序列长度 = 2048
head_dim = 64
```

需要：

```
位置 0
位置 1
...
位置 2047
```

每个位置：

```
64 个维度
```

但 RoPE 成对旋转：

```
(维度0, 维度1)

(维度2, 维度3)

(维度4, 维度5)

...
```

因此只需要一半维度的频率：

```
64 / 2 = 32
```

---

# 在 `_precompute_rotary_embeddings` 内部

## 4. 获取设备

```python
if device is None:
    device = self.transformer.wte.weight.device
```

将张量放在与嵌入相同的 GPU 上。

示例：

```
cuda:0
```

---

## 5. 创建频率索引

```python
channel_range = torch.arange(
    0,
    head_dim,
    2,
    dtype=torch.float32,
    device=device
)
```

对于：

```
head_dim=8
```

这会产生：

```
[0,2,4,6]
```

因为维度是成对的：

```
dim0 <-> dim1
dim2 <-> dim3
dim4 <-> dim5
dim6 <-> dim7
```

每对中只有第一个维度需要一个频率。

---

## 6. 计算逆频率

```python
inv_freq = 1.0 / (
    base ** (channel_range / head_dim)
)
```

这是 RoPE 的核心公式。

示例：

```
base=100000
head_dim=8
```

对于维度 0：

[
freq_0 =
1 / 100000^{0/8}
]

=1

对于维度 6：

[
freq_6 =
1 / 100000^{6/8}
]

小得多。

所以：

```
低维度：
    高频率旋转

高维度：
    慢速旋转
```

类似于傅里叶特征。

---

## 7. 创建位置

```python
t = torch.arange(seq_len)
```

示例：

```
seq_len=4
```

创建：

```
[0,1,2,3]
```

令牌位置。

---

## 8. 外积

这一行是核心：

```python
freqs = torch.outer(t, inv_freq)
```

想象一下：

```
t:

位置
0
1
2
3


inv_freq:

频率0
频率1
频率2
频率3
```

外积：

```
             频率0 频率1 频率2 频率3

位置0          0     0     0     0

位置1          f0    f1    f2    f3

位置2          2f0   2f1   2f2   2f3

位置3          3f0   3f1   3f2   3f3
```

形状：

```
(seq_len, head_dim/2)
```

示例：

```
(2048,32)
```

每个单元格是一个旋转角度。

---

## 9. 生成查找表

```python
cos, sin = freqs.cos(), freqs.sin()
```

现在：

```
cos[位置][维度对]

sin[位置][维度对]
```

示例：

```
cos:

[
 [1.0,1.0,1.0],
 [0.54,0.99,0.999],
 ...
]


sin:

[
 [0,0,0],
 [0.84,0.01,0.001],
 ...
]
```

---

## 10. 转换精度

```python
cos, sin = cos.to(COMPUTE_DTYPE)
```

通常：

```
bf16
```

因为存储：

```
2048 x 32
```

很小，但对于非常长的上下文：

```
128k x 64
```

就很重要了。

---

## 11. 添加广播维度

```python
cos, sin = cos[None,:,None,:]
```

原始：

```
(seq_len, head_dim/2)
```

示例：

```
(2048,32)
```

之后：

```
(1,2048,1,32)
```

为什么？

因为 Q/K 通常具有形状：

```
(batch, heads, seq_len, head_dim)
```

示例：

```
B=8
H=12
T=2048
D=64


q:

(8,12,2048,64)
```

RoPE 操作需要：

```
位置维度
```

来广播。

表格：

```
(1,2048,1,32)
```

会自动广播到：

```
(8,12,2048,32)
```

---

# 后续的实际旋转

这段代码只准备了：

```
cos
sin
```

稍后在某个地方：

```python
q_rotated = q * cos + rotate_half(q) * sin
```

其中：

```
rotate_half([x0,x1,x2,x3])

=

[-x1,x0,-x3,x2]
```

对于每一对：

```
[x,y]

旋转：

[x*cos - y*sin,
 x*sin + y*cos]
```

标准的二维旋转矩阵：

[
\begin{bmatrix}
cos\theta & -sin\theta\
sin\theta & cos\theta
\end{bmatrix}
]

---

所以整个流程：

```
令牌
 |
v
嵌入
 |
v
Q,K 投影
 |
v
分割成注意力头
 |
v
RoPE:

位置 t
 |
计算 theta
 |
应用：

[x,y] -> 旋转后的 [x',y']

 |
v
注意力机制：

Q_rot K_rot^T
 |
v
相对位置涌现
```

nanochat 的实现与原始 RoPE 论文非常接近。巧妙之处在于**整个位置编码仅仅是一个缓存的 sin/cos 表格加上逐元素运算——没有可学习的参数。**
