---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070 无法运行 GLM-5.3
translated: true
type: note
---

简短回答：**实际上不行。** 目标模型（GLM-5.3-Flash-NVFP4）有硬性要求，RTX 4070 无法满足：

**1. 显存不足（12 GB vs ~17+ GB 最低要求）**
即使是 `examples/serve_full.sh` 中最节省显存的配置，大致需要：

- 仅稠密（非专家）权重就需要约 17 GB
- 再加上常驻专家层、KV 缓存池、CUDA 开销等额外需求

仅稠密部分就已超过 4070 的 12 GB。本仓库中没有适合它的配置。

**2. NVFP4 需要 Blackwell（sm_100+）**
检查点已采用 NVFP4 量化。FP4 张量核心加速仅在 Blackwell 上存在；RTX 4070 是 Ada（sm_89）。此处的 `--nvfp4-backend auto` 和 Triton 内核均针对 Blackwell 的形状和带宽进行优化。即使你能在运行时反量化为 FP8/BF16，也会超出显存预算。

**3. 系统内存不足**
脚本预检要求 **≥138 GB MemAvailable**（129 GB 固定主机缓存用于卸载的专家层，加上引擎开销）。典型的 4070 机器只有 32–64 GB 内存。完整的专家集大小为 181 GB——必须存放在某处。

**4. PCIe 带宽也会使速度减半**
整个设计受限于 PCIe：参考平台使用 Gen5 x16（约 64 GB/s）。4070 是 Gen4 x16（约 32 GB/s），因此即使其他条件都满足，解码速度也只能达到测量值的一半左右。

**RTX 4070 *可能* 做到的事情：**

- 运行小得多的模型（上游 FreeToken 服务器本身与模型无关）
- 或许可以让一个较小的稠密模型完全驻留显存，或是一个带轻量卸载的小型 MoE——但这属于上游 FreeToken 的范畴，并非本补丁集优化的方向

如果你只能使用 12 GB 显存加常规内存，更适合的方案是直接运行 ~7–14B 的稠密模型（vLLM/llama.cpp），或者像 Qwen3-30B-A3B 这样的小型 MoE 并使用 CPU 卸载。
