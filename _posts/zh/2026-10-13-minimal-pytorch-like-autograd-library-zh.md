---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 极简类PyTorch自动求导库
translated: true
type: note
---

完成。**itorch** 是一个可用的、极简的类 PyTorch 自动求导库——总共约 1,200 行，仅依赖 numpy，灵感来自 tinygrad。所有测试通过。

## 布局

```
itorch/
  tensor.py    605 lines  Tensor + the whole autograd engine (ops → {_parents, _backward})
  nn.py        293 lines  Module, Sequential, Linear, Conv2d, MaxPool2d, BatchNorm1d/2d,
                          Dropout, Embedding, activations, Flatten
  optim.py      89 lines  SGD (momentum/nesterov), Adam, AdamW
  functions.py 211 lines  losses (mse/bce/cross_entropy), no_grad, DataLoader, clip_grad, save/load
tests/                  numeric-gradient checks vs finite differences + training smoke tests
examples/               01_xor, 02_linear_regression, 03_mnist_cnn (real MNIST, auto-download)
```

## 工作原理

每个 `Tensor` 包装一个 numpy 数组，并记录 `_parents` 和一个 `_backward(grad)` 闭包。`backward()` 执行一次拓扑遍历；每个闭包使用正确的 broadcasting 归约（`_unbroadcast`）、重复索引处理（`np.add.at`）以及 conv 的 col2im scatter 操作，将 `parent.grad += partial` 累加。其他一切都只是在此基础上提供的语法糖。

## 验证

- **每个运算**（`+ - * / ** @`、matmul（含 batched/1-D 混合）、reductions、softmax、shape ops、slicing、gather、cat/stack/where、im2col、conv、maxpool、batchnorm、两种损失）均通过**中心差分**校验——包括我在此过程中调试过的细微问题（`sum/max` 反向传播中 reduced axes 的 broadcasting、`no_grad` flag 共享，以及一个真实的 `Module.__call__` bug，它曾静默地将 row-splices 馈入 layers）。
- **真实训练**：XOR 100%，线性回归达到 1e-12 损失，合成 CNN 100%，以及**真实 MNIST → 3 个 epoch 内测试准确率 98.3%（CPU 上约 2 分钟）**。

## 试一试

```bash
python3 tests/test_autograd.py     # gradient checks
python3 examples/03_mnist_cnn.py --epochs 3
```

```python
import itorch as tt
from itorch import nn, optim, cross_entropy

model = nn.Sequential(nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10))
opt = optim.AdamW(model.parameters(), lr=1e-3)
loss = cross_entropy(model(x), y)   # x: Tensor(batch, 784)
loss.backward(); opt.step()
```