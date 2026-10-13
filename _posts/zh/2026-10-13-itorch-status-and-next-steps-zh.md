---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Itorch 状态与下一步
translated: true
type: note
---

现在是盘点的好时机。以下是 itorch 的现状以及我接下来会做的事情：

## 当前状态
- **引擎**：完整自动微分（25+ 个算子，im2col/col2im，广播，切片，gather），`grad_fn`，`retain_graph`，`tt.grad`
- **层**：CNN / Transformer / RNN / VAE 工具包全部通过有限差分梯度检查验证
- **7 个优化器 + 4 个调度器**，损失函数，DataLoader，`nn.init`，保存/加载
- **4 个测试套件，5 个示例**（98.3% MNIST CNN，char-GPT，数字生成 VAE）

## 真正缺失的部分 — 按优先级排序

**1. 性能（最大缺口）。即时自动微分每一步都会重建算子元数据。**
- `@tt.jit` — tinygrad 风格：只追踪一次前向传播，缓存算子计划，每次迭代用新的叶子数据复用。训练循环轻松获得 2–5× 加速。
- `tt.profile(ops=True)` — 反向传播中每个算子的耗时统计。

**2. 自动微分完整性（解锁真正的 SOTA 模型移植）。**
- `einsum` 算子（一个算子 = 批量矩阵乘法/注意力/缩并，带正确梯度），
- `scatter`/`index_put_`/`masked_fill`/`repeat`/`tile`（外加 `nn.Parameter` 以实现与 torch 对齐）。

**3. 对抗训练验证（这是最后一个未测试的主要训练范式）。**
- **MNIST 上的 DCGAN** — 生成器基于现有 `ConvTranspose2d` 构建，BCE + 实际最小最大优化，采样网格。如果 GAN 能训练起来，说明引擎真正具有通用性。

**4. 门面与开发者体验。**
- 导出 `tt.autograd.gradcheck()` 以便用户验证自定义层，
- CIFAR-10 加载器 + 使用 `ReduceLROnPlateau` 的数据增强示例，
- `nn.Parameter`，模型 FLOP 计数器。

## 我的建议
接下来做 **1 + 3 + gradcheck**（`@tt.jit` + DCGAN + 那个工具）— 这是最高杠杆组合：性能、一种新的训练范式，以及一个面向用户的调试工具。然后做 **2**（einsum/scatter）以补齐完整性。

要我按这个方案继续吗？