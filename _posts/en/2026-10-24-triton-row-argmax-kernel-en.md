---
audio: false
generated: true
image: false
lang: en
layout: post
title: Triton Row Argmax Kernel
translated: false
type: note
---

## What `kernels/decode_fuse/argmax.py` is

A **Triton row-argmax kernel** for the **MTP draft head** — the kernel that picks `argmax(logits)` at the end of the speculative-draft step, replacing PyTorch's `logits.max(dim=-1).indices`.

### The problem it solves

Stock `logits.max(dim=-1)` is a **1-CTA-per-row reduction**. On this model's vocab (98,304 columns), that's slow — the header quotes ~23 µs on the PRO 5000 for the naive path. The replacement is a **2-stage split reduction: 4096-wide chunks in stage 1, one small combine kernel in stage 2**, which parallelizes the reduction across many more CTAs than rows.

### The kernel structure

**Stage 1** `_argmax_stage1` — grid `(M, nchunk)`, one CTA per (row, chunk):
- Loads its 4096-element chunk (masked with `-inf` past the row end) into fp32.
- Computes the chunk's first max index *and* whether the chunk holds a NaN:
  - `first_nan = min(offs where isnan)` — NaN position
  - `m = max(vf)` where NaNs were replaced by `-inf` so they don't pollute the max
  - `i = min(offs where vf == m)` — **first** index of the chunk maximum (ties → lowest index)
- Stores per-chunk `(value, index)` — or `(NaN, first_nan)` if it found one.

**Stage 2** `_argmax_stage2` — grid `(M,)`, one warp per row:
- Loads all nchunk `(value, index)` pairs.
- A chunk with NaN beats everything (`nan_ix = min` of NaN-carrying chunk indices → earliest chunk wins, matching torch where the first NaN is the max).
- Otherwise `m = max(vals)`, `i = min(idx where vals == m)` — since chunks are in index order, **lowest global index wins ties**, exactly like `torch.max().indices`.
- Writes the `int64` global column index.

### Why the NaN handling matters

CUDA-graph padding rows can hold **NaN logits**, and `torch.max` semantics say *NaN counts as the maximum* and the *first* NaN wins. So this isn't just "find the max" — it must reproduce torch's exact tie/NaN behavior (the docstring asserts "same result as `torch.max(dim=-1).indices`" and it's used as a drop-in).

### Wiring

`vllm/model_executor/layers/logits_processor.py`:
1. Gated by `QWEN38_ARGMAX=1` (set in `scripts/duo.sh` for the SPEC layout, along with `DRAFT_VOCAB`).
2. The function is registered via `direct_register_custom_op("qwen38_row_argmax", ...)` with a `fake_impl` that returns an `int64[M]` empty tensor for torch.compile.
3. It's only used when `tp_size == 1` and logits are 2-D contiguous (`line 247`) — otherwise stock `logits.max(dim=-1)` runs. The local index is shifted by `org_vocab_start_index` to get the global vocab index.

The nice property: it lives in `kernels/decode_fuse/` (a Python-only Triton payload, no `.cu`) and is loaded via `sys.path` + the `QWEN27B_KERNELS` env var, same convention as the other JIT kernels — but with Triton instead of a CUDA extension.
