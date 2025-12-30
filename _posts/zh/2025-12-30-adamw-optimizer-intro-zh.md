---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: AdamW 优化器简介与详解
translated: true
type: note
---

Question: What is a comprehensive introduction to the AdamW optimizer?

Answer: 

# Comprehensive Introduction to the AdamW Optimizer

AdamW optimizer 是 Adam optimizer 的一种流行变体，广泛应用于深度学习中的神经网络训练。它通过正确处理 **weight decay**（一种 regularization 形式）改进了标准的 Adam，从而带来了更好的 generalization，尤其是在像 transformers 这样的模型中。

AdamW 是由 Ilya Loshchilov 和 Frank Hutter 在 2017 年的论文 "Decoupled Weight Decay Regularization"（发表于 ICLR 2019）中提出的。"W" 代表 "Weight decay"，其核心创新是将 weight decay 与 adaptive learning rate 的更新进行 **decoupling**（解耦）。

## Background: The Adam Optimizer

Adam (Adaptive Moment Estimation) 由 Kingma 和 Ba 于 2014 年提出，是一种结合了 Momentum 和 RMSProp 思想的 adaptive gradient algorithm。

它维护两个 moving averages：
- **First moment**（梯度的均值，类似于 momentum）：\\( m_t \\)
- **Second moment**（梯度的未中心化方差）：\\( v_t \\)

Adam 的更新规则为：

1. 计算 gradient：\\( g_t = \nabla_\theta f_t(\theta_{t-1}) \\)

2. 更新有偏的 first moment：  
   \\( m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t \\)

3. 更新有偏的 second moment：  
   \\( v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2 \\)

4. Bias correction：  
   \\( \hat{m}_t = \frac{m_t}{1 - \beta_1^t} \\)  
   \\( \hat{v}_t = \frac{v_t}{1 - \beta_2^t} \\)

5. Parameter 更新：  
   \\( \theta_t = \theta_{t-1} - \eta \cdot \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} \\)

默认超参数：  
- Learning rate \\( \eta = 0.001 \\)  
- \\( \beta_1 = 0.9 \\)  
- \\( \beta_2 = 0.999 \\)  
- \\( \epsilon = 10^{-8} \\)

Adam 虽然高效且鲁棒，但在使用强 regularization 时，其 generalization 表现有时不如带有 momentum 的 SGD。

## The Problem with Weight Decay in Standard Adam

Weight decay 是一种 regularization 技术，通过在 loss 中添加类似于 \\( \frac{\lambda}{2} \|\theta\|^2 \\) 的项（L2 regularization）或直接使权重衰减来惩罚过大的权重。

在 SGD 中，L2 regularization 和真实的 weight decay 是等价的（仅相差一个缩放因子）。但在像 Adam 这样的 adaptive optimizers 中，它们**并不**等价。

大多数 Adam 的实现（例如早期的 PyTorch、TensorFlow）通过在 gradient 中添加 \\( \lambda \theta \\) 来应用 "weight decay"（将其视为 L2 regularization）。这导致 weight decay 与 adaptive 机制耦合在一起，从而引起：
- 不同参数间的 regularization 不均匀
- 干扰 adaptive learning rates
- 与真实的 weight decay 相比，generalization 较差

## AdamW: Decoupled Weight Decay

AdamW 通过 **decoupling** weight decay 修复了这个问题：它先执行 Adam 更新（仅使用 loss gradient），然后单独应用 weight decay。

AdamW 的 moment 更新规则（上述步骤 1-4）与 Adam 相同，但参数更新变为：

\\( \theta_t = \theta_{t-1} - \eta \left( \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} + \lambda \theta_{t-1} \right) \\)

或者等效地（常见实现方式）：
- 首先，执行 Adam 步骤：\\( \theta_t' = \theta_{t-1} - \eta \cdot \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} \\)
- 然后，进行衰减：\\( \theta_t = \theta_t' - \eta \lambda \theta_{t-1} \\)（或使用 \\( (1 - \eta \lambda) \theta_t' \\) 近似）

这确保了：
- Weight decay 的应用是一致的（与当前权重成正比，独立于 gradient 幅度）
- Adaptive learning rates 不受 regularization 的影响
- 超参数（learning rate 和 weight decay）是独立的

## Advantages of AdamW

- **Better generalization**：通常优于标准 Adam，尤其是在配合 learning rate schedules（如 cosine annealing、warmup）时。
- **Improved performance**：广泛应用于 state-of-the-art 模型（BERT、ViT、GPT 等）。
- **Stability**：在大规模训练中收敛更可靠。
- **Standard in modern libraries**：PyTorch 的 `torch.optim.AdamW` 实现了正确的解耦版本；Keras 和 TensorFlow 也有专门的 AdamW。

典型的 weight decay 取值：0.01–0.1（在 transformers 中通常为 0.01 或 0.05）。

## When to Use AdamW

- 训练 transformers 或大型 vision models
- 当 regularization 对 generalization 至关重要时
- Fine-tuning 预训练模型
- 大多数现代深度学习任务（它现在通常是默认选择）

总结来说，AdamW 是对 Adam 的一个微小但至关重要的改进，它使 weight decay 在 adaptive optimizers 中能按预期工作，从而在实践中获得卓越的性能。

References:  

- [Decoupled Weight Decay Regularization (arXiv)](https://arxiv.org/abs/1711.05101)  
- [Decoupled Weight Decay Regularization (OpenReview)](https://openreview.net/forum?id=Bkg6RiCqY7)  
- [PyTorch AdamW Documentation](https://pytorch.org/docs/stable/generated/torch.optim.AdamW.html)  
- [Keras AdamW Documentation](https://keras.io/api/optimizers/adamw/)  
- [Cornell Optimization Wiki: AdamW](https://optimization.cbe.cornell.edu/index.php?title=AdamW)