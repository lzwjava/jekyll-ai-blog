---
audio: false
generated: true
lang: zh
layout: post
title: 深度学习中的Softmax函数
translated: true
type: note
---

### 什么是 Softmax？

**Softmax 函数**是一种在机器学习（尤其是深度学习）中使用的数学函数，用于将原始分数向量（通常称为 logits）转换为概率分布。它确保输出值为正数且总和为 1，从而使其可解释为概率。

Softmax 函数对于向量 \\( z = [z_1, z_2, \dots, z_n] \\) 的定义如下：

\\[
\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^n e^{z_j}}
\\]

其中：

- \\( z_i \\)：第 \\( i \\) 个类别的输入分数（logit）。
- \\( e^{z_i} \\)：输入分数的指数，确保结果为正数。
- \\( \sum_{j=1}^n e^{z_j} \\)：所有输入分数指数的总和，用于归一化。
- 输出 \\( \text{Softmax}(z_i) \\) 表示第 \\( i \\) 个类别的概率。

主要特性：

- **输出范围**：每个输出值介于 0 和 1 之间。
- **总和为 1**：所有输出值的总和等于 1，使其成为有效的概率分布。
- **放大差异**：Softmax 中的指数函数会放大较大的输入值，使得输出概率对于较大的 logits 更加明确。

### Softmax 在深度学习中的应用

Softmax 函数通常用于神经网络的**输出层**，用于**多类别分类**任务。以下是其应用方式：

1. **在神经网络中的上下文**：
   - 在神经网络中，最后一层通常为每个类别生成原始分数（logits）。例如，在一个包含 3 个类别的分类问题（如猫、狗、鸟）中，网络可能输出类似 \\([2.0, 1.0, 0.5]\\) 的 logits。
   - 这些 logits 不能直接解释为概率，因为它们可能是负数、无界的，且总和不为 1。

2. **Softmax 的作用**：
   - Softmax 函数将这些 logits 转换为概率。对于上述示例：
     \\[
     \text{Softmax}([2.0, 1.0, 0.5]) = \left[ \frac{e^{2.0}}{e^{2.0} + e^{1.0} + e^{0.5}}, \frac{e^{1.0}}{e^{2.0} + e^{1.0} + e^{0.5}}, \frac{e^{0.5}}{e^{2.0} + e^{1.0} + e^{0.5}} \right]
     \\]
     这可能会得到类似 \\([0.665, 0.245, 0.090]\\) 的概率，表示类别 1（猫）的概率为 66.5%，类别 2（狗）的概率为 24.5%，类别 3（鸟）的概率为 9.0%。

3. **应用场景**：
   - **多类别分类**：Softmax 用于图像分类（如图像中的物体识别）、自然语言处理（如多类别情感分析）或任何需要将输入分配到多个类别之一的任务。
   - **损失计算**：Softmax 通常与**交叉熵损失**函数配对使用，用于衡量预测概率分布与真实分布（独热编码标签）之间的差异。这种损失指导神经网络的训练。
   - **决策制定**：输出概率可用于选择最可能的类别（例如，选择概率最高的类别）。

4. **深度学习中的示例**：
   - **图像分类**：在卷积神经网络（如 ResNet）中，最后的全连接层为每个类别生成 logits（例如，ImageNet 中的 1000 个类别）。Softmax 将这些转换为概率，以预测图像中的物体。
   - **自然语言处理**：在模型（如 transformers，例如 BERT）中，Softmax 用于输出层，用于文本分类或下一个词预测等任务，其中需要词汇表或类别集合上的概率。
   - **强化学习**：Softmax 可用于将动作分数转换为概率，以便在基于策略的方法中选择动作。

5. **在框架中的实现**：
   - 在 **PyTorch** 或 **TensorFlow** 等框架中，Softmax 通常作为内置函数实现：
     - PyTorch：`torch.nn.Softmax(dim=1)` 或 `torch.nn.functional.softmax()`
     - TensorFlow：`tf.nn.softmax()`
   - 许多框架将 Softmax 与交叉熵损失结合在一个操作中（例如 PyTorch 中的 `torch.nn.CrossEntropyLoss`），以提高数值稳定性，因为单独计算 Softmax 可能会导致大 logits 的溢出问题。

### 实际注意事项

- **数值稳定性**：直接计算 Softmax 可能因指数函数而导致溢出。常见的技巧是在应用 Softmax 之前将所有 logits 减去最大 logit 值（\\( z_i - \max(z) \\)），这不会改变输出，但可以防止指数过大。
- **Softmax 与 Sigmoid**：对于**二分类**问题，通常使用 sigmoid 函数而不是 Softmax，因为它更高效地处理两个类别。Softmax 将 sigmoid 推广到多个类别。
- **局限性**：
  - Softmax 假设类别互斥（只有一个正确类别）。对于多标签分类（多个类别可能同时为真），更倾向于使用 sigmoid。
  - Softmax 可能因指数函数而对预测过于自信，这可能会放大 logits 中的微小差异。

### 示例计算

假设神经网络为一个 3 类别问题输出 logits \\([1.5, 0.8, -0.2]\\)：

1. 计算指数：\\( e^{1.5} \approx 4.482, e^{0.8} \approx 2.225, e^{-0.2} \approx 0.819 \\)。
2. 指数总和：\\( 4.482 + 2.225 + 0.819 = 7.526 \\)。
3. 计算概率：
   - 类别 1：\\( \frac{4.482}{7.526} \approx 0.596 \\)
   - 类别 2：\\( \frac{2.225}{7.526} \approx 0.296 \\)
   - 类别 3：\\( \frac{0.819}{7.526} \approx 0.109 \\)
4. 输出：\\([0.596, 0.296, 0.109]\\)，这是一个有效的概率分布。

### Softmax 可视化

为了说明 Softmax 如何将 logits 转换为概率，请考虑以下图表，显示 logits 及其对应的 Softmax 概率：

```chartjs
{
  "type": "bar",
  "data": {
    "labels": ["Class 1", "Class 2", "Class 3"],
    "datasets": [
      {
        "label": "Logits",
        "data": [1.5, 0.8, -0.2],
        "backgroundColor": "rgba(75, 192, 192, 0.6)",
        "borderColor": "rgba(75, 192, 192, 1)",
        "borderWidth": 1
      },
      {
        "label": "Softmax Probabilities",
        "data": [0.596, 0.296, 0.109],
        "backgroundColor": "rgba(255, 99, 132, 0.6)",
        "borderColor": "rgba(255, 99, 132, 1)",
        "borderWidth": 1
      }
    ]
  },
  "options": {
    "scales": {
      "y": {
        "beginAtZero": true,
        "title": {
          "display": true,
          "text": "Value"
        }
      },
      "x": {
        "title": {
          "display": true,
          "text": "Classes"
        }
      }
    },
    "plugins": {
      "legend": {
        "display": true
      },
      "title": {
        "display": true,
        "text": "Logits vs. Softmax Probabilities"
      }
    }
  }
}
```

此图表比较了原始 logits 与应用 Softmax 后的概率，突出了 Softmax 如何将值归一化为概率分布。

### 总结

Softmax 函数是深度学习中多类别分类的基石，它将原始分数转换为概率分布。它广泛用于神经网络的输出层，用于图像和文本分类等任务，使模型能够为多个类别分配概率，并通过交叉熵损失等损失函数促进训练。其指数特性使其对 logits 的差异敏感，而谨慎的实现确保了数值稳定性。
