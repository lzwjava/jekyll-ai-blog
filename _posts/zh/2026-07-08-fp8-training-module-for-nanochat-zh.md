---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat的FP8训练模块
translated: true
type: note
---

问题：您能否解释一下这个用于nanochat的最小FP8训练模块的设计和机制，并展示文档字符串中描述的`_Float8Matmul`实际实现会是什么样子？

答案：

这是一份设计文档，旨在用约150行的直接实现替换torchao的`Float8Linear`（约2000行，张量子类架构），该实现基于两个PyTorch原语：`float8_e4m3fn`/`float8_e5m2`数据类型和`torch._scaled_mm`。下面我将分解其机制，然后实现它。

## 核心原语：`torch._scaled_mm`

已确认的函数签名：_scaled_mm(Tensor self, Tensor mat2, *, Tensor? bias=None, ScalarType? out_dtype=None, Tensor? scale_a=None, Tensor? scale_b=None, Tensor? scale_result=None, bool use_fast_accum=False)。这是一个cuBLAS支持的缩放FP8通用矩阵乘法（GEMM）：接收两个FP8张量及其每个张量的fp32缩放标量，以FP8张量核心精度执行矩阵乘法，并在输出时反量化到`out_dtype`。`use_fast_accum=True`会跳过周期性的全精度累加器重新同步——这能显著提高吞吐量，但会牺牲一些数值精度，这与文档字符串中关于无编译图重写时eager模式按位一致性的说明相符。

文档字符串中的**布局约束**是真实存在的，而且很容易踩坑：cuBLAS要求A为行主序，B为列主序。从连续的`[out, in]`权重张量执行`weight.t()`已经是列主序且零拷贝——这正是`nn.Linear`将权重存储为`[out_features, in_features]`并执行`input @ weight.T`的原因。

## 为什么仅使用张量级缩放就能从2000行缩减到150行

torchao的通用性代价来源于`Float8Tensor`是一个`torch.Tensor`的子类，并带有`__torch_dispatch__`——每一个aten操作（`mm`、`t`、`view`、`clone`、`to`等）都需要一个FP8感知的处理函数，因为任意用户代码都可能在这些张量上调用这些操作。这相当于构建了一个微型调度表虚拟机。而一个单一的`autograd.Function`完全绕开了这一点：PyTorch的自动求导引擎只调用两个方法（`forward`、`backward`），并将内部所有内容视为不透明，因此您只需编写三个矩阵乘法即可完成——无需处理对携带FP8的张量进行转置、视图或其他任何操作，因为FP8张量永远不会逃逸出函数体。

## 实现

