---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 下载177GB的Gated FLUX模型
translated: true
type: note
---

`hf-mirror.com` 可访问！模型总大小为 **177 GB**。详细信息如下：

---

## 📦 FLUX.2-dev — 模型信息

| 属性 | 值 |
| ---------- | ------- |
| **模型** | `black-forest-labs/FLUX.2-dev` |
| **流水线** | `Flux2Pipeline` (diffusers) |
| **总大小** | **177 GB** |
| **受限访问** | ✅ 是 — 需要 HF 令牌 + 许可协议接受 |
| **磁盘空间** | 2.9T 可用 ✅ |
| **镜像站** | `hf-mirror.com` (可访问 ✅) |

### 文件详情

- `ae.safetensors` — 自编码器
- `flux2-dev.safetensors` — FLUX 主模型
- `text_encoder/model-00001~10-of-00010.safetensors` — T5 文本编码器（约10个分片）
- `transformer/diffusion_pytorch_model-00001~07-of-00007.safetensors` — Transformer（约7个分片）
- `vae/diffusion_pytorch_model.safetensors` — VAE

### 问题：模型为**受限访问**

您需要执行以下操作：

1. 前往 <https://huggingface.co/black-forest-labs/FLUX.2-dev> **接受许可协议**（点击"同意"）
2. 从 <https://huggingface.co/settings/tokens> 获取 **HF 令牌**（只读权限即可）
3. 将令牌提供给我们，以便通过 `huggingface-cli login --token YOUR_TOKEN` 登录

您准备好 HuggingFace 令牌了吗？如果已准备就绪，我将：

1. 创建一个 `tmux` 会话
2. 编写包含 `HF_ENDPOINT=https://hf-mirror.com` 的下载脚本
3. 开始下载至 `/root/FLUX.2-dev` 目录
