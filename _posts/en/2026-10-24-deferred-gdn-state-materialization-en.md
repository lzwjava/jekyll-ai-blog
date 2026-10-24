---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deferred GDN State Materialization
translated: false
type: note
---

Now I have the full picture. Here's what this file is:

## What `kernels/gdn_defer/gdn_defer.cu` is

A **custom CUDA kernel pair for the Qwen3.8-27B GDN (Gated DeltaNet) speculative-decode path**, derived from vLLM v0.30.0's `fused_gdn_decode_kernel.cu`. It's an optimization experiment in this heterogeneous-inference project.

### The problem it solves

In stock vLLM, the GDN MTP (multi-token prediction) decode kernel writes the full fp32 recurrent state after **every** speculative token — `k+1` slots × 3 MiB per sequence per layer — but only slot `accepted-1` is ever read back next step. Profile showed those stores became wasted DRAM write traffic on the **down GEMM** (37→52 µs at c=4).

### The fix: defer the state stores

**Kernel A — `gdn_mtp`** (per layer, in the forward): runs the identical compute as stock, but instead of storing the k+1 state slots, it saves the *ingredients* needed to replay later:
- normalized `k` (fp32), `v` (bf16), decay & beta per token (k+1 slots × 16 KiB vs. 3 MiB)
- `meta`: epoch stamp, source slot, token count, destination slots
- These buffers have fixed addresses so the forward stays **capturable in a CUDA graph** (epoch is read from device memory).

**Kernel B — `gdn_materialize`** (once per step, all layers, *after* accepted counts are known and before vLLM's mamba postprocess): reloads the source state, replays only the accepted tokens with the same per-token update code, and stores just the final slots — `slot[accepted-1]`, plus `slot[bias]` when the align-mode postprocess copies a block-boundary state.

### Key details

- `token_update<>` is templated and shared by both kernels so the state arithmetic (FMA contraction, shuffle order) is the *same instruction sequence* — bit-consistent with stock.
- `kDefer=false` compiles the stock kernel unchanged, used as the reference for the unit test (bit-identical outputs; the JIT script forces `--use_fast_math` to match vLLM's build).
- Supports both runner variants: V1 (per-batch-row counts) and V2 (`idx_map` → request slot, `precomputed` counts).
- `__trap()` on impossible accepted counts — refuses to write a wrong state silently.

### Wiring (in `registry.py`)

Activated only with `QWEN38_GDN_DEFER=1` + spec decode + TP=1/PP=1:
- `GdnDefer.__init__` allocates all fixed-address buffers
- `begin_step` bumps the device epoch and writes the spec-row → batch-row map
- `decode(...)` runs kernel A per layer
- `materialize(...)` runs kernel B after accepted counts are known

The gist: **"don't store the 3 MiB recurrent state for all speculative tokens — save the 16 KiB replay ingredients, then materialize only the states that will actually be read."**
