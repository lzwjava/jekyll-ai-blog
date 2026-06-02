---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: TinyGrad Lightweight ML Library
translated: false
type: note
---

### Introduction to TinyGrad
TinyGrad is a lightweight, minimalist machine learning and deep learning library in Python, designed for education and simplicity. It implements automatic differentiation (autograd) like PyTorch but is much smaller—around 1,000 lines of code. It's great for learning ML concepts or building small models without the overhead of larger libraries. It supports tensors, neural networks, and basic operations, including GPU acceleration via PyTorch or Metal.

You can find the official repository at: [tinygrad GitHub](https://github.com/geohot/tinygrad). Note: It's experimental and not as robust as PyTorch or TensorFlow for production use.

### Installation
Install TinyGrad via pip:

```bash
pip install tinygrad
```

It has minimal dependencies but optionally uses PyTorch for some backends. For GPU support, ensure you have PyTorch installed.

### Basic Usage
Start by importing and setting the context (TinyGrad requires specifying if you're training or inferring, as gradients are computed differently).

#### Importing and Context
```python
from tinygrad import Tensor
from tinygrad.nn import Linear, BatchNorm2d  # For neural nets

# Set context: training (for gradients) or inference
Tensor.training = True  # Enable gradient tracking
```

#### Creating and Manipulating Tensors
Tensors are the core data structure, similar to NumPy arrays or PyTorch tensors.

```python
# Create tensors from lists, NumPy arrays, or by shape
a = Tensor([1, 2, 3])          # From list
b = Tensor.zeros(3)            # Zeros tensor of shape (3,)
c = Tensor.rand(2, 3)          # Random tensor of shape (2, 3)

# Basic operations
d = a + b                      # Element-wise addition
e = d * 2                      # Scalar multiplication
f = a @ Tensor([[1], [2], [3]])  # Matrix multiplication (a is 1D, transposed implicitly)

print(e.numpy())               # Convert to NumPy for printing or further use
```

#### Automatic Differentiation (Backpropagation)
TinyGrad automatically computes gradients using the chain rule.

```python
# Enable gradient tracking
Tensor.training = True

x = Tensor([1.0, 2.0, 3.0])
y = (x * 2).sum()             # Some operation; y is a scalar

y.backward()                  # Compute gradients
print(x.grad.numpy())         # Gradients w.r.t. x: should be [2, 2, 2]
```

For exporting to NumPy, use `.numpy()`—gradients accumulate unless reset.

#### Neural Networks and Training
TinyGrad includes basic layers and optimizers. Here's a simple MLP example:

```python
from tinygrad.nn import Linear, optim

# Define a simple model (e.g., linear layer)
model = Linear(3, 1)          # Input 3, output 1

# Dummy data
x = Tensor.rand(4, 3)         # Batch of 4 samples, 3 features
y_true = Tensor.rand(4, 1)    # Target

# Forward pass
pred = model(x).sigmoid()      # Assuming binary classification

# Loss (e.g., MSE)
loss = ((pred - y_true) ** 2).mean()

# Backprop and optimize
loss.backward()
optim.Adam([model], lr=0.01).step()
```

For convolution networks, use `Conv2d` from `tinygrad.nn`.

### Advanced Features
- **Loss Functions and Activations**: Available in `tinygrad.nn` (e.g., `sigmoid`, `relu`, `cross_entropy`).
- **Optimizers**: `SGD`, `Adam` in `tinygrad.nn.optim`.
- **Layers**: `Linear`, `Conv2d`, `BatchNorm`, etc.
- **Saving/Loading**: Models can be saved as state dictionaries (similar to PyTorch).
- **GPU/Acceleration**: TinyGrad can run on GPU via PyTorch backend: `TESOR_SET_DEVICE='cuda:0'`. It also supports Metal on macOS.
- **Vision/Denoising Examples**: The repo has examples like training a ResNet on MNIST.

For full examples, check the `examples/` folder in the GitHub repo, such as image classification or reinforcement learning.

### Example: Training a Neural Network
Here's a complete, simple script for training a network on XOR:

```python
from tinygrad import Tensor
from tinygrad.nn import Linear, optim

# Data
X = Tensor([[0,0], [0,1], [1,0], [1,1]])
Y = Tensor([[0], [1], [1], [0]])

# Model
model = Linear(2, 1)
opt = optim.Adam([model], lr=0.1)

Tensor.training = True

for epoch in range(1000):
    pred = model(X).sigmoid()
    loss = ((pred - Y) ** 2).mean()
    loss.backward()
    opt.step()
    opt.zero_grad()

# Test
print(model(Tensor([[0,0]])))  # Should be ~0
```

### Tips and Caveats
- **Mode Switching**: Always set `Tensor.training = True` for training; switch to `False` for inference to avoid gradient computation.
- **Shape Handling**: Tensors follow NumPy-like broadcasting, but watch for overflows in small models.
- **Debugging**: Use `.numpy()` to inspect values. If something fails, check for shape mismatches.
- **Performance**: It's slow for large models—use PyTorch for production.
- **Updates**: TinyGrad evolves quickly; check the repo for the latest version.

For more details, visit the [docs/README.md](https://github.com/geohot/tinygrad/blob/master/README.md) or run examples locally. If you have a specific use case, provide more details for tailored advice!
