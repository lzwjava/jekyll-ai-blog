---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 完成！nano-vllm 正在使用 flash-attention 运行
translated: true
type: note
---

✅ **完成！** nano-vllm 正在运行，已启用 flash-attention。

以下是完成内容的完整摘要：

---

## 发生了什么

### 1. 安装了 `flash-attn==2.8.3`（预编译版）

- 避免了 20 分钟以上的 CUDA 编译
- 使用了 `cu13torch2.10` 预编译包 — CUDA 13.0 与你的 PyTorch 2.11.0+cu130 匹配
- 导入验证通过 ✓

### 2. 将注意力机制改为直接使用 flash-attn

**文件：** `/mnt/data/nano-vllm/nanovllm/layers/attention.py`

| 之前 | 之后 |
| -------- | ------- |
| `F.scaled_dot_product_attention` | `flash_attn_func` |
| 手动逐序列因果掩码循环 | `flash_attn_varlen_func` |
| 转置 (batch, heads, seq, dim) | 原生 (batch, seq, heads, dim) |

### 3. 运行推理 ✅

**模型：** Qwen3-0.6B 在 RTX 4070 上

| 指标 | 数值 |
| -------- | ------- |
| Prefill | 506 tok/s |
| Decode | ~4–30 tok/s |
| 提示 | 2 条，每条 256 个 token |
| 结果 | 两个生成结果均正确 ✓ |
