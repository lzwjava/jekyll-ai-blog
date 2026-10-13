---
audio: false
generated: true
image: false
lang: en
layout: post
title: Minimal PyTorch-Like Autograd Library
translated: false
type: note
---

Done. **itorch** is a working, minimal PyTorch-like autograd library — ~1,200 lines total, numpy-only, tinygrad-inspired. All tests pass.

## Layout

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

## How it works

Each `Tensor` wraps a numpy array and records `_parents` + a `_backward(grad)` closure. `backward()` does one topological pass; each closure accumulates `parent.grad += partial` with correct broadcasting reduction (`_unbroadcast`), duplicate-index handling (`np.add.at`), and col2im scatter for conv. Everything else is sugar on top.

## Verified

- **Every op** (`+ - * / ** @`, matmul incl. batched/1-D mixes, reductions, softmax, shape ops, slicing, gather, cat/stack/where, im2col, conv, maxpool, batchnorm, both losses) checked against **central finite differences** — including the subtle ones I debugged along the way (broadcasting of reduced axes in `sum/max` backprop, no_grad flag sharing, and a real `Module.__call__` bug that silently fed row-splices into layers).
- **Real training**: XOR 100%, linear regression to 1e-12 loss, synthetic CNN 100%, and **real MNIST → 98.3% test accuracy in 3 epochs (~2 min on CPU)**.

## Try it

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
