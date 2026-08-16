---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 滑动窗口GQA注意力
translated: true
type: note
---

问题：当 `q, k, v` 的维度为 `(B, H, T, D)` 时，`_sdpa_attention(q, k, v, window_size, enable_gqa)` 是如何工作的？

回答：

这基本上是 **PyTorch 的 `scaled_dot_product_attention`（SDPA）** 的一个轻量封装，增加了两个额外功能：

1. **滑动窗口注意力**——每个 token 只关注附近的 token。
2. **GQA**——查询头的数量可以多于 KV 头的数量。

其概念上的操作为：

\[
\text{Attention}(Q,K,V) = \operatorname{softmax}\left(\frac{QK^T}{\sqrt D} + M\right)V
\]

其中 `M` 是注意力掩码。

### 1. 标准 SDPA

假设：

```python
q.shape = (B, Hq, Tq, D)
k.shape = (B, Hk, Tk, D)
v.shape = (B, Hk, Tk, D)
```

PyTorch 期望的调用格式：

```python
F.scaled_dot_product_attention(
    q, k, v,
    ...
)
```

其内部大致执行：

```python
scores = q @ k.transpose(-2, -1)
scores = scores / sqrt(D)

scores += mask

attn = softmax(scores, dim=-1)

out = attn @ v
```

因此，关键的形状变换为：

```text
q:      (B, Hq, Tq, D)
k.T:    (B, Hk, D, Tk)

                 ↓ 矩阵乘法

scores: (B, Hq, Tq, Tk)

                 ↓ softmax

attn:   (B, Hq, Tq, Tk)

                 ↓ @ V

out:    (B, Hq, Tq, D)
```

对于自回归 LLM 注意力，通常 `Tq = Tk = T`。

---

## 2. `window_size` 的作用是什么？

假设：

```text
tokens:

0 1 2 3 4 5 6 7 8 9
```

普通因果注意力在 token 7 处：

```text
0 1 2 3 4 5 6 7
              ↑
```

Token 7 可以关注它 **之前的所有内容**。

当滑动窗口大小为 4 时：

```text
0 1 2 3 4 5 6 7 8 9
        └───┘ ↑
```

token 7 只关注：

```text
4 5 6 7
```

因此注意力矩阵大致变为：

```text
        K →
       0 1 2 3 4 5 6 7
Q 0    1
  1    1 1
  2    1 1 1
  3    1 1 1 1
  4        1 1 1 1
  5          1 1 1 1
  6            1 1 1 1
  7              1 1 1 1
```

关键点在于：

**滑动窗口注意力是通过掩码实现的，而不是通过改变基本的注意力公式。**

从概念上讲：

```python
mask = causal_mask & sliding_window_mask

F.scaled_dot_product_attention(
    q, k, v,
    attn_mask=mask,
)
```

最近的 PyTorch SDPA 实现也可以更高效地表示因果/滑动窗口行为，而无需显式构建整个 `T × T` 掩码，具体取决于后端。

---

## 3. `enable_gqa` 的含义是什么？

这指的是 **分组查询注意力（Grouped Query Attention）**。

例如：

```text
Q 头数 = 32
K 头数 = 8
V 头数 = 8
```

我们不存储 32 个独立的 K/V 头，而是将每个 KV 头共享给 4 个 Q 头：

```text
Q0  Q1  Q2  Q3  → K0 V0
Q4  Q5  Q6  Q7  → K1 V1
...
```

因此：

```python
Hq = 32
Hkv = 8
```

并且：

```python
Hq / Hkv = 4
```

使用 GQA 时，K/V 实际上被重复：

```python
k = repeat_interleave(k, Hq // Hkv, dim=1)
v = repeat_interleave(v, Hq // Hkv, dim=1)
```

从概念上讲：

```text
K:

之前：

K0 K1 K2 K3 K4 K5 K6 K7

之后：

K0 K0 K0 K0 K1 K1 K1 K1 K2 K2 K2 K2 ...
```

但优秀的 SDPA 后端可以避免真正实例化所有这些副本。

这就是 `enable_gqa=True` 存在的原因。

---

## 4. 因此 `_sdpa_attention` 可能非常精简

一个典型的实现从概念上讲是这样的：

```python
import torch.nn.functional as F

def _sdpa_attention(q, k, v, window_size, enable_gqa):
    """
    q, k, v: (B, H, T, D)
    """

    return F.scaled_dot_product_attention(
        q,
        k,
        v,
        is_causal=True,
        enable_gqa=enable_gqa,
        # 此处传入滑动窗口掩码
    )
```

有趣的部分并不在于这个 Python 函数。

**真正的工作发生在 SDPA 的内核中。**

根据 GPU / PyTorch 的组合，SDPA 可能会分发到以下实现之一：

```text
PyTorch
   │
   ▼
scaled_dot_product_attention
   │
   ├── FlashAttention 风格的内核
   ├── 内存高效注意力
   └── 数学/参考实现
```

这就是 SDPA 如此有用的原因：你的模型代码只需要写

```python
F.scaled_dot_product_attention(q, k, v)
```

而 PyTorch 会在底层选择一个高度优化的实现。

---

## 5. 为什么 SDPA 比你自己编写快得多

朴素的 Python/PyTorch 实现：

```python
scores = q @ k.transpose(-2, -1)
scores = scores / math.sqrt(q.size(-1))

scores = scores.masked_fill(mask == 0, float("-inf"))

probs = scores.softmax(dim=-1)

out = probs @ v
```

对于序列长度 `T`，这会创建：

```text
QKᵀ
(B, H, T, T)
```

这可能非常巨大。

例如：

```text
B = 1
H = 32
T = 8192
```

注意力矩阵包含：

```text
32 × 8192 × 8192
≈ 21.5 亿个元素
```

以 FP16 计算，大约需要：

```text
4.3 GB
```

仅仅是一个注意力矩阵。

FlashAttention / SDPA 避免在 HBM 中物化完整的 `T × T` 矩阵。它通过分块计算注意力：

```text
             K/V
       ┌────┬────┬────┬────┐
       │    │    │    │    │
       ├────┼────┼────┼────┤
 Q     │tile│tile│tile│tile│
       ├────┼────┼────┼────┤
       │tile│tile│tile│tile│
       └────┴────┴────┴────┘
```

并逐步执行 softmax。

这就是 **FlashAttention** 的核心思想。

因此，如果你在 LLM 推理实现中阅读这段内容，`_sdpa_attention()` 本质上是一个抽象边界：

```text
                    LLM 层
                       │
                       ▼
              _sdpa_attention()
                       │
                       ▼
        scaled_dot_product_attention()
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        因果掩码              GQA / MQA
             │                   │
             └─────────┬─────────┘
                       ▼
                优化的 GPU
                   注意力
```

如果你粘贴出 **完整的 `_sdpa_attention` 实现**，特别是构造 `window_size` 的代码，我可以 **逐行结合实际的张量形状** 进行讲解，包括滑动窗口掩码的具体工作原理。