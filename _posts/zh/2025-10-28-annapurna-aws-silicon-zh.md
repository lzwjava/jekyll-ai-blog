---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 安纳普尔纳实验室：AWS定制芯片
translated: true
type: note
---

### 什么是 Annapurna Labs？

**Annapurna Labs** 是一家以色列半导体公司，专注于为云计算、网络、存储和 AI 工作负载设计**高性能、高能效的处理器**。该公司于 **2015 年 1 月被亚马逊收购**，据报道交易金额约 3.5 亿至 3.7 亿美元，目前作为 **Amazon Web Services (AWS)** 的全资子公司运营。

Annapurna Labs 设计的**定制芯片**为 AWS 的大部分基础设施提供动力，使亚马逊能够在某些工作负载上减少对 Intel、Broadcom 和 NVIDIA 等第三方芯片供应商的依赖。

---

### Annapurna Labs 设计的关键芯片（在 AWS 中使用）

| 芯片系列 | 类型 | 主要特性 | 主要 AWS 用例 |
|-------------|------|--------------|-----------------------|
| **Alpine** | 基于 ARM 的 SoC | 多核 ARMv8 CPU，低功耗，集成网络/存储 | 早期 EC2 实例，存储控制器 |
| **Graviton** | 基于 ARM 的 CPU | 64 位 ARM Neoverse 核心（AWS 设计），高核心数，DDR5，PCIe Gen4/5 | **EC2 Graviton 实例**（通用计算） |
| **Nitro** | 智能网卡 / 卸载卡 | ARM CPU + 用于虚拟化、安全、存储、网络的定制加速器 | **EC2 Nitro 系统**，EBS，VPC，安全卸载 |
| **Inferentia** | AI 推理 | 高吞吐量张量处理，低延迟，Neuron 核心 | **EC2 Inf1/Inf2 实例**，用于 ML 推理 |
| **Trainium** | AI 训练 | 可扩展用于大语言模型，高内存带宽，NeuronLink 互连 | **EC2 Trn1/Trn2 实例**，用于训练 LLM |

---

### 旗舰芯片系列（截至 2025 年现状）

#### 1. **AWS Graviton (CPU)**
- **架构**：基于定制 ARM Neoverse 的核心（非现成）
- **代际**：
  - **Graviton1** (2018): 16 核 ARMv8，用于 A1 实例
  - **Graviton2** (2020): 64 核 Neoverse N1，价格性能比 x86 高约 40%
  - **Graviton3** (2022): Neoverse V1，DDR5，bfloat16，性能比 Graviton2 提升最高达 60%
  - **Graviton4** (2024): Neoverse V2，96 核，每瓦性能是 Graviton3 的 2.7 倍
- **用途**：为 **约 30–40% 的 AWS EC2 工作负载**（尤其是容器、微服务、数据库）提供动力

#### 2. **AWS Inferentia (AI 推理)**
- **Inferentia2** (2023): 性能是 Inferentia1 的 4 倍，支持 FP16/BF16/INT8
- 针对**实时推理**（推荐引擎、语音、视觉）优化
- 用于 **SageMaker**、**EC2 Inf2**

#### 3. **AWS Trainium (AI 训练)**
- **Trainium2** (2024 年发布，2025 年出货): 训练性能是 Trainium1 的 4 倍
- 旨在与 **NVIDIA H100** 竞争 LLM 训练
- 支持**万亿参数模型**，高带宽内存 (HBM)

#### 4. **Nitro 系统 (智能网卡 / DPU)**
- 带有硬件加速器的定制 ARM SoC
- 卸载管理程序、网络、存储、加密功能
- 在虚拟化环境中实现**裸机性能**

---

### Annapurna 为何重要

- **成本与效率**：AWS 声称其**价格性能比 x86 高出最多 40%**
- **垂直整合**：亚马逊控制芯片 → 创新更快，成本更低
- **AI 推进**：Trainium/Inferentia 直接挑战 NVIDIA 在云 AI 领域的统治地位
- **供应链韧性**：减少对仅依赖 Intel/TSMC 供应链的依赖

---

### 总结

> **Annapurna Labs = AWS 的秘密芯片武器。**
> 他们构建了**基于 ARM 的 Graviton CPU**、**Inferentia（推理）**、**Trainium（训练）** 以及 **Nitro 卸载芯片**——所有这些都针对云进行了优化。
> 这些芯片为**更便宜、更快、更环保**的 AWS 服务提供动力，也是 AWS 能够在扩展 AI 的同时在价格上低于竞争对手的关键原因。

如果您想深入了解任何特定芯片（例如，Graviton4 与 Apple M4，Trainium2 与 H100），请告诉我。
