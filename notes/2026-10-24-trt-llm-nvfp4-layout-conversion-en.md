---
audio: false
generated: true
image: false
lang: en
layout: post
title: TRT-LLM NVFP4 Layout Conversion
translated: false
type: note
---

This is `FlashInferTrtllmNvFp4LinearKernel.process_weights_after_loading` in `vllm/model_executor/kernels/linear/nvfp4/flashinfer.py` — the **load-time weight-layout conversion** for the NVFP4 W4A4 GEMM that runs through FlashInfer's TensorRT-LLM backend.

### Why it exists

The checkpoint stores the NVFP4 weights in the *standard* layout (packed e2m1 nibbles, plain block scales). But the trtllm tensor-core GEMM needs both operands in a **hardware-shuffled layout** — a byte permutation designed so the SM's `ldmatrix`/MMA fragment loaders can fetch exactly the bytes a 128-row epilogue tile needs, with no index arithmetic at compute time. Doing this once after loading instead of every forward is the whole point of the hook.

### Line by line

```python
weight = layer.weight.data
weight_scale = layer.weight_scale.data
epilogue_tile_m = 128
```

Snapshots the raw values, and fixes the shuffle granularity: trtllm NVFP4 GEMMs process output in **128-row tiles**, so both the fp4 bytes and the scale bytes are permuted independently per 128-row group.

```python
layer.weight = torch.nn.Parameter(
    shuffle_matrix_a(weight.view(torch.uint8), epilogue_tile_m),
    requires_grad=False,
)
```

- `weight` (e2m1 nibbles, 2-per-byte) is re-viewed as raw `uint8` because torch has no math on packed 4-bit data.
- `shuffle_matrix_a` reorders those bytes into the **shuffled 4-bit A-matrix layout** (the same permutation TRT-LLM's scaled-FP4 kernels use; FlashInfer mirrors it so `flashinfer_scaled_fp4_mm(..., backend="trtllm")` understands the result).
- Wrapped in a frozen `Parameter` so the model carries the shuffled weights but they're not trainable.

```python
layer.weight_scale = torch.nn.Parameter(
    shuffle_matrix_sf_a(weight_scale.view(torch.uint8), epilogue_tile_m)
    .reshape(weight_scale.shape)
    .view(torch.float8_e4m3fn),
    requires_grad=False,
)
```

- The scales (e4m3 per 16-value block) get their own shuffle: `shuffle_matrix_sf_a` reorganizes them into the layout the GEMM's scale-loading (dequant) step expects.
- `.reshape(weight_scale.shape)` — shuffled result comes back as a flat buffer or differently-shaped tensor; this restores the original `[N, K/16]` shape.
- `.view(torch.float8_e4m3fn)` — the shuffle ran on raw bytes; this re-labels the buffer as fp8 so downstream code sees `layer.weight_scale` with the right dtype for `flashinfer_scaled_fp4_mm`.
- Frozen `Parameter` again.

### The contrast that makes it worth explaining

This is the *third* operand-layout convention visible in `flashinfer.py`:

| backend | weight data prep | scale layout |
| --- | --- | --- |
| cute-dsl (`process_weights_after_loading` at line 148) | `flashinfer_prepare_bf16_fp4_weights(..., backend="cute-dsl")` | own repack |
| trtllm (this one) | `shuffle_matrix_a`, tile 128 | `shuffle_matrix_sf_a`, tile 128 |
| b12x + your `kernels/fp4_gemv/` | standard / raw | **128×4 blockscale swizzle** (`swizzle_blockscale`) |

So the fp4_gemv kernel you asked about works on the *standard* (swizzled-scale) layout — its `sf_offset`/`weight_row` helpers exist precisely because it chose *not* to adopt the trtllm shuffle. Each backend's `is_supported`/`can_implement` frictionlessly picks one convention; this hook is where the checkpoint data is funneled into it.
