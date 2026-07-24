---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch基础与训练指南
translated: true
type: note
---

## 问题：PyTorch 入门

## 答案：

PyTorch 是一个开源深度学习框架，最初由 Meta AI 开发。它主要用于：

* 训练神经网络
* 研究原型设计
* LLM 训练与微调
* 计算机视觉
* 强化学习
* 生产环境推理

核心理念：**PyTorch 让你能够将计算表示为张量操作的动态图，然后通过反向传播自动计算梯度。**

一个心智模型：

```
Python 代码
    |
    v
PyTorch 张量
    |
    v
CUDA 内核 / CPU 内核
    |
    v
GPU 执行矩阵运算
```

---

## 1. 张量：基础对象

张量是一个多维数组，类似于 NumPy 的 ndarray，但支持 GPU 加速和自动求导。

```python
import torch

x = torch.tensor([
    [1., 2.],
    [3., 4.]
])

print(x)
```

输出：

```
tensor([[1., 2.],
        [3., 4.]])
```

维度：

```
标量       0D
向量       1D
矩阵       2D
图像       4D (N,C,H,W)
LLM 输入   3D (batch, sequence, hidden)
```

示例：

```python
x = torch.randn(2, 3)

print(x.shape)
```

```
torch.Size([2,3])
```

---

## 2. GPU 加速

PyTorch 存在的主要原因：

```python
device = "cuda"

x = torch.randn(10000,10000).to(device)

y = x @ x

print(y)
```

这个过程：

```
CPU：
10000x10000 矩阵乘法
    |
    慢

GPU：
10000x10000 矩阵乘法
    |
    CUDA 内核
    |
    数千个 CUDA 核心
    |
    快
```

运算符：

```python
@
```

是矩阵乘法。

AI 本质上就是：

```
tokens
 |
embedding 查找
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

# 3. Autograd：自动微分

神奇的部分。

示例：

```python
import torch

x = torch.tensor(3.0, requires_grad=True)

y = x ** 2

y.backward()

print(x.grad)
```

输出：

```
tensor(6.)
```

因为：

```
y = x²

dy/dx = 2x

当 x=3 时：

dy/dx = 6
```

PyTorch 构建了一个计算图：

```
x
|
square
|
y

backward：

dy/dx
```

---

# 4. 神经网络示例

一个简单的线性模型：

```
y = Wx + b
```

PyTorch 实现：

```python
import torch
import torch.nn as nn


model = nn.Linear(10, 1)

x = torch.randn(32,10)

output = model(x)

print(output.shape)
```

内部过程：

```
输入：

32 x 10


权重：

1 x 10


矩阵乘法：

32x10 @ 10x1

=

32x1
```

---

# 5. 训练循环

深度学习的核心：

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

循环过程：

```
前向传播：

x
 |
model
 |
prediction
 |
loss


反向传播：

loss
 |
gradient
 |
权重


优化器：

weights -= learning_rate * gradient
```

---

# 6. PyTorch 架构

高层概览：

```
                 PyTorch

                    |
        ------------------------
        |                      |
     Python API             C++ 后端

        |
     ATen Tensor Library

        |
   ------------------
   |                |
 CPU 内核       CUDA 内核

                    |
                 NVIDIA GPU
```

对于 AMD：

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

# 7. PyTorch 中的 LLM 训练

一个 transformer 块：

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

真实的 LLM：

```
GPT-2
 |
PyTorch
 |
Transformer 层
 |
CUDA 内核
 |
GPU tensor cores
```

---

# 8. 为什么 PyTorch 主导 AI 研究

在 PyTorch 之前：

```
TensorFlow 1.x

定义图
      |
编译图
      |
执行
```

PyTorch：

```python
x = model(input)

if condition:
    x = layer1(x)
else:
    x = layer2(x)
```

常规 Python。

研究人员喜欢这样，因为实验变得容易多了。

---

# 9. PyTorch 与 CUDA 的关系

重要区别：

```
PyTorch
  |
  |  高层张量操作
  |
CUDA
  |
  |  GPU 编程模型
  |
GPU 硬件
```

示例：

你写：

```python
torch.matmul(a,b)
```

PyTorch 内部调用：

```
torch.matmul
      |
      v
cuBLAS GEMM
      |
      v
CUDA 内核
      |
      v
Tensor cores
```

对于 LLM 训练，大部分时间花在：

```
GEMM（矩阵乘法）
+
attention 内核
+
通信
```

---

# 10. 现代 LLM 的 PyTorch 技术栈

典型的 2026 年技术栈：

```
                 HuggingFace Transformers
                          |
                       PyTorch
                          |
        ---------------------------------
        |                               |
    torch.compile                    FSDP
        |                               |
    Triton 内核                 分布式训练
        |
      CUDA/HIP
        |
      GPU 集群
```

示例：

```python
model = torch.compile(model)
```

PyTorch 可以自动生成优化的内核。

---

## LLM 工程师的极简 PyTorch 学习路径

考虑到你的 GPU/LLM 工作，最短路径：

```
1. 张量基础
        |
2. Autograd
        |
3. nn.Module
        |
4. 训练循环
        |
5. CUDA 内存
        |
6. DistributedDataParallel
        |
7. FSDP
        |
8. Triton 内核
        |
9. torch.compile
```

一个好的下一步是实现：

```
microGPT
   |
   +-- tokenizer
   +-- transformer
   +-- attention
   +-- 训练循环
   +-- checkpoint
```

用大约 500 行 PyTorch 从头开始。这将为你提供与现代 LLM 训练系统相同的思维模型。