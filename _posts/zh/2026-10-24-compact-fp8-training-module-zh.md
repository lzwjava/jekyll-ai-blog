---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 紧凑型FP8训练模块
translated: true
type: note
---

`nanochat/fp8.py` 是一个约150行的、自包含的FP8训练实现，它替代了该项目原本依赖的torchao `Float8Linear`（约2000行）。以下是它的功能：

## 核心思想

一个 `nn.Linear` 在前向传播中需要1次矩阵乘法，在反向传播中需要2次。FP8训练将**每次**矩阵乘法都包装为：将两个操作数量化为FP8格式 → 调用 `torch._scaled_mm` (cuBLAS FP8内核) → 使用逆缩放因子在内部进行反量化。其关键洞察在于 `torch._scaled_mm` 和 `float8_*` 数据类型是PyTorch的内置功能——torchao只是围绕它们进行的编排工作。

## 关键组件

**1. 量化辅助函数 — `_to_fp8` (tensorwise 缩放)**

- 每个张量一个标量缩放因子：`scale = fp8_max / max(|x|)`
- 饱和截断（PyTorch的强制类型转换默认是*环绕*，而非饱和），然后强制转换为FP8格式
- 返回 `(fp8_data, inverse_scale)` — `_scaled_mm` 在矩阵乘法过程中乘以逆缩放因子以恢复数值范围
- 使用float64进行除法运算，以确保 eager 模式和 `torch.compile` 之间的数值一致性（torchao也是如此做的）

**2. FP8数据类型选择（NVIDIA vs AMD）**

- `float8_e4m3fn`/`e4m3fnuz`：4位指数，3位尾数 → 用于**输入和权重**（需要精度）
- `float8_e5m2`/`e5m2fnuz`：5位指数，2位尾数 → 用于**梯度**（可能数值较大，需要范围）
- 通过 `torch.version.hip` 自动检测

**3. 布局要求**

- `torch._scaled_mm` 要求参数A为行主序（连续），参数B为列主序。`_to_col_major` 通过 `x.t().contiguous().t()` 实现。巧妙的是，对于连续的权重，`weight.t()` *已经*是列主序了，因此在 forward 中不需要进行拷贝。

**4. `_Float8Matmul` autograd.Function** — 核心所在：

- **前向传播**：将输入和权重量化为e4m3格式，调用 `_scaled_mm` 并设置 `use_fast_accum=True`（速度更快，精度略低——这对于前向传播来说可以接受），保存FP8张量和缩放因子用于反向传播
- **反向传播**：计算 `grad_input = grad_output @ weight` 和 `grad_weight = grad_output.T @ input`，两者均使用e5m2格式（处理梯度）并设置 `use_fast_accum=False` 以保证精度
- 标记了 `@torch._dynamo.allow_in_graph`，使得 torch.compile 将其视作一个不透明节点

**5. `Float8Linear`** — `nn.Linear` 的即插即用替代方案：

- 权重和偏置保持在 fp32/bf16 格式；只有矩阵乘法在 FP8 下运行
- 将 batch 维度展平为二维（`_scaled_mm` 的要求），计算后再恢复原始形状
- `from_float` 通过 meta device 共享原始模块的权重和偏置（无需拷贝，不占用额外内存）

**6. `convert_to_float8_training`** — 以后序遍历方式遍历模块树，替换每个 `nn.Linear`，并允许传入一个可选的过滤器（例如，跳过维度不是16倍数的层）。`Float8LinearConfig.from_recipe_name` 仅为了与 torchao 的 API 兼容而存在；任何非 `"tensorwise"` 的值都会引发异常。

## 与 torchao 的权衡

- **torchao**：采用张量子类分发——编译时会看到每个操作（amax、缩放、强制类型转换、`_scaled_mm`）都是独立的图节点，因此 Inductor 可以跨层边界进行融合（例如，将 amax 与前一个激活融合）。
- **本项目**：编译时会看到一个不透明的调用——它会优化 FP8 线性层*周围*的一切，但无法跨越边界进行融合。无论哪种方式，GPU内核都是相同的；胶水操作很小，因此这种方式通常稍快一些，并且在 eager 模式下数值结果完全一致，但在 `torch.compile` 下可能会有不同的舍入结果。

实际上：`COMPUTE_DTYPE` 来自 `common.py`（在 Ampere+ 代 GPU 上通常是 bf16），因此输入在进入 FP8 路径之前会被强制转换为 bf16。通过 `module_filter_fn`，当矩阵乘法维度不是16的倍数（H100 的 Tile 大小要求）时，这会直接丢弃掉整个层，使其达到生产使用的标准。
