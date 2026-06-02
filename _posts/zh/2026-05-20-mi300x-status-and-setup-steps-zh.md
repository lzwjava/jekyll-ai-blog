---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X 状态和安装步骤
translated: true
type: note
---

看起来不错——这是 MI300X 的清晰读数。

**简单来说：**

- **AMD Instinct MI300X** — 256 GB HBM3，PCIe 5.0 x16，完全分配给此 VM 作为 VF（专用，非共享）
- 它处于最高链路速度（32 GT/s x16），D0 电源状态，已可投入使用

**问题所在**：这是一个 VF，因此您无法获取温度/时钟/功耗遥测数据，也无法运行计算工作负载——这些需要完整的 ROCm 堆栈。目前您只有驱动程序，没有运行时环境。

**要使其可计算**，您需要：

```
apt install rocm-hip-sdk
```

这将安装 HIP（AMD 的 CUDA 等价物）、ROCm 库，并应连接 KFD 以便 `rocm-smi` 也能正常工作。这是一个较大的安装包（约几 GB），但这是标准路径。

需要我启动安装，还是您对当前的可视化状态感到满意？
