---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'DeepSpeed: 极大规模深度学习训练'
translated: true
type: note
---

## DeepSpeed — 微软的深度学习训练优化库

你现在身处 DeepSpeed 仓库（Microsoft/DeepSpeedAI）。该系统曾训练了 **MT-530B** 和 **BLOOM**——当时世界上最大的语言模型。

**核心使命**：在 PyTorch 上实现深度学习训练的极致速度与规模。

**关键创新**：

- **ZeRO**（零冗余优化器）——将优化器状态、梯度和参数分片到多个 GPU 上，而非复制。当前分支包含支持 AMD GPU 的 ZeRO-3 与 SDMA（系统 DMA）卸载。
- **ZeRO-Infinity**——卸载到 CPU/NVMe，实现超越 GPU 显存容量的训练。
- **3D 并行**——数据并行 + 流水线并行 + 张量并行。
- **DeepSpeed-MoE**——混合专家模型训练支持。
- **Ulysses 序列并行**——长上下文 LLM 训练。
- **DeepCompile**——分布式训练的编译器优化。
- **ZenFlow**——无阻塞卸载引擎。
- **SuperOffload**——ASLPOS 2026 荣誉提名，超级芯片上的卸载技术。

**为何使用它**：当需要训练一个无法放入单张 GPU 的模型时。DeepSpeed 处理分布式系统的复杂性，你只需编写标准的 PyTorch 前向/反向传播，由它管理分片、通信和内存。

**近期动态**（2026 年）：支持 Muon 优化器、ZeRO-3 集合通信的 SDMA、超级芯片的 SuperOffload、以及采用 PyTorch 风格反向传播的 DeepSpeed Core API。

你当前位于 `master` 分支，代码干净，包含最近两次 ZeRO 修复。项目使用 `setup.py`/`setup.cfg` + `pre-commit`（yapf+flake8）。如果你正在查看此仓库，很可能对大规模分布式训练的内部机制感兴趣——ZeRO 的梯度分桶、流水线调度或通信重叠。
