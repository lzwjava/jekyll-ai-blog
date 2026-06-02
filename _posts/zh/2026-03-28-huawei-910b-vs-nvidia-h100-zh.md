---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华为 910B 与 NVIDIA H100 的对比
translated: true
type: note
---

问题：Huawei Ascend 910B 与 NVIDIA H100 相比如何（一个是约 320 TFLOPS，另一个是约 989 TFLOPS）？以及需要多少块 RTX 4070 才能等同一块 H100？

回答：

## Huawei Ascend 910B vs NVIDIA H100

首先，让我们澄清一下你提到的数字：

| Chip | FP16 TFLOPS | Notes |
|---|---|---|
| **Huawei Ascend 910B** | ~320–600 TFLOPS | Huawei 未发布官方 Spec；估计值差异很大 |
| **NVIDIA H100** | ~989 TFLOPS (SXM5) | NVIDIA 官方 Spec |
| **RTX 4070** | ~58.2 TFLOPS | 你的服务器 GPU |

> **为何 910B 的范围很模糊：** Huawei Ascend 910B 声称在 310W 功耗下具备高达 320 TFLOPS 的 FP16 计算能力。然而，Huawei 并没有发布 Ascend 910B 的详细 Spec —— 一些来源估计为 ~600 TFLOPS FP16，这是技术分析中经常引用的数字。320 TFLOPS 的数字可能指的是特定的配置或单 Die 的 Spec。

---

## 正面交锋：910B vs H100

910B 的计算能力约为 H100 的 60%，Memory Bandwidth 约为 36%，且软件生态系统比 CUDA 落后多年。

910B 的性能大致与 A100 平齐 —— 后者是 Nvidia 2020 年的旗舰芯片。一名 Huawei 官员甚至声称，在 2024 年的一些 Training 任务中，910B 的表现超过 A100 约 20%。但该芯片仍依赖较旧的 HBM2E Memory，显存容量比 H100 少约三分之一，且芯片间的数据传输速度慢约 40%。

简而言之：

- **Raw TFLOPS 差距：** 取决于使用 320 还是 600 TFLOPS 的估算值，H100 大约比 910B **快 1.6x – 3x**。
- **真实场景 Training 差距：** 对于大 Batch Size 的 Compute-bound 训练，由于 H100 更高的计算能力和 Memory Bandwidth 产生的叠加效应，差距更接近 2.5 – 3x。对于较小的模型和受显存容量限制的 Inference，差距缩小到 1.5 – 2x。
- **Process Node 差距：** Ascend 910B 依赖 7nm 制程技术，而 Nvidia H100 采用 4nm 技术生产 —— 领先了数代。

---

## 需要多少块 RTX 4070 才能等同一块 H100？

使用 **Raw FP16 TFLOPS**（理论峰值）计算：

| Target | TFLOPS needed | RTX 4070 FP16 | Cards needed |
|---|---|---|---|
| Match H100 (~989 TFLOPS FP16) | 989 | 58.2 | **~17 张卡** |
| Match 910B (~320 TFLOPS) | 320 | 58.2 | **~6 张卡** |
| Match 910B (~600 TFLOPS) | 600 | 58.2 | **~11 张卡** |

所以：仅从纸面上的 TFLOPS 数值计算，**≈17 块 RTX 4070s ≈ 1 块 H100**。

> ⚠️ **但这在实践中具有误导性。** Raw TFLOPS 并不等于实际的 Training 性能。H100 拥有：
> - **HBM3 Memory**，具备 3.35 TB/s 带宽（对比 4070 的 GDDR6X 约为 504 GB/s）
> - **NVLink** 用于多 GPU 扩展
> - 在大规模 Batch Size 下的 **Tensor Core 效率**
> - **80GB VRAM**（对比 4070 的 12GB）
>
> 你不能简单地将 17 块消费级 GPU 串联起来就等效于一块 H100。VRAM 大小、Memory Bandwidth 和 Interconnect 才是 LLM 工作的实际瓶颈。你那块拥有 12GB VRAM 的单块 4070 甚至无法在 FP16 精度下容纳 30B 参数的模型 —— 而一块 H100 可以在单卡上运行 70B+ 的模型。

---

## 总结

| Metric | 910B vs H100 | 4070 vs H100 |
|---|---|---|
| Raw FP16 | 约为 H100 的 33–60% | 约为 H100 的 6% |
| Real-world LLM training | 约为 H100 的 33–66% | 不具可比性 (受 VRAM 限制) |
| Cards to match H100 (paper) | ~2–3 块 910B | ~17 块 RTX 4070 |
| Practical scalability | 是 (Data Center 级) | 否 (消费级 GPU) |

你的 `lzw-server` 中的 RTX 4070 对于小模型（7B–13B 量化版）的本地 Inference 是非常出色的 GPU，但对于 H100 级别的工作，你面对的是完全不同级别的硬件。

参考资料：

- [Huawei Ascend 910B specs and analysis](https://awesomeagents.ai/hardware/huawei-ascend-910b/)
- [Huawei Ascend 910C vs NVIDIA H100 comparison](https://www.nexgen-compute.com/blog/huawei-ascend-910c-vs-nvidia-h100-ai-chip-comparison)
- [China's AI Chip Race — IEEE Spectrum](https://spectrum.ieee.org/china-ai-chip)
- [Huawei 910B challenges NVIDIA — TrendForce](https://www.trendforce.com/news/2024/06/11/news-huaweis-self-developed-ai-chip-challenges-nvidia-boasting-its-ascend-910b-to-be-equal-in-match-with-a100/)
