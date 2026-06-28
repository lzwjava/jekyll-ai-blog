---
audio: false
generated: true
image: false
lang: zh
layout: post
title: B200 GPU 就绪与空闲
translated: true
type: note
---

B200 GPU 状态正常，已就绪。以下是摘要：

```
=== B200 GPU 摘要 ===

硬件
  GPU：              NVIDIA B200（Blackwell 架构）
  内存：            183 GB HBM3（可用 178.4 GB）
  SM 数量：         148
  计算能力：       10.0
  PCIe：            Gen 5 x16
  ECC：             已启用（0 错误）
  温度：           33°C（空闲）
  功耗：           190W / 1000W 限制

软件
  驱动：           580.126.20
  CUDA：           13.0（驱动）/ 12.8（PyTorch）
  PyTorch：        2.8.0+cu128
  内核：           6.8.0-107-generic

主机系统
  CPU：            AMD EPYC 9555 64 核
  内存：           2.2 TB（已用 446 GB，可用 1.8 TB）

基准测试
  矩阵乘法 4096x4096：   415.8 次/秒
  矩阵乘法 8192x8192：   59.8 次/秒
  内存带宽：            2,222 GB/s
```

GPU 空闲，无进程运行，182 GB 空闲显存，2.2 TB 主机内存。80GB 与 183GB 显存以及 148 个 SM 确认这是完整版 B200（非缩减版本）。计算能力 10.0 属于 Blackwell 代——原生支持 FP4/FP8，第五代 Tensor Core。

准备训练。
