---
audio: false
generated: true
image: false
lang: en
layout: post
title: "M3 Debug: RoPE Fix, Box Down"
translated: false
type: note
---

## Summary — mini-llama.cpp M3 investigation/state

### What was found

**Milestone 3 committed & pushed** (`fad109a`, on `origin/main`): tokenizer + Qwen2 CPU forward pass + `m3_cpu.c` driver.

**Then I verified M3 end-to-end** — it was previously never built or run. Two bugs surfaced:

1. **Garbage output (root cause: RoPE pairing)**
   - Reference `llama.cpp` on the box generates`"The capital of France is Paris."` ✓
   - Our driver produced nonsense (`));// thá»...ition`), top-5 logits flat at ~13–15.
   - Confirmed from reference source (`ggml-cpu/ops.cpp` + `llama-model.cpp`): **Qwen2 = `LLAMA_ROPE_TYPE_NEOX` = half-split pairs `(i, i + head_dim/2)`** with `theta_i = pos·base^(−2i/d)`. Our `rope_cpu` paired `(2i, 2i+1)` — interleaved, wrong.
   - ✅ **Fix applied** (half-split pairing; theta formula verified identical to ggml's `rope_cache_init`).

2. **Cleanup segfault** — crashes in `tokenizer_free`/heap teardown after generation (no `[cleanup] tokenizer freed`). Likely heap corruption in the forward pass (suspicious buffers: `score` sizing, unused `ctx`). **Remaining, unverified** — was mid-diagnosis with ASAN when things went sideways.

**Build/hygiene fixes also applied but NOT yet committed/pushed:**
- `Makefile`: added `mini-llama-m3` CPU target (`-lm`)
- `quant.c`: misleading-indentation warning fixed
- `qwen2.c`: unused-param warning silenced
- Model downloaded: `~/models/qwen2.5-0.5b-instruct-q8_0.gguf` (675MB, from `hf-mirror.com` — HF direct is blocked)

### Current urgent status ⚠️

**The Debian box (192.168.1.137) is DOWN/unreachable** — no ping, no SSH. It disappeared right after a GCC `-fsanitize=address,undefined` compile segfaulted the compiler itself (internal compiler error, likely RAM exhaustion). Box probably crashed or is thrashing.

### What's at risk on the box (uncommitted, un-pushed)
- `src/qwen2.c` (RoPE fix + warning fix), `Makefile`, `src/quant.c` — scp'd to disk ✅, but **not committed**
- The source changes *are* safe on the local Mac at `/tmp/ww-m3/` (backup copies exist)

### Next steps (when the box comes back)
1. **FIRST: commit the pending fixes** (`git add -A && commit && push`) so they're not lost
2. Rebuild `mini-llama-m3` (plain `cc -O2`, no sanitizers) and re-run — expect "Paris" now
3. Diagnose the segfault: use a small **address-space check by code inspection** or a lighter approach (e.g. `-fsanitize=address` alone with `-O0`, or add guard debug prints) rather than the heavy UBSan build that killed the box
4. Verify against reference logits, then commit the verified fix

Want me to keep polling for the box and resume once it's back?
