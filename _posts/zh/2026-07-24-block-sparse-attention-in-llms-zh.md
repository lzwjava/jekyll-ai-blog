---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大语言模型中的块稀疏注意力
translated: true
type: note
---

## 问题：什么是LLM中的block sparse attention？

## 答案

**Block sparse attention** 是对Transformer注意力机制的一种优化，模型**不会计算每个token两两之间的所有注意力对**。它不是计算完整的`N × N`注意力矩阵，而是只计算选定**块**内部的注意力。

目标：降低注意力的二次复杂度。

---

## 1. 标准注意力

正常的自注意力：

\[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt{d}})V
\]

对于长度为`N`的序列：

* `Q`: `N × d`
* `K^T`: `d × N`

因此：

\[
QK^T = N \times N
\]

示例：

```
序列长度：32,768 tokens

注意力矩阵：

          token
       0 1 2 3 ... 32767
0      x x x x ... x
1      x x x x ... x
2      x x x x ... x
...
32767  x x x x ... x
```

注意力分数数量：

\[
32768^2 \approx 1.07B
\]

巨大的内存和计算量。

---

## 2. 稀疏注意力思想

不再是：

```
每个token关注每个token

O(N²)
```

而是：

```
只让选定的token相互关注

O(N * k)
```

其中`k << N`。

示例：

```
全注意力：

A 关注：
B C D E F G H I


稀疏注意力：

A 关注：
B C
```

---

## 3. 为什么是“块”稀疏？

一种朴素的稀疏模式：

```
token 0 关注 token 100
token 1 关注 token 500
token 2 关注 token 999
```

对GPU极不友好。

GPU喜欢连续的内存访问。

因此我们将token划分成块。

示例：

序列：

```
tokens:

[0-63][64-127][128-191][192-255]
```

块：

```
B0       B1       B2       B3
```

不再计算：

```
       B0 B1 B2 B3

B0     x  x  x  x
B1     x  x  x  x
B2     x  x  x  x
B3     x  x  x  x
```

只计算：

```
       B0 B1 B2 B3

B0     x  x
B1        x  x
B2           x  x
B3              x
```

注意力矩阵变成了块掩码。

---

## 4. 示例：长上下文LLM

假设：

```
上下文长度 = 1M tokens
块大小 = 1024
```

块数量：

```
1,000,000 / 1024 ≈ 976 个块
```

密集注意力：

```
976 × 976 个块
≈ 952k 次块操作
```

稀疏：

```
局部窗口 + 全局块

可能只有20k次块操作
```

巨大的节省。

---

## 5. 常见的块稀疏模式

### A. 局部注意力

最常见。

每个token关注附近的token：

```
          window

<---------------->

A B C D E F G H I J

        X
        |
        v

A B C D E F G H I J
      ^^^^^
```

用于：

* Longformer
* BigBird
* 许多长上下文模型

---

### B. 滑动窗口 + 全局token

示例：

```
Token 关注：

附近：

[1000]
  |
  v

900 901 902 ...1100


加上：

特殊token：
<system>
<summary>
```

适用于文档。

---

### C. 检索/块注意力

只关注检索到的块：

```
问题：

"Who is Einstein?"

检索：

block 3000
block 7000
block 9000

注意力：

query ---> 仅这些块
```

用于：

* RAG系统
* 记忆架构

---

## 6. GPU实现视角

一个普通的注意力kernel：

```
for i in tokens:
    for j in tokens:
        score = Q[i] @ K[j]
```

复杂度：

```
N*N*d
```

块稀疏：

```
for query_block in blocks:
    for key_block in allowed_blocks:
        matmul(query_block,key_block)
```

示例：

```
allowed_blocks = {
 B0: [B0,B1],
 B1: [B0,B1,B2],
 B2: [B1,B2,B3]
}
```

kernel跳过所有其他内容。

---

## 7. 与FlashAttention的关系

重要区别：

### FlashAttention

它做的是：

```
相同的全注意力

但：
- 分块计算
- 避免显式生成NxN矩阵
- 优化内存带宽
```

复杂度：

\[
O(N^2)
\]

但更快。

---

### Block sparse attention

它做的是：

```
减少注意力计算量

跳过块
```

复杂度：

\[
O(N \times k)
\]

不同的思路。

两者可以结合：

```
块稀疏模式
        +
FlashAttention kernel
        =
极长上下文注意力
```

---

## 8. 为什么现代LLM不全用这个？

因为密集注意力很强大。

问题在于：

稀疏注意力引入了信息瓶颈。

示例：

```
Token A 需要来自 token Z 的信息

但稀疏模式阻断了连接

A --------X-------- Z
```

模型需要多层来传播信息。

权衡：

| 注意力            | 质量   | 速度       |
| ---------------- | ------ | ---------- |
| 密集             | 最好   | 代价高     |
| 局部稀疏         | 好     | 快         |
| 块稀疏           | 好     | 快得多     |
| 检索稀疏         | 看情况 | 非常快     |

---

## 9. 当前使用情况

示例：

* Google的长上下文架构探索了稀疏注意力变体
* Microsoft的Longformer引入了滑动窗口+全局注意力
* BigScience在BigBird中使用了稀疏注意力思想

现代前沿LLM通常结合：

```
密集注意力
+
FlashAttention
+
KV cache优化
+
MLA / GQA
+
有时使用稀疏注意力
```

---

对于正在构建/训练模型的人来说：**block sparse attention本质上就是将注意力掩码从密集的NxN矩阵改为结构化的稀疏矩阵，以便GPU kernel跳过无用的QK matmul。难点不在于数学，而在于设计一种既能保持模型质量又能高效映射到GPU内存访问的稀疏模式。**