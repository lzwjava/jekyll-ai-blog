---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD ROCm开源GPU软件栈
translated: true
type: note
---

## AMD ROCm — 简介

### 什么是 ROCm？

ROCm（Radeon Open Compute）是一个主要基于开源软件构建的开放计算栈，专为图形处理器（GPU）计算而设计。它包含一系列驱动程序、开发工具和API，支持从底层内核到最终用户应用的GPU编程。

ROCm针对生成式AI和HPC应用进行了优化，旨在简化现有代码的迁移过程。

---

### 核心技术：HIP

ROCm基于AMD的异构接口可移植性（HIP）构建，这是一个开源的C++ GPU编程环境及其对应的运行时。HIP允许ROCm开发者在不同平台上创建可移植应用，代码可部署在从专用游戏GPU到百亿亿级HPC集群的多种平台上。

---

### 主要应用场景

ROCm尤其适用于GPU加速的高性能计算（HPC）、人工智能（AI）、科学计算和计算机辅助设计（CAD）。

---

### 编程模型与框架支持

ROCm支持多种编程语言和编程接口，如HIP、OpenCL和OpenMP。它还是一个开源软件平台，经优化可从AMD Instinct GPU和AMD Radeon GPU中挖掘HPC和AI工作负载性能，同时保持与行业软件框架的兼容性。

ROCm已完全集成到PyTorch和TensorFlow等机器学习框架中，并支持所有AMD Instinct™加速器型号。

---

### 硬件支持

ROCm支持所有AMD Instinct™加速器型号，且部分ROCm功能支持特定AMD Radeon™显卡。最新版本提供对AMD Instinct™ MI350系列GPU的全面支持、基于开源框架的分布式推理、企业级AI工具，以及对FP6和FP4新数据类型的大规模模型支持。

---

### 平台扩展（2025–2026）

ROCm 7.2同时支持Linux和Windows环境——这与以往以Linux为中心的部署方式相比有了显著转变。AMD还确认了其与最新Ryzen AI 400处理器和Radeon AI PRO GPU的兼容性，并声称在关键AI模型上相比ROCm 6.4.4性能提升最高可达5倍。

---

### 实际规模：超级计算机

截至2024年11月，AMD为TOP500榜单上的156台超级计算机提供算力支持，较上一年增长29%。全球最快的超级计算机El Capitan在HPL基准测试中实现了1.742 exaflops的性能，其动力来自运行ROCm 6.0的AMD Instinct MI300A APU。

---

### 历史与里程碑

2026年恰逢ROCm AI计算栈问世十周年，AMD首席技术官Mark Papermaster指出，该计算栈最初面向HPC应用，如今已成为运行在全球最大超级计算机上的生产就绪型软件。

---

### 仓库速览

| 项目 | 详情 |
|------|---------|
| GitHub Star数 | 6.2k |
| Fork数 | 517 |
| 许可证 | MIT |
| 最新版本 | ROCm 7.2.0（2026年1月） |
| 主要语言 | Shell、Python、Makefile |
| 文档地址 | [rocm.docs.amd.com](https://rocm.docs.amd.com) |

参考来源：

- [AMD ROCm GitHub仓库](https://github.com/ROCm/ROCm)
- [AMD ROCm官方产品页面](https://www.amd.com/en/products/software/rocm.html)
- [ROCm官方文档](https://rocm.docs.amd.com/)
- [ROCm 7.2 Windows与Linux扩展 — Neowin](https://www.neowin.net/news/amd-rocm-open-source-nvidia-cuda-rival-gets-massive-windows--linux-improvements/)
- [AMD ROCm助力超级计算机](https://rocm.blogs.amd.com/ecosystems-and-partners/rocm-revisited-power/README.html)
- [ROCm在Radeon上支持Windows与Linux之路 — AMD博客](https://www.amd.com/en/blogs/2025/the-road-to-rocm-on-radeon-for-windows-and-linux.html)