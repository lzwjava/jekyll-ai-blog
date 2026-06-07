---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA DGX Spark：黄仁勋的愿景
translated: true
type: note
---

**问题：** 英伟达发布的 DGX Spark 表现如何？黄仁勋在近期的 GTC 主题演讲中对此有何评价？

---

## 答案

DGX Spark 是英伟达基于 Grace Blackwell 架构打造的个人 AI 超级计算机，已于 2026 年 5 月底发货。这是一款桌面级系统，正好满足你在工作站上进行本地模型开发的需求。

### 硬件与性能

该系统采用英伟达最新的 Grace Blackwell 架构，集成了 GPU、CPU、网络和 CUDA 库，能够对高达 2000 亿参数的模型进行推理，并在本地微调 700 亿参数的模型。它采用紧凑的桌面形态，拥有 128GB 统一内存，并且可以将两台系统组网，提供 256GB 的合并内存以支持更大规模的模型。

**关键规格**：可实现 1 petaFLOP 的 AI 性能。对比来看，你的 MI300X 拥有 192GB 显存，对于大多数推理场景来说性能过剩；而 DGX Spark 的统一内存架构使其在 700 亿参数模型的微调方面效率极高，刚好处于最佳甜点区。Founder's Edition 于 2025 年 10 月以 3999 美元的价格推出。

### 发布后的性能提升

到 2026 年国际消费电子展（CES 2026，即 9 月发布后的几个月），英伟达展示了自发布以来最高达 2.5 倍的性能提升，其中包括 2025 年 11 月推送的更新。在至少一个图像生成工作流中，DGX Spark 相比 M4 Max MacBook Pro 实现了 8 倍的速度优势。

### 黄仁勋的定位

在 GTC 2025 上，黄仁勋将 DGX Spark 描述为“AI 时代的计算机”，其前身为 Project DIGITS。这一表述强调了面向智能体 AI 的本地开发——并非数据中心规模，而是面向个人开发者的生产力。

### 近期路线图（GTC 台北 2026）

英伟达发布了 RTX Spark，这是一款面向 Windows on Arm 的一体化芯片，配备 20 核英伟达 Grace GPU（与联发科共同设计）以及拥有 6144 个 CUDA 核心的 RTX Blackwell GPU——其定位在 GeForce RTX 5070 笔记本 GPU 的层级。RTX Spark 的路线图包括 2028 年的 Vera Rubin 处理器和 2030 年的 Rosa Feynman。

GTC 2026 的更广泛信息传递转向了**智能体 AI**——Vera Rubin 被定位为英伟达首款专为智能体工作负载而构建的垂直集成 AI 系统。DGX Spark 处于该堆栈的开发者层级。

### 这对你的意义

你已经在本地推理中消耗了海量的 token 量。对比 DGX Spark 和你的 RTX 4070：Spark 拥有 1 TFLOP 算力，而你的 4070 峰值约为 40 TFLOPS，但 128GB 的统一内存才是真正的亮点——它让你在运行 700 亿参数模型时避免了内存碎片和页面交换。对于 nanoGPT 规模的训练，你的 RTX 4070 完全够用。而对于生产级推理服务及更大模型的微调，DGX Spark 填补了空白，无需升级到 MI300X 的级别。

CES 2026 上展示的 DGX Spark 驱动 Reachy Mini 机器人（与 Pollen Robotics 合作）这一事实表明，黄仁勋正在押注桌面与机器人的融合——智能体在本地单机上运行，而非仅依赖云端。

---

## 参考文献

- 《英伟达在 CES 2026 上提升 DGX Spark 性能并推出新的开发者工具》（HotHardware）
- 《英伟达 DGX Spark 面向全球 AI 开发者开售》（英伟达新闻中心，2026 年 5 月 31 日）
- 《GTC 2025 公告与实时更新》（英伟达博客）
- 《英伟达 GTC 2026 亮点：回顾你可能错过的一切》（Deeper Insights，2026 年 3 月 17 日）
- 《英伟达 GTC 2026：AI 下一站实时更新》（英伟达博客）
