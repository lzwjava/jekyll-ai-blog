---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GT 730与M60并非相同
translated: true
type: note
---

**问题：** GT 730 与 Tesla M60 相比如何，它们是同一张卡吗，GT 730 有 384 位显存总线吗？

**回答：**

不，GT 730 和 Tesla M60 是**完全不同的显卡**——根本不是同一张卡。而且 GT 730 **没有** 384 位显存总线。以下是完整说明：

---

### NVIDIA GeForce GT 730 — 显存总线

GT 730 实际上有**三种版本**，总线宽度各不相同，这造成了很大的混淆：

| 版本 | GPU | CUDA 核心 | 显存总线 |
|---|---|---|---|
| GT 730 DDR3 | GF108（Fermi） | 96 | **128 位** |
| GT 730 DDR3 | GK208（Kepler） | 384 | **64 位** |
| GT 730 GDDR5 | GK208（Kepler） | 384 | **64 位** |

基于 Fermi 架构的 GT 730（GF108）使用**128 位**显存总线，搭配 DDR3 显存。

更常见的基于 Kepler 架构的 GT 730（GK208）拥有 384 个 CUDA 核心，但仅使用**64 位**显存接口，配备 2 GB DDR3 显存，带宽为 14.4 GB/s。

**不存在 384 位总线的 GT 730。** 数字 384 指的是它的 CUDA 核心数量，而不是总线宽度——很容易混淆。

---

### NVIDIA Tesla M60 — 完全不同的另一种产品

Tesla M60 是一款基于 **Maxwell** 架构的双 GPU 服务器/虚拟化加速卡，拥有**总计 4096 个 CUDA 核心**（每个 GPU 2048 个）和 **16 GB GDDR5** 显存（每个 GPU 8 GB）。

其显存接口为**每个 GPU 256 位**（两个 GPU 合计 512 位），显存带宽为**每个 GPU 160.4 GB/s**（总计 320 GB/s）。

功耗高达 **300W**，专为企业级虚拟工作站和虚拟桌面设计。

---

### GT 730 与 Tesla M60 — 并排对比

| 规格 | GT 730（最佳版本） | Tesla M60（每 GPU） |
|---|---|---|
| 架构 | Kepler | Maxwell |
| CUDA 核心 | 384 | 2048 |
| 显存 | 2 GB GDDR5 | 8 GB GDDR5 |
| 显存总线 | 64 位 | 256 位 |
| 带宽 | ~14–28 GB/s | ~160 GB/s |
| 用途 | 入门级台式机 | 数据中心 / vGPU |
| TDP | ~23–49W | 300W（整卡） |

它们**毫无相似之处**——M60 是专业级双 GPU 数据中心显卡，而 GT 730 是来自不同时代和架构的低端消费级台式机显卡。

**参考链接：**
- [VideoCardz – GT 730（GF108）](https://videocardz.com/nvidia/geforce-700/geforce-gt-730)
- [GPUZoo – GT 730 DDR3 64 位](https://www.gpuzoo.com/GPU-NVIDIA/GeForce_GT_730_DDR3_64-bit.html)
- [GPUZoo – GT 730 DDR3 128 位](https://www.gpuzoo.com/GPU-NVIDIA/GeForce_GT_730_DDR3_128-bit.html)
- [NVIDIA Tesla M60 数据表（PDF）](https://images.nvidia.com/content/tesla/pdf/188417-Tesla-M60-DS-A4-fnl-Web.pdf)
- [VideoCardz – Tesla M60](https://videocardz.net/nvidia-tesla-m60)