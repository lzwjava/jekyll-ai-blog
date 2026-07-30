---
audio: false
generated: true
image: false
lang: zh
layout: post
title: vLLM中的预填充芒果类比
translated: true
type: note
---

**问题：**
“切 mango 就是 prefill（预填充）吗？token 预填充在 vLLM 里面是什么？”

**回答：**

是的。在 LLM 推理中，**prefill（预填充）** 基本上是指模型在开始生成新 token 之前，**一次性处理所有输入提示 token** 的阶段。

考虑一个 LLM 请求：

```
用户：
"详细解释 transformer 注意力机制"

Tokens：
[详细, 解释, transformer, 注意力, 机制]
```

推理分为两个阶段：

```
             提示 tokens                 输出 tokens
                  |                          |
                  v                          v

        +----------------+          +----------------+
        |    Prefill     |          |    Decode      |
        | 处理输入       |--------->| 逐 token 生成  |
        +----------------+          +----------------+
```

## 1. Prefill = 计算 prompt KV 缓存

在 prefill 阶段：

```
输入：
x1 x2 x3 x4 x5

Transformer 前向传播：

x1 -> hidden
x2 -> hidden
x3 -> hidden
x4 -> hidden
x5 -> hidden

生成：

K1 V1
K2 V2
K3 V3
K4 V4
K5 V5
```

模型存储：

```
KV 缓存：

Layer 0：
 K: [k1,k2,k3,k4,k5]
 V: [v1,v2,v3,v4,v5]

Layer 1：
 K: [...]
 V: [...]

...

Layer 32：
 K: [...]
 V: [...]
```

这就是为什么它被称为：

> 预填充注意力缓存

中文“预填充”是一个很好的翻译。

---

## 2. Decode = 生成新 tokens

Prefill 之后：

生成 token 6：

```
输入：
仅 x6

注意力：

Q6 关注：

K1 K2 K3 K4 K5

加上新的：

K6 V6
```

然后 token 7：

```
x7

关注：

K1 ... K6
```

解码是顺序进行的。

---

## 3. 为什么 prefill 很快？

因为它是一个大的矩阵运算。

例子：

提示：

```
4096 tokens
```

在 prefill 期间：

```
4096 tokens 一起

matmul：

[4096,d_model]
       *
[d_model,d_model]

GPU 喜欢这样。
```

GPU 利用率高。

---

解码：

```
1 token

[1,d_model]
      *
[d_model,d_model]
```

小矩阵。

GPU 利用率低。

这就是为什么 LLM 服务会出现：

* prefill 瓶颈 → 计算受限
* decode 瓶颈 → 内存带宽受限

---

## 4. vLLM 架构

vLLM 将这两者分开：

```
                调度器

                    |
          +---------+---------+
          |                   |
          v                   v

      Prefill 批次        Decode 批次

      提示 tokens         生成的 tokens

          |                   |
          +---------+---------+

                    |
                    v

              GPU 执行
```

例子：

请求：

```
请求 A：
提示 = 4000 tokens


请求 B：
提示 = 2000 tokens
```

vLLM 执行：

```
Prefill 批次：

A：
4000 tokens

B：
2000 tokens


总计：
6000 tokens
```

GPU 运行一次大规模前向传播。

然后：

```
Decode：

A -> 下一个 token
B -> 下一个 token
```

---

## 5. vLLM PagedAttention 的联系

KV 缓存非常大。

例子：

Llama 70B：

```
layers: 80
heads: 64
head_dim:128
tokens: 8192
```

KV 缓存：

```
2 * layers * tokens * heads * head_dim * bytes
```

大致为：

```
2*80*8192*64*128*2 bytes

≈ 21 GB
```

对于多个用户：

```
用户1：
8192 tokens

用户2：
4096 tokens

用户3：
16000 tokens
```

会发生内存碎片。

vLLM 通过以下方式解决：

```
PagedAttention

KV 缓存：

GPU 内存：

[block][block][block][block]

请求 A：
block 1
block 7
block 9

请求 B：
block 2
block 3
```

类似于操作系统的虚拟内存。

---

## 6. “切 mango” 类比

如果你指的是中文短语：

> 切 mango

想象一下吃芒果：

### Prefill：

切整个芒果：

```
🥭 -> 🔪 -> 许多块
```

你处理所有现有的 tokens。

### Decode：

一次吃一块：

```
块1
块2
块3
...
```

但芒果本身代表着上下文。

---

对于 vLLM，重要的思维模型：

```
请求到达

          提示
            |
            v
       PREFILL
       - 处理所有 tokens
       - 创建 KV 缓存
       - 计算密集

            |
            v

       DECODE 循环

       token -> token -> token

       - 重用 KV 缓存
       - 内存带宽受限
```

理解这一点是理解为什么 vLLM 具有 **连续批处理**、**PagedAttention**、**分块预填充**，以及为什么现代推理系统围绕 prefill/decode 拆分来设计的关键。