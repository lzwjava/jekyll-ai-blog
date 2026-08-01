---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch张量：带自动求导的多维数组
translated: true
type: note
---

问题：PyTorch 中的张量（tensor）是什么？

回答：

`torch.Tensor` 是一个多维数组 —— 与 numpy 的 `ndarray` 概念相同 —— 但具有 numpy 无法提供的三个特性：GPU 放置、自动求导跟踪，以及用于融合操作的 C++/CUDA 后端。

从结构上看，它是对连续一维存储缓冲区的视图，由 `shape`、`stride`、`dtype`、`device` 和偏移量描述：

```python
import torch

x = torch.randn(2, 3)
x.shape      # torch.Size([2, 3])
x.stride()   # (3, 1) —— 每个维度移动一个元素需要跳过的元素个数
x.dtype      # torch.float32
x.device     # cpu
x.storage().data_ptr()  # 实际内存地址
```

步幅（strides）解释了为什么 `.reshape()` 有时会失败而 `.view()` 能成功，以及为什么 `.transpose()` 是零成本的（仅交换步幅，无需复制）：

```python
x = torch.randn(2, 3)
y = x.t()            # 转置：步幅变为 (1,3) 而非 (3,1)，无复制
y.is_contiguous()    # False
y.reshape(6)         # 内部强制复制，因为步幅不允许视图
```

自动求导（Autograd）：每个张量都有 `.requires_grad`、`.grad_fn`、`.grad`。操作构建一个由 `Function` 节点组成的有向无环图（DAG）； `.backward()` 通过向量-雅可比乘积反向遍历该图。

```python
x = torch.randn(3, requires_grad=True)
y = (x ** 2).sum()
y.backward()
x.grad   # dy/dx = 2x
```

`y.grad_fn` 是一个 `SumBackward0`，指向 `PowBackward0`，再指向 `x` 上的 `AccumulateGrad` —— 这条链就是张量记忆其计算方式的关键，也是它区别于普通数组的地方。

设备：`x.to('cuda')` 将存储复制到不同的分配器；操作通过 ATen 的基于 `dtype` + `device` + 布局（稠密/稀疏）的每设备内核表进行分发。正是这种分发机制，使得相同的 `torch.matmul(a, b)` 调用根据张量所在位置路由到 cuBLAS、MKL 或 Triton 内核。

既然你正在 MI300X 上训练 GPT-2 —— 有一点值得注意：ROCm 的张量分发镜像了 CUDA 的分发键，但某些 ATen 操作的内核覆盖有所滞后（例如某些稀疏操作或较旧的 `aten::_foreach_*` 变体）。如果遇到“not implemented for backend HIP”错误，建议检查 `torch.__config__.show()` 和 ROCm 发行说明。

参考：

- [PyTorch Tensor 文档](https://pytorch.org/docs/stable/tensors.html)
- [PyTorch Autograd 机制](https://pytorch.org/docs/stable/notes/autograd.html)
- [PyTorch 内部原理（ezyang 博客）](http://blog.ezyang.com/2019/05/pytorch-internals/)
