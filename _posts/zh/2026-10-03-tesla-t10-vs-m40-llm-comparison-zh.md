---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 特斯拉T10与M40 LLM对比
translated: true
type: note
---

**NVIDIA Tesla T10 是什么？与 Tesla M40 相比，在 LLM/计算用途上表现如何？**

答案：

首先，有一个重要的命名陷阱：**“Tesla T10”可以指代非常不同的产品。**

* **最初的 Tesla T10** 是 Tesla C1060 时代使用的 GPU：**GT200 代，4 GB GDDR3，约 0.93 TFLOPS FP32**。NVIDIA 的旧文档将 C1060 中的 T10 处理器标识为 T10。（[NVIDIA][1]）
* 但**如今二手 GPU 列表中常见的“T10 24GB”/“Tesla T10”显卡**通常是 **Turing TU102 架构**，通常与 NVIDIA 的数据中心/虚拟化生态系统相关。这些产品比最初的 T10 要新得多，也快得多。（[Technical City][2]）

对于你的 GPU 实验室场景，**我假设你指的是较新的 Turing T10**，而不是 2008 年的 T10。

### Turing T10 与 M40 对比

|                    | **T10 24GB** |  **M40 24GB** |
| ------------------ | -----------: | ------------: |
| 架构               |       Turing |     Maxwell 2 |
| GPU                |        TU102 |         GM200 |
| 制程               |        12 nm |         28 nm |
| CUDA 核心数         |        4,608 |         3,072 |
| VRAM               |  24 GB GDDR6 |   24 GB GDDR5 |
| 显存总线           |      384-bit |       384-bit |
| 显存带宽           |    ~624 GB/s |     ~288 GB/s |
| FP32               | ~14.4 TFLOPS | ~6.8–7 TFLOPS |
| PCIe               |      3.0 ×16 |       3.0 ×16 |
| TDP                |       ~260 W |         250 W |
| 计算能力           |      **7.5** |       **5.2** |

T10 的**原始 FP32 吞吐量**约为 M40 24GB 的 **2 倍**，**显存带宽**约为其 **2.2 倍**。独立的基准测试汇总也显示 T10 领先，尽管这些并不代表所有 CUDA/LLM 工作负载。（[Technical City][2]）

M40 是 2015 年的 Maxwell 加速器，拥有 3,072 个 CUDA 核心、24GB GDDR5 和 288 GB/s 带宽。NVIDIA 明确将其计算能力列为 **5.2**。（[NVIDIA Images][3]）

### 对你的 LLM 实验来说，真正重要的区别

**T10 = Turing = CUDA 7.5**

**M40 = Maxwell = CUDA 5.2**

这在今天是一个**巨大的**差异。

对于现代 CUDA 软件：

```text
M40
  GM200
    Maxwell
      sm_52
        ↓
      CUDA 5.2
        ↓
      现代框架越来越难以支持
```

T10
  TU102
    Turing
      sm_75
        ↓
      CUDA 7.5
        ↓
      更好的兼容性
```

Turing 还为你提供了 **Tensor Cores**，而 M40 没有。这对于 FP16/INT8 推理工作负载尤其重要。

所以如果你的目标是：

```text
llama.cpp
PyTorch
Transformers
vLLM 类实验
量化 LLM 推理
CUDA 内核
agent/LLM 实验
```

我会认为 T10 与 M40 相比，属于**完全不同的实用旧 GPU 类别**。

### 但有一个问题

T10 的 **24 GB** 并不自动意味着它等同于 RTX 3090。

你仍然有：

```text
T10
  24 GB
  ~624 GB/s
  Turing
  与 RT 无关
  面向旧数据中心/虚拟化的显卡
  ~260 W

RTX 3090
  24 GB
  ~936 GB/s
  Ampere
  Tensor Cores
  更现代的 CUDA 生态
  ~350 W
```

因此，对于 LLM 推理来说，T10 之所以有吸引力，主要是因为**24 GB + Turing + 相对较高的带宽**可以在二手市场上以低价获得。

### 与你的 M40 项目相比

如果你要在以下之间做选择：

```text
便宜的 M40 24GB
        vs
便宜的 T10 24GB
```

我会为你的用途**优先研究 T10**。

M40 最大的优势是：

> **以极低的价格获得 24 GB 显存。**

这对于模型必须放入显存的实验仍然有用。

但 T10 给你的是：

> **24 GB + Turing + ~2 倍 FP32 + ~2 倍带宽 + Tensor Cores + 更现代的 CUDA 能力。**

这使得 T10 作为**便宜的 LLM 实验卡**有趣得多。

在购买特定 T10 型号之前，我要验证的一件事是**确切的板卡/GPU 识别**，因为二手中文列表可能使用像 `T10`、`T10 8G`、`T10 24G`、`RTX T10`、`GRID T10` 等名称。它们不一定是相同的产品。例如，一个数据库列出了 **8GB GRID RTX T10**，功耗 150 W，这与 24GB T10 有本质区别。（[TopCPU][4]）

参考：

* [NVIDIA Tesla M40 数据表](https://images.nvidia.com/content/tesla/pdf/78071_Tesla_M40_24GB_Print_Datasheet_LR.PDF?utm_source=chatgpt.com)
* [NVIDIA Tesla/M40 技术博客](https://developer.nvidia.com/blog/accelerating-hyperscale-datacenter-applications-tesla-gpus/?utm_source=chatgpt.com)
* [T10 vs M40 规格对比](https://technical.city/en/gpu/Tesla-T10-vs-Tesla-M40-24-GB?utm_source=chatgpt.com)

我还可以专门针对 `llama.cpp` 和当前 PyTorch/CUDA 兼容性，绘制 **M40 → T10 → P40 → P100 → V100 → RTX 2080 Ti → 3090** 的映射，这对你的廉价 GPU 实验室会很有用。

[1]: https://www.nvidia.com/content/quadro_oem/presentations/Tesla_GPU_Computing_Oct2008.pdf?utm_source=chatgpt.com "幻灯片 1"
[2]: https://technical.city/en/gpu/Tesla-T10-vs-Tesla-M40-24-GB?utm_source=chatgpt.com "Tesla M40 24 GB vs Tesla T10 [1-Benchmark Showdown]"
[3]: https://images.nvidia.com/content/tesla/pdf/78071_Tesla_M40_24GB_Print_Datasheet_LR.PDF?utm_source=chatgpt.com "数据表：Quadro M6000"
[4]: https://www.topcpu.net/en/gpu-c/grid-rtx-t10-8-vs-tesla-m40-24-gb?utm_source=chatgpt.com "NVIDIA GRID RTX T10 8 vs NVIDIA Tesla M40 24 GB - GPU 对比 | 哪个更好"