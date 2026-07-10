---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA V100 GPU 概述
translated: true
type: note
---

问题：什么是 V100？

回答：

NVIDIA Tesla V100（通常称为 **V100**）是一款**2017 年发布的 NVIDIA 数据中心 AI GPU**，基于 **Volta 架构**。它是首批配备专用 **Tensor Core** 的 GPU 之一，专为深度学习训练和 HPC 设计。([NVIDIA][1])

可以将其视为当今 A100/H100 的前身。

架构时间线：

```
Tesla P100 (Pascal, 2016)
        |
Tesla V100 (Volta, 2017)  <-- Tensor Core 时代开始
        |
A100 (Ampere, 2020)
        |
H100 (Hopper, 2022)
```

主要规格：

```
GPU：              GV100
架构：             Volta
CUDA 核心数：       5120
Tensor Core 数：    640
显存：             16GB / 32GB HBM2
显存带宽：         ~900 GB/s
功耗：             250W PCIe / 300W SXM
计算能力：         sm_70
```

([NVIDIA 图片][2])

对 AI 来说重要的部分：

### 1. HBM2 显存

与 RTX 显卡对比：

```
RTX 4070：
12GB GDDR6X
~500 GB/s 带宽

V100：
16/32GB HBM2
~900 GB/s 带宽
```

HBM 是一种快得多的显存，有助于大型矩阵运算。

### 2. Tensor Core

V100 引入了 NVIDIA Tensor Core：

```
普通 CUDA 核心：
    FP32 乘法/加法

Tensor Core：
    矩阵乘法累加

    A @ B + C
```

深度学习主要是：

```
Y = XW
```

大型矩阵乘法，因此 Tensor Core 加速了训练/推理。([arXiv][3])

### 与你的 RTX 4070 对比

大致如下：

|                  | V100         | RTX 4070     |
| ---------------- | ------------ | ------------ |
| 年份             | 2017         | 2023         |
| 架构             | Volta        | Ada          |
| 显存             | 16/32GB HBM2 | 12GB GDDR6X  |
| Tensor Core      | 第一代       | 第四代       |
| CUDA 核心数      | 5120         | 5888         |
| FP16 AI 性能     | 不错         | 好得多       |
| 显存容量         | 优势         | 劣势         |
| 软件支持         | 较旧         | 较新         |

对于现代大模型工作：

* **训练小模型** → V100 仍然可用。
* **运行大模型（因为显存很重要）** → V100 32GB 版本值得考虑。
* **现代 CUDA / FlashAttention / FP8 / 最新框架** → RTX 4070 更胜一筹。

最大的问题是软件兼容性。V100 的**计算能力为 7.0**，而许多新的 AI 优化针对 Ampere+（sm80+）或 Hopper。([Reddit][4])

### V100 与你的 MI50 对比

你的 AMD MI50 对比很有意思：

```
MI50：
- 16GB HBM2
- ~1TB/s 带宽
- 300W
- ROCm 生态

V100：
- 16/32GB HBM2
- ~900GB/s 带宽
- 250-300W
- CUDA 生态
```

硬件属于同一时代，但 CUDA 支持使得 V100 在 PyTorch 中更容易使用。

如今的廉价 V100 基本上是一个“数据中心遗留物”，但仍然可以完成有用的 AI 工作，因为**显存容量和带宽比原始算力更保值**。([Reddit][5])

针对你的使用场景（nanoGPT/GPT-2 风格训练），V100 32GB 实际上会是一块非常强大的实验卡，但你的 RTX 4070 拥有现代 CUDA 内核和更低的使用门槛优势。

[1]: https://www.nvidia.com/en-in/data-center/v100/?utm_source=chatgpt.com "NVIDIA V100 | NVIDIA"
[2]: https://images.nvidia.com/content/technologies/volta/pdf/tesla-volta-v100-datasheet.pdf?utm_source=chatgpt.com "NVIDIA V100"
[3]: https://arxiv.org/abs/1803.04014?utm_source=chatgpt.com "NVIDIA Tensor Core Programmability, Performance & Precision"
[4]: https://www.reddit.com/r/LocalLLM/comments/1tx6emj/v100_question/?utm_source=chatgpt.com "v100 question"
[5]: https://www.reddit.com/r/RigBuild/comments/1t9xeyj/nvidias_v100_an_8year_old_gpu_now_sells_for_100/?utm_source=chatgpt.com "NVIDIA’s V100, An 8-Year Old GPU, Now Sells for $100 and Crushes Modern Consumer Cards in AI LLM Workloads"