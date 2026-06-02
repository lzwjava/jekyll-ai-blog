---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于100亿token训练的GPT-2小型
translated: true
type: note
---

这是 **GPT-2 small (124M)** — 不是 medium。

- `n_layer=12, n_head=12, n_embd=768` → GPT-2 small（1.24亿参数）
- 批次：4 × 1024 × 128 梯度累积 = 每步 524,288 个 token
- 19,073 次迭代 × 524K ≈ **100亿训练 token**
- 尽管文件名是 `gpt3`，其架构实际上是 GPT-2 small，采用了 GPT-3 风格的 100亿 token 训练方案

供参考（你不需要运行这些）：
- medium：24L / 16H / 1024d（3.5亿）
- large：36L / 20H / 1280d（7.74亿）
- XL：48L / 25H / 1600d（15亿）
