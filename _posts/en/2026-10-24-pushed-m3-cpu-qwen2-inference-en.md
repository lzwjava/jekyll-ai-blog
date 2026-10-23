---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pushed M3 CPU Qwen2 Inference
translated: false
type: note
---

All pushed. Summary:

## Done — `lzw@192.168.1.137` → `github.com/lzwjava/mini-llama.cpp`

**Commit `fad109a`** (11 files changed, +591/−18) rebased onto the remote's newer `eb4b536`:
```
fad109a feat: M3 - CPU Qwen2 inference: tokenizer + quantized forward pass
eb4b536 chore: remove mini-llama-m2 binary, add to .gitignore   (was on remote)
33853e3 feat: M2 - block dequant (Q5_0/Q8_0/Q4_K/Q6_K) + VRAM upload + real GEMM
```
Working tree clean, `main` in sync with `origin/main`.

## What the issue was (before you asked to commit)

1. **Milestone 3 work was stranded uncommitted** — the new CPU-inference code (`tokenizer.c/h`, `qwen2.c/h`, `m3_cpu.c`) was untracked, plus fixes in `gguf.c/h` (array-type KV for `tokenizer.ggml.*`, subnormal fp16) and `quant.c/h` (Q4_K file-layout scale unpacking).
2. **`mini-llama-m2` ELF binary was accidentally committed** in the M2 commit and then rebuilt, leaving a dirty binary in the tree. Fixed: `git rm --cached`, and closed the `.gitignore` gap (`mini-llama-m2`/`mini-llama-m3` were missing).
3. **The `make` build stalls on the `nvcc` M2 target** (sm_52 CUDA compile) — that's why `make` appeared hung; the CPU path itself is fast.
4. **Two latent build issues** (not committed-blocking, but flagging for your next session):
   - `Makefile` has no CPU driver target for `m3_cpu.c` and doesn't link `-lm`, so `qwen2.c` fails at link: undefined `sqrtf`, `pow`, `sincosf`, `expf`
   - `quant.c:105` misleading-indentation warning (for-loop + bare `return 0` on one line)

Want me to wire the M3 CPU target into the `Makefile` (with `-lm`) as a follow-up?
