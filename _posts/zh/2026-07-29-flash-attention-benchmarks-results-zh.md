---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Flash-Attention 基准测试结果
translated: true
type: note
---

以下是启用 flash-attention 后的完整基准测试结果：

---

## ⚡ Flash-Attention 基准测试（Qwen3-0.6B，RTX 4070）

| 工作负载 | 吞吐量 |
| ---------- | -------- |
| **预填充** — 8 序列 × 1024 token | **19,548 tok/s** |
| **解码** — 8 序列 × 512 token | **1,389 tok/s** |
| **解码** — 16 序列 × 256 token | **2,307 tok/s** |
| **混合** — 16 序列（可变长度） | **1,660 tok/s** |
| **2 序列 × 256 token**（对等对比） | **357 tok/s** |
| **64 序列 × 512 token**（最大吞吐） | **646 tok/s** |

### 与之前（PyTorch SDPA）对比

| 指标 | 之前（SDPA） | 现在（FlashAttn） | 加速比 |
| ------ | ------------- | ------------------ | -------- |
| 预填充 | 506 tok/s | **19,548 tok/s** | **约 38 倍** |
| 解码（2 序列） | 约 4–30 tok/s | **357 tok/s** | **约 12–89 倍** |

Flash-attention 消除了每个序列的因果掩码循环和 `transpose` 开销，采用融合内核，速度显著提升——尤其是在预填充阶段，大型矩阵乘法因内存高效的 flash 算法而获益最大。
