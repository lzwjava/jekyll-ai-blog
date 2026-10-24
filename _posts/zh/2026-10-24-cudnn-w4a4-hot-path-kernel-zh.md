---
audio: false
generated: true
image: false
lang: zh
layout: post
title: cuDNN W4A4热路径内核
translated: true
type: note
---

这是 `FlashInferCudnnNvFp4LinearKernel.apply_weights`（W4A4 GEMM 路径的 cuDNN 后端孪生函数）。与 `process_weights_after_loading`（一次性布局准备）不同，这里是 **每次前向传播的 hot path**：它接受一个 BF16 激活值 `x` 并产生 `out = x @ Wᵀ`，其中 `W` 是 NVFP4 量化后的权重。逐行解释：

## 1. 记录

```python
output_size = layer.output_size_per_partition   # N (output dim of this TP partition)
output_dtype = x.dtype                           # keep BF16
output_shape = [*x.shape[:-1], output_size]      # remember leading dims ([tokens] or [batch, seq, d])
weights_padding_bytes = nvfp4_weight_padding_bytes(layer)
```

cuDNN kernel 无法处理任意矩阵维度——权重已在 `process_weights_after_loading` 中进行了填充（K 和 N 被向上取整，例如到 8/64 的倍数）。`weights_padding_bytes` 记录了填充量，以便下游所有操作与填充后的 `layer.weight` 保持对齐，并且你知道之后需要修剪多少。

## 2. 即时量化激活值（W4A4）

```python
x_fp4, x_blockscale = scaled_fp4_quant(
    x, layer.input_global_scale_inv,
    is_sf_swizzled_layout=True,
    backend="flashinfer-cudnn",
    padded_n=x.shape[-1] + weights_padding_bytes * 2,
)
```

由于权重是 4 位的，因此为了让 GEMM 使用混合精度，它也会将 *输入* `x` 转换为 FP4：

- `x_fp4` — 激活值作为 FP4，每字节打包 2 个值，
- `x_blockscale` — 每块的缩放因子，以 FlashInfer 的 swizzled ("sf") 格式排列，
- `input_global_scale_inv` — 被合并进来，使得除法变为乘法。

`padded_n` 对激活值的 K 维度进行填充，以匹配填充后的权重 K（`* 2` 因为一个字节容纳两个 4 位值），从而使形状与 kernel 对齐。

## 3. 反量化后的 GEMM

```python
out = flashinfer_scaled_fp4_mm(x_fp4, layer.weight, x_blockscale,
                               layer.weight_scale, layer.alpha, output_dtype,
                               backend="cudnn")
```

实际运算在 CUDA kernel 内部完成，使用 fp32 累加：

```
out[m, n] = Σ_k (x_fp4[m,k] · x_blockscale) · (W_fp4[n,k] · w_scale · alpha)
```

即，将打包的 4 位矩阵相乘，然后通过激活块缩放因子、权值块缩放因子和 `layer.alpha`（全局 FP4 权值缩放因子）重新缩放乘积，以恢复近似 BF16 的值。所有 4 位操作数在内存中保持打包状态；只有累加器/输出具有更宽的位数。

## 4–5. 修剪填充、添加偏置、恢复形状

```python
out = slice_nvfp4_output(out, output_size)  # drop pad columns the kernel wrote
if bias is not None: out = out + bias
return out.view(*output_shape)              # [tokens, N] → original rank
```

kernel 输出的是完整填充后的 N，因此它被切片到实际的 `output_size`，偏置（如果有的话）被加上，并且前导维度（`batch`、`seq` 或仅 `tokens`）被恢复。

## 为何与文件中的其他部分不同

这里有四个兄弟 kernel——W4A16 cutedsl、cutedsl、trtllm 和这个 cuDNN 版本——它们都汇集到同一个 `scaled_fp4_quant` + `flashinfer_scaled_fp4_mm` 辅助函数中，但每个 backend 使用不同的 `backend=` 字符串以及不同的填充/swizzling 选择：

- cuDNN 和 CUTLASS 复用**相同的 swizzled + padded 权重布局**（两者均在 `process_weights_after_loading` 中通过 `swizzle_blockscale` + `pad_nvfp4_weight_for_cutlass` 设置），因此它们的前向路径几乎相同；
- 而 trtllm 路径（你的第一个问题）则使用 `shuffle_matrix_a`/`shuffle_matrix_sf_a`，并通过 `padded_n=` 以不同的方式填充激活值。

输入侧的量化（`scaled_fp4_quant`）也是 vLLM 连接到其动态激活量化融合（`kNvfp4Dynamic` + `QuantizedActivation`）的方式，因此来自前一层的量化输入可以完全跳过此步骤。
