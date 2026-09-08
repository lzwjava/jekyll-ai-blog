---
audio: false
generated: true
image: false
lang: zh
layout: post
title: KDA：通道级线性注意力
translated: true
type: note
---

**问题：** 什么是 LLM 中的 KDA（Kimi Delta Attention）？

**回答：**

**KDA = Kimi Delta Attention** — 一种**线性注意力**机制，由 Kimi 团队引入，作为其 *Kimi Linear* 模型系列（以及后来的 Kimi K3）的核心。它是为长上下文效率而设计的 *Gated DeltaNet* 的改进版本。

---

### 它解决的问题

传统的线性注意力机制维护一个矩阵值的内存状态，但存在内存无限增长和无法擦除旧信息的问题。

标准 softmax 注意力在序列长度上是二次复杂度 O(n²)。KDA 是一种线性注意力机制，它保持一个固定大小的循环状态，而不是不断增长的 KV 缓存，使得 100 万 token 上下文变得可行。

---

### 核心公式

KDA 将 Gated DeltaNet 的标量 α_t 替换为一个**逐通道衰减向量** α_t ∈ ℝ^{d_k}：

$$S_t = (I - \beta_t k_t k_t^{\top}) \operatorname{Diag}(\alpha_t) S_{t-1} + \beta_t k_t v_t^{\top}$$

其中 Diag(α_t) ∈ ℝ^{d_k × d_k} 是对角矩阵，其对角线上的元素为 α_t。

---

### 三个关键组件

| 组件 | 作用 |
| --- | --- |
| `Diag(α_t)` | 逐通道遗忘——每个特征维度以自身速率遗忘 |
| `(I - β_t k_t k_tᵀ)` | Delta 规则——在当前键位置定向覆盖旧记忆 |
| `β_t` | 标量写入门——控制新值写入的程度 |

由于权重矩阵 W 将变换后的键特征映射到值，对角衰减矩阵在 W 的右侧相乘，并沿键特征维度作用。这使得某些特征维度得以保留，而其他维度被更积极地遗忘。如果向量门退化为标量，则更新将简化为 Gated DeltaNet 使用的标量遗忘形式。

---

### 与你的代码片段的关联

你发布的 CUDA 内核融合了恰好实现 α_t 和 β_t 的门计算：

```python
# g[t,h,j] = lower_bound * sigmoid(decay[h] * (raw[t, h*K+j] + dt_bias[h*K+j]))
# 这是 α_t —— 逐通道衰减（每个键维度 j 对应一个值）

# beta[t,h] = sigmoid(b_raw[t,h])
# 这是 β_t —— 标量写入/擦除门（每个注意力头对应一个值）
```

- **`decay[h]`** 是每个注意力头的指数衰减（`exp(A_log)`），即全局遗忘率。
- **`dt_bias[h*K+j]`** 在应用 sigmoid 之前按通道移动原始输入——这使 α 成为**逐通道**的。
- **`lower_bound`** 防止 α 衰减到零（灾难性遗忘）。
- 该内核将约 7 个独立的浮点操作（类型转换 → 偏置 → sigmoid → 乘法）融合为一个元素级 CUDA 内核，以提高效率。

---

### 架构使用

Kimi Linear 采用 3:1 的比例——每三个使用 KDA 线性注意力的 Transformer 块，就有一个使用完整注意力。Kimi Linear 还使用多头潜在注意力（MLA）替换标准完整注意力模块，并在 MLA 层中应用 NoPE（无位置嵌入），使得 MLA 在推理时作为纯多头查询注意力运行。

---

### KDA 与 Gated DeltaNet 对比

| | Gated DeltaNet | KDA |
| --- | --- | --- |
| 遗忘门 | 标量 α（所有通道相同） | 向量 α（每个键通道一个） |
| 写入门 | 标量 β | 标量 β |
| 内存控制 | 粗粒度（整个注意力头） | 细粒度（每个特征维度） |

Gated DeltaNet-2（后续版本）进一步推广了 KDA，将擦除门和写入门分离，而 KDA 仍将它们绑定为单个标量 β_t。

---

**参考文献：**

- [Kimi Linear 解释（Medium）](https://medium.com/@cenghanbayram35/kimi-linear-a-revolutionary-attention-mechanism-for-ai-models-03f4de12047c)
- [KDA 主题概述（EmergentMind）](https://www.emergentmind.com/topics/kimi-delta-attention-kda)
- [线性注意力架构论文](https://arxiv.org/pdf/2607.07953)
- [vLLM Kimi K3 支持博客](https://vllm.ai/blog/2026-07-27-k3)
- [你也可以想出 KDA（Doubleword）](https://blog.doubleword.ai/you-could-have-come-up-with-kimi-delta-attention)
