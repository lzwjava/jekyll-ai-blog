---
audio: false
generated: true
image: false
lang: en
layout: post
title: M3 CPU Forward Pass Bug
translated: false
type: note
---

Hi! Quick status check-in — we're deep in the M3 GPU work. Here's where things stand:

## Done ✅
- **M3 groundwork**: repo cloned, `mini-llama-m3` (your CPU forward) built & wired into the Makefile, model downloaded, CUDA toolkit + nvcc 12.4 installed (survived one crash mid-install)
- **Built llama.cpp** on the box as the gold reference

## The problem I'm debugging 🔍
Your committed **CPU forward pass (qwen2.c) produces garbage** — for *"The capital of France is"* it emits `èĹ¿anaå®ĩØ¯Ø§...`, while llama.cpp (even greedy, even raw-no-template) cleanly says *"Paris. It is the largest city in Europe..."*

I've verified exhaustively and eliminated:
- ✅ Tokenizer (round-trip perfect)
- ✅ Weights & dequant — **byte-identical** to llama.cpp (dumped llama.cpp's own mmap bytes with an instrumentation patch: `db 96 89 03 3e ed a5 20...` matches my reader & gguf-py exactly)
- ✅ Forward structure (matches llama.cpp's qwen2 graph op-for-op)
- ✅ RoPE dims / eps / GQA grouping / cuBLAS-style matmul orientations

...but h was exploding at layer 2 (rms 0.24 → 36), and an **independent numpy re-implementation** also reproduces the garbage — so my code and the numpy ref agree with each other but not with llama.cpp, leaving a *very* subtle difference still hiding. I was about to build **llm-gym** (llama.cpp's internal-graph explorer) to bisect layer-by-layer where activations first diverge.

Before I keep burning time here — how do you want to play it?

1. **Keep digging** — find the CPU M3 bug first, so the GPU M3 has a verified oracle
2. **Pivot** — GPU M3 verifies directly against llama.cpp (skip fixing the CPU reference)
3. **Something else?**
