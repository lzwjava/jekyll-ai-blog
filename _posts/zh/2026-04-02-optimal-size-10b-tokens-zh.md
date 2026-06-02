---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 10B 令牌的最优模型规模
translated: true
type: note
---

在 H200 上针对 **10B tokens**：

**124M** → 太小了。你将有每个参数 ~80,000 个 tokens — 远多于所需，你会 **overfit** 或只是记忆。浪费 GPU。

**500M** → 更好，但根据 Chinchilla scaling laws 仍然偏小。对于 10B tokens，最优大小更接近 **1B-2B**。

**我的选择：** 选择 **1B 或 1.5B** — 你有足够的 VRAM。以 `bf16` 混合精度，1.5B 模型应该能舒适地在 H200 上运行，并留有空间支持不错的 batch size。

1.5B 的快速内存估算：

- Weights: ~3GB (bf16)
- Adam states: ~12GB
- Gradients + activations: ~20-30GB
- **总计：~40-50GB** — 绰绰有余

要我从 nanoGPT examples 中拉一个 1.5B 的 config 吗？
