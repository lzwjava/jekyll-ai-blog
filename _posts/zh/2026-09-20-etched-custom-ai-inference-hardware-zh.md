---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Etched：定制AI推理硬件
translated: true
type: note
---

问题：**Etched是做什么的？**

答案：**Etched正在构建定制的AI推理硬件——本质上就是用于提供大型AI模型服务的NVIDIA GPU的替代品。**

有趣的是，他们是在**ASIC + 机架 + 内存 + 软件**层面来解决这个问题，而不是制造另一个可编程GPU。

### 最初的构想：硬编码Transformer

Etched从**Sohu**开始，这是一款专用于Transformer推理的ASIC。

而不是：

```text
GPU
 ├── CUDA
 ├── Tensor核
 ├── 大量通用计算机制
 └── 可以运行多种类型的工作负载
```

他们的理念是：

```text
                 Transformer推理
                         │
                         ▼
              ┌───────────────────┐
              │   Etched ASIC      │
              │  专用硬件          │
              └───────────────────┘
                         │
                         ▼
                 令牌/秒
```

本质上这个赌注是：

> Transformer已经重要到我们应该**放弃可编程性**，专门为它们执行的计算来制造硅片。

这就是为什么最初的Sohu刻意无法运行CNN、LSTM等模型。Etched声称一台8芯片Sohu服务器可以在Llama 70B上达到**每秒50万+令牌**，并且相对H100/B200级别的GPU服务器有着巨大的性能优势声明。这些是公司自己的基准测试，不应被视为独立验证的数据。（[TechCrunch][1]）

### 但2026年的Etched视野更广

如果你只看到过旧的Sohu故事，这是一个重要的更新。

他们目前网站不再把公司定位为仅仅是“一家Transformer ASIC公司”，而是将产品称为：

> **前沿推理集群**

他们正在共同设计：

```text
                ┌──────────────────────────┐
                │      Etched机架          │
                │                          │
模型 ────────► │  ASIC                    │
                │  SRAM + HBM              │
                │  互连                     │
                │  编译器/运行时            │
                │  电源传输                 │
                │  散热                     │
                │  封装                     │
                └──────────────────────────┘
                           │
                           ▼
                    推理令牌
```

Etched表示，其A0芯片已从台积电N4P工艺回片，并且正在与客户验证其首个机架级产品。（[Etched][2]）

他们目前宣传的两个特别有趣的架构理念是：

**1. 低电压推理（LVI）**

他们声称其数学单元的工作电压低于典型AI芯片的一半，从而在热节流之前实现更高的计算密度。（[Etched][2]）

**2. 集群规模内存（CSM）**

对于推理来说，这可能更有意思。

解码通常是**内存/延迟受限**，而不仅仅是FLOP受限：

```text
解码：

KV缓存 ──► 内存 ──► 权重 ──► 矩阵乘 ──► 令牌
                 ▲
                 │
         带宽 / 延迟
```

Etched正在构建一个结合了**HBM + SRAM + 定制低延迟互连**的共享内存系统，试图在不放弃HBM级容量的情况下，获得更接近SRAM的访问延迟。（[Etched][2]）

### 那么实际业务是什么？

可以这样看待这个技术栈：

| NVIDIA     | Etched                         |
| ---------- | ------------------------------ |
| GPU        | 专用ASIC                       |
| CUDA       | 专用推理软件                   |
| HGX/DGX    | 定制推理机架                   |
| HBM        | HBM + SRAM架构                 |
| NVLink     | 定制互连                       |
| GPU服务器  | 整个推理集群                   |

所以他们并不是真的在卖“一个更快的芯片”。

他们试图销售的是**前沿模型推理的每令牌成本、每秒令牌数、延迟和每令牌功耗**。

这是一个有趣得多的定位。

这也是为什么这家公司现在谈论的是**机架级系统**，而不仅仅是Sohu。他们自己的网站表明他们瞄准的是万亿参数稀疏MoE、长上下文工作负载和智能体工作负载。（[Etched][2]）

对于构建推理基础设施的人来说，关键问题不是*“他们的ASIC比H100快吗？”*而是**一旦你把内存容量、利用率、批处理、KV缓存行为、网络、模型变更以及软件/编译器约束都考虑进去，他们能否在端到端的每令牌成本上击败GPU。**

[Etched官网](https://www.etched.com/?utm_source=chatgpt.com)

参考：

* [Etched — 前沿推理集群](https://www.etched.com/?utm_source=chatgpt.com)（[Etched][2]）
* [TechCrunch — Etched最初只运行Transformer模型的AI芯片](https://techcrunch.com/2024/06/25/etched-is-building-an-ai-chip-that-only-runs-transformer-models/?utm_source=chatgpt.com)
* [Etched最初的Sohu发布报道](https://threadreaderapp.com/thread/1805625693113663834.html?utm_source=chatgpt.com)

我还可以详细解析**Sohu如何理论上实现比H100高10–20倍的吞吐量**，从Transformer前向传播开始，将每个操作映射到ASIC硬件上。

[1]: https://techcrunch.com/2024/06/25/etched-is-building-an-ai-chip-that-only-runs-transformer-models/?utm_source=chatgpt.com "Etched正在构建一款只运行一种模型的AI芯片 | TechCrunch"
[2]: https://www.etched.com/ "Etched"