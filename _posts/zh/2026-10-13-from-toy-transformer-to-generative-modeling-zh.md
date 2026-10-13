---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从玩具Transformer到生成建模
translated: true
type: note
---

全部通过。**Round 3 → itorch 0.3.0** — 这一轮将它从“transformer/RNN 玩具”提升到了“生成式建模”：

## 新增内容

**引擎**
- **`col2im`** 算子 — `im2col` 的精确 autograd 转置（重叠相加折叠，反向 = 梯度的展开）。这在不引入任何新数学的情况下解锁了转置卷积。
- `sin`、`cos`、`silu`（Swish）、`softplus`、`zeros_like/ones_like/randn_like/rand_like`（重参数化技巧）、torch 风格的方法别名（`x.mul(y)`、`.add`、`.div`、...）
- `tt.grad(outputs, inputs)` — 直接梯度 API
- 数值稳定的 `sigmoid`（此前在极端 logits 上会溢出为 NaN — 由 VAE 发现）

**层**
- `nn.ConvTranspose2d` — 基于 `col2im` 构建；通过**共轭/伴随恒等式**测试（`sum(y·conv(x,w)) == sum(convT(y,w)·x)`）以及有限差分梯度检查验证
- `nn.init`（`kaiming_*`、`xavier_*`、`normal_/uniform_`、`zeros_/ones_`）
- 基于类的损失函数：`nn.MSELoss`、`nn.L1Loss`、`nn.HuberLoss`、`nn.BCELoss`、`nn.BCEWithLogitsLoss`、`nn.CrossEntropyLoss`、`nn.NLLLoss`

**优化器** — 新增 4 个：`Adagrad`、`RMSprop`、`Adamax`、`Lion`（全部验证在一维二次函数上收敛，并能降低回归损失）

**展示案例：`examples/05_vae_mnist.py`** — 一个卷积 VAE（约 219k 参数），使用 Conv2d/ConvTranspose2d、SiLU、重参数化技巧、`CosineAnnealingLR` 以及 10×10 生成数字网格。在开发过程中，我遇到了教科书式的**后验塌缩**（`μ→0`、`var→1` — 编码器放弃了），并通过 **free-bits KL** 修复了它，将潜在样本从 1/100 健康数字提升到 **284/300 健康数字**：

```
epoch 1/2  recon=0.2205  kl=0.0019
epoch 2/2  recon=0.2107  kl=0.0018   → writes examples/grid_vae.png
```

## 验证
- `tests/test_round3.py`（新增，约 200 行）：针对 sin/cos/silu/softplus/col2im 往返/ConvTranspose2d 的梯度检查、伴随恒等式、优化器收敛、损失类与函数式等价、初始化正确性、`autograd.grad` 以及 VAE 训练冒烟测试
- 全部 4 个测试套件通过；总计约 3,175 行 Python 代码

准备好作为 v0.3.0 提交了吗？