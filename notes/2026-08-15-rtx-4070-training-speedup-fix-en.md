---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 Training Speedup Fix
translated: false
type: note
---

## Summary

**Why it's slow** — the `Not enough SMs to use max_autotune_gemm mode` warning isn't cosmetic. Inductor's `is_big_gpu()` check requires ≥68 SMs (RTX 3080-class); the RTX 4070 has only 46, so inductor **silently skips its fast Triton GEMM templates for every matmul** and falls back to generic reduction kernels. Combined with no cudagraphs and a tiny micro-batch (4), you get 28.9K tok/s / 47 TFLOPS (28.7% of the 4070's bf16 peak, 14.7% vs the A100 reference nanoGPT uses) — and a ~26-hour total run.

**Fixes applied** (in `/mnt/data/nanoGPT`):
1. `train.py` — force `is_big_gpu` → True before `torch.compile`, so the Triton GEMM templates are used; added a `compile_mode` config knob.
2. `config/train_bilingual.py` — set `compile_mode = 'reduce-overhead'` (cudagraphs, removes ~13K kernel launches/iter). Also left a commented option for `batch_size=8` + `grad_accum=64` (same 524K tok/iter, bigger GEMMs — VRAM has ~3.5GB headroom).

**To apply** (the running process won't pick up file changes — it's only ~45/5000 iters in, so restarting loses ~15 min):
```
# in tmux session 1: Ctrl-C, then
cd /mnt/data/nanoGPT && python3.12 train.py config/train_bilingual.py
```
Expect: iter 0 will be slower (few minutes of kernel recompilation + template autotune + cudagraph capture), then steady-state should drop from ~19s to roughly 11–14s/iter (1.3–1.8×). The inductor kernel cache will remember the new kernels for future restarts.

Want me to restart the run in tmux now and watch the first few iterations to verify the speedup?