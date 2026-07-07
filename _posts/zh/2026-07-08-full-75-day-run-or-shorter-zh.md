---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 7.5天全程运行还是更短？
translated: true
type: note
---

根据 MI300X 参考数据和 H200 规格粗略估算：

**约 7.5 天**（Chinchilla 最优规模，参数比为 20 倍，对应 290 亿 tokens）

详细分解：

- 760M 模型在 MI300X 上：68K tok/s，训练 152 亿 tokens 需 62 小时
- 1.45B 模型在 H200 上：**约 40-45K tok/s**（模型大 2 倍，但 FA3 更快）
- 290 亿 tokens ÷ 42K tok/s ≈ **180 小时 ≈ 7.5 天**

**可选方案：**

| 训练规模 | 数据量 | 预估时间 | 效果 |
| --- | --- | --- | --- |
| **Chinchilla (20 倍)** | 290 亿 tokens | ~7.5 天 | 最优 |
| **半 Chinchilla (10 倍)** | 145 亿 tokens | ~3.7 天 | 尚可 |
| **快速 (5 倍)** | 72.5 亿 tokens | ~1.9 天 | 粗略基准 |

或者选择更小的模型以加快迭代周期：

| 模型 | 参数量 | 时间（20× Chinchilla） |
| --- | --- | --- |
| d24 (MI300X 参考) | 760M | ~2.6 天 |
| d30 | **1.45B** | ~7.5 天 |
| d20 | 530M | ~1.9 天 |

要跑满 7.5 天还是选择更短的训练？
