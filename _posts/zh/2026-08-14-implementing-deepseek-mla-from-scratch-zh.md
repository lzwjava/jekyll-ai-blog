---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从零开始实现DeepSeek MLA
translated: true
type: note
---

问题：有哪些好的GitHub项目可以学习DeepSeek MLA（多头潜在注意力）？

回答：

要深入学习MLA，我会按以下顺序进行：

## 1. 最佳起点：自己实现MLA

### [LLMs-from-scratch MLA章节](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch04/05_mla/README.md?utm_source=chatgpt.com)

这可能是最好的学习资源。

原因：

* 从普通MHA开始
* 比较GQA → MLA
* 解释KV缓存缩减
* 小型的PyTorch代码

学习路径：

```
MHA
 |
 v
GQA
 |
 v
MLA
 |
 v
DeepSeek-V2/V3 优化版MLA
```

先理解这个：

普通MHA KV缓存：

```
[K,V ∈ R^{seq × n_heads × d}]
```

MLA：

```
c_{KV} = xW_{down}
```

存储：

```
c_{KV}
```

而不是：

```
K,V
```

在解码时：

```
K = c_{KV}W_k
V = c_{KV}W_v
```

所以内存变化：

```
MHA：

seq × heads × head_dim

MLA：

seq × latent_dim
```

---

## 2. 简洁的PyTorch实现

### [Multi-Head-Latent-Attention-MLA-](https://github.com/joey00072/Multi-Head-Latent-Attention-MLA-?utm_source=chatgpt.com)

仓库：

```
joey00072/Multi-Head-Latent-Attention-MLA-
```

优点：

```
mla.py
modeling_mla.py
train_mla.py
```

文件都很小。

你可以直接阅读：

```python
class MLA(nn.Module):
```

并追踪：

```
x
 |
 +--> q压缩
 |
 +--> kv压缩
 |
 潜在缓存
 |
 重构k/v
 |
 attention
```

这更接近“nanoGPT风格的学习”。

---

## 3. MiniGPT + MLA

### [MiniGPT-and-DeepSeek-MLA-Multi-Head-Latent-Attention](https://github.com/junfanz1/MiniGPT-and-DeepSeek-MLA-Multi-Head-Latent-Attention?utm_source=chatgpt.com)

适合理解集成：

```
miniGPT.py

        |
        v

Self Attention

        |
        v

GQA

        |
        v

MLA
```

包含：

```
Multi-Head Self Attention.py
Group Query Attention.py
Multi-Head Latent Attention.py
```

非常适合对比架构。

---

## 4. 真正的DeepSeek实现

### [DeepSeek-V3 GitHub MLA实现](https://github.com/deepseek-ai/DeepSeek-V3/blob/main/inference/model.py?utm_source=chatgpt.com)

最终阅读：

```
DeepSeek-V3/inference/model.py

class MLA(nn.Module)
```

这是真实代码。

关键行：

```python
self.wkv_a =
    Linear(
        self.dim,
        self.kv_lora_rank + self.qk_rope_head_dim
    )
```

核心思想：

不再是：

```
x
 |
 +--> Wk
 |
 +--> Wv
```

DeepSeek的做法：

```
x
 |
 Wkv_down
 |
 潜在c_kv
 |
 +--> Wk_up
 |
 +--> Wv_up
```

潜在向量就是KV缓存。

---

## 5. 生产级内核实现

理解数学之后：

### [FlashMLA](https://github.com/deepseek-ai/FlashMLA/blob/main/README.md?utm_source=chatgpt.com)

这不是初学用的。

它是CUDA优化：

```
PyTorch MLA
      |
      v
FlashMLA kernel
      |
      v
H100/B200 优化推理
```

你会看到：

* 内存布局
* 融合内核
* FP8 KV缓存
* 解码优化

---

## 我推荐的学习路线

鉴于你已经训练过GPT-2/nanoGPT，我会建议：

### 第一天

阅读：

```
LLMs-from-scratch MLA
```

实现：

```python
class MLA(nn.Module):
    def forward(self,x):
        c = self.kv_down(x)

        k = self.k_up(c)
        v = self.v_up(c)

        attn = q @ k.transpose(-2,-1)

        return attn @ v
```

---

### 第二天

修改nanoGPT：

替换：

```python
self.key = nn.Linear(n_embd,n_embd)
self.value = nn.Linear(n_embd,n_embd)
```

为：

```python
self.kv_down = nn.Linear(
    n_embd,
    kv_rank
)

self.k_up = nn.Linear(
    kv_rank,
    n_embd
)

self.v_up = nn.Linear(
    kv_rank,
    n_embd
)
```

在TinyStories上训练。

对比：

```
MHA
vs
GQA
vs
MLA
```

测量：

* KV缓存大小
* 吞吐量
* 验证损失

---

与你之前关于Q/K/V讨论的最深层次概念联系：

MLA本质上是在说：

> 既然KV投影本身已经是一个有损的学习信息过滤器，为什么还要存储扩展后的K/V？存储扩展前的潜在压缩表示即可。

因此不再是：

```
x → K,V
```

而是存储：

```
x → z_{KV}
```

其中：

```
dim(z_{KV}) << dim(K,V)
```

然后在需要时重构注意力空间。

这就是为什么在理解Q/K/V作为学习到的低秩信息过滤之后，MLA是一个非常自然的下一步。
