---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英特尔 Iris Plus 640 概览
translated: true
type: note
---

问题：**什么是 Intel Iris Plus Graphics 640？**

回答：**Intel Iris Plus Graphics 640** 是英特尔 **第七代 Kaby Lake** 时代推出的集成 GPU（iGPU），发布时间大约在 **2016–2017 年**。

### 快速规格

| 规格 | Iris Plus Graphics 640 |
| --------------- | ----------------------------------- |
| 架构 | Intel Gen9.5 |
| CPU 代际 | Kaby Lake（第七代酷睿） |
| 执行单元 | **48 EUs** |
| 最高频率 | ~1.0–1.05 GHz，取决于 CPU |
| VRAM | **共享系统内存** |
| API | DirectX 12, OpenCL 2.1 |
| FP32 | 约 **0.4–0.5 TFLOPS** |
| 典型系统 | MacBook Pro、MacBook、Intel 笔记本 |
| 功耗 | 非常低；集成于 CPU 内 |

一个重要区别是，它 **没有独立显存（VRAM）**，不像你的 RTX 4070。它使用的是计算机 DDR4/LPDDR3 内存中的一部分。

### 它在 GPU 性能中的位置

大致如下：

```text
RTX 4070                  ████████████████████████
GTX 1060                  ███████████
GTX 1050                  ███████
Iris Xe 96 EU             ████
Iris Plus 640             ██
Intel HD 620              █
```

所以 Iris Plus 640 **与现代独立 GPU 根本无法相提并论**。

它主要用于：

* 桌面渲染
* 视频播放
* 4K 视频输出
* 轻量级 Photoshop / 视频处理
* 较老/轻量级游戏
* 非常轻量级的机器学习实验

### ML / LLM 工作

这是你需要关注的重点：

**不要把 Iris Plus 640 当作实用的 CUDA/LLM GPU。**

它不支持 NVIDIA CUDA，只有英特尔的 GPU 计算生态。以现代 LLM 的标准来看，其计算能力微不足道。

例如，即使是一个相对较小的模型：

```text
7B parameters × 2 bytes (BF16)
≈ 14 GB just for weights
```

Iris Plus 640 完全不具备接近该容量的专用高带宽内存。

如果你在机器清单中看到这块 GPU，我会把它理解为：

> **“这是一块老旧的 Intel 笔记本/台式机 iGPU，适合显示/视频和基础图形，不适合严肃的 GPU 计算。”**

有趣的是，**Iris Plus 640 在其时代其实是一款相当不错的 iGPU**——它比 Intel HD Graphics 620 快得多，因为英特尔将 EU 数量从 24 → **48 EUs**。
