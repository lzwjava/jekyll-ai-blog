---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA NCCL 集合通信库
translated: true
type: note
---

以下是该项目的全面概述：

## NVIDIA NCCL（NVIDIA 集体通信库）

**位置：** `https://github.com/NVIDIA/nccl` — 这是官方 NVIDIA NCCL 仓库，版本为 **2.32.3-1**。

### 什么是 NCCL？

**NCCL**（读作 "Nickel"）是由 NVIDIA 开发的 **独立 GPU 通信例程标准库**。它为多 GPU 和多节点深度学习工作负载实现了高度优化的集体通信原语。

### 核心功能

**已实现的集体操作：**

- **全规约（All-Reduce）** – 对所有 GPU 的数据进行求和/规约，并将结果广播回所有 GPU
- **全收集（All-Gather）** – 从所有 GPU 收集数据到每个 GPU
- **规约（Reduce）** – 将数据从所有 GPU 规约到单个 GPU
- **广播（Broadcast）** – 将数据从一个 GPU 广播到所有其他 GPU
- **规约-分散（Reduce-Scatter）** – 先规约再分散数据块
- **发送/接收（Send/Receive）** – 点对点通信模式

### 通信后端（传输层）

`src/transport/` 目录揭示了多种传输层：

| 传输层 | 描述 |
| ----------- | ------------- |
| **P2P** | 直接 GPU 点对点（NVLink，PCIe） |
| **SHM** | 用于节点内通信的共享内存 |
| **Net IB** | 用于 RDMA 网络的 InfiniBand Verbs |
| **Net Socket** | 用于网络的 TCP/IP 套接字 |
| **Net EFA GDA** | 支持 GPU Direct Async 的 AWS EFA |
| **NVLS** | NVLink 交换机（NVSwitch） |
| **NVLS UB** | NVLink 交换机单播/广播 |
| **Multicast** | NVLink 多播 |
| **RMA Socket** | 基于套接字的 RDMA |

### 关键源码组件

| 目录/文件 | 用途 |
| --------------- | --------- |
| `src/device/` | 集体操作的 GPU 内核代码（CUDA 内核） |
| `src/transport/` | 通信传输层实现 |
| `src/include/` | 公开及内部头文件 |
| `src/graph/` | 通信图/拓扑算法 |
| `src/tuning/` | 自动调优以选择最佳算法 |
| `src/init.cc` | 核心初始化（约 169K，最大源文件） |
| `src/proxy.cc` | 用于异步操作的代理线程 |
| `src/bootstrap.cc` | 引导网络设置 |
| `src/collectives.cc` | 集体操作编排 |
| `src/enqueue/` | 操作入队/出队机制 |
| `src/plugin/` | 用于自定义传输/调优器的插件系统 |
| `src/ras/` | 可靠性、可用性、可服务性 |
| `src/rma/` | 远程内存访问 |

### 附加组件

- **`bindings/`** – 语言绑定（Python 的 `nccl4py`，中间表示的 `ir`）
- **`plugins/`** – 针对环境、网络、分析器、调优器、RMA、GIN 的插件实现
- **`contrib/`** – 社区贡献（检查点、M2N、UBX、Rust 绑定等）
- **`docs/`** – 文档
- **`pkg/`** – 用于 Debian、RPM、tar 包和 Python wheel 的打包脚本

### 使用方式

NCCL 是深度学习框架中多 GPU 通信的 **事实标准**，例如：

- **PyTorch**（通过 `torch.distributed`）
- **TensorFlow**（通过 `tf.distribute`）
- **MPI** 应用
- **JAX** 及其他机器学习框架

它是跨数千个 GPU 大规模分布式训练的骨干，支持在 `DDP`（分布式数据并行）训练期间执行梯度全规约等操作。
