---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Kimi K3 MoE 本地推理
translated: true
type: note
---

**问题：什么是 Kimi K3 本地 Mac 推理的故事，以及为何其架构使其成为可能？**

**回答：**

本文描述的是**在本地运行超大规模 LLM 的一个新方向**：不是缩小一个巨型模型直到它能被容纳，而是设计模型使其在推理时只需激活一小部分。

核心思想在于：

> **Kimi K3 巨大（2.8T 参数），但 MoE 架构意味着你无需为每个 token 将全部 2.8T 参数都加载到内存中。**

这与 Mixtral、DeepSeek-V3 等模型背后的基本原理相同，但被推向了更极致的程度。

---

## 1. 首先：什么是 Kimi K3？

Kimi K3（据文章所述）是：

*   约 2.8 万亿参数
*   采用 MoE（混合专家）架构
*   原生 MXFP4 训练
*   权重大小为 1.6TB
*   混合架构，包含：
    *   KDA（Kimi Delta Attention）
    *   LatentMoE
    *   NoPE（无旋转位置编码）

重要的数字不是 2.8T。

重要的数字是：

**每个 token 激活了多少参数？**

一个稠密模型：

```
GPT-4 风格：

token
 |
所有参数
 |
输出
```

如果你有：

```
2T 参数
```

你需要：

```
每个 token 激活 2T 参数
```

这在本地是不可能实现的。

---

而 MoE 则是：

```
                 Expert 1
                /
token -> router -> Expert 37
                \
                 Expert 2000
```

只有少数专家被运行。

例如：

```
总计：
2.8T 参数

激活：
~30B-100B 参数
```

其余参数可以留在磁盘上。

这就是为什么 Mac 的“魔法”能够奏效。

---

## 2. 为什么 Mac 能运行 1.6TB 的模型？

一种天真的做法：

```
加载模型

RAM：
[1.6TB weights]

计算
```

不可能。

即使是顶配的 Mac Studio：

```
512GB 统一内存
}

也无法容纳。
```

而 Deltafin 的做法更接近于：

```
               SSD / HTTP 存储
                     |
                     v

              专家权重

                     |
                     v

                RAM 缓存

                     |
                     v

              Metal GPU / NEON CPU

                     |
                     v

               下一个 token
```

只抓取所需的专家。

就像 LLM 的虚拟内存。

操作系统在 50 年前就做过类似的事情：

```
磁盘
 |
交换
 |
RAM
 |
CPU
```

现在是：

```
巨大的 LLM 存储
 |
专家分页
 |
GPU
 |
token 生成
```

---

## 3. LatentMoE 是其中有趣的部分

标准 MoE：

```
专家：

FFN：
7680 -> 30000 -> 7680
```

巨大的矩阵。

LatentMoE 压缩了专家表示。

概念上：

标准方式：

```
hidden
  |
big matrix
  |
output
```

潜在方式：

```
hidden
 |
small latent space
 |
expert computation
 |
output
```

与以下概念的哲学相似：

*   LoRA
*   潜在扩散模型 (latent diffusion)
*   低秩分解 (low-rank factorization)

模型在保持能力的同时，减少了活跃计算量。

---

## 4. MXFP4 原生训练

这实际上是一件大事。

通常做法：

训练：

```
BF16 模型

↓

量化

↓

INT4 / FP4
```

问题：

量化可能会损害质量。

Kimi K3 的做法：

```
训练本身
       |
       v
     MXFP4
       |
       v
 部署
```

模型学会了在低精度下工作。

这与 NVIDIA 的 FP8 训练哲学类似。

未来的方向：

```
旧方式：

训练大模型
然后压缩


新方式：

为部署格式进行训练
```

---

## 5. NoPE：移除 RoPE

大多数现代 Transformer：

```
token 嵌入

+

RoPE 位置编码

+

注意力机制
```

RoPE 提供了：

“token 100 与 token 500 不同”的信息

因为仅靠注意力机制本身没有明确的位置信息。

Kimi 认为：也许我们并不需要它。

为什么？

因为 KDA 类似于循环神经网络。

一个简化的视图：

传统注意力机制：

```
Q K V

比较每个 token 与所有其他 token
```

复杂度：

```
O(n²)
```

KDA：

```
state_t = update(state_t-1, token_t)

output = f(state)
```

像 RNN：

```
位置信息自然显现
```

所以：

```
移除 RoPE
+
在注意力机制前加入 KDA 层
```

模型在没有显式位置编码的情况下学习顺序。

---

## 6. 为何这对本地 AI 至关重要

历史模式：

### 旧方式

大型模型：

```
70B

↓

社区量化

↓

4-bit

↓

本地运行
```

你会损失质量。

---

Kimi K3 的方法：

```
架构

↓

已针对稀疏激活优化

↓

本地推理成为可能
```

类比一下：

旧方式：

```
将法拉利减重直到适合自行车轮胎
```

新方式：

```
设计带有可拆卸模块的法拉利
```

---

## 7. 0.3 token/秒 有用吗？

对于聊天：

没用。

人类体验：

```
问题
（等待 10 秒）
一个句子
```

很痛苦。

但对于批处理任务：

非常有趣。

例如：

评估：

```
100 万个提示

通宵运行

比较模型
```

速度不那么重要。

一个本地 K3 变成了：

```
私有的 GPT-5 级别评估器
```

且无需 API 成本。

---

## 8. 更大的图景

重要的趋势是：

### 模型架构正变得对硬件感知。

2020 年：

```
Transformer
+
GPU
```

2026 年：

```
Transformer
+
MoE
+
稀疏激活
+
低精度训练
+
内存层次结构
+
消费级硬件
```

未来的本地 AI 堆栈可能看起来像：

```
Mac Studio
     |
     |
Thunderbolt 集群
     |
     |
MoE 模型
     |
     |
本地智能体系统
```

并非每个人都需要在 RAM 中拥有一个 2.8T 的模型。

他们需要的是：

*   便宜的存储
*   足够的带宽
*   智能路由
*   稀疏激活

---

对于你的配置（RTX 4070 12GB + 本地实验），实际的教训不是“明天就运行 Kimi K3”。而是：

**MoE 改变了游戏规则。**

你的 nanoGPT 实验是稠密模型：

```
124M 参数

每个 token：
124M 激活
```

未来的本地模型：

```
总计 2.8T

可能：
50B 激活
```

研究问题从：

> “我们如何适配更大的模型？”

转变为：

> “我们如何让模型为每个 token 接触更少的自身部分？”

这正是 DeepSeek-V3、Kimi K3、Mixtral 这类模型如此重要的原因。

参考文献：

*   Sebastian Raschka, "Kimi K3 Architecture Notes" — [https://sebastianraschka.com/blog/2026/kimi-k3-architecture-notes.html](https://sebastianraschka.com/blog/2026/kimi-k3-architecture-notes.html)
*   Deltafin GitHub — [https://github.com/gavamedia/deltafin](https://github.com/gavamedia/deltafin)
*   Hacker News 讨论: Running Kimi K3 on M1 Max — [https://news.ycombinator.com/item?id=49090233](https://news.ycombinator.com/item?id=49090233)