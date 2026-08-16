---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FP8梯度权重反向GEMM布局
translated: true
type: note
---

这是FP8线性层反向传播中的**`grad_weight` GEMM**。以下是完整详解：

## 数学原理

对于线性层 `output = input @ weight.T`，形状为：

- `input`: `[B, K]`，`weight`: `[N, K]` → `output`: `[B, N]`

反向传播给出 `grad_weight = grad_output.T @ input`，即 `[N, B] @ [B, K] → [N, K]`（与权重形状相同，这是自动求导函数必须返回的）。

## 布局问题

`torch._scaled_mm` 对内存布局有严格要求：

- **第1个参数（A）：必须是行主序（连续）**
- **第2个参数（B）：必须是列主序**

对于GEMM 2，保存的FP8张量不满足此要求：

- `go_fp8` 是 `[B, N]` 连续（行主序）——但我们需要的第1个参数是 `[N, B]`
- `in_fp8` 是 `[B, K]` 连续（行主序）——但第2个参数必须是列主序

因此每个操作数都需要重新排列：

```python
go_T = go_fp8.t().contiguous()   # [N, B] 行主序
in_col = _to_col_major(in_fp8)   # [B, K] 列主序
```

**`go_T`**：单独 `go_fp8.t()` 会得到 `[N, B]`，步长为 `(1, B)`（列主序）——对于第1个参数位置是错误的。`.contiguous()` 强制进行物理拷贝，将内存重新排列为行主序步长 `(B, 1)`。这是一个真正的内存拷贝（“转置+拷贝”内核）。

**`in_col`**：`_to_col_major` 执行 `x.t().contiguous().t()`。对于 `in_fp8`，这产生相同的逻辑形状 `[B, K]`，但步长为 `(1, B)`（列主序）而不是 `(K, 1)`，因此内核可以高效地按列读取。

## 缩放因子

`scale_a=go_inv` 和 `scale_b=in_inv` 是**反量化**缩放因子（来自 `_to_fp8`）。内核计算：

```
grad_weight = (go_T * go_inv) @ (in_col * in_inv)   # 在FP8算术中
```

反量化操作被融合到cuBLAS内核本身中，因此 `grad_weight` 以全精度（`grad_output.dtype`）输出，无需单独的反量化步骤。

## 为什么这里使用 `use_fast_accum=False`

- `use_fast_accum=True` 以降低精度累积点积（更快，精度略低）——用于**前向**传播。
- 反向传播使用 `False`，使得 `[N, B] @ [B, K]` 的点积以fp32累积，尽可能保持梯度精度。梯度是训练中数值最敏感的部分（它们会进入优化器状态），因此精度值得付出微小的速度代价。

## 一个微妙之处：为什么第一个参数必须拷贝

与GEMM 1（`grad_input = grad_output @ weight`）对比：在GEMM 1中，`w_fp8` 是 `[N, K]` 连续，因此 `w_fp8.t()` 已经具有列主序步长——**无需拷贝**（这就是GEMM 1设置开销小的原因）。GEMM 2需要在**第一个**参数位置进行转置，这强制进行了 `.contiguous()` 拷贝。`go_T` 和 `in_col` 都只计算一次并被复用——注意 `go_fp8` 在GEMM 1和GEMM 2之间共享，因此量化工作被分摊到两个反向矩阵乘法中。

简而言之：这是标准的 `grad_output.T @ input` 矩阵乘法，量化为FP8（梯度使用e5m2，输入使用e4m3），通过布局调整满足 `_scaled_mm` 的A行主序/B列主序要求，由缩放因子在内部反量化，并以全精度累积以保证梯度精度。