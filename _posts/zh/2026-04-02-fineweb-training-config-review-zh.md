---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FineWeb 训练配置审查
translated: true
type: note
---

明白了。FineWeb sample-10BT（~10B tokens）的配置看起来很稳固。几点注意事项：

**优点：**
- `block_size = 1024` — FineWeb 正确
- `compile = True` — 良好的加速
- `bias = False` — LLaMA 风格，正确
- `weight_decay = 0.1` — 标准
- `beta2 = 0.99` — 合适

**注意这些：**
- `batch_size = 8` 与 `gradient_accumulation_steps = 64` → 有效 batch = 512。对于 125M 模型合理
- `max_iters = 12000` → block_size 1024 和 batch 8，每个 epoch ~98M tokens。对于 10B tokens 需要 ~100 次迭代才能看完所有数据一次... 等一下，实际上 `max_iters` 为 12k 时总共 ~98B tokens，这没问题因为 FineWeb 是 10B
- `dropout = 0.0` — 长时间运行可能过拟合，但干跑没问题

**一个建议：** `max_iters = 12000` 表示处理 ~98B tokens — 数据集大小的 10 倍。你可能想要 `max_iters = 100000` 或者让它运行直到 loss 趋于平稳。对于这个配置的 10B token 数据集，12k 迭代相当短。

总体来说：**这是一个好的起点**，但如果你想真正训练整个数据集，我建议大幅增加 `max_iters`。
