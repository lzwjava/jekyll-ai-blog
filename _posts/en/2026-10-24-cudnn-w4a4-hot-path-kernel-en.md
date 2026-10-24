---
audio: false
generated: true
image: false
lang: en
layout: post
title: cuDNN W4A4 Hot Path Kernel
translated: false
type: note
---

This is `FlashInferCudnnNvFp4LinearKernel.apply_weights` (the cuDNN-backend twin of the W4A4 GEMM path). Unlike `process_weights_after_loading` (one-time layout prep), this is the **per-forward-pass hot path**: it takes a BF16 activation `x` and produces `out = x @ Wᵀ` where `W` is NVFP4-quantized. Line by line:

## 1. Bookkeeping
```python
output_size = layer.output_size_per_partition   # N (output dim of this TP partition)
output_dtype = x.dtype                           # keep BF16
output_shape = [*x.shape[:-1], output_size]      # remember leading dims ([tokens] or [batch, seq, d])
weights_padding_bytes = nvfp4_weight_padding_bytes(layer)
```
The cuDNN kernel can't handle arbitrary matrix dims — weights were padded in `process_weights_after_loading` (K and N rounded up, e.g. to multiples of 8/64). `weights_padding_bytes` records how much, so everything downstream stays aligned with the padded `layer.weight`, and you know how much to trim afterward.

## 2. Quantize the activations on the fly (W4A4)
```python
x_fp4, x_blockscale = scaled_fp4_quant(
    x, layer.input_global_scale_inv,
    is_sf_swizzled_layout=True,
    backend="flashinfer-cudnn",
    padded_n=x.shape[-1] + weights_padding_bytes * 2,
)
```
The weights are 4-bit, so for the GEMM to be mixed-precision it converts the *input* `x` to FP4 too:
- `x_fp4` — activation values as FP4, packed 2 values per byte,
- `x_blockscale` — per-block scale factors, laid out in FlashInfer's swizzled ("sf") format,
- `input_global_scale_inv` — folded in so the divisor becomes a multiply.

`padded_n` pads the activations' K dim to match the padded weight K (`* 2` because one byte holds two 4-bit values) so shapes line up for the kernel.

## 3. The dequantized GEMM
```python
out = flashinfer_scaled_fp4_mm(x_fp4, layer.weight, x_blockscale,
                               layer.weight_scale, layer.alpha, output_dtype,
                               backend="cudnn")
```
The actual math, done *inside the CUDA kernel* with fp32 accumulation:
```
out[m, n] = Σ_k (x_fp4[m,k] · x_blockscale) · (W_fp4[n,k] · w_scale · alpha)
```
i.e. multiply the packed 4-bit matrices and rescale the products by the activation block scale, weight block scale, and `layer.alpha` (the global FP4 weight scale) to recover roughly-BF16 values. All 4-bit operands stay packed in memory; only the accumulator/output are wider.

## 4–5. Trim padding, add bias, restore shape
```python
out = slice_nvfp4_output(out, output_size)  # drop pad columns the kernel wrote
if bias is not None: out = out + bias
return out.view(*output_shape)              # [tokens, N] → original rank
```
The kernel outputs the full padded N, so it gets sliced down to the real `output_size`, bias (if any) is added, and the leading dims (`batch`, `seq`, or bare `tokens`) are restored.

## Why it looks different from the others in the file
There are four sibling kernels — W4A16 cutedsl, cutedsl, trtllm, and this cuDNN one — all funneling into the same `scaled_fp4_quant` + `flashinfer_scaled_fp4_mm` helper but with different `backend=` strings and different padding/swizzling choices per backend:
- cuDNN and CUTLASS reuse the **same swizzled + padded weight layout** (both set up in `process_weights_after_loading` via `swizzle_blockscale` + `pad_nvfp4_weight_for_cutlass`), so their forward paths are near-identical;
- the trtllm path (your first question) instead uses `shuffle_matrix_a`/`shuffle_matrix_sf_a` and pads the activation via `padded_n=` differently.

The input-side quant (`scaled_fp4_quant`) is also what vLLM hooks up to its dynamic-activation-quantization fusion (`kNvfp4Dynamic` + `QuantizedActivation`), so a quantized input from a previous layer can skip this step entirely.
