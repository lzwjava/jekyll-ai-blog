---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Flash Attention 中的 KV 缓存
translated: true
type: note
---

问题：这段Flash Attention代码中的KV缓存是什么意思？

答案：

**KV缓存 = 键/值缓存。** 这是自回归大语言模型生成时的一种推理优化技术，可以避免重新计算之前标记的注意力键和值。

在Transformer注意力层中：

\[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt d})V
\]

对于提示词：

```
法国的首都是
```

模型处理以下标记：

```
T1  T2  T3  T4  T5
```

在每一层中计算：

```
K1 V1
K2 V2
K3 V3
K4 V4
K5 V5
```

生成下一个标记时：

```
法国的首都是巴黎
```

新的查询只针对：

```
T6 = "巴黎"
```

不使用KV缓存：

```
需要重新计算K、V：

T1 T2 T3 T4 T5 T6
```

使用KV缓存：

```
缓存：
K1 V1
K2 V2
K3 V3
K4 V4
K5 V5

只需计算：

K6 V6

然后注意力：

Q6 关注：

[K1 K2 K3 K4 K5 K6]
[V1 V2 V3 V4 V5 V6]
```

---

## 在你的代码中

关键函数：

```python
def flash_attn_with_kvcache(
    q,
    k_cache,
    v_cache,
    k=None,
    v=None,
    cache_seqlens=None,
    ...
):
```

是推理路径。

### 形状

```python
q:        (B, T_new, H, D)
k_cache:  (B, T_max, H_kv, D)
v_cache:  (B, T_max, H_kv, D)
```

示例：

```
B = 1              批次大小
T_max = 32768      最大上下文长度
H = 32             注意力头数
D = 128            头部维度
```

内存：

```
k_cache:

[
 token0: [head0...head31]
 token1: [head0...head31]
 token2: ...
]
```

本质上是一个存储历史数据的大张量。

---

## 这部分将新标记写入缓存

```python
if k is not None and v is not None:
    k_cache[:, pos:pos+T_new, :, :] = k
    v_cache[:, pos:pos+T_new, :, :] = v
```

示例：

之前：

```
k_cache

位置：
0  1  2  3  4  5  6  7
K  K  K  K  K  ?  ?  ?
```

生成标记5：

```
pos = 5
```

插入后：

```
0  1  2  3  4  5  6  7
K  K  K  K  K  K5 ?  ?
```

---

## 然后注意力使用全部历史数据

```python
k_full = k_cache[:, :end_pos, :, :]
v_full = v_cache[:, :end_pos, :, :]
```

所以：

```
k_full:

K0 K1 K2 K3 K4 K5
```

然后：

```python
Attention(
    Q5,
    K0..K5,
    V0..V5
)
```

模型可以"记住"之前的标记。

---

## 为什么训练不需要KV缓存

你的注释：

```python
# Training (no KV cache)
y = flash_attn.flash_attn_func(...)
```

训练期间：

输入：

```
hello world this is GPT
```

你一次性处理所有标记：

```
Q:
q1 q2 q3 q4 q5

K:
k1 k2 k3 k4 k5

V:
v1 v2 v3 v4 v5
```

Flash Attention高效计算整个矩阵：

```
       k1 k2 k3 k4 k5

q1     x
q2     x  x
q3     x  x  x
q4     x  x  x  x
q5     x  x  x  x  x
```

因为因果掩码防止向前看。

无需存储KV。

---

## 为什么KV缓存对长上下文智能体很重要

对于像这样的智能体：

* Claude Code
* OpenClaw
* Hermes
* 长上下文Qwen
* GPT风格的聊天

生成通常是：

```
提示词：
5万标记

输出：
2千标记
```

不使用KV缓存：

每个输出标记：

```
重新计算5万标记
```

成本：

```
5万 + 5万 + 5万 + ...
```

使用KV缓存：

```
初始提示词：
计算一次K/V

然后：

标记1 -> 仅新K/V
标记2 -> 仅新K/V
标记3 -> 仅新K/V
```

成本大约变为：

```
5万 + 2千
```

而不是：

```
5万 * 2千
```

---

## 权衡

KV缓存加速推理但消耗显存。

内存：

\[
KV\ 内存 =
2 \times 层数 \times 序列长度 \times 头数 \times 头部维度 \times 字节数
\]

示例：

Llama 70B：

```
80层
64个KV头
128维
12.8万上下文
bf16
```

KV缓存可能达到：

```
数百GB
```

这就是为什么较新的模型使用：

* GQA（分组查询注意力）
* MQA（多查询注意力）
* KV量化
* 分页注意力（vLLM）

以减少KV内存。

---

## 与你RTX 4070 / 本地推理的关系

你的RTX 4070：

```
12GB显存
```

长上下文的限制因素通常不是模型权重，而是KV缓存。

示例：

Qwen 32B：

```
权重：
~64GB bf16
```

本地无法运行。

但即使是较小的模型：

```
Qwen3 8B
12.8万上下文
```

可能达到：

```
KV缓存 > 几GB
```

在权重成为问题之前。

这就是为什么像这样的推理引擎：

* vLLM
* llama.cpp
* TensorRT-LLM

拥有复杂的KV缓存管理。

在你的代码中，`flash_attn_with_kvcache()` 本质上就是这些引擎所依赖的底层原语。
