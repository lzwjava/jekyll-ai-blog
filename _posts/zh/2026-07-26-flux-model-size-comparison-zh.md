---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FLUX模型尺寸对比
translated: true
type: note
---

以下是两者的对比：

## 🔄 FLUX.2-dev 对比 FLUX.1-dev

| 特性 | FLUX.2-dev | FLUX.1-dev |
| --------- | ----------- | ----------- |
| **总大小** | **约 177 GB** | **约 69 GB** |
| **流程** | `图像到图像` | `文本到图像` |
| **需要授权** | ✅ 自动 | ✅ 自动 |
| **下载量** | 130万 | 56.9万 |
| **点赞数** | 1,941 | 13,786 |

FLUX.1-dev 体积**小得多**（69 GB 对比 177 GB），因为它使用了：

- 单文件 T5 文本编码器（而非 2-dev 中的10个分片）
- CLIP text_encoder_2（2个分片）
- 3个分片的 Transformer（而非 2-dev 中的7个分片）
- 更简单的 VAE（无独立的 `ae.safetensors`）

**不过**，两者均**需要授权**——你仍然需要：

1. 在 <https://huggingface.co/black-forest-labs/FLUX.1-dev> 接受许可协议
2. 提供 HuggingFace **读取令牌**

如果你已经接受了 FLUX.1-dev 的许可协议，我可以立即开始下载。你想选择哪一个？
