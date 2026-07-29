---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Kimi-K3开源前沿模型
translated: true
type: note
---

问题：Hugging Face 上的 `moonshotai/Kimi-K3` 是什么？

回答：

Moonshot AI 的 **Kimi-K3** 是他们在 Hugging Face 上发布的最新 **开放权重前沿大语言模型**。它本质上是 Moonshot 对标 GPT-5 级系统和 Claude 级模型的产物，但权重可下载。([Hugging Face][1])

重要的不是“2.8万亿参数”这个数字——架构才是其亮点所在。([Hugging Face][1])

## 1. 架构

```
Kimi K3

总参数 2.8T
        |
        v
混合专家（MoE）
        |
        +-- 896 个专家
        |
        +-- 每个 token 仅激活 16 个专家
        |
        v
每个 token 约 104B 活跃参数
```

所以它并非一个稠密的 2.8T 模型。

稠密模型：

```
token
 |
全部 2.8T 参数运行
 |
巨大算力
```

K3：

```
token
 |
路由器
 |
选择 16 / 896 个专家
 |
仅约 104B 参数执行
```

这与 Mixtral、DeepSeek MoE 等模型使用的扩展思路相同。([Hugging Face][1])

---

## 2. 关键规格

来自模型卡片：([Hugging Face][1])

| 项目          | Kimi K3                          |
| ------------- | -------------------------------- |
| 架构          | MoE                              |
| 总参数        | 2.8T                             |
| 活跃参数      | 104B                             |
| 专家数        | 896                              |
| 每 token 专家 | 16                               |
| 上下文长度    | 1,048,576 tokens                 |
| 视觉能力      | 是                               |
| 层数          | 93                               |
| 注意力机制    | Kimi Delta Attention + Gated MLA |
| 权重格式      | MXFP4                            |
| 词表大小      | 160K                             |

---

## 3. 为什么 Kimi Delta Attention（KDA）重要

标准 Transformer 注意力：

[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt d})V
]

其：

```
序列长度 N

内存：
O(N²)
```

对于百万 token 的上下文：

```
1,000,000 tokens

注意力矩阵：
1e12 个条目
```

不可能实现。

Kimi 引入了 **Kimi Delta Attention**，旨在通过压缩注意力状态来降低长上下文处理的成本。([Hugging Face][1])

概念上：

传统方式：

```
token1 token2 token3 ... token1000000

每个 token 关注所有 token
```

KDA：

```
token 流
    |
压缩后的记忆状态
    |
检索相关历史
```

与以下方向类似：

* 循环记忆
* 线性注意力
* 状态空间模型（Mamba 风格）

但集成在 Transformer 架构中。

---

## 4. 为什么人们感到兴奋

重大转变：

过去：

```
前沿模型
=
OpenAI / Anthropic / Google
=
封闭权重
```

现在：

```
前沿级能力
+
可下载权重
+
自托管
```

K3 加入了这一趋势：

* DeepSeek R1
* Qwen 系列
* Llama 系列
* Kimi K3

研究人员可以检查、修改、量化和本地部署。([GitHub][2])

---

## 5. 你的 RTX 4070 能运行它吗？

简短回答：**不能，通常不行。**

你的 RTX 4070：

```
显存：12GB
```

K3 检查点：

```
~1.5TB+
```

完整模型被分割成多个 safetensor 分片。([Hugging Face][3])

但由于它是 MoE，巧妙的系统可以部分加载专家：

```
CPU 内存
 |
模型权重
 |
GPU
 |
活跃专家
```

可能的实验：

* CPU 卸载
* 量化 MXFP4
* 分布式推理
* 专家流式加载

社区实验已经展示了不寻常的低 GPU 部署，因为只有选定的专家处于活跃状态。([Reddit][4])

对于实用的本地推理：

```
RTX 4070 12GB
    |
    +-- Qwen3-8B
    +-- Qwen3-14B 量化版
    +-- Llama 70B 通过 CPU 卸载（慢）

Kimi K3
    |
    +-- 服务器集群
    +-- 多 GPU
```

---

## 6. 这对 AI 工程师为什么重要

对于正在学习 vLLM / 推理栈的人来说，K3 实际上是一个非常好的架构研究案例。

你可以学习：

### MoE 路由

```
隐藏状态
      |
      v
路由器()
      |
      +--> 专家 13
      +--> 专家 201
      +--> 专家 777
```

### 专家并行

```
GPU0:
 专家 0-100

GPU1:
 专家 101-200

GPU2:
 专家 201-300
```

### KV 缓存压力

1M 上下文使得：

```
KV 缓存
+
注意力内存
+
分页
```

成为主要瓶颈。

这正是 vLLM 正在解决的问题。

---

我的看法：Kimi K3 之所以有趣，并非因为“2.8T”，而是因为它是一个 **MoE + 长上下文 + 面向智能体的架构**。它代表了未来前沿模型可能的样子：

```
巨大的稀疏模型
+
廉价的活跃计算
+
持久化记忆
+
工具智能体
+
本地/私有部署
```

这与你正在学习的推理工程工作非常契合。

参考：

* [Kimi-K3 Hugging Face 模型卡片](https://huggingface.co/moonshotai/Kimi-K3/blob/main/README.md?utm_source=chatgpt.com)
* [MoonshotAI Kimi-K3 GitHub](https://github.com/MoonshotAI/Kimi-K3?utm_source=chatgpt.com)
* [Kimi K3 技术报告（arXiv）](https://arxiv.org/abs/2607.24653?utm_source=chatgpt.com)

[1]: https://huggingface.co/moonshotai/Kimi-K3/blob/main/README.md?utm_source=chatgpt.com "README.md · moonshotai/Kimi-K3 at main"
[2]: https://github.com/MoonshotAI/Kimi-K3?utm_source=chatgpt.com "GitHub - MoonshotAI/Kimi-K3: Open Frontier Intelligence · GitHub"
[3]: https://huggingface.co/moonshotai/Kimi-K3/blob/main/model-00022-of-000096.safetensors?utm_source=chatgpt.com "model-00022-of-000096.safetensors · moonshotai/Kimi-K3 at main"
[4]: https://www.reddit.com/r/LocalLLM/comments/1v8sy23/ran_moonshots_28tparameter_kimi_k3_on_a_gpuless/?utm_source=chatgpt.com "Ran Moonshot's 2.8T-parameter Kimi K3 on a GPU-less mini-PC, one day after release"