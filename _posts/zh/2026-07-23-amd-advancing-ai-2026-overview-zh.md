---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD 推进AI 2026 概述
translated: true
type: note
---

问题：什么是 **AMD Advancing AI 2026**？

答案：

AMD Advancing AI 2026 是 AMD 面向 AI 开发者和客户的高规格会议，其地位类似于 NVIDIA GTC。会议聚焦 AMD 在 AI 基础设施市场的布局：GPU、CPU、网络、软件栈以及 AI 系统。2026 年的活动于 7 月 22 日至 23 日在旧金山举行，CEO 苏姿丰将发表主题演讲。（[AMD][1]）

核心思想：

> AMD 希望向 AI 界证明，存在一个足以与 NVIDIA CUDA + H100/H200/B200 抗衡的替代生态系统。

AMD 正在推广的堆栈：

```
AI Factory
|
+-- 加速器
|     AMD Instinct MI300X
|     AMD Instinct MI350/MI400 系列
|
+-- CPU
|     EPYC 服务器 CPU
|
+-- 网络
|     Pensando / Ethernet 架构
|
+-- 软件
      ROCm
      AI 库
      PyTorch 集成
```

（[AMD][2]）

## 这个活动为何重要

当前的 AI 硬件市场：

```
NVIDIA
  CUDA
  H100/H200/B200
  NVLink
  DGX
       |
       |
       v

AI 公司围绕 NVIDIA 构建一切
```

AMD 的策略：

```
AMD
  ROCm
  Instinct GPU
  EPYC CPU
  开放生态系统
       |
       |
       v

为超大规模计算商提供第二来源
```

最大的客户（Microsoft、Meta、OpenAI 生态系统、云提供商）不希望单一供应商控制 AI 算力。AMD 正将自己定位为“第二匹马”。（[Advanced Micro Devices, Inc.][3]）

## 可能讨论的内容

### 1. MI300X / 下一代 Instinct GPU

MI300X 是 AMD 当前主力的 AI 加速器。

粗略对比：

| GPU          | 内存          | 主要生态系统 |
| ------------ | ------------- | ------------ |
| NVIDIA H100  | 80GB HBM3     | CUDA         |
| AMD MI300X   | 192GB HBM3    | ROCm         |
| NVIDIA H200  | 141GB HBM3E   | CUDA         |

AMD 的优势：

* 更多的 HBM 内存
* 开放的软件理念
* 有竞争力的定价

AMD 的劣势：

* ROCm 生态系统远小于 CUDA
* 许多 AI 研究者优先为 NVIDIA 优化

---

### 2. ROCm 成为 CUDA 的竞争对手

这可能是最重要的部分。

CUDA：

```python
import torch

x = torch.randn(1000,1000).cuda()
```

之所以随处可用，是因为 NVIDIA 花了 15 年构建库。

AMD 的目标：

```python
import torch

x = torch.randn(1000,1000).to("cuda")
```

也能在 AMD GPU 上高效运行。

这场竞争不仅是芯片层面的。

而是：

```
硬件 30%
软件生态 70%
```

---

### 3. AI 集群 / “AI 工厂”

AMD 正在超越单个 GPU 的范畴。

未来的产品是：

```
100,000 GPU 集群

=
GPU
+
CPU
+
网络
+
存储
+
编译器
+
软件
+
散热
```

AMD 称之为“AI 基础设施”。（[AMD][4]）

---

## 为什么这对你（MI300X / 本地训练视角）有意义

鉴于你曾尝试过：

* RTX 4070
* MI300X 云实例
* GPT-2 训练
* nanoGPT
* ROCm

这个活动本质上关乎以下转变：

```
旧 AI：

一位研究者
一块 GPU
CUDA

↓

新 AI：

AI 工厂
1000-100000 个加速器
开放的硬件/软件栈
```

对于小型开发者：

* NVIDIA 仍然是最容易上手的。
* 如果你运营集群或需要内存容量，AMD 会变得有趣。

例如：

一个 70B 模型：

```
FP16：

70B 参数 × 2 字节
≈ 仅权重就需要 140GB
```

单张 RTX 4090/4070 无法处理。

MI300X：

```
192GB HBM
```

可以用更少的卡运行更大的模型。

---

## 我的解读

AMD Advancing AI 2026 主要不是为了宣布“一款更快的 GPU”。

而是 AMD 在说：

> “AI 基础设施变得过于重要，不能只属于 NVIDIA。”

真正的竞争：

```
NVIDIA：
CUDA 护城河 + 生态系统 + 网络

AMD：
硬件 + 内存 + 开放生态 + 价格

Google：
TPU

Amazon：
Trainium

Microsoft：
Azure AI 基础设施
```

未来 5 年的 AI 算力很可能是一个多平台的世界，而不是单一的 NVIDIA 世界。（[AMD][4]）

参考文献：

* [AMD Advancing AI 2026 官方活动页面](https://www.amd.com/en/corporate/events/advancing-ai.html?utm_source=chatgpt.com)
* [AMD Advancing AI 2026 值得期待的内容](https://www.amd.com/en/solutions/data-center/insights/what-to-expect-at-amd-advancing-ai-2026.html?utm_source=chatgpt.com)
* [AMD 宣布 Advancing AI 2026](https://www.amd.com/en/newsroom/press-releases/2026-4-28-amd-announces-advancing-ai-2026-.html?utm_source=chatgpt.com)

[1]: https://www.amd.com/en/solutions/data-center/insights/what-to-expect-at-amd-advancing-ai-2026.html?utm_source=chatgpt.com "What to Expect at AMD Advancing AI 2026"
[2]: https://www.amd.com/en/newsroom/press-releases/2026-4-28-amd-announces-advancing-ai-2026-.html?utm_source=chatgpt.com "AMD Announces “Advancing AI 2026”"
[3]: https://ir.amd.com/news-events/press-releases/detail/1283/amd-announces-advancing-ai-2026?utm_source=chatgpt.com "AMD Announces “Advancing AI 2026” :: Advanced Micro Devices, Inc. (AMD)"
[4]: https://www.amd.com/en/corporate/events/advancing-ai.html?utm_source=chatgpt.com "AMD Advancing AI 2026 | San Francisco, July 22-23"
