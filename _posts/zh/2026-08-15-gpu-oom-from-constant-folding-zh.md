---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU 常量折叠导致显存不足
translated: true
type: note
---

回溯完全由源解释。以下是事件链：

## 实际失败的原因

`aten.scalar_tensor(0, dtype=torch.int64, device=cuda:0)` 处的 OOM **并非**因为该操作很大——它是一个 8 字节的 0 维张量。它是第一个分配失败的地方，因为 GPU 已经完全满了。这个分配发生在 Inductor 的 **联合图常量折叠** 过程中，该过程在编译期间在真实 CUDA 设备上执行操作。

## 源追踪

**1. `model.py:196`** — `F.cross_entropy(..., ignore_index=-1)` 是起源。在 `torch.compile` 下，它通过 `torch/_decomp/decompositions.py` 中的 `_nll_loss_forward`（约第 4760 行）分解：

```python
safe_target = torch.where(target != ignore_index, target, 0)
result = torch.where(target != ignore_index, result, 0)
```

由于 `targets` 是 CUDA 上的 int64，字面量 `0` 被追踪为 `aten.scalar_tensor(0, dtype=torch.int64, device=cuda:0)`——正好是错误中的节点（`target != ignore_index` 比较也创建了一个用于 `-1` 的节点）。

**2. `joint_graph.py:410`** — `constant_fold_uniform_value()` 作为联合图 pass 在 Inductor 编译期间运行（由 `torch._inductor.config.joint_graph_constant_folding = True` 控制，`config.py:900`）。这纯粹是一种优化：找到输出为统一常量的节点，并将其重写为 `aten.full(shape, value)`，这样 Inductor 就会发出一个廉价的填充操作，而不是一个内核。

**3. `joint_graph.py:385` / `constant_folding.py:251`** — `UniformValueConstantFolder._deduce_value` 通过在记录的设备上 **实际运行操作** 来确定常量性：

```python
# pointwise ops
if isinstance(node.target, torch._ops.OpOverload) and (
    torch.Tag.pointwise in node.target.tags
    or node.target is torch.ops.aten.scalar_tensor.default
):
    args, kwargs = self.fetch_args_kwargs_from_env(node)
    ...
    return node.target(*args, **kwargs)   # <-- 编译时真实的 CUDA 分配
```

没有 faketensor，没有 CPU 卸载，没有围绕此调用的 OOM `try/except`——它只在遇到 `SymInt` 输入时退出，并剥离 `memory_format`。

**4. OOM 本身** — 在训练期间，编译发生在 GPU 已经饱和的情况下（权重 + Adam 状态 + 当前批次的激活/梯度）。缓存分配器甚至无法满足一个 8 字节的 `scalar_tensor` 分配（`cudaMalloc` 失败），因此抛出 `AcceleratorError: CUDA error: out of memory`，Inductor 将其表现为 `BackendCompilerFailed`。

## 为什么该 pass “有问题”

- 它在编译时执行 **真实的设备上分配**，且 GPU 已经满了。这在推理/编译时有内存余量时没问题，但在训练期间，这是一个额外的峰值，即使折叠后的张量很小，也可能导致 OOM。
- 它唯一的保护是 SymInt 检查——没有对饱和分配器的保护，而且 `scalar_tensor(0)` 甚至不需要设备执行就能知道其值（它从构造上就是常量）。

## 修复方法

- **针对性：** 禁用该 pass——它仅仅是一个优化：
  ```python
  torch._inductor.config.joint_graph_constant_folding = False
  ```
  正确性不受影响；你失去了统一常量折叠和 `+0`/`*1` 无操作消除。
- **真正的修复：** 你的 GPU 没有余量。减小批量大小/序列长度或使用梯度检查点——编译时的峰值会持续导致失败。
- `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` 有助于解决碎片化问题，但当内存真正耗尽时无效。

如果这是用于 bug 报告的重现，那么有趣的 bug 是：常量折叠在编译时在设备上执行操作，没有内存压力回退，因此训练期间的 OOM 会以一个微不足道的 `scalar_tensor` 节点上的虚假 `BackendCompilerFailed` 表现出来。