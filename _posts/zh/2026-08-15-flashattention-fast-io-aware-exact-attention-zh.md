---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'FlashAttention: 快速IO感知精准注意力'
translated: true
type: note
---

问题：arXiv论文2205.14135说了什么？

回答：这篇论文是 **《FlashAttention：具有IO感知的快速且内存高效的精确注意力机制》**，作者为Tri Dao等人。它介绍了 **FlashAttention**，这是现代LLM训练/推理背后最重要的优化之一。（[Hugging Face][1]）

核心思想：

> Transformer注意力之所以慢，主要不是由于FLOPs，而是因为GPU在内存层级之间移动数据花费了太多时间。

他们重新设计了注意力机制，使其具有 **IO感知**。（[SciSpace][2]）

---

## 1. 问题：标准注意力浪费GPU内存带宽

标准注意力：

给定：

```
Q = XWq
K = XWk
V = XWv
```

注意力：

\[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt d})V
\]

对于序列长度 `N`：

```
Q: N × d
K: N × d
V: N × d

QK^T:
N × N
```

注意力矩阵巨大。

示例：

```
序列长度 = 4096
头维度 = 128

注意力矩阵：

4096 × 4096
= 16,777,216 个元素

FP16:
约32 MB 每个头
```

对于多个头和层：

```
GPU HBM 内存爆炸
```

---

## 2. 令人惊讶的观察：计算并非瓶颈

现代GPU：

```
GPU SRAM（快速）
       |
       |
HBM VRAM（慢速）
       |
       |
CPU 内存
```

GPU每秒能进行数万亿次操作。

但移动数据：

```
HBM → SRAM
SRAM → HBM
```

代价高昂。

论文指出：

> 注意力算法应考虑IO复杂度，而不仅仅是计算复杂度。（[SciSpace][2]）

---

# 3. 标准注意力实现

通常：

```python
scores = Q @ K.T

attention = softmax(scores)

output = attention @ V
```

GPU执行：

```
1. 计算 QK^T
2. 将 NxN 矩阵写入 HBM
3. 读取 NxN 矩阵
4. Softmax
5. 写入结果
6. 再次读取
7. 乘以 V
```

巨大的 NxN 矩阵被实例化。

---

# 4. FlashAttention 理念：永不存储完整注意力矩阵

取而代之：

```
将 Q,K,V 分块
```

示例：

```
Q:

[ block ]
[ block ]
[ block ]


K,V:

[ block ]
[ block ]
[ block ]
```

计算：

```
Q_block × K_block^T
```

在 GPU SRAM 内部。

然后立即：

```
softmax
乘以 V
丢弃临时结果
```

永不将：

```
NxN 注意力矩阵
```

写入 VRAM。

---

可视化：

标准：

```
Q
 \
  \
   QK^T  ---> HBM
              |
              |
           softmax
              |
              |
              V
```

FlashAttention：

```
Q block
   \
    \
     SRAM
      |
      |
   softmax
      |
      |
      V

（无 NxN 矩阵存储）
```

---

# 5. 数学技巧：在线 softmax

问题：

Softmax 需要：

\[
softmax(x_i)=\frac{e^{x_i}}{\sum e^{x_i}}
\]

通常需要所有值。

FlashAttention 使用在线算法。

维护：

```
运行中的最大值 m
运行中的总和 l
运行中的输出 O
```

对于每个块：

```
新块到达

更新：
    最大值
    归一化
    输出
```

因此注意力可以逐块计算。

---

# 6. 结果

论文报告：（[Hugging Face][1]）

训练速度提升：

```
BERT-large:
+15%

GPT-2 序列长度 1K:
约 3 倍提升

Long Range Arena:
约 2.4 倍提升
```

它还支持更长的上下文：

```
16K tokens
64K tokens
```

---

# 7. 为何它改变了LLM工程

FlashAttention 之前：

```
长上下文 = 不可能

原因：

内存 ∝ 序列长度²
```

之后：

```
长上下文变得可行
```

现代模型使用变体：

* FlashAttention-1（本论文）
* FlashAttention-2
* FlashAttention-3

用于：

* GPT风格模型
* LLaMA
* Qwen
* DeepSeek
* Mistral
* 扩散Transformer

---

# 8. 代码直觉

无 FlashAttention：

```python
def attention(Q,K,V):
    scores = Q @ K.transpose(-2,-1)
    probs = softmax(scores)
    return probs @ V
```

内存：

```
O(N²)
```

---

有 FlashAttention：

```python
def flash_attention(Q,K,V):
    for q_block in Q:
        for k_block,v_block in KV:
            update_online_softmax(q_block,k_block,v_block)

    return output
```

内存：

```
O(N)
```

---

# 9. 为何这对你的GPU实验很重要

对于你的 RTX 4070 / Qwen / nanoGPT 训练：

无 FlashAttention：

```
长上下文
+
大批量
=
OOM
```

有 FlashAttention：

```
相同 GPU

能训练：
- 更长的序列长度
- 更大的批量
- 更大的模型
```

瓶颈从：

```
VRAM 容量
```

转向：

```
GPU 计算
```

这就是为什么 FlashAttention 被视为基础性的LLM基础设施突破，其重要性堪比：

* CUDA 内核
* cuBLAS
* NCCL
* 融合优化器

参考文献：

* FlashAttention 论文：（[Hugging Face][1]）
* DBLP 条目：（[DBLP][3]）
* 论文摘要和概述：（[SciSpace][2]）

[1]: https://huggingface.co/papers/2205.14135?utm_source=chatgpt.com "Paper page - FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
[2]: https://scispace.com/papers/flashattention-fast-and-memory-efficient-exact-attention-1cickunc?utm_source=chatgpt.com "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness (2022) | Tri Dao | 1035 Citations"
[3]: https://dblp.org/rec/journals/corr/abs-2205-14135.html?utm_source=chatgpt.com "dblp: FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness."