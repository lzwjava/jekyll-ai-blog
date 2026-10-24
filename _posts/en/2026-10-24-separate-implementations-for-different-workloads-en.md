---
audio: false
generated: true
image: false
lang: en
layout: post
title: Separate Implementations for Different Workloads
translated: false
type: note
---

## The two kernels are unrelated implementations for *different* workloads

They're not competing alternatives of the same op — each replaces a different stock vLLM path for a specific shape/regime. That's why there's **no single if/else choosing between them**; each has its own env-gated dispatch with a fallback.

### `kernels/fp4_gemv/` — W4A4 NVFP4 **GEMV** (the MLP linears)

- Computes `out[t,n] = Σ_g sa·sw · Σ_{i<16} qa[t,16g+i]·qw[n,16g+i]` — a *linear-layer* math kernel (few tokens `M≤8` × hidden `K` × output `N`).
- Replaces FlashInfer's `mm_fp4` (b12x backend) for the Qwen3.8-27B **MLP** at small M: down (`N=5120,K=17408`, M≤5) and gate_up (`N=34816,K=5120`, M≤4).
- This is the **decode/MTP-verify** workload — GQKV/MLP linears that run on tiny token counts.

### `kernels/fp8attn/` — paged FP8 tensor-core **attention** (KV-cache reads)

- A full-flash-attention-style kernel: FP8 E4M3 QK/PV on `mma.sync.m16n8k32.f8f6f4`, online softmax, paged KV. Two builds: 8-warp prefill (`ext()`) and 4-warp spec-verify decode (`ext_verify()`, `FP8_NW=4`).
- Replaces b12x's paged *extend attention* and trtllm's *xqa decode* for the Qwen3.8-27B **full-attention layers** (HQ 24, HK 4, D 256, page 64), deduplicating cache reads/repacks.

So: **fp4_gemv = the linear/MLP phase; fp8attn = the attention phase**. Peers in the same "heterogeneous-inference" kernel suite (both sm_120a, both fixed-shape hand-written CUDA with a JIT loader, both activated by `QWEN38_*` flags), but they never see each other's inputs.

### The dispatch branches

**fp4_gemv** — `vllm/model_executor/kernels/linear/nvfp4/flashinfer.py`:

1. Import gate (line 61–66): `_QWEN38_GEMV_ON = os.environ.get("QWEN38_FP4_GEMV","0")=="1"` → JIT-loads the extension.
2. `apply_weights` (line 474):

   ```python
   max_m = _QWEN38_GEMV_MAX_M.get((layer.weight.shape[0], x_fp4.shape[-1]*2), 0)  # (N,K)->M cap
   if (_QWEN38_GEMV_ON and max_m and output_dtype==torch.bfloat16 and x_fp4.dim()==2
           and not nvfp4_weight_padding_bytes(layer)):
       out = torch.ops.vllm.qwen38_fp4_mm(...)
   else:
       out = flashinfer_scaled_fp4_mm(..., backend="b12x")
   ```

3. The M-vs-b12x threshold is inside the custom op `_qwen38_fp4_mm` (`if 1 <= M <= max_m: gemv else b12x`) — deliberately inside a custom op so `torch.compile` doesn't specialize on `M`, which changes per step.

**fp8attn** — `vllm/v1/attention/backends/flashinfer.py`:

1. Whole b12x-prefill pathway is gated at metadata-build time (line 1903): `prefill.b12x = ... if _B12X_PF and not use_dcp and causal else None`.
2. Prefill forward (`_qwen38_b12x_prefill`, line 276): `_FP8EMU` emulation first (evaluation), then `if _FP8ATTN and page==64 and head_size==256 and num_heads==24 and num_kv_heads==4 and contiguous` → `fp8_extend_batch`; else the b12x plan.
3. Spec-verify decode (line 2729): `if _FP8DEC and _qwen38_fp8_verify(...)` → the `FP8_NW=4` build; `_qwen38_fp8_verify` returns False for non-applicable batches (non-causal, wrong configs, non-contiguous), so it **falls back to `flashinfer_xqa_batch_decode_with_kv_cache` automatically**.

Bottom line: fp4_gemv and fp8attn belong to *different pipeline stages* (linear vs attention); the only thing connecting them is the same env-flag/KN kernel-suite convention, with b12x/trtllm as the shared fallback.
