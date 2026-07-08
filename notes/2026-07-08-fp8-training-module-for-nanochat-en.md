---
audio: false
generated: true
image: false
lang: en
layout: post
title: FP8 Training Module for Nanochat
translated: false
type: note
---

Question: Can you explain the design and mechanics of this minimal FP8 training module for nanochat, and show what the actual `_Float8Matmul` implementation described in the docstring would look like?

Answer:

This is a design doc for replacing torchao's `Float8Linear` (~2000 lines, tensor-subclass architecture) with a ~150-line direct implementation built on two PyTorch primitives: the `float8_e4m3fn`/`float8_e5m2` dtypes and `torch._scaled_mm`. Let me break down the mechanics and then implement it.

## The core primitive: `torch._scaled_mm`

Confirmed signature _scaled_mm(Tensor self, Tensor mat2, *, Tensor? bias=None, ScalarType? out_dtype=None, Tensor? scale_a=None, Tensor? scale_b=None, Tensor? scale_result=None, bool use_fast_accum=False). It's a cuBLAS-backed scaled FP8 GEMM: takes two FP8 tensors + their per-tensor fp32 scale scalars, does the matmul in FP8 tensor-core precision, and dequantizes on the way out to `out_dtype`. `use_fast_accum=True` skips periodic full-precision resync of the tensor-core accumulator — it increases throughput noticeably but trades off some numerical accuracy, which matches the docstring's note about eager-mode being bitwise-identical only without compile-graph rewrites.

The **layout constraint** in the docstring is real and easy to trip on: cuBLAS wants A row-major, B column-major. `weight.t()` from a contiguous `[out, in]` weight is already column-major with zero copy — this is exactly why `nn.Linear` stores weight as `[out_features, in_features]` and does `input @ weight.T`.

## Why tensorwise-only cuts 2000 → 150 lines

torchao's generality tax comes from `Float8Tensor` being a `torch.Tensor` subclass with `__torch_dispatch__` — every aten op (`mm`, `t`, `view`, `clone`, `to`, ...) needs an FP8-aware handler because arbitrary user code might call any of them on the tensor. You're building a mini dispatch-table VM. A single `autograd.Function` sidesteps that entirely: PyTorch's autograd engine calls exactly two methods (`forward`, `backward`) and treats everything inside as opaque, so you write the three matmuls once and you're done — no need to handle transpose, view, or any other op on an FP8-carrying tensor because the FP8 tensor never escapes the function body.

## Implementation

