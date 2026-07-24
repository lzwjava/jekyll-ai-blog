---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD ROCm GPU 运行 FLUX.2-dev
translated: true
type: note
---

以下是完整的画面概览：

---

## ✅ GPU 确认 — AMD ROCm

| 组件 | 详情 |
| ----------- | -------- |
| **GPU** | **gfx1100**（RDNA 3 架构）—— 可能为 AMD Radeon PRO W7900 或云端分区的 Instinct |
| **显存** | **48 GB**（三星） |
| **ROCm** | v7.2.1（HIP 7.2.53211） |
| **驱动** | v6.16.13 |
| **PCIe** | Gen4 x16 @ 16GT/s |
| **功耗** | 上限 241W，当前 17W |
| **操作系统** | Ubuntu 24.04，Python 3.12.3 |
| **CPU** | AMD EPYC 9334 — 128 线程 |
| **内存** | 503 GB |

## 📦 PyTorch (ROCm 7.2) 可用

支持 ROCm 7.2 的官方 PyTorch wheels 可在 PyTorch 索引中找到：

```bash
pip install torch --index-url https://download.pytorch.org/whl/rocm7.2
```

可用版本：`2.13.0+rocm7.2`（最新）、`2.12.1`、`2.12.0`、`2.11.0`

## 🎨 FLUX.2-dev 能在此运行吗？

**完全可以。** 以下是详细说明：

### FLUX.2-dev 显存需求

| 组件 | 估算大小 | 备注 |
| ----------- | ----------- | ------- |
| 文本编码器 (T5-XXL) | ~10 GB | 仅加载一次，通常为 fp16 |
| Transformer (flux2-dev) | ~12-16 GB | bf16 权重 |
| VAE | ~1 GB | 极小 |
| **运行所需总计** | **~25-30 GB** | 默认 1024×1024 设置 |
| 推理开销 | ~2-4 GB | 中间激活值 |

### 你拥有 48 GB → ✅ 完全足够

还有余量用于 **更高分辨率**（如 1536×1536）或 **更大批处理尺寸**。

### 预期性能

| 硬件 | 每张图像耗时（1024×1024，4-step schnell / 28-step dev） |
| ---------- | ---------------------------------------------------------- |
| 你的 GPU（RDNA 3，48 GB） | ~3-10 秒/张（估计，与 RX 7900 XTX 类似） |
| NVIDIA A100（80 GB） | ~2-5 秒 |
| 仅 CPU（128 核） | 几分钟 |

### ⚠️ 一个注意事项

**FLUX.2-dev 是受限模型** —— 你需要一个 HuggingFace 令牌（需先在 huggingface.co 上接受许可协议）才能下载。

---

需要我在服务器上 **安装 PyTorch + diffusers 并测试 FLUX 推理** 吗？我需要执行以下步骤：

1. `pip install torch --index-url https://download.pytorch.org/whl/rocm7.2`
2. `pip install diffusers transformers accelerate sentencepiece`
3. 使用你的 HF 令牌登录并下载 FLUX.2-dev
