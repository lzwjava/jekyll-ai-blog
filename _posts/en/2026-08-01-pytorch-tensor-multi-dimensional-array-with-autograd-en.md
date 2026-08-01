---
audio: false
generated: true
image: false
lang: en
layout: post
title: "PyTorch Tensor: Multi-Dimensional Array with Autograd"
translated: false
type: note
---

Question: What is a tensor in PyTorch?

Answer:

A `torch.Tensor` is a multi-dimensional array — same idea as a numpy `ndarray` — but with three things numpy doesn't give you: GPU placement, autograd tracking, and a C++/CUDA backend for fused ops.

Structurally it's a view over a contiguous 1D storage buffer, described by `shape`, `stride`, `dtype`, `device`, and an offset:

```python
import torch

x = torch.randn(2, 3)
x.shape      # torch.Size([2, 3])
x.stride()   # (3, 1) -- how many elements to skip per dim to move by 1
x.dtype      # torch.float32
x.device     # cpu
x.storage().data_ptr()  # actual memory address
```

Strides are why `.reshape()` sometimes fails but `.view()` works, and why `.transpose()` is free (just swaps strides, no copy):

```python
x = torch.randn(2, 3)
y = x.t()            # transpose: stride (1,3) instead of (3,1), no copy
y.is_contiguous()    # False
y.reshape(6)         # forces a copy internally because strides don't allow a view
```

Autograd: every tensor has `.requires_grad`, `.grad_fn`, `.grad`. Ops build a DAG of `Function` nodes; `.backward()` walks it in reverse with vector-Jacobian products.

```python
x = torch.randn(3, requires_grad=True)
y = (x ** 2).sum()
y.backward()
x.grad   # dy/dx = 2x
```

`y.grad_fn` is a `SumBackward0` pointing to `PowBackward0` pointing to `AccumulateGrad` on `x` — that chain *is* the tensor's memory of how it was computed, which is what distinguishes it from a plain array.

Device: `x.to('cuda')` copies storage to a different allocator; ops dispatch through ATen's per-device kernel table based on `dtype` + `device` + layout (dense/sparse). This dispatch is why the same `torch.matmul(a, b)` call routes to cuBLAS, MKL, or a Triton kernel depending on where the tensors live.

Given you're training GPT-2 on MI300X — the one gotcha worth knowing: ROCm's tensor dispatch mirrors CUDA's dispatch keys, but kernel coverage for some ATen ops lags (things like certain sparse ops or older `aten::_foreach_*` variants). Worth checking `torch.__config__.show()` and ROCm release notes if you hit a "not implemented for backend HIP" error.

References:
- [PyTorch Tensor docs](https://pytorch.org/docs/stable/tensors.html)
- [PyTorch Autograd mechanics](https://pytorch.org/docs/stable/notes/autograd.html)
- [PyTorch Internals (ezyang blog)](http://blog.ezyang.com/2019/05/pytorch-internals/)
