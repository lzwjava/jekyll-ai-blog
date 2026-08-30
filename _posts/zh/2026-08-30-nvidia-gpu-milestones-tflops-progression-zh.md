---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英伟达GPU里程碑TFLOPS演进
translated: true
type: note
---

现在我有了所有所需的数据。让我来构建一个图表和一张全面的表格。

**问题：** 英伟达 GPU 的关键里程碑有哪些？它们的 TFLOPS/PFLOPS 数据是多少？

**回答：**

以下是每代主要英伟达 GPU 的计算性能演进历程：该图表使用对数刻度，因为数值跨越了 4 个数量级。以下是详细的完整分解：

---

| GPU | 年份 | 架构 | FP32 TFLOPS | FP16 TFLOPS | 备注 |
| --- | --- | --- | --- | --- | --- |
| **GTX 980** | 2014 | Maxwell | ~5.1 | ~5.1 | 无 Tensor Core；FP16 = FP32 |
| **GTX 1080 Ti** | 2017 | Pascal | ~11.3 | ~11.3 | 首款 FP32 突破 10 TFLOPS |
| **RTX 2080 Ti** | 2018 | Turing | ~13.4 | ~107.9 (Tensor) | 首款硬件 RT + Tensor Core |
| **RTX 3080** | 2020 | Ampere | ~29.8 | ~119 (Tensor) | 相比 2080 Ti 提升约 2 倍 |
| **A100** | 2020 | Ampere | ~19.5 | ~312 (Tensor) | 数据中心；HBM2e；MIG |
| **H100** | 2022 | Hopper | ~67 | ~1,979 (Tensor) | Transformer Engine，FP8 |
| **H200** | 2024 | Hopper+ | ~67 | ~3,958 (Tensor FP8) | 141 GB HBM3e；与 H100 相同芯片 |
| **B200** | 2025 | Blackwell | ~75 | ~4,500 (FP16 Tensor) | 9 PFLOPS FP4；180 GB HBM3e |

---

几个关键观察点：

**FP32** 在十年间从约 5 TFLOPS 增长至约 75 TFLOPS——大约 **15 倍**。表现扎实，但相对温和。真正的爆发发生在 AI 精度格式上。

**FP16 Tensor** 从几乎为零增长到 B200 上的 4,500 TFLOPS FP8 密集计算，这大约是 **H100 的 1,979 TFLOPS 的 2.3 倍**，比 Maxwell 所能提供的性能高出数千倍。

**FP4（B200 的杀手锏）：** Tensor Core 性能达到 9 PFLOPS FP4 密集计算（采用 2:4 结构化稀疏时可达 18 PFLOPS）——这是一个全新的精度层级，H100 完全不支持。

**GB200 NVL72 机架** 整合了 72 个 B200，总 FP4 Tensor Core 性能达到 1,440 petaFLOPS——单个机架超过 1 exaFLOP。

---

**参考资料：**

- [NVIDIA B200 Specs & Benchmarks — Spheron](https://www.spheron.network/blog/nvidia-b200-complete-guide/)
- [NVIDIA B200 SXM Specs — Flopper.io](https://flopper.io/gpu/nvidia-b200-sxm-180gb)
- [NVIDIA Blackwell B200 Datasheet](https://www.primeline-solutions.com/media/categories/server/nach-gpu/nvidia-hgx-h200/nvidia-blackwell-b200-datasheet.pdf)
- [NVIDIA Data Center GPU Specs — IntuitionLabs](https://intuitionlabs.ai/articles/nvidia-data-center-gpu-specs)
- [Comparing Nvidia B200 and H100 — Civo](https://www.civo.com/blog/comparing-nvidia-b200-and-h100)
