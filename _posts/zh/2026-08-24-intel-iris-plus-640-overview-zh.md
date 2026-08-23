---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英特尔Iris Plus 640 概述
translated: true
type: note
---

问题：**什么是 Intel Iris Plus Graphics 640？**

答案：**Intel Iris Plus Graphics 640** 是英特尔**第七代 Kaby Lake** 时代的一款集成 GPU（iGPU），大约于 **2016–2017 年** 推出。

### 快速规格

| Spec            | Iris Plus Graphics 640              |
| --------------- | ----------------------------------- |
| Architecture    | Intel Gen9.5                        |
| CPU generation  | Kaby Lake（第七代酷睿）             |
| Execution Units | **48 EUs**                          |
| Max clock       | ~1.0–1.05 GHz，取决于 CPU           |
| VRAM            | **共享系统内存**                    |
| API             | DirectX 12、OpenCL 2.1              |
| FP32            | 约 **0.4–0.5 TFLOPS**              |
| Typical systems | MacBook Pro、MacBook、Intel 笔记本  |
| Power           | 极低；集成于 CPU 内部               |

重要的区别在于：它**没有像你的 RTX 4070 那样的专用显存**，而是使用计算机的 DDR4/LPDDR3 内存的一部分。

### 在 GPU 性能中的位置

粗略示意：

```text
RTX 4070                  ████████████████████████
GTX 1060                  ███████████
GTX 1050                  ███████
Iris Xe 96 EU             ████
Iris Plus 640             ██
Intel HD 620              █
```

因此，Iris Plus 640 **与当代独立 GPU 完全不可比**。

它主要用于：

* 桌面渲染
* 视频播放
* 4K 视频输出
* 轻度 Photoshop/视频工作
* 较老/轻量级游戏
* 非常轻量级的机器学习实验

### 针对 ML / LLM 工作

这部分对你来说很重要：

**不要将 Iris Plus 640 视为可用的 CUDA/LLM GPU。**

它没有 NVIDIA CUDA 支持，只有 Intel 的 GPU 计算生态系统。以现代 LLM 标准来看，它的计算能力微乎其微。

例如，即使是一个相对较小的模型：

```text
7B 参数 × 2 字节 (BF16)
≈ 14 GB 仅用于权重
```

Iris Plus 640 完全没有接近那么多专用高带宽内存。

如果你在机器清单中看到这款 GPU，我会这样理解：

> **“这是一款老旧 Intel 笔记本/台式机 iGPU，适用于显示/视频和基础图形处理，不适合严肃的 GPU 计算。”**

有趣的是，**Iris Plus 640 在其时代确实是一款相当不错的 iGPU**——它比 Intel HD Graphics 620 快得多，因为英特尔将 EU 数量从 24 个增加到了 **48 个 EU**。