---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tensor：一种引用计数的句柄
translated: true
type: note
---

以下是基于代码对PyTorch中张量（Tensor）的解释：

## 张量（Tensor）是对`TensorImpl`的引用计数句柄

`torch.Tensor`并非数据本身，而是一个轻量级的、引用计数的指针，指向持有数据及其元数据的对象（`TensorImpl`）。这就是为什么复制张量成本低廉，以及视图（view）共享内存的原因。

### 类的三个层次

**1. `torch.Tensor`（用户直接接触的）** — `torch/_tensor.py:102`

```python
class Tensor(torch._C.TensorBase):
```

它继承自C++暴露的核心，并添加了Python功能：`__deepcopy__`、序列化、dlpack交换、torch函数分发（`__torch_function__`）等。

**2. `torch._C.TensorBase`（Python/C++绑定）** — 定义在`torch/csrc/autograd/python_variable.cpp`中，其类型存根在`torch/_C/__init__.pyi.in:1998`。其属性展示了公开接口：`shape`、`dtype`、`device`、`layout`、`requires_grad`、`grad_fn`、`grad`、`ndim`、`T`等。

**3. `at::TensorBase`（C++核心）** — `aten/src/ATen/core/TensorBase.h`。头文件中的“Tensor vs. TensorBase”注释解释了设计：

> “TensorBase表示对TensorImpl的引用计数句柄，与Tensor完全相同。”

该句柄实际上就是：

```cpp
c10::intrusive_ptr<TensorImpl, UndefinedTensorImpl> impl_;   // TensorBase.h:921
```

### `TensorImpl`包含的内容 — `c10/core/TensorImpl.h`

| Field | Meaning |
| --- | --- |
| `Storage storage_` (line 2888) | 指向持有元素的原始内存缓冲区的指针 |
| `sizes_and_strides_` | 形状和步长（如何索引到存储） |
| `storage_offset_` | 存储偏移量——这是视图工作的关键 |
| `data_type_` (line 2934) | 数据类型（`float32`、`int64`，...）和元素大小 |
| `device_opt_` (line 2948) | 数据所在的设备（CPU、CUDA、MPS，...） |
| `key_set_` | 分发器用于路由操作的调度键 |
| `version_counter_` | 原地操作时递增（驱动自动求导的“被原地操作修改”检查） |
| `autograd_meta_` (line 2902) | `grad`、`grad_fn`、`requires_grad`；当不需要梯度时为`nullptr` |

### 代码中可见的推论

- **视图共享存储**：像`t[0]`这样的切片会创建一个新的`TensorImpl`，它拥有相同的`storage_`，但不同的`sizes_and_strides_`/`storage_offset_`。
- **自动求导元数据是惰性分配的**：`autograd_meta_`是一个`std::unique_ptr`，对于不需要梯度的张量保持为`nullptr`（在`TensorImpl.h:2895`处有文档记录的优化）。

因此，一句话总结：**张量是一个轻量级的、引用计数的包装器（`TensorBase`/`Tensor`），包裹着一个`TensorImpl`，该实现将存储缓冲区与形状/步长、数据类型、设备、调度键和自动求导状态捆绑在一起。**
