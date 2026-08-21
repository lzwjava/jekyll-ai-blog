---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU RX/TX 即 PCIe 吞吐量
translated: true
type: note
---

**问题：** NVIDIA GPU 指标中的 “RX: 96.37 MiB/s” 是否指 GPU 主板连接器引脚上的 RX/TX 信号？

**答案：**

不是，它并非指 PCIe 连接器引脚上的物理 RX/TX 电信号。在 NVIDIA GPU 监控工具（如 `nvidia-smi`、`nvtop` 或类似工具）中，指标语境下的 **RX** 和 **TX** 含义如下：

- **RX（接收）** — 数据通过 PCIe 总线 **被 GPU 接收**（即数据从系统内存 → GPU 显存）
- **TX（发送）** — 数据通过 PCIe 总线 **从 GPU 发送**（即数据从 GPU 显存 → 系统内存）

因此 `RX: 96.37 MiB/s` 表示 GPU 当前通过 PCIe 接口 **每秒接收约 96 MB 数据** —— 这是一个 **带宽/吞吐量指标**，而非指物理引脚级别的信号。

### 与网络的类比

该命名借用了网络术语（就像网卡有 RX/TX），但这里的“通道”是 **PCIe 总线**，而不是连接器上的物理 RX/TX 引脚对。

### 对比 PCIe 物理引脚

实际的 PCIe 连接器确实有差分对（接收端 PERp/PERn，发送端 PETp/PETn），但这些从未作为标记指标暴露出来 —— 你只会在硬件/信号完整性文档中看到它们，而不会出现在 GPU 监控软件中。

---

**参考：**

- [NVIDIA SMI 文档](https://developer.nvidia.com/nvidia-system-management-interface)
- [PCIe 基本规范 – 通道信号](https://pcisig.com/specifications)
