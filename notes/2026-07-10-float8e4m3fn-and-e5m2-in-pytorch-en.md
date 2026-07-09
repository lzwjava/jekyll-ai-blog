---
audio: false
generated: true
image: false
lang: en
layout: post
title: Float8_e4m3fn and e5m2 in PyTorch
translated: false
type: note
---

Question: What do `float8_e4m3fn` and `float8_e5m2` mean in PyTorch?

Answer:

Both are 8-bit floating point formats defined in the OCP FP8 spec (based on the FP8 paper from NVIDIA/ARM/Intel, arXiv:2209.05433). The suffixes tell you the exponent/mantissa split, and the `fn` tells you the special-value encoding rules.

## Bit layout

```
sign(1) + exponent(e) + mantissa(m) = 8 bits total

float8_e4m3fn:  1 sign | 4 exponent | 3 mantissa
float8_e5m2:    1 sign | 5 exponent | 2 mantissa
```

More exponent bits → wider dynamic range, fewer mantissa bits → coarser precision. It's the classic range-vs-precision tradeoff, same tradeoff as fp16 vs bf16 but pushed to 8 bits.

## What `fn` means

From PyTorch's own naming convention (mirrors LLVM/MLIR):

- **f** = finite values only, no `inf` encoding (unlike IEEE754 which reserves an exponent pattern for ±inf)
- **n** = NaN encoding differs from IEEE (e4m3fn uses a single NaN pattern: `S.1111.111`, reclaiming what IEEE would spend on inf/NaN combos)
- **uz** variant (`e4m3fnuz`, `e5m2fnuz`) = unsigned zero only, no `-0.0`, and shifts the exponent bias by 1 (used by AMD ROCm / some HW backends)

So `e4m3fn` trades away inf representation to squeeze out one more representable value near the top of the range (max magnitude 448 instead of a smaller number if inf were reserved).

## Concrete numbers (`torch.finfo`)

float8_e4m3fn has 8 bits, max value 448, min value -448, smallest normal 0.015625, and eps of 0.125. float8_e5m2 has 8 bits, max value 57344, min value -57344, smallest normal 6.10352e-05, and eps of 0.25.

```python
import torch

for dtype in [torch.float8_e4m3fn, torch.float8_e5m2]:
    info = torch.finfo(dtype)
    print(dtype, info.max, info.min, info.smallest_normal, info.eps)

# float8_e4m3fn   448.0    -448.0    0.015625    0.125
# float8_e5m2    57344.0  -57344.0   6.10352e-05 0.25
```

`e4m3fn`: ~3 decimal digits of range (max 448), better precision (3 mantissa bits → eps 0.125).
`e5m2`: much wider dynamic range (max 57344, close to fp16's range), worse precision (2 mantissa bits → eps 0.25).

## Practical usage — this maps directly onto your MI300X / DeepSeek-v4 MoE work

**e4m3fn** is the standard choice for **weights and forward activations** in FP8 training/inference — you need precision more than range there, since well-normalized activations sit in a bounded region.

**e5m2** is typically used for **gradients** in FP8 mixed-precision training — gradients can have much larger dynamic range (spiky, long-tailed), so you trade mantissa bits for exponent range. This mirrors the original Transformer Engine FP8 recipe (NVIDIA Hopper): E4M3 forward, E5M2 backward.

```python
import torch

x = torch.randn(4, 4, device="cuda", dtype=torch.bfloat16)

x_e4m3 = x.to(torch.float8_e4m3fn)   # weights/activations
x_e5m2 = x.to(torch.float8_e5m2)     # gradients

print(x_e4m3.dtype, x_e5m2.dtype)
```

Important caveat for your nanochat/DeepSeek-v4 work: performing basic arithmetic operations directly on FP8 tensors is largely unsupported in PyTorch — these are what PyTorch calls **"shell dtypes"**: a specialized dtype where only a small subset of ops and backends are supported. You don't do `a + b` on raw fp8 tensors. Instead:

1. Store/cast data as fp8 (memory savings, and feeds fp8 GEMM kernels on Hopper/MI300X)
2. Actual matmul happens via a dedicated FP8 GEMM kernel (`torch._scaled_mm`, or Transformer Engine, or `torchao`'s `Float8Tensor`) that takes per-tensor or per-row **scale factors** alongside the fp8 data — because 448 max range clips fast, so you rescale activations before quantizing
3. Accumulation happens in higher precision (fp32/bf16), then optionally re-quantized

```python
# torchao pattern — closer to what you'd actually use for DeepSeek v4 MoE experts
from torchao.float8 import convert_to_float8_training

# per-row scaling is what makes e4m3fn viable for MoE —
# each expert's activation distribution differs, so per-tensor
# scaling alone underutilizes the [-448, 448] range
convert_to_float8_training(model)  # swaps nn.Linear -> Float8Linear internally
```

For MoE specifically (DeepSeek v4), the tricky part isn't the dtype itself — it's **scale factor granularity**. DeepSeek's own FP8 training recipe (from the v3 paper, and presumably continued into v4) uses **fine-grained per-tile/per-block scaling** rather than per-tensor, because different experts see very different activation magnitudes and a single scale factor per tensor wastes dynamic range. If you're implementing this from scratch on the MI300X, that's the part worth spending your engineering time on, not the dtype selection itself.

References:

- [PyTorch Native FP8 Data Types (Medium/TDS)](https://towardsdatascience.com/pytorch-native-fp8-fedc06f1c9f7/)
- [MX basic dtypes in pytorch/pytorch · Issue #146414](https://github.com/pytorch/pytorch/issues/146414)
- [Float8 in PyTorch [1/x] — PyTorch Dev Discuss](https://dev-discuss.pytorch.org/t/float8-in-pytorch-1-x/1815)
- [FP8 Formats for Deep Learning (arXiv:2209.05433)](https://arxiv.org/pdf/2209.05433.pdf)
