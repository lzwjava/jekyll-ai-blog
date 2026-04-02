---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 0% GPU 利用率的常见原因
translated: true
type: note
---

不对。GPU-Util 为 **0%** 表示 GPU 完全空闲 — 没有在进行任何计算。

56GB 已使用 = 模型 + 优化器状态已加载。但 0% GPU-Util = 它只是坐在那里等待。

常见原因：

1. **Data loading bottleneck** — 脚本在从磁盘读取/CPU 预处理上遇到瓶颈，GPU 空闲等待批次
2. **`torch.compile` profiling phase** — 前几个步骤较慢，同时它在跟踪图
3. **Disk I/O** — 如果 fineweb 数据在慢速存储上，批次准备跟不上 GPU

快速诊断 — 在训练活跃时（在另一个终端）再次运行 `nvidia-smi`。GPU-Util 还是 0% 吗？

如果是，则几乎肯定是 **data loader**。在你的 `download_fineweb.py` 中使用 `streaming=True`，你每个 epoch 都在从原始文本文件读取 — 那很慢。对于 1.5B 模型训练，你希望数据预处理成 **binary `.bin` 文件**，`train.py` 可以 memory-map 以快速加载。

你运行了 `prepare.py` 将 FineWeb 转换为 nanoGPT 的 binary 格式吗？那很可能就是你缺失的步骤。