---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双曲正切激活函数详解
translated: true
type: note
---

**问题：** 什么是 tanh（双曲正切函数）？

**答案：**

Tanh 是**双曲正切激活函数**。在实践中，它是神经网络中最重要的非线性函数之一。

### 数学公式

$$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}} = \frac{\sinh(x)}{\cosh(x)}$$

或者等价地（且更稳定地）：
$$\tanh(x) = \frac{2}{1 + e^{-2x}} - 1 = 2 \cdot \sigma(2x) - 1$$

其中 $\sigma$ 是 Sigmoid 函数。这个恒等式很有用——tanh 实际上是一个**经过缩放和平移的 Sigmoid 函数**。

### 关键属性

| 属性 | 值 |
|----------|-------|
| **输出范围** | $(-1, 1)$（零中心化） |
| **导数** | $\frac{d}{dx}\tanh(x) = 1 - \tanh^2(x)$ |
| **在 x=0 处的梯度** | $1$（强于 Sigmoid 的 $0.25$） |
| **对称性** | 奇函数：$\tanh(-x) = -\tanh(x)$ |

### 代码实现

```python
import numpy as np
import matplotlib.pyplot as plt

# 前向传播
def tanh(x):
    return np.tanh(x)

# 导数（用于反向传播）
def tanh_derivative(x):
    return 1 - np.tanh(x)**2

# 数值稳定版本（避免 x 过大时溢出）
def tanh_stable(x):
    return np.tanh(x)  # NumPy 已实现

# 可视化
x = np.linspace(-5, 5, 1000)
y = np.tanh(x)
dy = 1 - np.tanh(x)**2

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(x, y, label='tanh(x)', linewidth=2)
plt.axhline(0, color='k', linestyle='-', linewidth=0.5)
plt.axvline(0, color='k', linestyle='-', linewidth=0.5)
plt.grid(True, alpha=0.3)
plt.legend()
plt.title('tanh 激活函数')
plt.xlabel('x')
plt.ylabel('tanh(x)')

plt.subplot(1, 2, 2)
plt.plot(x, dy, label="1 - tanh²(x)", linewidth=2, color='orange')
plt.grid(True, alpha=0.3)
plt.legend()
plt.title('tanh 导数')
plt.xlabel('x')
plt.ylabel('梯度')
plt.tight_layout()
plt.show()
```

### 为何它在深度学习中重要

1. **零中心化输出**：与 Sigmoid（输出 $(0, 1)$）不同，tanh 输出 $(-1, 1)$。这使激活值围绕零中心化，有助于反向传播时的梯度流动。负值意味着神经元可以强烈地“关闭”，而不仅仅是静默。

2. **更强的梯度**：导数峰值为 $\frac{d}{dx}\tanh(x)|_{x=0} = 1$，而 Sigmoid 仅为 $0.25$。这有助于缓解深层网络中的梯度消失问题。

3. **RNN/LSTM 标准**：由于这些特性，Tanh 是 LSTM 和 GRU 单元中的默认选择。门控激活通常使用 Sigmoid，但候选隐藏状态使用 Tanh。

4. **对称性**：奇对称性意味着如果将权重初始化为零，网络不会对正或负激活产生偏向。

### 与 ReLU 的对比

**Tanh：**

- 处处平滑，可微
- 输出有界（数值稳定）
- 若 $|x|$ 很大，存在梯度消失问题
- 用于 RNN、LSTM、早期的前馈网络

**ReLU：**

- 神经元死亡问题（当 $x < 0$ 时梯度为零）
- 输出无界
- 对于正输入无梯度消失问题
- **现代前馈/CNN 的默认选择**，速度更快

### 何时使用

- **LSTM/GRU**：细胞状态更新始终使用 tanh
- **RNN**：通常比 Sigmoid 更好，尽管 GRU 已基本取代了原始 RNN
- **早期网络**：前 ReLU 时代（2010年代），tanh 是标准选择
- **回归输出层**：如果目标值在 $(-1, 1)$ 范围内（经过归一化后），使用 tanh 输出 + MSE 损失非常自然

### PyTorch / TensorFlow

```python
import torch
import torch.nn.functional as F

x = torch.randn(32, 64)
y = torch.tanh(x)  # 直接应用
y = F.tanh(x)       # 效果相同

# 在层中使用
lstm = torch.nn.LSTM(input_size=128, hidden_size=256)
```

**核心要点：** Tanh 是一个**更平滑、零中心化的 Sigmoid 函数**。它在数学上很优雅，并且对于循环架构至关重要。对于前馈网络，ReLU 胜出是因为它速度更快且避免了一些梯度问题，但 tanh 的属性在许多方面理论上仍然更优——只是它无法很好地扩展到超过 100 亿参数的模型。
