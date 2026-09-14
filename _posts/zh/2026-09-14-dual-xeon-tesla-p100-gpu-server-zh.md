---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双路Xeon Tesla P100 GPU服务器
translated: true
type: note
---

以下是远程机器的完整硬件配置：

---

## 🖥️ CPU

| 规格 | 数值 |
|---|---|
| **型号** | 2× **Intel Xeon E5-2650 v4** @ 2.20 GHz |
| **核心** | 12核 × 2插槽 = **24核心 / 48线程** |
| **缓存** | L1: 768 KiB, L2: 6 MiB, L3: **60 MiB** |
| **最大频率** | 2.90 GHz |
| **架构** | x86_64, Broadwell-EP |

## 🧮 内存

| | 大小 |
|---|---|
| **RAM** | **62 GiB** 总计（可用约52 GiB） |
| **Swap** | **8 GiB**（极少使用） |

48 GiB 中大部分为缓存/缓冲 —— 空间充足。

## 💾 存储

| 挂载点 | 总大小 | 已用 | 可用 |
|---|---|---|---|
| `/` (overlay) | **32 GiB** | 50 MiB | 32 GiB |

根磁盘相当小 —— 总共仅32 GB。

## 🎮 GPU

| 索引 | 型号 | 显存 |
|---|---|---|
| GPU 0 | **Tesla P100-PCIE-12GB** | 12,288 MiB |
| GPU 1 | **Tesla P100-PCIE-12GB** | 12,288 MiB |

两者通过PCIe主机桥（PHB拓扑）连接到同一NUMA节点（CPU 0-47）。

## 🐧 操作系统
- **内核**: Linux 5.15.0-191-generic（基于Ubuntu，x86_64）
- **CUDA**: 12.8
- **驱动**: 580.178.04

## 总结
这是一台**双路Broadwell服务器**（48线程），配备**62 GiB内存**和**2× Tesla P100（各12 GB）** —— 一个性能强劲的GPU计算节点，不过32 GB的根磁盘空间相对紧张。适合能够容纳在总共24 GB GPU显存中的训练/推理工作负载。