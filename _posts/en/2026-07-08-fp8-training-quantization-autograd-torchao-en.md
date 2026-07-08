---
audio: false
generated: true
image: false
lang: en
layout: post
title: "FP8 Training: Quantization, Autograd, Torchao"
translated: false
type: note
---

Question: Explain how this minimal FP8 training implementation for nanochat works — the quantization math, the three-GEMM autograd function, the `_scaled_mm` layout constraints, and how/why it differs from torchao's tensor-subclass approach.

Answer:

## 1. Why FP8 at all

On H100/MI300X, the tensor cores have a throughput hierarchy: FP8 GEMMs run at roughly 2x the FLOPs/s of BF16 GEMMs (same peak FLOP count per cycle, but FP8 uses half the bits per operand, so cuBLAS/cuBLASLt and the CUTLASS kernels can push more MACs/cycle through the same silicon). The catch is FP8 has only 8 bits total (1 sign + 4/5 exponent + 3/2 mantissa), so you can't just cast weights/activations to FP8 statically — you need **dynamic scaling** to keep the tensor's values inside FP8's representable range without losing all your precision to underflow/overflow.

This file implements exactly one recipe: **tensorwise dynamic scaling** — one scalar scale per tensor, recomputed every forward/backward call from the tensor's actual max value. That's the cheapest variant (cuBLAS does the scaling for you inside `_scaled_mm`); rowwise scaling needs a fancier CUTLASS kernel because each row needs its own scale factor threaded through the accumulation.

## 2. The quantization math

```python
fp8_max = torch.finfo(fp8_dtype).max          # e.g. 448.0 for e4m3fn
amax = x.float().abs().max()                   # tensorwise max magnitude
scale = fp8_max / amax.double().clamp(min=EPS)  # maps [0, amax] -> [0, fp8_max]
x_fp8 = (x.float() * scale).clamp(-fp8_max, fp8_max).to(fp8_dtype)
inv_scale = scale.reciprocal()
```

This is just min-max affine quantization with zero-point pinned at 0 (symmetric quantization). The reason for `.double()` in the scale division: FP8 quantization error compounds fast, and if `torch.compile` traces this differently than eager mode (different fusion order → different intermediate rounding), you get numeric drift between compiled/uncompiled runs. Doing the division in fp64 removes that ambiguity — it's the same trick torchao uses.

Note `inv_scale`, not `scale`, is what gets passed to `_scaled_mm`. That's because `_scaled_mm`'s contract is: *dequantize by multiplying by `scale_a * scale_b`* — so it needs the inverse of what you multiplied by to quantize. This is a classic "which direction does the API want the scale" footgun; get it backwards and your outputs are off by `scale²`.

## 3. Format choice: e4m3 vs e5m2

|  | exponent bits | mantissa bits | dynamic range | precision |
|---|---|---|---|---|
| e4m3 | 4 | 3 | ±448 (NVIDIA) / ±240 (AMD fnuz) | higher (8 mantissa levels per octave) |
| e5m2 | 5 | 2 | ±57344 | lower, wider range |

Activations and weights (used in forward, i.e. `input @ weight.T`) use e4m3 because their distributions are relatively bounded and you want mantissa precision. Gradients use e5m2 because gradient magnitudes vary by orders of magnitude across layers/steps (vanishing/exploding gradient territory) and you'd rather have range than precision — an e4m3 gradient tensor would clip or underflow constantly.

