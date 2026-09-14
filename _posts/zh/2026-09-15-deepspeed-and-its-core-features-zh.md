---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSpeed及其核心特性
translated: true
type: note
---

**问题：** 什么是 DeepSpeed，它的核心特性是什么？

**回答：**

**DeepSpeed** 是一个深度学习优化库，使分布式训练和推理变得简单、高效且有效。它由微软开发，采用 Apache 2.0 许可开源。

**核心创新**

DeepSpeed 的系统创新包括几项关键技术：

**ZeRO（零冗余优化器）** — 旗舰级内存优化技术。它将优化器状态、梯度和模型参数在 GPU 之间进行分区，从而大幅降低每个 GPU 的内存使用。有多个变体：
- **ZeRO-Offload** — 将优化器状态和梯度卸载到 CPU 内存，使数十亿参数的训练能够在较少的 GPU 上完成。
- **ZeRO-Infinity** — 将卸载扩展到 NVMe SSD，彻底打破 GPU 内存墙。
- **ZeRO++** — 减少巨型模型训练的集合通信开销。

**3D 并行** — 同时结合三种并行形式：
- 数据并行
- 张量（模型）并行
- 流水线并行

**Ulysses 序列并行** — 支持极长序列（数百万 token）的训练。

**DeepSpeed-MoE** — 针对混合专家模型的优化训练和推理。

**通信压缩** — 1-bit Adam 和 1-bit LAMB 等技术可减少分布式训练期间的通信开销。

**推理优化** — DeepSpeed Inference 可加速 Transformer 模型的大规模服务。

**关键能力**

- 支持全球最强大的语言模型，例如 **MT-530B** 和 **BLOOM（176B）**。
- 支持 NVIDIA、AMD、Intel Gaudi、Intel XPU 和华为昇腾 NPU 硬件。
- 与主流框架集成：HuggingFace Transformers、Accelerate、PyTorch Lightning、MosaicML 等。

**安装**

```bash
pip install deepspeed
ds_report  # 检查您机器上的兼容功能
```

**近期亮点（2025–2026）**
- **ZenFlow** — 用于 LLM 训练的无停滞卸载引擎。
- **SuperOffload** — 在超级芯片上进行大规模 LLM 训练（ASPLOS 2026 荣誉提名）。
- **DeepCompile** — 分布式训练的编译器优化。
- **AutoTP** — HuggingFace 模型的自动张量并行训练。

---

**参考：**
- [DeepSpeed GitHub 仓库](https://github.com/deepspeedai/DeepSpeed)
- [DeepSpeed 官方网站](https://www.deepspeed.ai/)
- [API 文档](https://deepspeed.readthedocs.io/en/latest/)
- [入门教程](https://www.deepspeed.ai/getting-started/)