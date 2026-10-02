---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSpeed无法在Tesla M40上运行
translated: true
type: note
---

不，**DeepSpeed 无法运行**在 Tesla M40 上。存在两个硬性障碍：

### 1. PyTorch 依赖

DeepSpeed 是一个 PyTorch 库。PyTorch 多年前就已放弃对 CC 5.x 的支持：

| PyTorch | 最小 CC | 您的 M40 |
| --------- | -------- | ---------- |
| 1.10+ | **6.0**（Pascal） | ❌ |
| 2.x | **7.0**（Volta） | ❌ |

### 2. 系统内存

DeepSpeed 需要大量主机内存来存储优化器状态、梯度累积、数据加载等。您的机器总共只有 **3.2GB** —— 远远不够。

---

**结论：** 任何依赖 **PyTorch** 的方案都无法使用。这就是为什么 llama.cpp（直接通过 CUDA 与硬件交互，无需 PyTorch）才是适合此硬件的正确工具。
