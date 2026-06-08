---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hyperbolic Tangent Activation Explained
translated: false
type: note
---

**Question:** What is tanh (hyperbolic tangent)?

**Answer:**

Tanh is the **hyperbolic tangent activation function**. In practice, it's one of the most important nonlinearities in neural networks.

### The Math

$$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}} = \frac{\sinh(x)}{\cosh(x)}$$

Or equivalently (and more stably):
$$\tanh(x) = \frac{2}{1 + e^{-2x}} - 1 = 2 \cdot \sigma(2x) - 1$$

where $\sigma$ is the sigmoid function. This identity is useful — tanh is just a **scaled and shifted sigmoid**.

### Key Properties

| Property | Value |
|----------|-------|
| **Output range** | $(-1, 1)$ (zero-centered) |
| **Derivative** | $\frac{d}{dx}\tanh(x) = 1 - \tanh^2(x)$ |
| **Gradient at x=0** | $1$ (stronger than sigmoid's $0.25$) |
| **Symmetry** | Odd function: $\tanh(-x) = -\tanh(x)$ |

### Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

# Forward pass
def tanh(x):
    return np.tanh(x)

# Derivative (useful for backprop)
def tanh_derivative(x):
    return 1 - np.tanh(x)**2

# Numerically stable version (avoids overflow on large x)
def tanh_stable(x):
    return np.tanh(x)  # NumPy already does this

# Visualize
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
plt.title('tanh activation')
plt.xlabel('x')
plt.ylabel('tanh(x)')

plt.subplot(1, 2, 2)
plt.plot(x, dy, label="1 - tanh²(x)", linewidth=2, color='orange')
plt.grid(True, alpha=0.3)
plt.legend()
plt.title('tanh derivative')
plt.xlabel('x')
plt.ylabel('gradient')
plt.tight_layout()
plt.show()
```

### Why It Matters in Deep Learning

1. **Zero-centered output**: Unlike sigmoid (which outputs $(0, 1)$), tanh outputs $(-1, 1)$. This centers the activation around zero, which helps gradient flow during backprop. The negative values mean neurons can "turn off" strongly, not just be quiet.

2. **Stronger gradients**: The derivative peaks at $\frac{d}{dx}\tanh(x)|_{x=0} = 1$, vs sigmoid's $0.25$. This helps mitigate vanishing gradients in deeper networks.

3. **RNN/LSTM standard**: Tanh is the default in LSTM and GRU cells because of these properties. The gate activations typically use sigmoid, but the candidate hidden states use tanh.

4. **Symmetric**: The odd symmetry means if you initialize weights to zero, the network doesn't have a bias toward positive or negative activations.

### Comparison to ReLU

**Tanh:**
- Smooth everywhere, differentiable
- Bounded output (numerically stable)
- Vanishing gradient problem if $|x|$ is large
- Used in RNNs, LSTMs, older feedforward nets

**ReLU:**
- Dead neuron problem (zero gradient for $x < 0$)
- Unbounded output
- No vanishing gradient for positive inputs
- **Modern default** for feedforward/CNN, much faster

### When to Use

- **LSTMs/GRUs**: Always tanh for cell state updates
- **RNNs**: Often better than sigmoid, though GRUs have mostly replaced vanilla RNNs
- **Older networks**: Pre-ReLU era (2010s), tanh was standard
- **Output layer for regression**: If your target is in $(-1, 1)$ (after normalization), tanh output + MSE loss is natural

### PyTorch/TensorFlow

```python
import torch
import torch.nn.functional as F

x = torch.randn(32, 64)
y = torch.tanh(x)  # Direct application
y = F.tanh(x)       # Same thing

# In a layer
lstm = torch.nn.LSTM(input_size=128, hidden_size=256)
```

**Bottom line:** Tanh is a **smoother, zero-centered sigmoid**. It's mathematically elegant and essential for recurrent architectures. For feedforward nets, ReLU won out because it's faster and avoids some gradient pathologies, but tanh's properties are still theoretically superior in many ways — it just doesn't scale as well to 10B+ parameter models.
