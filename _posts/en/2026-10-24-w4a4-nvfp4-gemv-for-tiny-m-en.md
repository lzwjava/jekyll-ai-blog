---
audio: false
generated: true
image: false
lang: en
layout: post
title: W4A4 NVFP4 GEMV for Tiny M
translated: false
type: note
---

`fp4_gemv_kernel` is the single compute kernel in `kernels/fp4_gemv/fp4_gemv.cu` — a hand-written **W4A4 NVFP4 GEMV for tiny M** (decode/MTP-verify MLP), targeted at sm_120a. It computes exactly the tensor-core b12x semantics, just with the FP16-vector ALU path instead of `mma`:

```
out[t,n] = alpha * Σ_g (sa[t,g]·sw[n,g]) * Σ_{i<16} qa[t,16g+i]·qw[n,16g+i]
```

One GEMV per token t: activations `qa` (NVFP4/e2m1) dotted with weights `qw`, per 16-value group scaled by the activation scale `sa` × weight scale `sw`, times a global `alpha` (= input_scale · weight_scale_2).

### Template & launch shape

```cpp
template <int K, int T, int kRowsPerWarp, int kBlockRows>
__global__ void fp4_gemv_kernel(const uint8_t* xq, const uint8_t* xs,
                                const uint8_t* wq, const uint8_t* ws,
                                const float* alpha, __nv_bfloat16* out, int n)
```

- `K` = reduction dim, `T` = tokens (runtime M, 1–8, dispatched by `switch (m)`), `kRowsPerWarp` = 1 or 2, `kBlockRows` = 8 or 16.
- Grid = `n / kBlockRows` (one CTA per output-row block), block = `kBlockRows/kRowsPerWarp × 32` threads.
- Every CTA covers all M tokens × full K for its 8/16 output rows — the "small M" trick: no tensor-core tile padding waste on the token dim.

### Data layout helpers (the NVFP4 block-scale swizzle)

- `decode16(packed, h[8])`: unpacks 16 packed e2m1 bytes into 8 `f16x2` registers via `cvt.rn.f16x2.e2m1x2` (native PTX). Exact: e2m1 decodes exactly into f16.
- `hfma2` = `fma.rn.f16x2`, `group_sum` splits an `f16x2` back into two fp32s and adds.
- `sf_offset(row, group, groups)`: locates a block scale in the **swizzled 128×4 layout** — `(row/128)·(groups/4) + group/4` selects the 512-byte block, then `(row%32)·16 + ((row%128)/32)·4 + group%4` the byte inside.
- `weight_row(flat)`: de-swizzles the CTA's row block — flat rows 0..3 → {...0, 32, 64, 96} (a *quartet*), 4..7 → {1,33,65,97}, etc.

The point of the quartet mapping: for one 64-column scale tile, the CTA's 4 rows' scales are **64 contiguous bytes** → one `uint4` load each.

### Stage 1 — prologue (scales to shared memory)

- `w_scale[kBlockRows][kGroups]`: each lane-task loads a `uint4` per (tile, quartet) from `ws` and scatters the 4 bytes to `w_scale[quartet*4+quartile][kt*4]` — rebuilding the per-row/per-group weight scale table.
- `x_scale[T][kGroups]`: activation scales via `sf_offset`.
- One `__syncthreads()`; weights/activation scales stay resident the whole kernel.

### Stage 2 — the group-parallel main loop

```cpp
for (phase = 0; phase < kPhases; ++phase) {
    g = phase * 32 + lane;                        // each lane owns one 16-value group
    // decode weight group -> wv[r][8] f16x2, wsc[r] = e4m3(scale)
    for (t = 0; t < T; ++t)
      for (r = 0; r < kRowsPerWarp; ++r)
        h = Σ_i hfma2(wv[r][i], xv[i], 0);         // f16x2 even/odd partial sums, EXACT
        acc[r][t] += group_sum(h) * wsc[r] * xsc;
}
```

**This is the whole kernel in one paragraph:** lanes stride K in 16-value groups, one group per lane per phase (32 groups per phase because there are 32 lanes); each lane accumulates the per-group products into register accumulators `acc[kRowsPerWarp][T]`. Unrolled by `FP4_GEMV_UNROLL` (default 4, tunable).

### Stage 3 — epilogue

For each (row, token): **warp-shuffle reduce** `acc` across the 32 lanes (each lane holds a different group offset), then lane 0 writes `out[t·n + row[r]] = bf16(acc · alpha)`. K × 1 row → 32 partial group sums → full dot product.

### Numerics — why it's exact per group

- e2m1 → f16: exact. 8 products of ≤2^6 values: each f16 partial ≤ 8·36 = 288 < 512, so every `fma.rn.f16x2` is **exact** (f16 ulp 1/4 below 512).
- Even + odd partials add exactly in fp32; `sa·sw` (two e4m3) is exact; group_sum · (sa·sw) ≤ 2^20 bits, still exact in fp32.
- So the only difference from the b12x tensor-core path is the **order of cross-group fp32 additions** — hence "bit-identical to b12x in the kernel tests," making it a safe drop-in.

Why this shape: at M ≤ 5 (down K=17408) / M ≤ 4 (gate_up N=34816, K=5120), a tensor-core tile wastes most of its M-dim work, so the FP16-vector path with K split across lanes beats it; above those M's the `.cu` header says b12x is "as fast or faster," and the Python dispatch falls back to `flashinfer_scaled_fp4_mm(..., backend="b12x")`.
