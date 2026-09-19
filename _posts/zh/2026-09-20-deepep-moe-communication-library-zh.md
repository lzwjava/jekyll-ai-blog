---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepEP：MoE通信库
translated: true
type: note
---

问题：**DeepEP 在 LLM 中是什么意思？**

答案：

**DeepEP = DeepEveryParallel**。它是来自 DeepSeek 的高性能 **专家并行（EP）通信库**，主要用于分布式 MoE LLM，例如 DeepSeek-V3/R1。([GitHub][1])

关键在于：**DeepEP 不是 MoE 模型架构，而是使分布式 MoE 变得实用的通信层。**

### 它所解决的问题

假设你有一个 MoE 层：

```text
                    路由器
                      │
tokens ──────────────┼──────────────
       │             │
       ▼             ▼
    专家 3         专家 127
       │             │
       └──────┬──────┘
              ▼
            合并
```

采用 **专家并行** 时，专家分布在不同的 GPU 上：

```text
GPU 0                 GPU 1                 GPU 2
┌─────────┐            ┌─────────┐            ┌─────────┐
│ E0 E1   │            │ E2 E3   │            │ E4 E5   │
└─────────┘            └─────────┘            └─────────┘
     ▲                      ▲                      ▲
     └──────────── all-to-all 通信 ──────────────┘
```

GPU 0 上的 token 可能被路由到 GPU 2 上的专家 5。

因此每个 MoE 层大致有以下过程：

```text
GPU 本地 tokens
      │
      ▼
   路由器
      │
      ▼
┌──────────────┐
│   分发       │  ← 将 tokens 发送到包含专家的 GPU
└──────────────┘
      │
      ▼
 专家 GEMM
      │
      ▼
┌──────────────┐
│   合并       │  ← 将结果发送回来
└──────────────┘
      │
      ▼
下一层
```

这个 **分发/合并** 本质上就是一个 all-to-all 通信问题。

DeepEP 为此提供了高度优化的 GPU 内核。([GitHub][2])

### 为什么普通的 NCCL 不够用

概念上，你可以这样实现：

```python
dist.all_to_all(...)
```

但大规模 MoE 有苛刻的要求：

* token 级路由
* 高度不规则的消息大小
* 节点内的 NVLink
* 跨节点的 RDMA
* FP8 token 分发
* 解码期间非常小的消息
* 通信与计算的重叠
* 避免在延迟敏感的通信期间消耗 SM

DeepEP 正是围绕这些约束设计的。

例如，它的通信路径可以是这样的：

```text
              节点 0                        节点 1
       ┌──────────────────┐          ┌──────────────────┐
       │ GPU0 GPU1 GPU2   │          │ GPU4 GPU5 GPU6   │
       └─┬────┬────┬──────┘          └─┬────┬────┬──────┘
         │    │    │                    │    │    │
         └────┴────┴── NVLink ──────────┘    │    │
                         │                   │
                         └──── RDMA ─────────┘
```

DeepEP 专门提供了高吞吐量的 NVLink/RDMA all-to-all 内核以及低延迟的 RDMA 路径。([GitHub][1])

### 为什么 DeepSeek-V3 如此重视

DeepSeek-V3 使用 **大规模 EP**。例如，DeepSeek 自己的性能分析数据中，训练使用 EP64，prefill 使用 EP32；解码可以使用 EP128。([GitHub][3])

在这种规模下，MoE 计算本身不一定是瓶颈：

```text
MoE 层时间

        ┌──────────────────────┐
计算    │     专家 GEMM       │
        └──────────────────────┘

        ┌──────────────────────┐
网络    │ 分发 + 合并         │  ← 可能非常巨大
        └──────────────────────┘
```

因此优化 **通信** 可能与优化 GEMM 同等重要。

这也是为什么 DeepSeek 开源堆栈包含几个互补组件：

```text
DeepSeek-V3/R1
      │
      ├── DeepGEMM   → FP8 GEMM
      │
      ├── DeepEP     → MoE 专家通信
      │
      └── FlashMLA   → MLA 注意力内核
```

DeepSeek 将 DeepEP 描述为其用于 MoE 训练和推理的开源 EP 通信库。([GitHub][4])

### 一个有用的思维模型

如果你正在实现一个 MoE 推理引擎，可以这样考虑：

```text
                 MoE 层
                    │
          ┌─────────┴─────────┐
          │                   │
       计算                通信
          │                   │
      DeepGEMM             DeepEP
          │                   │
     专家 GEMM          分发/合并
```

因此：

> **DeepEP 本质上就是分布式 MoE 底下的高性能“token 路由网络”。**

而真正有趣的部分不是 Python API——而是 **GPU 发起的 RDMA + NVLink 通信设计，以及它如何与专家计算重叠**。这里面蕴含了大量 DeepSeek-V3 的系统工程。([GitHub][1])

[DeepEP GitHub 仓库](https://github.com/deepseek-ai/DeepEP?utm_source=chatgpt.com)

我还可以详细讲解 **DeepEP 的分发内核，从 `topk_idx → NVLink/RDMA → 专家 GEMM → 合并`**，包括实际的张量布局和通信步骤。

[1]: https://github.com/deepseek-ai/DeepEP?utm_source=chatgpt.com "GitHub - deepseek-ai/DeepEP: DeepEP：一个高效的专家并行通信库 · GitHub"
[2]: https://github.com/deepseek-ai/DeepEP/blob/main/deep_ep/buffers/legacy.py?utm_source=chatgpt.com "DeepEP/deep_ep/buffers/legacy.py at main · deepseek-ai/DeepEP · GitHub"
[3]: https://github.com/deepseek-ai/profile-data?utm_source=chatgpt.com "GitHub - deepseek-ai/profile-data: 分析 V3/R1 中的计算-通信重叠 · GitHub"
[4]: https://github.com/deepseek-ai/open-infra-index/blob/main/README.md?utm_source=chatgpt.com "open-infra-index/README.md at main · deepseek-ai/open-infra-index · GitHub"