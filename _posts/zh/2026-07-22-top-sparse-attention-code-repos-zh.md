---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 顶级稀疏注意力代码仓库
translated: true
type: note
---

问题：有哪些开源代码可以帮助我们理解稀疏注意力？

答案：

如果你的目标是**理解稀疏注意力实际是如何工作的**，我建议按以下顺序阅读实现代码——从最简单到生产级别。

| 项目                          | 最适合用于                         | 难度     |
| ----------------------------- | ---------------------------------- | -------- |
| lucidrains/sparse-attention   | 学习算法                           | ⭐        |
| OpenAI Sparse Transformers    | 原始实现                           | ⭐⭐       |
| Hugging Face Longformer       | 滑动窗口注意力                     | ⭐⭐       |
| Google BigBird                | 随机 + 全局注意力                  | ⭐⭐⭐      |
| Google Reformer               | LSH 注意力                         | ⭐⭐⭐      |
| Dao-AILab FlashAttention      | 高效内核（主要是密集注意力）       | ⭐⭐⭐⭐     |
| vLLM                          | 生产环境服务                       | ⭐⭐⭐⭐     |

---

## 1. lucidrains/sparse-attention ⭐（最好的起点）

官方仓库：

[lucidrains/sparse-attention](https://github.com/lucidrains/sparse-attention?utm_source=chatgpt.com)

这可能是最容易理解的代码库。

典型实现：

```python
class SparseAttention(nn.Module):
    def forward(self, x):

        q = self.to_q(x)
        k = self.to_k(x)
        v = self.to_v(x)

        # local attention
        local = local_attention(q, k, v)

        # strided attention
        global = strided_attention(q, k, v)

        return local + global
```

几乎没有 CUDA 代码。
大部分是 PyTorch。

非常适合学习算法。

---

## 2. OpenAI Sparse Transformers ⭐⭐

论文：

> Generating Long Sequences with Sparse Transformers

仓库：

[OpenAI sparse_attention](https://github.com/openai/sparse_attention?utm_source=chatgpt.com)

这是论文的原始实现。

包含：

```
blocksparse/
attention.py
ops.py
```

你会看到诸如

```
block sparse matrix
block layout
block masks
```

之类的概念，而不是 token 级别的稀疏性。

该项目启发了许多后来的稀疏实现。

---

## 3. Longformer ⭐⭐

仓库：

[Longformer](https://github.com/allenai/longformer?utm_source=chatgpt.com)

滑动窗口注意力。

不再是

```
N × N
```

而是只计算

```
N × window
```

可视化：

```
█████
 █████
  █████
   █████
```

只有附近的 token 参与注意力计算。

核心代码：

```
longformer/sliding_chunks.py
```

是有史以来写的最清晰的稀疏实现之一。

---

## 4. BigBird ⭐⭐⭐

仓库：

[BigBird](https://github.com/google-research/bigbird?utm_source=chatgpt.com)

BigBird 混合了三种模式：

```
local

□□□□■■■■□□□□

global

■□□□□□□□□□□■

random

□■□□□■□□□□□
```

总注意力：

```
local
+ global
+ random
```

阅读这段代码有助于理解为什么稀疏注意力能够在降低复杂度的同时保持表达能力。

---

## 5. Reformer ⭐⭐⭐

仓库：

[Reformer](https://github.com/google/trax/tree/master/trax/models/reformer?utm_source=chatgpt.com)

它不是选择邻居，

而是对查询进行哈希：

```
Q

↓

LSH

↓

bucket

↓

attention inside bucket
```

复杂度：

```
O(N log N)
```

而不是

```
O(N²)
```

如果你正在研究替代固定模式的稀疏机制，这会很有趣。

---

## 6. FlashAttention ⭐⭐⭐⭐

仓库：

[FlashAttention](https://github.com/Dao-AILab/flash-attention?utm_source=chatgpt.com)

严格来说，

FlashAttention **并不是稀疏注意力**。

它计算完整的注意力矩阵，但避免在 HBM 中将其具体化，而是使用分块计算。

不过，如果你以后有兴趣实现高效的稀疏内核，它的内核组织方式至关重要。

查看

```
flash_attn/
hopper/
csrc/
```

---

## 7. xFormers

仓库：

[xFormers](https://github.com/facebookresearch/xformers?utm_source=chatgpt.com)

包含多种注意力算子：

```
Dense

Block Sparse

Memory Efficient

Local

Causal

Flash
```

对于在统一接口下比较各种实现很有用。

---

## 8. vLLM

仓库：

[vLLM](https://github.com/vllm-project/vllm?utm_source=chatgpt.com)

现代推理引擎。

感兴趣的文件：

```
attention/
paged_attention/
flash_attn/
```

尽管当前大多数模型使用密集注意力，但 vLLM 展示了生产系统如何组织注意力内核、KV 缓存管理和调度。

---

# 如果你自己想实现一个

一个最小的稀疏注意力实现出奇地简短。

```python
scores = q @ k.transpose(-2, -1)

scores.masked_fill_(~mask, float("-inf"))

attn = scores.softmax(-1)

out = attn @ v
```

与密集注意力唯一的区别在于 `mask` 的构建方式。

例如，一个滑动窗口掩码：

```python
mask = torch.zeros(n, n, dtype=torch.bool)

for i in range(n):
    left = max(0, i - w)
    right = min(n, i + w + 1)
    mask[i, left:right] = True
```

其他一切——softmax 和值聚合——保持不变。优化的实现通过只计算非零块或邻域来避免创建完整的 `N × N` 掩码。

## 我推荐的阅读顺序

1. **lucidrains/sparse-attention** —— 用纯 PyTorch 理解算法。
2. **Longformer** —— 学习滑动窗口注意力。
3. **OpenAI Sparse Transformers** —— 研究块稀疏布局。
4. **BigBird** —— 理解混合稀疏模式（局部 + 全局 + 随机）。
5. **FlashAttention** —— 学习高性能注意力内核。
6. **vLLM** —— 看看高效注意力如何集成到生产推理引擎中。

这个顺序从概念简单性逐步过渡到越来越真实的系统，同时保持实现复杂度的可控性。