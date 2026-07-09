---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch中的Float8_e4m3fn和e5m2
translated: true
type: note
---

问题：PyTorch 中的 `float8_e4m3fn` 和 `float8_e5m2` 是什么意思？

回答：

两者都是 OCP FP8 规范中定义的 8 位浮点格式（基于 NVIDIA/ARM/Intel 的 FP8 论文，arXiv:2209.05433）。后缀表示指数/尾数的划分方式，而 `fn` 表示特殊值的编码规则。

## 位布局

```
符号(1) + 指数(e) + 尾数(m) = 总共 8 位

float8_e4m3fn:  1 符号 | 4 指数 | 3 尾数
float8_e5m2:    1 符号 | 5 指数 | 2 尾数
```

指数位越多 → 动态范围越宽，尾数位越少 → 精度越粗。这是经典的精度与范围权衡，与 fp16 vs bf16 的权衡相同，但被压缩到了 8 位。

## `fn` 的含义

根据 PyTorch 自身的命名约定（镜像 LLVM/MLIR）：

- **f** = 仅限有限值，没有 `inf` 编码（与 IEEE754 不同，后者为 ±inf 保留了一个指数模式）
- **n** = NaN 编码与 IEEE 不同（e4m3fn 使用单一的 NaN 模式：`S.1111.111`，收回了 IEEE 用于 inf/NaN 组合的那部分位模式）
- **uz** 变体（`e4m3fnuz`、`e5m2fnuz`）= 仅无符号零，没有 `-0.0`，并且将指数偏置偏移 1（由 AMD ROCm / 某些硬件后端使用）

因此 `e4m3fn` 舍弃了 inf 表示，以在接近范围上限处挤出另一个可表示的值（最大幅值 448，而如果保留 inf，这个值会更小）。

## 具体数值（`torch.finfo`）

float8_e4m3fn 有 8 位，最大值 448，最小值 -448，最小正规数 0.015625，eps 为 0.125。float8_e5m2 有 8 位，最大值 57344，最小值 -57344，最小正规数 6.10352e-05，eps 为 0.25。

```python
import torch

for dtype in [torch.float8_e4m3fn, torch.float8_e5m2]:
    info = torch.finfo(dtype)
    print(dtype, info.max, info.min, info.smallest_normal, info.eps)

# float8_e4m3fn   448.0    -448.0    0.015625    0.125
# float8_e5m2    57344.0  -57344.0   6.10352e-05 0.25
```

`e4m3fn`：约 3 位十进制数的范围（最大 448），精度更好（3 位尾数 → eps 0.125）。
`e5m2`：动态范围宽得多（最大 57344，接近 fp16 的范围），精度更差（2 位尾数 → eps 0.25）。

## 实际应用——这直接映射到你的 MI300X / DeepSeek-v4 MoE 工作

**e4m3fn** 是 FP8 训练/推理中**权重和正向激活**的标准选择——因为那里更需要精度而非范围，归一化良好的激活值位于有界区域内。

**e5m2** 通常用于 FP8 混合精度训练中的**梯度**——梯度可能具有更大的动态范围（陡峭、长尾），因此你用尾数位换取指数范围。这镜像了原始的 Transformer Engine FP8 方案（NVIDIA Hopper）：前向使用 E4M3，反向使用 E5M2。

```python
import torch

x = torch.randn(4, 4, device="cuda", dtype=torch.bfloat16)

x_e4m3 = x.to(torch.float8_e4m3fn)   # 权重/激活
x_e5m2 = x.to(torch.float8_e5m2)     # 梯度

print(x_e4m3.dtype, x_e5m2.dtype)
```

对于你的 nanochat/DeepSeek-v4 工作，一个重要注意事项：在 PyTorch 中直接对 FP8 张量执行基本算术运算基本上是不支持的——这些是 PyTorch 所谓的 **"shell dtypes"**：一种专门的 dtype，只支持一小部分操作和后端。你不会对原始的 fp8 张量执行 `a + b`。相反：

1. 将数据存储/转换为 fp8（节省内存，并为 Hopper/MI300X 上的 fp8 GEMM 内核提供输入）
2. 实际的矩阵乘法通过专用的 FP8 GEMM 内核（`torch._scaled_mm`、Transformer Engine 或 `torchao` 的 `Float8Tensor`）完成，该内核会接收与 fp8 数据一同提供的**逐张量或逐行缩放因子**——因为 448 的最大范围会快速截断，所以你在量化之前需要重新缩放激活值
3. 累加在更高精度（fp32/bf16）中进行，然后可选地重新量化

```python
# torchao 模式——更接近你实际上会用于 DeepSeek v4 MoE 专家的情况
from torchao.float8 import convert_to_float8_training

# 逐行缩放使得 e4m3fn 对 MoE 可行——
# 每个专家的激活分布不同，因此仅使用逐张量缩放会低估 [-448, 448] 的范围
convert_to_float8_training(model)  # 内部将 nn.Linear 替换为 Float8Linear
```

对于 MoE 来说（DeepSeek v4），棘手的部分不是 dtype 本身——而是**缩放因子的粒度**。DeepSeek 自己的 FP8 训练方案（来自 v3 论文，并且很可能延续到 v4）使用**细粒度的逐块/逐瓦片缩放**，而不是逐张量缩放，因为不同专家看到的激活幅值差异很大，单个张量缩放因子会浪费动态范围。如果你要从头在 MI300X 上实现这一点，那才是值得你投入工程时间的部分，而不是 dtype 选择本身。

参考资料：

- [PyTorch Native FP8 Data Types (Medium/TDS)](https://towardsdatascience.com/pytorch-native-fp8-fedc06f1c9f7/)
- [MX basic dtypes in pytorch/pytorch · Issue #146414](https://github.com/pytorch/pytorch/issues/146414)
- [Float8 in PyTorch [1/x] — PyTorch Dev Discuss](https://dev-discuss.pytorch.org/t/float8-in-pytorch-1-x/1815)
- [FP8 Formats for Deep Learning (arXiv:2209.05433)](https://arxiv.org/pdf/2209.05433.pdf)
