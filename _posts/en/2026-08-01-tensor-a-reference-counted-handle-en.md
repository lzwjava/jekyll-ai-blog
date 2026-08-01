---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Tensor: A Reference-Counted Handle"
translated: false
type: note
---

Here's what a Tensor is in PyTorch, based on the code:

## A Tensor is a reference-counted handle to a `TensorImpl`

A `torch.Tensor` is not the data itself — it's a cheap, reference-counted pointer to an object (`TensorImpl`) that holds the data and its metadata. That's why copying a tensor is cheap and why views share memory.

### The three layers of the class

**1. `torch.Tensor` (what users touch)** — `torch/_tensor.py:102`
```python
class Tensor(torch._C.TensorBase):
```
It subclasses the C++-exposed core and adds Python functionality: `__deepcopy__`, serialization, dlpack exchange, torch-function dispatch (`__torch_function__`), etc.

**2. `torch._C.TensorBase` (Python/C++ binding)** — defined in `torch/csrc/autograd/python_variable.cpp`, with its type stub in `torch/_C/__init__.pyi.in:1998`. Its attributes there show the public surface: `shape`, `dtype`, `device`, `layout`, `requires_grad`, `grad_fn`, `grad`, `ndim`, `T`, etc.

**3. `at::TensorBase` (C++ core)** — `aten/src/ATen/core/TensorBase.h`. The header's "Tensor vs. TensorBase" note explains the design:

> "TensorBase represents a reference counted handle to TensorImpl, exactly the same as Tensor."

The handle is literally:
```cpp
c10::intrusive_ptr<TensorImpl, UndefinedTensorImpl> impl_;   // TensorBase.h:921
```

### What `TensorImpl` holds — `c10/core/TensorImpl.h`

| Field | Meaning |
|---|---|
| `Storage storage_` (line 2888) | pointer to the raw memory buffer holding the elements |
| `sizes_and_strides_` | the shape and strides (how to index into storage) |
| `storage_offset_` | offset into storage — this is what makes views work |
| `data_type_` (line 2934) | the dtype (`float32`, `int64`, ...) and element size |
| `device_opt_` (line 2948) | which device the data lives on (CPU, CUDA, MPS, ...) |
| `key_set_` | dispatch keys used by the dispatcher to route operators |
| `version_counter_` | bumped on in-place ops (drives autograd's "modified by inplace" checks) |
| `autograd_meta_` (line 2902) | `grad`, `grad_fn`, `requires_grad`; `nullptr` when grad isn't needed |

### Implications visible in the code

- **Views share storage**: a slice like `t[0]` creates a new `TensorImpl` with the same `storage_` but a different `sizes_and_strides_`/`storage_offset_`.
- **Autograd metadata is lazily allocated**: `autograd_meta_` is a `std::unique_ptr` that stays `nullptr` for tensors that don't require grad (an optimization documented right at `TensorImpl.h:2895`).

So, in one line: **a tensor is a lightweight, reference-counted wrapper (`TensorBase`/`Tensor`) around a `TensorImpl`, which bundles a storage buffer with shape/strides, dtype, device, dispatch keys, and autograd state.**
