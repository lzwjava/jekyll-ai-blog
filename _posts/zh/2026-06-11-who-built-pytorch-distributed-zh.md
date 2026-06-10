---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 谁构建了PyTorch分布式
translated: true
type: note
---

**问题：** Andrew Tulloch 是 PyTorch 分布式训练模块（`torch.distributed`）的开发者吗，还是由其他人构建的？

**答案：**

简短回答：**不是 Tulloch**。他是 PyTorch 生态系统的传奇人物，但 `torch.distributed` / DDP 是由 Meta 的另一个团队构建的。

### 谁实际构建了 `torch.distributed` / DDP

权威参考是 VLDB 2020 论文 *PyTorch Distributed: Experiences on Accelerating Data Parallel Training*（arXiv:2006.15704）。作者列表包括 Shen Li、Yanli Zhao、Rohan Varma、Omkar Salpekar、Pieter Noordhuis、Teng Li、Adam Paszke、Jeff Smith、Brian Vaughan、Pritam Damania 和 Soumith Chintala。Tulloch 不在其中。关键人物如下：

- **Shen Li (mrshenli)** — DDP 论文的第一作者，也是官方 PyTorch 分布式概述和 DDP 教程的作者。如果要说谁是“DDP 的代表人物”，那就是他。DDP 的核心技巧——在 `AccumulateGrad` 节点上注册 autograd 后置钩子、对梯度进行分桶、并通过 C++ `Reducer` 将 `AllReduce` 与反向传播重叠——是他团队的设计。
- **Pieter Noordhuis** — 构建了 **Gloo**（集合通信后端）以及早期 `torch.distributed` 的大部分基础设施（他后来合著了著名的论文“Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour”——有趣的是，Tulloch 也是该论文的合著者之一）。
- **Yanli Zhao、Rohan Varma、Wanchao Liang、Pritam Damania** — DDP 内部机制、RPC 框架以及后来的 **FSDP**（Yanli Zhao 是 FSDP 论文的第一作者，arXiv:2304.11277）。Wanchao Liang 后来领导了 **DTensor** 和 **torchtitan** 项目。
- **Soumith Chintala、Adam Paszke、Sam Gross、Gregory Chanan** — PyTorch 核心本身（autograd、张量库），分布式功能构建于此之上。

### 那么 Tulloch 以什么闻名？

领域相近但不同——**性能和推理基础设施**，而非分布式训练 API：

- 跨 PyTorch、Caffe2、TVM 和 FBGEMM 的低级、硬件感知优化——torch/nn 中的 C 和 CUDA 加速、量化推理内核，以及用于移动端推理的 NNPACK/ARM NEON 工作。
- 对 PyTorch 和用于高效矩阵运算的 FBGEMM 库的贡献——FBGEMM 是 int8 量化 GEMM 后端，为 Meta 的大量 CPU 推理和 DLRM 训练提供动力。
- 他*确实*合著了与分布式系统相关的工作，例如关于训练 12 万亿参数 DLRM 的高性能分布式训练的 ZionEX 论文，其中包含嵌入表的分片算法以及支持模型并行和数据并行的基于 PyTorch 的训练栈——但这是一个构建在 `torch.distributed`/FBGEMM *之上*的系统，而非模块本身。
- 职业轨迹：2012 年起担任 Meta 杰出工程师，2023 年加入 OpenAI，负责训练 GPT-4o、GPT-4.5 和 o3，与 Mira Murati 共同创立 Thinking Machines Lab，并于 2025 年 10 月离开 Thinking Machines 重新加入 Meta 的 TBD Lab——据报道，其薪酬方案在六年内高达 15 亿美元。

### 供你参考的思维模型

既然你在研究 nanoGPT 规模的训练和 DeepSeek 风格的 MoE，可以将这些名字映射到各个层级：

```
torch.distributed (c10d, ProcessGroup, NCCL/Gloo)  → Pieter Noordhuis, Teng Li
DDP (Reducer, bucketing, comm/compute overlap)      → Shen Li
FSDP (param sharding, ZeRO-3-style)                 → Yanli Zhao, Rohan Varma, Min Xu (fairscale)
DTensor / torchtitan (TP/PP/FSDP2 composition)      → Wanchao Liang
Kernels / quantization / inference perf (FBGEMM)    → Andrew Tulloch
```

如果你想阅读代码，可以从 `torch/csrc/distributed/c10d/reducer.cpp` 开始——这是 Shen Li 的 DDP 设计的核心（梯度桶 + autograd 钩子 + 异步 AllReduce），而且它出奇地易读。

**参考文献：**

- [PyTorch Distributed: Experiences on Accelerating Data Parallel Training (arXiv:2006.15704)](https://arxiv.org/abs/2006.15704)
- [DDP paper, VLDB 2020 PDF](https://www.vldb.org/pvldb/vol13/p3005-li.pdf)
- [PyTorch DDP tutorial — Author: Shen Li](https://docs.pytorch.org/tutorials/intermediate/ddp_tutorial.html)
- [Reuters: Thinking Machines Lab co-founder Tulloch departs for Meta](https://in.tradingview.com/news/reuters.com,2025:newsml_L2N3VS042:0-thinking-machines-lab-co-founder-tulloch-departs-for-meta-wsj-reports)
