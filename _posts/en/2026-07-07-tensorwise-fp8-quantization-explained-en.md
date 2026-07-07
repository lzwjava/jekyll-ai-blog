---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tensorwise FP8 Quantization Explained
translated: false
type: note
---

Question: Explain this `_to_fp8()` function and the math behind tensorwise FP8 quantization.

Answer:

This is **dynamic symmetric tensorwise quantization**.

The goal is:

> Convert a float tensor into FP8 while preserving as much dynamic range as possible, then return the scale needed to recover the original values during matrix multiplication.

The important thing is:

> **The FP8 tensor is not useful by itself.**
> It is always paired with a scale.

---

## Step 0. Disable gradients

```python
@torch.no_grad()
```

Quantization is not part of backpropagation.

This tells PyTorch:

* don't build autograd graph
* save memory
* slightly faster

---

# Step 1

```python
fp8_max = torch.finfo(fp8_dtype).max
```

Suppose

```
fp8_dtype = torch.float8_e4m3fn
```

then

```
fp8_max ≈ 448
```

For another FP8 format

```
e5m2

max ≈ 57344
```

This is simply

```
largest representable FP8 number
```

---

# Step 2

```python
amax = x.float().abs().max()
```

Suppose

```
x =
[
    2,
   -5,
    9,
    1
]
```

Then

```
amax = 9
```

Notice

```
ONE scalar

for the ENTIRE tensor
```

That's why this is called

```
Tensorwise scaling
```

instead of

```
Rowwise
Columnwise
Blockwise
```

---

# Step 3

```python
scale = fp8_max / amax
```

Suppose

```
fp8_max = 448

amax = 9
```

Then

```
scale = 49.777...
```

Why?

Because we want

```
9

↓

448
```

So every value gets multiplied by

```
448 / 9
```

Think of stretching the tensor until its largest value exactly fills the FP8 range.

Original

```
[-9,9]
```

Scaled

```
[-448,448]
```

This maximizes precision because it uses nearly the full representable range.

---

# Why clamp?

```python
clamp(min=EPS)
```

Suppose

```
amax = 0
```

Then

```
448 / 0
```

would produce infinity.

Instead

```
amax = max(amax, EPS)
```

avoids division by zero.

---

# Why double precision?

```python
amax.double()
```

Comment says

```
compile
vs

eager
```

The issue is

```
float32 division
```

can produce tiny rounding differences.

Example

```
448 / 0.3
```

Depending on optimization,

```
1493.333374

or

1493.333252
```

Those tiny differences may cause values to fall on different sides of an FP8 rounding boundary.

Using

```
float64
```

makes both execution modes deterministic.

---

# Step 4

```python
x_scaled = x.float() * scale
```

Suppose

```
x =
[
2,
5,
9
]
```

Scale

```
49.777
```

Result

```
[
99.5,
248.9,
448
]
```

Now the tensor fully occupies the FP8 numeric range.

---

# Step 5

```python
x_clamped = x_scaled.clamp(
    -fp8_max,
     fp8_max
)
```

Suppose numerical error gives

```
449.2
```

FP8 cannot represent that.

Without clamp,

casting may overflow or produce undefined behavior (depending on the implementation and dtype). Clamping ensures values stay within the valid FP8 range before conversion.

---

# Step 6

```python
x_fp8 = x_clamped.to(fp8_dtype)
```

Now convert

```
248.9
```

into FP8.

Remember

FP8 has

* very few exponent bits
* very few mantissa bits

so

```
248.9
```

might become

```
248
```

or

```
256
```

depending on the nearest representable FP8 value.

This is where quantization error is introduced.

---

# Step 7

```python
inv_scale = scale.reciprocal()
```

Instead of returning

```
scale
```

they return

```
1 / scale
```

Why?

Because

`torch._scaled_mm` expects:

```
real_value

=

fp8_value

×

inverse_scale
```

Suppose

Original

```
9
```

Scaled

```
448
```

Stored

```
448 (FP8)
```

Later

```
448 × (9/448)

=

9
```

No explicit dequantization step is needed. During the matrix multiplication, `torch._scaled_mm` multiplies FP8 operands by their inverse scales internally while accumulating in higher precision.

---

# Entire pipeline

```
FP32 tensor

      │

      ▼

Find max(abs(x))

      │

      ▼

Compute

scale

=

fp8_max / amax

      │

      ▼

Multiply tensor

      │

      ▼

Clamp

      │

      ▼

Cast to FP8

      │

      ▼

Store

(
FP8 tensor,
inverse scale
)
```

---

# Why tensorwise scaling?

Advantages:

```
Only ONE scale

Very little metadata

Fast

cuBLAS supports it directly
```

Disadvantages:

Suppose

```
[
0.001,
0.002,
0.003,
100
]
```

The scale is determined by

```
100
```

After scaling,

```
0.001
```

becomes a very small FP8 value and may lose significant precision because the dynamic range is dominated by the large outlier.

Rowwise or blockwise scaling would compute multiple scales, preserving more precision for smaller values at the cost of additional metadata and more complex kernels.

---

# Why return `(x_fp8, inv_scale)` instead of dequantizing later?

Modern FP8 GEMM kernels (such as those behind `torch._scaled_mm`) fuse the computation:

```
FP8 A
FP8 B
↓

Multiply

↓

Apply inverse scales

↓

Accumulate in FP16/BF16/FP32

↓

Output
```

This avoids materializing dequantized FP16 tensors in memory, reducing bandwidth and improving performance. The hardware effectively computes:

[
C = (A_{fp8} \times s_A^{-1}) \times (B_{fp8} \times s_B^{-1})
]

while performing the accumulation in higher precision, which is why this function returns both the quantized tensor and its inverse scale rather than reconstructing the original tensor first.
