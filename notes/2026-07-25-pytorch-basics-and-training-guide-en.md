---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyTorch Basics and Training Guide
translated: false
type: note
---

## Question: Intro to PyTorch

## Answer

PyTorch is an open-source deep learning framework originally developed by Meta AI. It is mainly used for:

* training neural networks
* research prototyping
* LLM training and fine-tuning
* computer vision
* reinforcement learning
* production inference

The core idea: **PyTorch lets you express computation as a dynamic graph of tensor operations, then automatically compute gradients through backpropagation.**

A mental model:

```
Python code
    |
    v
PyTorch tensors
    |
    v
CUDA kernels / CPU kernels
    |
    v
GPU executes matrix operations
```

---

## 1. Tensor: the fundamental object

A tensor is a multidimensional array, like NumPy ndarray, but GPU-enabled and differentiable.

```python
import torch

x = torch.tensor([
    [1., 2.],
    [3., 4.]
])

print(x)
```

Output:

```
tensor([[1., 2.],
        [3., 4.]])
```

Dimensions:

```
scalar       0D
vector       1D
matrix       2D
image        4D (N,C,H,W)
LLM input    3D (batch, sequence, hidden)
```

Example:

```python
x = torch.randn(2, 3)

print(x.shape)
```

```
torch.Size([2,3])
```

---

## 2. GPU acceleration

The main reason PyTorch exists:

```python
device = "cuda"

x = torch.randn(10000,10000).to(device)

y = x @ x

print(y)
```

This:

```
CPU:
10000x10000 matmul
    |
    slow

GPU:
10000x10000 matmul
    |
    CUDA kernel
    |
    thousands of CUDA cores
    |
    fast
```

The operator:

```python
@
```

is matrix multiplication.

AI is basically:

```
tokens
 |
embedding lookup
 |
matmul
 |
attention
 |
matmul
 |
MLP
 |
logits
```

---

# 3. Autograd: automatic differentiation

The magic part.

Example:

```python
import torch

x = torch.tensor(3.0, requires_grad=True)

y = x ** 2

y.backward()

print(x.grad)
```

Output:

```
tensor(6.)
```

Because:

```
y = x²

dy/dx = 2x

when x=3:

dy/dx = 6
```

PyTorch builds a computation graph:

```
x
|
square
|
y

backward:

dy/dx
```

---

# 4. Neural network example

A simple linear model:

```
y = Wx + b
```

PyTorch:

```python
import torch
import torch.nn as nn


model = nn.Linear(10, 1)

x = torch.randn(32,10)

output = model(x)

print(output.shape)
```

Internally:

```
input:

32 x 10


weight:

1 x 10


matmul:

32x10 @ 10x1

=

32x1
```

---

# 5. Training loop

The heart of deep learning:

```python
model = nn.Linear(10,1)

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=1e-3
)

loss_fn = nn.MSELoss()


for step in range(1000):

    x = torch.randn(32,10)
    y = torch.randn(32,1)


    prediction = model(x)

    loss = loss_fn(
        prediction,
        y
    )


    optimizer.zero_grad()

    loss.backward()

    optimizer.step()
```

The loop:

```
forward:

x
 |
model
 |
prediction
 |
loss


backward:

loss
 |
gradient
 |
weights


optimizer:

weights -= learning_rate * gradient
```

---

# 6. PyTorch architecture

High level:

```
                 PyTorch

                    |
        ------------------------
        |                      |
     Python API             C++ Backend

        |
     ATen Tensor Library

        |
   ------------------
   |                |
 CPU kernels     CUDA kernels

                    |
                 NVIDIA GPU
```

For AMD:

```
PyTorch
   |
ROCm
   |
HIP
   |
AMD GPU
```

---

# 7. LLM training in PyTorch

A transformer block:

```python
class Block(nn.Module):

    def __init__(self, dim):
        super().__init__()

        self.attn = nn.MultiheadAttention(
            dim,
            8
        )

        self.mlp = nn.Linear(
            dim,
            dim*4
        )


    def forward(self,x):

        x,_ = self.attn(
            x,x,x
        )

        x = self.mlp(x)

        return x
```

Real LLMs:

```
GPT-2
 |
PyTorch
 |
Transformer layers
 |
CUDA kernels
 |
GPU tensor cores
```

---

# 8. Why PyTorch dominates AI research

Before PyTorch:

```
TensorFlow 1.x

define graph
      |
compile graph
      |
execute
```

PyTorch:

```python
x = model(input)

if condition:
    x = layer1(x)
else:
    x = layer2(x)
```

Normal Python.

Researchers liked this because experimenting became much easier.

---

# 9. PyTorch vs CUDA relationship

Important distinction:

```
PyTorch
  |
  |  high-level tensor operations
  |
CUDA
  |
  |  GPU programming model
  |
GPU hardware
```

Example:

You write:

```python
torch.matmul(a,b)
```

PyTorch internally calls:

```
torch.matmul
      |
      v
cuBLAS GEMM
      |
      v
CUDA kernel
      |
      v
Tensor cores
```

For LLM training, most time is:

```
GEMM (matrix multiplication)
+
attention kernels
+
communication
```

---

# 10. Modern PyTorch stack for LLMs

Typical 2026 stack:

```
                 HuggingFace Transformers
                          |
                       PyTorch
                          |
        ---------------------------------
        |                               |
    torch.compile                    FSDP
        |                               |
    Triton kernels              distributed training
        |
      CUDA/HIP
        |
      GPU cluster
```

Example:

```python
model = torch.compile(model)
```

PyTorch can generate optimized kernels automatically.

---

## Minimal PyTorch learning path for an LLM engineer

Given your GPU/LLM work, the shortest path:

```
1. Tensor basics
        |
2. Autograd
        |
3. nn.Module
        |
4. Training loop
        |
5. CUDA memory
        |
6. DistributedDataParallel
        |
7. FSDP
        |
8. Triton kernels
        |
9. torch.compile
```

A good next step is implementing:

```
microGPT
   |
   +-- tokenizer
   +-- transformer
   +-- attention
   +-- training loop
   +-- checkpoint
```

from scratch in ~500 lines of PyTorch. That gives the same mental model used by modern LLM training systems.
