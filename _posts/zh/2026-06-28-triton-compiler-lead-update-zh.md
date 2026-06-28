---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Triton 编译器负责人更新
translated: true
type: note
---

让我搜索一下当前的相关信息。**问题：** Philippe Tillet（Triton 的作者）目前在做什么？

**回答：**

Philippe Tillet 仍在 OpenAI 担任技术团队成员，领导 Triton 编译器项目。他常驻圣地亚哥，拥有约 13 年在高性能机器学习系统、编译器工程和 GPU 内核优化方面的经验。以下是他的职业轨迹和当前工作重点的简要回顾：

**背景。** 他于 2011 年作为 ViennaCL 贡献者开始接触 GPU，2012 年获得 Telecom SudParis 学士学位，2014 年获得台湾国立交通大学硕士学位，2020 年获得哈佛大学博士学位，博士论文主题为 GPU 上分块算法的编译器。他于 2020 年全职加入 OpenAI，致力于 Triton 项目——该项目始于 2018 年，源于他对用 CUDA 编写矩阵乘法自动调优器的不满。

**当前工作——对您而言值得关注的要点：**

1. **Triton 在定制芯片上的应用。** 这是近期最有趣的信号。他正在扩大 OpenAI 的 Triton 编译器团队，并招聘工程师以提升 OpenAI 自研第一方加速器上的性能。这证实了 OpenAI 将 Triton 作为其自家芯片（与 Broadcom 合作的硬件）的内核编写层，而不仅限于 NVIDIA——这是一项硬件可移植性策略，如果您关注 MoE/推理优化栈的走向，这一点非常重要。

2. **Blackwell 支持。** 他于 2025 年初发表了题为“Blackwell Programming for the Masses with OpenAI Triton”的演讲，涵盖了 CUDA-C++ 与 XLA/Torch 的权衡空间，以及新的 TMA 风格 API（如用于 Blackwell 上分块 GEMM 的 `tl.make_tensor_descriptor`）。该演讲深入探讨了实际硬件限制——例如在 H100 上，`wgmma.sync` 无法区分 QK 和 PV MMA，因此无法独立进行流水线处理（这与 FlashAttention 内核调度直接相关）。

3. **研究成果。** 他与博士生 Nasib Ullah、Jinbin Zhang 和 Erik Schultheis 合作发表了一篇 ICML 2025 论文（ELMO），关于大型输出空间模型的纯 16 位和 8 位训练，利用融合的 Triton 内核将峰值 GPU 内存从约 40GB 降低到约 6GB（基于一个包含 300 万项目的推荐数据集）。

**这对您的职业发展为何重要：** Triton 在定制加速器上的应用方向值得深入关注。如果您正朝着推理优化和 GPU 计算方向发展，Triton 正日益成为可移植的内核中间表示层——而 OpenAI 将其押注在自己的 ASIC 上（正如 AMD 已经维护了一个 [ROCm Triton 分支](https://github.com/ROCm/triton)，您可以在 MI300X 上使用它），这意味着用 Triton 编写的内核技能在不同硬件供应商之间具有叠加效应，这是 CUDA 所不具备的。建议您直接对照 MI300X 研究 Triton 教程，了解 ROCm 后端代码生成与 NVIDIA 路径的差异。

**参考文献：**

- [Philippe Tillet — LinkedIn](https://www.linkedin.com/in/philippe-tillet-809b5536/)
- [作者：Philippe Tillet — NVIDIA 技术博客](https://developer.nvidia.com/blog/author/philopenai/)
- [Blackwell Programming for the Masses with OpenAI Triton（幻灯片 PDF）](https://semianalysis.com/wp-content/uploads/2025/03/Blackwell-Programming-for-the-Masses-With-OpenAI-Triton-Phil-Tillet.pdf)
- [getprog.ai 档案 — Philippe Tillet](https://getprog.ai/profile/614788)
- [ptillet — GitHub](https://github.com/ptillet)