```python
import torch
import torch.nn as nn
from torch.autograd import Function

# --- 平台相关数据类型选择 ---
def _is_amd() -> bool:
    return torch.version.hip is not None

if _is_amd():
    E4M3 = torch.float8_e4m3fnuz
    E5M2 = torch.float8_e5m2fnuz
    FP8_MAX = 240.0       # AMD e4m3fnuz 范围
else:
    E4M3 = torch.float8_e4m3fn
    E5M2 = torch.float8_e5m2
    FP8_MAX = 448.0       # NVIDIA e4m3fn 范围

EPS = 1e-12

def _amax_scale(t: torch.Tensor, fp8_max: float = FP8_MAX) -> torch.Tensor:
    """scale = fp8_max / max(|t|)，在fp32中计算以保证稳定性。"""
    amax = t.abs().float().max().clamp_min(EPS)
    return fp8_max / amax

def _quantize(t: torch.Tensor, dtype: torch.dtype, scale: torch.Tensor) -> torch.Tensor:
    fp8_max = FP8_MAX if dtype in (torch.float8_e4m3fn, torch.float8_e4m3fnuz) else 57344.0
    return (t.float() * scale).clamp(-fp8_max, fp8_max).to(dtype)

def _to_col_major(t: torch.Tensor) -> torch.Tensor:
    """cuBLAS要求B为列主序。如果t.t()已经是连续的
    （即t本身来自转置），则这是一个不进行复制的视图操作。"""
    if t.stride(-1) == 1:          # 已是行主序 -> 需要列主序副本
        return t.t().contiguous().t()
    return t                        # 已是列主序，例如weight.t()

class _Float8Matmul(Function):
    """`input @ weight.T`的即插即用FP8替代品。
    输入输出均为全精度；FP8仅发生在内部。"""

    @staticmethod
    def forward(ctx, input: torch.Tensor, weight: torch.Tensor):
        # --- 前向：output = input @ weight.T ---
        in_scale = _amax_scale(input)
        w_scale = _amax_scale(weight)

        input_fp8 = _quantize(input, E4M3, in_scale)
        weight_fp8 = _quantize(weight, E4M3, w_scale)          # [out, in]
        weight_fp8_t = _to_col_major(weight_fp8.t())            # [in, out], 列主序

        out, _ = torch._scaled_mm(
            input_fp8, weight_fp8_t,
            scale_a=(1.0 / in_scale).reshape(1),
            scale_b=(1.0 / w_scale).reshape(1),
            out_dtype=torch.bfloat16,
            use_fast_accum=True,
        )

        ctx.save_for_backward(input, weight)
        return out

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor):
        input, weight = ctx.saved_tensors
        # 梯度使用e5m2——动态范围更宽，尾数精度较低
        go_scale = _amax_scale(grad_output, fp8_max=57344.0)
        go_fp8 = _quantize(grad_output, E5M2, go_scale)

        grad_input = grad_weight = None

        if ctx.needs_input_grad[0]:
            # grad_input = grad_output @ weight
            w_scale = _amax_scale(weight)
            weight_fp8 = _quantize(weight, E4M3, w_scale)
            weight_fp8_cm = _to_col_major(weight_fp8)            # [out, in] 列主序
            grad_input, _ = torch._scaled_mm(
                go_fp8, weight_fp8_cm,
                scale_a=(1.0 / go_scale).reshape(1),
                scale_b=(1.0 / w_scale).reshape(1),
                out_dtype=input.dtype,
                use_fast_accum=True,
            )

        if ctx.needs_input_grad[1]:
            # grad_weight = grad_output.T @ input
            in_scale = _amax_scale(input)
            input_fp8 = _quantize(input, E4M3, in_scale)
            go_fp8_t = _to_col_major(go_fp8.t())                 # [B, out] -> [out, B]...
            input_fp8_cm = _to_col_major(input_fp8)
            grad_weight, _ = torch._scaled_mm(
                go_fp8.t().contiguous(), input_fp8_cm,
                scale_a=(1.0 / go_scale).reshape(1),
                scale_b=(1.0 / in_scale).reshape(1),
                out_dtype=weight.dtype,
                use_fast_accum=True,
            )

        return grad_input, grad_weight


@torch.compiler.allow_in_graph
def float8_matmul(input, weight):
    return _Float8Matmul.apply(input, weight)


class Float8Linear(nn.Linear):
    """即插即用替代nn.Linear。为简单起见，不融合FP8内的偏置——在bf16中后加偏置。"""
    def forward(self, input):
        out = float8_matmul(input, self.weight)
        if self.bias is not None:
            out = out + self.bias
        return out
```

## 编译图权衡的具体体现

`@torch.compiler.allow_in_graph`使得这能折叠成一个不透明节点给Inductor，正如文档字符串所述。与torchao对比：`Float8Tensor.__tensor_flatten__`让`torch.compile`将子类解包成其组成的普通张量（数据、缩放因子），并追踪*经过*量化/反量化操作，从而Inductor能够将例如`amax`归约融合到前一个操作的尾声中。而使用`allow_in_graph`，FP8边界之间的所有内容（注意力、RMSNorm、MoE路由）仍然会得到充分优化——您只是失去了跨越线性边界的融合。考虑到胶水操作是O(numel)的归约/类型转换，紧邻着O(numel × dim)的矩阵乘法，这通常可以忽略不计。

## 在信任它用于nanochat之前需要检查的内容

1. **`use_fast_accum=True` + e5m2梯度**：DeepSeek v3/v2的FP8方案明确警告，e5m2（2位尾数）在多次反向传播中会快速累积误差——这正是DeepSeek实际训练中对流经反向传播的张量使用**分块/瓦片缩放**而非张量级缩放的原因。torch._scaled_mm对DeepSeek-V3风格分块GEMM的支持最近在Hopper+上添加——值得检查现在是否已经足够上游化，以至于可以跳过只写张量级缩放，因为您正在进入MoE v4领域，在那种情况下分块缩放更接近实际需求。
2. 上面的行主序/列主序转置簿记是手动FP8代码中唯一可能因转置错误而静默产生错误数值的地方——在真正运行之前，值得在几种形状上对照`torchao.float8.Float8Linear`进行数值一致性测试。
3. `out_dtype`在实践中是非可选的——省略它会导致一个难以理解的cuBLAS错误而不是清晰的默认行为，上面的代码通过始终显式传递它来避免这一点。

参考：

- [Scaled MM API变更日志（gist）](https://gist.github.com/drisspg/783616821043ab4594b9784f556c6714)
- [torch._scaled_mm use_fast_accum讨论](https://discuss.pytorch.org/t/what-does-the-use-fast-accum-option-do-in-torch-scaled-mm/208719)
- [PyTorch问题：DeepSeek-V3分块scaled-mm支持](https://github.com/pytorch/pytorch/issues/160816)
- [PyTorch Native FP8使用示例](https://towardsdatascience.com/pytorch-native-fp8-fedc06f1c9f7/)
