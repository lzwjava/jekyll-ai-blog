---
audio: false
generated: true
image: false
lang: en
layout: post
title: Triton Crash on Ada GPUs
translated: false
type: note
---

**What happened:**

1. Launched sglang with Qwen/Qwen2.5-1.5B-Instruct on the workstation (lzw@192.168.1.36, RTX 4070)
2. Triton 3.5.1 segfaulted during JIT — first during graph capture, then during inference
3. Tried `--attention-backend torch_native --disable-cuda-graph` — still crashed, and sglang consumed enough resources to drop the SSH connection
4. Tried downgrading Triton to 3.4.0 — pip dependency resolution reverted it back to 3.6.0
5. Current installed versions: torch 2.11.0+cu130, triton 3.6.0, sglang 0.5.9, driver 580.126.20 (CUDA 13.0)

**Root cause:**

Triton 3.5/3.6 JIT compilation crashes on CUDA 13.0 + consumer Ada (sm_89). The segfault happens in Triton's compiler pipeline (MLIR → LLVM → PTX → ptxas), not in GPU compute. Datacenter GPUs (H100/A100) get validated first; consumer cards hit edge bugs. Hardware is fully capable — it's purely a toolchain incompatibility.

**Why simple fixes don't work:**

- `--attention-backend torch_native` — still triggers Triton somewhere in the sglang pipeline
- `pip install triton==3.4.0` — torch 2.11.0 requires triton>=3.5, pip re-upgrades it
- `--no-deps` pin — torch may runtime-reject a lower triton version

**Proposed fix:**

Create a fresh Python venv with CUDA 12.4 wheels: torch 2.5.1+cu124 + triton 3.1.0. This is a known-stable combination for Ada GPUs. The driver 580.x is backward-compatible with CUDA 12.4. Install sglang 0.4.x which works with that torch version.

**Alternative:** Drop vLLM into a fresh venv — it bundles its own validated torch+triton+cuda pins, less manual version management.

**Status:** Analysis done, no action taken yet. Awaiting your decision on which path.
