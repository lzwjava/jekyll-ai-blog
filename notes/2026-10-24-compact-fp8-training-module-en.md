---
audio: false
generated: true
image: false
lang: en
layout: post
title: Compact FP8 Training Module
translated: false
type: note
---

`nanochat/fp8.py` is a ~150-line, self-contained FP8 training implementation that replaces torchao's `Float8Linear` (~2000 lines) for this project. Here's what it does:

## Core idea

A `nn.Linear` needs 3 matmuls: 1 in forward, 2 in backward. FP8 training wraps **each** matmul with: quantize both operands to FP8 → call `torch._scaled_mm` (the cuBLAS FP8 kernel) → it dequantizes internally using inverse scales. The key insight (from the docstring) is that `torch._scaled_mm` and the `float8_*` dtypes are PyTorch built-ins — torchao is just orchestration around them.

## Key components

**1. Quantization helper — `_to_fp8` (tensorwise scaling)**
- One scalar scale per tensor: `scale = fp8_max / max(|x|)`
- Saturating clamp (PyTorch's cast defaults to *wrap*, not saturate) then cast to FP8
- Returns `(fp8_data, inverse_scale)` — `_scaled_mm` multiplies by the inverse to restore range during the matmul
- Uses float64 for the division to keep numerics identical between eager and `torch.compile` (torchao does the same)

**2. FP8 dtype selection (NVIDIA vs AMD)**
- `float8_e4m3fn`/`e4m3fnuz`: 4-bit exponent, 3-bit mantissa → used for **input and weights** (needs precision)
- `float8_e5m2`/`e5m2fnuz`: 5-bit exponent, 2-bit mantissa → used for **gradients** (can be large, needs range)
- Auto-detected via `torch.version.hip`

**3. Layout requirements** — `torch._scaled_mm` needs arg A row-major (contiguous) and arg B column-major. `_to_col_major` does `x.t().contiguous().t()`. Cleverly, `weight.t()` from a contiguous weight is *already* column-major, so no copy is needed in the forward.

**4. `_Float8Matmul` autograd.Function** — the heart:
- **Forward**: quantizes input+weight to e4m3, calls `_scaled_mm` with `use_fast_accum=True` (faster, slightly less accurate — fine for forward), saves the FP8 tensors + scales for backward
- **Backward**: computes `grad_input = grad_output @ weight` and `grad_weight = grad_output.T @ input`, both in e5m2 (gradients) with `use_fast_accum=False` for precision
- Marked `@torch._dynamo.allow_in_graph` so torch.compile treats it as one opaque node

**5. `Float8Linear`** — drop-in `nn.Linear` replacement:
- Weights/biases stay in fp32/bf16; only matmuls run in FP8
- Flattens batch dims to 2D (required by `_scaled_mm`), restores shape after
- `from_float` shares the original module's weight/bias via meta device (no copy, no extra memory)

**6. `convert_to_float8_training`** — walks the module tree post-order, swaps each `nn.Linear` passing an optional filter (e.g. skip dims not divisible by 16). `Float8LinearConfig.from_recipe_name` exists only for API compat with torchao; anything other than `"tensorwise"` raises.

## Trade-off vs torchao

- **torchao**: tensor-subclass dispatch — compile sees every op (amax, scale, cast, `_scaled_mm`) as separate graph nodes, so Inductor can fuse across layer boundaries (e.g. amax with the previous activation).
- **Here**: compile sees one opaque call — it optimizes everything *around* the FP8 linear but can't fuse across the boundary. Same GPU kernel either way; glue ops are tiny, so this is usually slightly faster with identical eager-mode numerics but potentially different rounding under `torch.compile`.

Practically: `COMPUTE_DTYPE` comes from `common.py` (typically bf16 on Ampere+ GPUs), so inputs are cast to bf16 before entering the FP8 path. This drops entire layers for production use when the matmul dimensions aren't multiples of 16 (H100 tile-size requirement) via the `module_filter_fn`.
