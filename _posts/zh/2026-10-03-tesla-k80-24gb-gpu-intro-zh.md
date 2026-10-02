---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tesla K80 24GB GPU 简介
translated: true
type: note
---

**NVIDIA Tesla K80 24GB** 是一款发布于 2014 年的老旧 **数据中心 / HPC GPU 加速器**。它专为科学计算、CUDA 工作负载、模拟和服务器设计——**而非游戏**。([NVIDIA][1])

## 硬件概述

| 项目             | 规格                                   |               |
| --------------- | -------------------------------------- | ------------- |
| 架构             | Kepler GK210                           |               |
| GPU 芯片         | **2 × GK210 GPU**                      |               |
| CUDA 核心数      | 总计 4,992（2,496 × 2）               |               |
| 显存             | **总计 24GB GDDR5**                    |               |
| 显存分配         | **每颗 GPU 12GB**                      |               |
| 显存带宽         | 总计 480 GB/s（每颗 GPU 240 GB/s）    |               |
| PCIe             | PCIe 3.0 x16                           |               |
| 功耗             | 300W                                   |               |
| 散热             | 被动散热（需要服务器气流）             |               |
| 显示输出         | 无                                     |               |
| 计算能力         | CUDA 3.7                               | ([NVIDIA][2]) |

## 重要提示：“24GB 显存”与 RTX 3090 的 24GB 不同

K80 实际上是 **同一块 PCB 上的两颗 GPU**：

```
Tesla K80
 ├── GK210 GPU #1
 │    ├── 2496 个 CUDA 核心
 │    └── 12GB GDDR5
 │
 └── GK210 GPU #2
      ├── 2496 个 CUDA 核心
      └── 12GB GDDR5
```

它 **没有** 统一可用的 24GB 内存池。单个 CUDA 进程通常只能看到两个独立的 GPU。([TechYorker][3])

例如：

* 模型需要 16GB 显存 → ❌ 无法存放在单颗 K80 GPU 上
* 两个 8GB 工作负载 → ✅ 可分别运行
* 使用旧 CUDA 框架的多 GPU 训练 → ✅ 可能可行

## 当前 AI / LLM 用途

对于现代 LLM 工作，K80 基本已过时。

问题：

### 1. 无 Tensor Core

现代 AI GPU：

* RTX 3090 → Ampere Tensor Core
* RTX 4090 → Ada Tensor Core
* A100/H100 → 数据中心 Tensor Core

K80：

* 无 Tensor Core
* 无 BF16
* 无 FP8
* 无现代混合精度加速

因此 PyTorch 的 LLM 推理/训练极为缓慢。

### 2. 旧 CUDA 架构

K80 = Kepler（`sm_37`）。

许多现代 CUDA 库已停止支持。

例如：

* 最新的 PyTorch 版本通常无法使用
* FlashAttention ❌
* 现代 vLLM ❌
* TensorRT-LLM ❌

### 3. 功耗效率极低

性能：

* ~5.6 TFLOPS FP32
* 300W 功耗

对比：

* RTX 3090：
  * ~35.6 TFLOPS FP32
  * 24GB GDDR6X
  * Tensor Core

一块二手 RTX 3090 在 AI 方面快得多。

## K80 仍有价值的场景

良好用途：

### 学习 CUDA

好处：

* CUDA 编程
* 内存管理
* 内核
* 多 GPU 概念

因为它便宜。

### 旧科学软件

好处：

* 分子动力学
* HPC 模拟
* CUDA 教学
* 遗留研究

### GPU 维修练习

对于你的 GPU 维修实验，K80 实际上很有意思：

* 大尺寸 PCB
* 双 GPU
* 众多 VRM 组件
* 服务器级设计
* 存在便宜的损坏卡

在接触昂贵的 RTX 卡之前，它是一块很好的“练习板”。

## 与你的 RTX 4070 12GB 对比

|               | Tesla K80  | RTX 4070    |
| ------------- | ---------- | ----------- |
| 发布年份       | 2014       | 2023        |
| 显存           | 24GB GDDR5 | 12GB GDDR6X |
| GPU 数量       | 2          | 1           |
| AI 速度        | 非常慢     | 快得多       |
| Tensor Core    | 无         | 有           |
| CUDA 支持      | 旧         | 现代        |
| LLM 推理       | 差         | 良好        |
| 功耗           | 300W       | ~200W       |

对于 LLM 工作，你的 **RTX 4070 12GB 要快得多**，尽管显存只有一半。

## 二手市场价值

如今 K80 卡通常很便宜，因为云提供商已将其退役。吸引人的点是“24GB 显存”，但实际情况是：

> 它是一张 2 × 12GB 的 Kepler 卡，而不是一张便宜的 24GB AI GPU。

对于 AI 爱好者/研究，我通常会选择：

1. RTX 3090 24GB
2. RTX 3060 12GB（便宜）
3. RTX 4090
4. Tesla P40 24GB（如果仅看重显存）

而不是 K80。

参考资料：

* NVIDIA Tesla K80 数据表 ([NVIDIA][1])
* NVIDIA Tesla K80 板规格 ([NVIDIA][2])
* TechPowerUp Tesla K80 数据库 ([TechPowerUp][4])

[1]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/TeslaK80-datasheet.pdf?utm_source=chatgpt.com "<visual_element id=\"e1\">"
[2]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/Tesla-K80-BoardSpec-07317-001-v05.pdf?cjevent=5c16c62be38411e9804803050a180513&utm_source=chatgpt.com "TESLA K80 GPU ACCELERATOR"
[3]: https://techyorker.com/nvidia-tesla-k80-how-the-dual-gk210-gpu-accelerator-worked/?utm_source=chatgpt.com "NVIDIA Tesla K80 Explained: Dual GK210 GPUs, Specs and CUDA Support"
[4]: https://www.techpowerup.com/gpu-specs/tesla-k80.c2616?utm_source=chatgpt.com "NVIDIA Tesla K80 Specs | TechPowerUp GPU Database"