AMD's ROCm doesn't implement IEEE-754-style FP8 subnormals the same way NVIDIA does — it uses "fnuz" (finite, no negative zero) variants with a shifted exponent bias, hence smaller magnitude range (240 vs 448). The code detects this via `torch.version.hip` and picks the right dtype — this is the single line that makes it portable across your RTX 4070 (well, actually Ada doesn't have FP8 tensor cores at fast rates, but MI300X does) and AMD Dev Cloud:

```python
_IS_AMD = torch.cuda.is_available() and hasattr(torch.version, 'hip') and torch.version.hip is not None
FP8_E4M3 = torch.float8_e4m3fnuz if _IS_AMD else torch.float8_e4m3fn
```

## 4. `_scaled_mm` layout requirements — the part that actually breaks if you get it wrong

cuBLAS's FP8 kernel (`cublasLtMatmul` under the hood) has a hardware constraint: **A must be row-major, B must be column-major**. This isn't a PyTorch API choice, it's literally how the FP8 tensor core instructions are wired (they read A row-by-row and B column-by-column for the same reason regular GEMM kernels prefer specific layouts — memory coalescing on the load path).

```python
def _to_col_major(x):
    return x.t().contiguous().t()
```

Walk through this: if `x` is `[N, K]` row-major (strides `(K, 1)`), then `x.t()` is `[K, N]` with strides `(1, K)` — that's already column-major logically, but it's a *view*, and if the underlying storage isn't contiguous in that view's traversal order the kernel can't just reinterpret strides — some paths need an actual materialized column-major buffer. `.t().contiguous().t()`: transpose (view), force a copy in that transposed order (`.contiguous()` now physically lays out memory as `[K,N]` row-major = `[N,K]` column-major), transpose back to restore the logical `[N,K]` shape. Net effect: same shape, different memory layout, forcing a copy if one is needed.

The forward pass is the free case:

```python
output = torch._scaled_mm(
    input_fp8,          # [B, K] contiguous → row-major, correct for A ✓
    weight_fp8.t(),     # weight_fp8 is [N, K] contiguous → .t() is [K, N] with strides (1, K) → already column-major ✓ NO COPY
    ...
)
```

This is why `nn.Linear` stores `weight` as `[out_features, in_features]` and not the other way — it's not just convention, it makes `weight.t()` free-to-use as the column-major operand for `input @ weight.T`.

Backward needs two more GEMMs, and here the layouts aren't free:

```python
# grad_input = grad_output @ weight       [B,N] @ [N,K] -> [B,K]
go_fp8, go_inv = _to_fp8(grad_output, FP8_E5M2)     # [B,N] row-major, correct for A ✓
w_col = _to_col_major(w_fp8)                         # w_fp8 is [N,K] row-major, needs conversion to col-major — COPY
grad_input = torch._scaled_mm(go_fp8, w_col, ...)

# grad_weight = grad_output.T @ input     [N,B] @ [B,K] -> [N,K]
go_T = go_fp8.t().contiguous()   # go_fp8.t() view is [N,B] col-major; but A needs row-major -> physical copy
in_col = _to_col_major(in_fp8)   # in_fp8 is [B,K] row-major, needs col-major -> copy
grad_weight = torch._scaled_mm(go_T, in_col, ...)
```

So per Linear layer per step you get: 1 free transpose (forward), 2 forced copies (`w_col`, `in_col`) + 1 forced copy (`go_T`) in backward = 3 physical FP8 tensor copies. These are cheap (FP8 = 1 byte/elem, and the tensors are already-quantized so it's a fast memcpy-with-stride-remap), but they're real GPU-bandwidth-bound kernels — this is the actual overhead beyond the "glue op" cost the docstring mentions.

## 5. `use_fast_accum`

```python
use_fast_accum=True   # forward
use_fast_accum=False  # backward (both GEMMs)
```

`_scaled_mm`'s fast-accum mode accumulates partial dot products in reduced precision inside the tensor core pipeline (skips some of the FP32 accumulation staging) for extra throughput. Forward output feeds into a nonlinearity/loss where a bit more noise is tolerable; gradients directly determine weight updates over thousands of steps, so accumulated rounding error compounds — hence full accumulation precision in backward. This mirrors what torchao and NVIDIA's own recipes (e.g. Transformer Engine) do.

## 6. The autograd.Function itself

```python
@torch._dynamo.allow_in_graph
class _Float8Matmul(torch.autograd.Function):
```

`torch.autograd.Function` is the standard way to hand-write a custom forward/backward pair when you want to bypass PyTorch's op-by-op autograd tracing (here: because the FP8 casts, `_scaled_mm` calls, and layout juggling aren't things you want individually recorded in the autograd graph — you want one atomic "FP8 linear" node whose backward you define by hand).

`ctx.save_for_backward(input_fp8, input_inv, weight_fp8, weight_inv)` — notice it saves the **already-quantized FP8 tensors**, not the original fp32/bf16 tensors. This is a memory-saving trick: FP8 tensors are 4x/2x smaller than fp32/bf16, so activation memory for the backward pass drops proportionally — this is one of the main practical wins of FP8 training beyond raw matmul speed, since activation memory is usually the binding constraint for batch size on a 192GB MI300X vs a 12GB 4070.

`@torch._dynamo.allow_in_graph` — tells Dynamo (the tracer behind `torch.compile`) "don't try to trace inside this function's Python control flow, just record one opaque call node in the FX graph, and rely on the class's own forward/backward for autograd." Without this, `torch.compile` would try to trace through the autograd.Function's Python body directly, choke on `ctx.save_for_backward`, and either graph-break or produce something semantically wrong.

## 7. Where this fundamentally differs from torchao

torchao's `Float8TrainingTensor` is a **tensor subclass**: it wraps FP8 data + scale as a proper `torch.Tensor` subtype and implements `__torch_dispatch__`, meaning every aten op (`aten.mm`, `aten.t`, `aten.reshape`, `aten.clone`, ...) that touches this tensor type gets intercepted and re-routed to FP8-aware kernels. This is powerful — it means arbitrary code (`x.reshape(...).clone()[0:10]`) "just works" and stays FP8-aware without you writing a matmul-specific autograd.Function. But it needs a dispatch handler for basically every op that could reasonably touch the tensor, hence ~2000 lines.

This file instead treats FP8-ness as a *local implementation detail of one Linear layer's matmul*, not a property that propagates through the tensor type system. `Float8Linear.forward` takes normal bf16 tensors in and returns normal bf16 tensors out — FP8 never leaves this function. This is why it's ~150 lines: you're not building a type system, you're writing three GEMM calls.

Compile-graph consequence, concretely: with torchao, if you have `Float8Linear -> LayerNorm -> Float8Linear`, Inductor sees the amax/scale/cast ops as individual graph nodes and can potentially fuse the LayerNorm's output write with the next layer's `amax` reduction (same memory pass). With this approach, Inductor sees `Float8Linear` as one opaque call — it can optimize everything *around* it (fuse attention internals, fuse norms) but treats the FP8 boundary as a hard wall. In practice the matmul itself dominates FLOPs by orders of magnitude over the glue ops, so this fusion loss is a rounding error on total step time — the actual reason this file is "slightly faster" per its own docstring is avoiding tensor-subclass dispatch overhead (Python-level `__torch_dispatch__` calls are not free) and simpler compile graphs (less time in Dynamo/Inductor tracing).

## 8. `convert_to_float8_training` — the module-surgery function

```python
def _convert(mod, prefix=""):
    for name, child in mod.named_children():
        fqn = f"{prefix}.{name}" if prefix else name
        _convert(child, fqn)   # post-order: recurse into children first
        if isinstance(child, nn.Linear) and not isinstance(child, Float8Linear):
            if module_filter_fn is None or module_filter_fn(child, fqn):
                setattr(mod, name, Float8Linear.from_float(child))
```

Post-order traversal (children before parent) matters here mainly for correctness of `named_children()` iteration when you're mutating the tree via `setattr` mid-walk — recursing first avoids any ordering surprise from replacing a node before its children are visited. `module_filter_fn` is the hook you'd use to skip e.g. the final `lm_head` (vocab-sized, might not be a multiple of 16 which some FP8 kernels require) or embedding-adjacent linears where FP8 hurts convergence more than it's worth (this matches what DeepSeek-v2/v3 papers report — they keep some layers, like the output projection or MoE router, in higher precision).

`Float8Linear.from_float` uses `torch.device("meta")` to build the new module shell without allocating real storage, then reassigns `.weight`/`.bias` to point at the *original* tensors — zero extra GPU memory for the conversion, just a type-level shim. This is the same pattern as `nn.Module._apply` internals and matches how you'd want to bolt FP8 onto your existing GPT-2/nanochat checkpoint loading path without touching the state dict.

## Practical note for your MI300X runs

Given you're mid-way through nanochat + heading toward DeepSeek v4 MoE: the MoE router/gating linears are exactly the layers you'd want `module_filter_fn` to exclude from FP8 (small dims relative to expert FFNs, and routing decisions are precision-sensitive — a mis-routed token from quantization noise is a bigger correctness risk than a slightly-off gradient in a regular FFN). Also worth checking: MI300X's FP8 tensor core throughput advantage over BF16 is real but smaller than H100's in some benchmarks due to different matrix core generations (CDNA3 vs Hopper) — worth profiling `_scaled_mm` vs plain `bf16 @ bf16` on your actual shapes before assuming the 2x number holds.
