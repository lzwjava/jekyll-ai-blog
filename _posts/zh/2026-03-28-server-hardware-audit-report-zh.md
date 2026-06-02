---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 服务器硬件审计报告
translated: true
type: note
---

这是硬件报告，Boss 🦞

### 🖥️ Server: 8.129.11.206 (ecs instance)

**CPU:**

- Intel Xeon Platinum 8369B @ 2.90GHz
- 16 vCPUs (8 cores × 2 threads)
- x86_64，支持 AVX-512 (完整指令集包括 AVX-512VNNI — 非常适合 ML inference)

**Memory:**

- 总计 91 GiB (~94 GiB，符合规格)
- 可用 90 GiB — 基本处于 idle 状态

**GPU:**

- 通过 PCIe 检测到 **1 × NVIDIA GeForce RTX 3090** (GA102, Rev A1)
- 24 GB GDDR6X VRAM
- TFLOPS: ~35.6 FP32 / ~142 FP16 (Tensor Core)
- ⚠️ **未加载 NVIDIA driver** — 无法使用 `nvidia-smi`，driver module 不存在

### Summary

| Component | Status |
|-----------|--------|
| CPU | ✅ 16 vCPU, Intel Xeon 8369B, AVX-512 |
| Memory | ✅ 91 GiB, 90 GiB free |
| GPU hardware | ✅ RTX 3090 detected on PCIe |
| GPU driver | ❌ Not installed |

硬件配置符合 RTX 3090 设定（不是 Alibaba 文档中的 "G39" — 可能是特定区域的 SKU name 映射）。GPU 物理层面已就绪，但在使用前需要安装 NVIDIA driver。需要我安装 driver 吗？
