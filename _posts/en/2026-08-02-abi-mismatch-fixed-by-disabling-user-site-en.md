---
audio: false
generated: true
image: false
lang: en
layout: post
title: ABI Mismatch Fixed by Disabling User Site
translated: false
type: note
---

Everything works end-to-end. Here's the full picture:

## What happened

The **install succeeded** (torch 2.9.1+cu128, transformers 4.57.3, flashinfer 0.6.16, sgl-kernel 0.3.21, minisgl editable — all in `/usr/local/lib/python3.12/dist-packages`). The earlier run died with `ENOSPC` only because the harness's output buffer hit a transient disk-full state on `/` (it has 15G free now).

## The real bug found

At runtime, Python loaded **torch 2.11.0 from the user site** (`/home/lzw/.local/lib/python3.12/site-packages` — a separate env with nano_vllm, flash_attn, etc.), which shadowed the project's torch 2.9.1. `sgl_kernel` 0.3.21's `common_ops.abi3.so` was built against torch 2.9's `c10_cuda` ABI and failed with:

```
undefined symbol: _ZN3c104cuda29c10_cuda_check_implementationEiPKcS2_ib
```

I confirmed with `cuobjdump` that the sm100 build is a fat binary containing **sm_89 cubins** (fine for the RTX 4070), and that torch 2.9.1's `libc10_cuda.so` exports the required symbol — so the ABI mismatch was the *only* problem.

## Fix

Disable the user site (which the project's own `torch<2.10.0` constraint already anticipated):

```bash
PYTHONNOUSERSITE=1 /usr/bin/python3.12 ...   # or: /usr/bin/python3.12 -s ...
```

I added a wrapper at **`/mnt/data/mini-sglang/run_python.sh`** so you don't have to remember it.

## Verification (all pass)

- torch 2.9.1+cu128, CUDA available, RTX 4070 detected
- sgl_kernel imports + **sampling kernel runs on GPU** ✓
- flashinfer **paged-KV prefill runs on GPU** ✓
- `./run_python.sh -m minisgl --help` → MiniSGL server CLI works ✓

⚠️ One caveat: every python invocation for this project must use `-s` / `PYTHONNOUSERSITE=1` (or `run_python.sh`), or sgl_kernel will break again. The user-site torch 2.11 env is left untouched.