---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RoPE的外积
translated: true
type: note
---

**问题：**
`freqs = torch.einsum("i,j -> ij", t, inv_freq)` 是什么意思？

**回答：**

这行代码计算了两个一维张量的**外积**：

```python
freqs = torch.einsum("i,j -> ij", t, inv_freq)
```

等效的 PyTorch 实现：

```python
freqs = t[:, None] * inv_freq[None, :]
```

或：

```python
freqs = torch.outer(t, inv_freq)
```

### 逐步解释

假设：

```python
t = torch.tensor([0, 1, 2, 3])      # shape: [4]

inv_freq = torch.tensor([1.0, 0.1, 0.01])  # shape: [3]
```

einsum 记号：

```
"i,j -> ij"
```

意味着：

* 输入1有维度 `i`
* 输入2有维度 `j`
* 输出保留两个维度：`ij`

数学上：

\[
freqs_{ij}=t_i \times inv_freq_j
\]

所以：

```
          inv_freq
          1.0    0.1    0.01
t=0       0      0      0
t=1       1      0.1    0.01
t=2       2      0.2    0.02
t=3       3      0.3    0.03
```

输出：

```python
freqs.shape
# torch.Size([4, 3])
```

---

### 为什么在 Transformer 中使用？

这通常来自 **RoPE（旋转位置编码）**。

典型代码：

```python
t = torch.arange(seq_len)
inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2) / dim))

freqs = torch.einsum("i,j->ij", t, inv_freq)
```

这里：

* `t` = token 位置

例如：

```
t = [0,1,2,3,...,2047]
```

* `inv_freq` = 每个嵌入维度对的频率

例如：

```
inv_freq =
[
 1.0000,
 0.1000,
 0.0100,
 0.0010,
 ...
]
```

输出：

```
freqs[position, dimension]
```

包含旋转角度：

\[
\theta_{pos,k}=pos \times \frac{1}{10000^{2k/d}}
\]

然后：

```python
cos = torch.cos(freqs)
sin = torch.sin(freqs)
```

用于旋转 Q/K 向量：

\[
q' = q \cos(\theta) + rotate(q)\sin(\theta)
\]

---

### 前向视角

对于序列长度 4096 和隐藏维度 4096：

```python
t.shape
# [4096]

inv_freq.shape
# [2048]
```

经过 einsum 后：

```python
freqs.shape
# [4096,2048]
```

含义：

```
             维度频率
位置 0   θ0 θ1 θ2 ... θ2047
位置 1   θ0 θ1 θ2 ... θ2047
位置 2   θ0 θ1 θ2 ... θ2047
...
位置4095
```

每个 token 位置在每个旋转维度对上获得不同的相位。

所以这一行代码本质上就是：

> "生成完整的位置 × 频率矩阵，用于在 RoPE 中旋转每个 token 的嵌入维度。"
