---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PaLM并行Transformer架构指南
translated: true
type: note
---

问题：关于 **PaLM：使用 Pathways 扩展语言建模** 的介绍——尤其是 **并行注意力 + FFN** 架构。

答案：

PaLM：使用 Pathways 扩展语言建模 是 Google 的一篇论文，提出了一种 **540B 参数的语言模型**，并证明了通过更好的架构和训练方法扩展 Transformer 模型可以显著提升推理、编码、多语言理解和少样本学习能力。

论文链接：
[https://arxiv.org/abs/2204.02311](https://arxiv.org/abs/2204.02311)

你提到的有趣部分是其 **并行注意力 + 前馈网络（FFN）** 的设计。

## 1. 标准 Transformer 块

经典的 GPT 风格 Transformer 使用：

```
x
|
|---- LayerNorm
|
Attention
|
Add residual
|
LayerNorm
|
FFN
|
Add residual
|
y
```

数学上表示为：

注意力：

\[
h_1 = x + Attention(LN(x))
\]

FFN：

\[
h_2 = h_1 + FFN(LN(h_1))
\]

两个子层是 **顺序执行** 的。

FFN 必须等到注意力计算完成后才能开始。

---

## 2. PaLM 并行 Transformer 块

PaLM 改变了这一点：

不再是：

```
x
 |
 Attention
 |
 FFN
 |
 y
```

而是：

```
             Attention
                |
x ------------ + ------------ y
                |
              FFN
```

两个分支接收相同的输入：

\[
y = x + Attention(LN(x)) + FFN(LN(x))
\]

因此：

```
输入 x

       +----------------+
       |                |
       v                v

 Multi-head        Feed Forward
 Attention           Network

       |                |
       +-------+--------+
               |
               v

          残差输出
```

---

## 3. 为什么这有帮助？

### 原因 1：更好的硬件利用率

大型模型的大量计算消耗在：

* 矩阵乘法
* 内存移动
* GPU 之间的通信

顺序执行：

```
Attention
(等待)
FFN
(等待)
```

并行执行：

```
Attention
   \
    +---- 合并
   /
FFN
```

GPU 可以执行更多独立的操作。

对于 TPU Pod 来说，这一点很重要。

---

## 4. 数学视角

普通 Transformer：

\[
x_{l+1}=x_l+FFN(LN(x_l+Attention(LN(x_l))))
\]

PaLM：

\[
x_{l+1}=x_l+Attention(LN(x_l))+FFN(LN(x_l))
\]

梯度路径变得更短。

不再是：

```
x
 |
attention
 |
FFN
 |
output
```

而是：

```
x
 |\
 | \
A  F
|   |
+---+
 |
output
```

这可以在极大规模下改善优化。

---

## 5. PaLM 相关的架构变化

PaLM 不仅仅是并行注意力。

主要变化：

### SwiGLU 激活函数

不再使用：

\[
FFN(x)=W_2 ReLU(W_1x)
\]

PaLM 使用：

\[
FFN(x)=W_2(SiLU(W_1x)\odot W_3x)
\]

同一系列也用于：

* LLaMA
* Qwen
* Mistral

---

### 多头查询注意力（MQA）

普通注意力：

```
head1: Q K V
head2: Q K V
head3: Q K V
...
```

MQA：

```
head1: Q
head2: Q
head3: Q

       共享的 K,V
```

好处：

* 更小的 KV 缓存
* 更快的推理速度

对服务大型模型很重要。

---

### Pathways 系统

这个名称来自 Google 的分布式 AI 基础设施。

目标：

一个模型可以跨以下资源运行：

* TPU Pod
* 多个任务
* 多种模态

而不是训练独立的系统。

概念上：

```
多个 TPU 设备

       |
       v

Pathways 运行时

       |
       +---- 语言
       |
       +---- 视觉
       |
       +---- 机器人
```

---

## 6. 为什么 PaLM 很重要

在 PaLM 之前：

```
GPT-3:
175B 参数
```

PaLM：

```
540B 参数
```

扩展趋势：

```
模型大小 ↑
数据 ↑
计算 ↑

↓

更好的推理能力
```

PaLM 展示了：

* 思维链（chain-of-thought）涌现
* 代码生成改进
* 多语言能力
* 算术推理

它影响了后来的模型：

```
PaLM
 |
 +--> PaLM 2
 |
 +--> Gemini
 |
 +--> 许多现代解码器 LLM 设计
```

---

## 7. 最小 PyTorch 实现

一个 PaLM 风格的块：

```python
class PaLMBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()

        self.norm = nn.LayerNorm(dim)

        self.attn = Attention(dim)

        self.ffn = SwiGLU(dim)

    def forward(self, x):

        h = self.norm(x)

        attn_out = self.attn(h)

        ffn_out = self.ffn(h)

        return x + attn_out + ffn_out
```

与 GPT 对比：

```python
x = x + attention(norm(x))
x = x + ffn(norm(x))
```

PaLM：

```python
h = norm(x)

x = x + attention(h) + ffn(h)
```

---

对于训练 nanoGPT 风格模型的人来说：PaLM 块只是很小的代码改动，但在从 **数亿参数扩展到数千亿参数** 时变得非常重要，因为瓶颈从纯粹的 FLOPs 转变为 **并行性、内存带宽和优化稳定性**。
