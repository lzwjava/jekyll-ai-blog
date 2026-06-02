---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: AdamW 优化器简介
translated: true
type: note
---

Question: 什么是 AdamW Optimizer 的详细介绍？

Answer:

### AdamW Optimizer 简介

**AdamW** 是深度学习中广泛使用的 Adam (Adaptive Moment Estimation) optimizer 的变体。它的引入是为了解决标准 Adam 在处理 weight regularization 时的局限性，从而提高模型的 generalization 能力和性能，特别是在像 transformers 这样的大规模模型中。

AdamW 代表 "Adam with decoupled Weight decay"，基于 Ilya Loshchilov 和 Frank Hutter (2019) 撰写的论文 *"Decoupled Weight Decay Regularization"*。

### 背景：Adam Optimizer

要理解 AdamW，首先回顾一下 Adam：

- Adam 结合了 Momentum（使用 first moment：过去 gradient 的指数衰减平均值）和 RMSProp（使用 second moment：过去 gradient 平方的指数衰减平均值）的思想。
- 它为每个参数计算 adaptive learning rates。
- 更新规则（简化版）为：

  1. 计算 gradient \\( g_t \\)
  2. 更新 biased first moment：\\( m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t \\)
  3. 更新 biased second moment：\\( v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2 \\)
  4. Bias-correct：\\( \hat{m}_t = m_t / (1 - \beta_1^t) \\)，\\( \hat{v}_t = v_t / (1 - \beta_2^t) \\)
  5. 更新参数：\\( \theta_{t+1} = \theta_t - \eta \cdot \hat{m}_t / (\sqrt{\hat{v}_t} + \epsilon) \\)

典型 hyperparameters：\\( \eta = 0.001 \\)，\\( \beta_1 = 0.9 \\)，\\( \beta_2 = 0.999 \\)，\\( \epsilon = 10^{-8} \\)。

Adam 非常高效且几乎不需要 hyperparameter tuning，但它有时在 generalization 方面不如传统的 SGD with momentum，尤其是在需要强 regularization 的情况下。

### Adam 中 Weight Decay 的问题

Weight decay 是一种常见的 regularization 技术，通过惩罚过大的 weights 来防止 overfitting（在 SGD 中等同于 L2 regularization）。

- 在标准 SGD 中，将 L2 regularization 添加到 loss 中在数学上等同于 "weight decay"（直接缩减参数：\\( \theta \leftarrow \theta (1 - \eta \lambda) - \eta g \\)）。
- 然而，在像 Adam 这样的 adaptive optimizers 中，两者**并不等价**。
- Adam 的大多数早期实现通过 L2 regularization 添加 weight decay（修改 gradient：\\( g_t \leftarrow g_t + \lambda \theta_t \\)），但这会干扰 Adam 的 adaptive learning rates。
- 这种耦合使得有效的 regularization 取决于 learning rate，导致次优的 generalization。

### AdamW 的核心创新：Decoupled Weight Decay

AdamW 通过将 weight decay 从 gradient 更新中**解耦 (decoupling)** 来修复这个问题：

- 照常执行 Adam 更新（仅针对 loss gradient）。
- 然后，将 weight decay 直接应用于参数。

参数更新变为：

\\[ \theta_{t+1} = \theta_t - \eta_t \cdot \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} - \lambda \eta_t \cdot \theta_t \\]

（或者等效地，先执行 decay：\\( \theta_t \leftarrow \theta_t (1 - \lambda \eta_t) \\)，然后再进行 Adam 步骤）。

这使得 weight decay 的行为就像真正的 SGD weight decay 一样：独立于 adaptive 机制，且最优的 \\( \lambda \\) 与 learning rate \\( \eta \\) 的相关性更低。

### AdamW 的优势

- **更好的 Generalization**：与使用 L2 的标准 Adam 相比，显著减少了 overfitting。
- **提升性能**：在图像分类等任务上（如 CIFAR-10/100, ImageNet），其表现可以媲美甚至超过 SGD with momentum。
- **训练稳定**：能很好地配合 learning rate schedules（如 cosine annealing, warm restarts）。
- **解耦的 Hyperparameters**：更容易分别调整 learning rate 和 weight decay。
- **广泛应用**：在现代模型中被广泛采用，BERT, ViT, GPT 系列以及大多数基于 transformer 的架构都使用 AdamW。

### 使用方法与 Hyperparameters

在 PyTorch 和 TensorFlow/Keras 等库中：

- 典型设置：learning rate \\( 10^{-4} \\) 到 \\( 10^{-3} \\)，weight decay \\( 0.01 \\) 到 \\( 0.05 \\)。
- 通常与 learning rate warm-up 和 decay schedules 结合使用。

PyTorch 示例：

```python
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)
```

### 何时使用 AdamW

- 对于大多数监督学习深度学习任务，特别是对于大模型或 regularization 至关重要时，AdamW 优于普通 Adam。
- 它依然保留了 Adam 这种 adaptive 且 robust 的特性，但具备更好的 regularization 属性。

总之，AdamW 是对 Adam 的一个简单却强大的改进，已成为许多 state-of-the-art 深度学习流程中的默认 optimizer。

参考文献：

- [Decoupled Weight Decay Regularization (原始论文)](https://arxiv.org/abs/1711.05101)
- [PyTorch AdamW 文档](https://pytorch.org/docs/stable/generated/torch.optim.AdamW.html)
- [Keras AdamW 文档](https://keras.io/api/optimizers/adamw/)
