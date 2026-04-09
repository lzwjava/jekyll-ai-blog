---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DGX Spark处理器核心配置
translated: true
type: note
---

问题：上个月发布的新版英伟达DGX OS是什么？在英伟达DGX Spark或类似系统的语境中，“10 Cortex”和“CPU中的10 Cortex”这两个数字是否必须一致？它们分别代表什么含义？

答案：

英伟达DGX OS是一款专为英伟达DGX系统定制的Linux发行版（基于Ubuntu）。它预装了优化的驱动程序、完整的英伟达AI软件栈（包括CUDA、cuDNN、TensorRT等）、诊断工具以及针对AI、机器学习和分析工作负载进行稳定性与高性能优化的平台专属配置。近期版本（如DGX OS 7.x系列）支持包括DGX Spark在内的最新硬件。本质上，这是经过调优的Ubuntu Linux版本，深度融合了英伟达的增强功能，以在其基于Grace Blackwell的平台上实现更好的兼容性与性能。

你提到的“10 Cortex”和“CPU中的10 Cortex”指的是**英伟达DGX Spark**（亦称GB10 Grace Blackwell超级芯片系统）的CPU配置——这是一款于2025-2026年初发布的紧凑型桌面AI超级计算机。这里的“10 Cortex”并非通用概念，具体指：

- **10个Cortex-X925核心**：这些是高性能Arm Cortex-X925 CPU核心（大核）。专为最大化单线程与多线程性能设计，用于处理AI数据预处理、任务编排、令牌化、模型微调及高计算强度工作负载等 demanding 任务。它们以更高时钟频率运行，承担系统中的“重负载”计算。

- **10个Cortex-A725核心**：这些是高能效Arm Cortex-A725 CPU核心（小核）。专注于能效优化与轻量后台或并行任务，协助系统整体调度、处理较小工作负载，并在大核处理密集型任务时降低功耗。

两者共同构成GB10超级芯片中Grace部分的**20核Armv9混合架构（big.LITTLE）CPU**。该CPU与集成的Blackwell GPU共享128 GB统一LPDDR5x内存。此类big.LITTLE设计在现代基于Arm的处理器（如智能手机或高端SoC中常见）中普遍采用，以实现性能与能效的平衡。

一般而言，Arm big.LITTLE架构设计中**核心数量无需对称**——许多配置采用非对称设计（例如8个大核+4个小核）。但在DGX Spark/GB10的特定设计中，英伟达选择了平衡的**10+10**配置，以在桌面级系统中实现AI工作负载的最优处理。这种设计在紧凑形态下提供了强劲性能，同时避免了过高功耗或发热。

简言之：
- 两个“10”指这款20核Arm CPU中每种核心类型的数量。
- Cortex-X925 = 性能导向核心。
- Cortex-A725 = 能效导向核心。

此配置搭配强大的Blackwell GPU（最高达1 petaFLOP的FP4 AI性能），使DGX Spark适用于本地AI开发、运行大型模型（最高约2000亿参数）、推理以及机器人/计算机视觉任务。

若在DGX Spark运行DGX OS的系统规格、日志或`lscpu`/`cat /proc/cpuinfo`输出中看到这些参数，其所指正是上述内容。

参考文献：  
- https://docs.nvidia.com/dgx/dgx-spark/hardware.html  
- https://www.nvidia.com/en-us/products/workstations/dgx-spark/  
- https://newsroom.arm.com/blog/arm-nvidia-dgx-spark-high-performance-ai