```python
import torch
import torch.nn as nn
from torch.autograd import Function

# --- platform-aware dtype selection ---
def _is_amd() -> bool:
    return torch.version.hip is not None

if _is_amd():
    E4M3 = torch.float8_e4m3fnuz
    E5M2 = torch.float8_e5m2fnuz
    FP8_MAX = 240.0       # AMD e4m3fnuz range
else:
    E4M3 = torch.float8_e4m3fn
    E5M2 = torch.float8_e5m2
    FP8_MAX = 448.0       # NVIDIA e4m3fn range

EPS = 1e-12

def _amax_scale(t: torch.Tensor, fp8_max: float = FP8_MAX) -> torch.Tensor:
    """scale = fp8_max / max(|t|), computed in fp32 for stability."""
    amax = t.abs().float().max().clamp_min(EPS)
    return fp8_max / amax

def _quantize(t: torch.Tensor, dtype: torch.dtype, scale: torch.Tensor) -> torch.Tensor:
    fp8_max = FP8_MAX if dtype in (torch.float8_e4m3fn, torch.float8_e4m3fnuz) else 57344.0
    return (t.float() * scale).clamp(-fp8_max, fp8_max).to(dtype)

def _to_col_major(t: torch.Tensor) -> torch.Tensor:
    """cuBLAS wants B column-major. If t.t() is already contiguous
    (i.e. t itself came from a transpose), this is a no-op view."""
    if t.stride(-1) == 1:          # already row-major -> need col-major copy
        return t.t().contiguous().t()
    return t                        # already col-major, e.g. weight.t()

class _Float8Matmul(Function):
    """Drop-in FP8 replacement for `input @ weight.T`.
    Full-precision in, full-precision out; FP8 happens only inside."""

    @staticmethod
    def forward(ctx, input: torch.Tensor, weight: torch.Tensor):
        # --- forward: output = input @ weight.T ---
        in_scale = _amax_scale(input)
        w_scale = _amax_scale(weight)

        input_fp8 = _quantize(input, E4M3, in_scale)
        weight_fp8 = _quantize(weight, E4M3, w_scale)          # [out, in]
        weight_fp8_t = _to_col_major(weight_fp8.t())            # [in, out], col-major

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
        # gradients use e5m2 — wider dynamic range, less mantissa precision
        go_scale = _amax_scale(grad_output, fp8_max=57344.0)
        go_fp8 = _quantize(grad_output, E5M2, go_scale)

        grad_input = grad_weight = None

        if ctx.needs_input_grad[0]:
            # grad_input = grad_output @ weight
            w_scale = _amax_scale(weight)
            weight_fp8 = _quantize(weight, E4M3, w_scale)
            weight_fp8_cm = _to_col_major(weight_fp8)            # [out, in] col-major
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
    """nn.Linear drop-in. No bias-in-FP8 fusion for simplicity — add bias in bf16 after."""
    def forward(self, input):
        out = float8_matmul(input, self.weight)
        if self.bias is not None:
            out = out + self.bias
        return out
```

## The compile-graph tradeoff, made concrete

`@torch.compiler.allow_in_graph` is what makes this collapse into one opaque node for Inductor, exactly as the docstring says. Contrast with torchao: `Float8Tensor.__tensor_flatten__` lets `torch.compile` unpack the subclass into its constituent plain tensors (data, scale) and trace *through* the quantize/dequantize ops, so Inductor can fuse e.g. the `amax` reduction into the epilogue of the preceding op. With `allow_in_graph`, everything between the FP8 boundaries (attention, RMSNorm, MoE routing) still gets fully optimized — you just lose fusion *across* the linear boundary. Given the glue ops are O(numel) reductions/casts next to an O(numel × dim) matmul, this is usually noise.

## What I'd sanity-check before trusting it in nanochat

1. **`use_fast_accum=True` + e5m2 gradients**: DeepSeek v3/v2's FP8 recipes explicitly warn e5m2 (2 mantissa bits) accumulates error fast over many backward passes — this is why DeepSeek's actual training uses **blockwise/tile scaling**, not tensorwise, for exactly the tensors flowing through backward. torch._scaled_mm support for DeepSeek-V3 style blockwise GEMMs was added recently on Hopper+ — worth checking if that's now upstream enough to skip writing tensorwise-only, since you're heading into MoE v4 territory where blockwise is closer to what you'll actually want.
2. Row-major/col-major transpose bookkeeping above is the single place manual FP8 code silently produces wrong numerics if you get a transpose backwards — worth a numerical parity test against `torchao.float8.Float8Linear` on a few shapes before trusting it in a real run.
3. `out_dtype` is non-optional in practice — omitting it causes an inscrutable cuBLAS error rather than a clean default, which the code above avoids by always passing it explicitly.

References:

- [Scaled MM API changelog (gist)](https://gist.github.com/drisspg/783616821043ab4594b9784f556c6714)
- [torch._scaled_mm use_fast_accum discussion](https://discuss.pytorch.org/t/what-does-the-use-fast-accum-option-do-in-torch-scaled-mm/208719)
- [PyTorch issue: DeepSeek-V3 blockwise scaled-mm support](https://github.com/pytorch/pytorch/issues/160816)
- [PyTorch Native FP8 usage example](https://towardsdatascience.com/pytorch-native-fp8-fedc06f1c9f7/)
