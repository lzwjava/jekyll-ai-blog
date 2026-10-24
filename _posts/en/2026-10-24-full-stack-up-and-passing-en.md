---
audio: false
generated: true
image: false
lang: en
layout: post
title: Full Stack Up and Passing
translated: false
type: note
---

Everything works — **full stack up and passing on 192.168.1.34**. Here's the summary:

## ✅ mini-llama.cpp is cloned, built, and RUNNING

**Setup on the box:**
| Step | Status |
|---|---|
| `git clone git@github.com:lzwjava/mini-llama.cpp` → `~/projects/` | ✓ |
| `nvidia-cuda-toolkit` **12.4.131** installed (apt) — nvcc + libcublas ✓ | ✓ — one hard freeze/reboot mid-install, fixed via `dpkg --configure -a` + reinstall |
| Model `qwen2.5-0.5b-instruct-q4_k_m.gguf` (468 MB) → `/mnt/models/` (HF via local clash proxy) | ✓ |
| `make` → all 3 targets built | ✓ |

**Runs:**
- `./mini-llama <model>` → `mini-llama.cpp skeleton -- build OK` ✓
- `./mini-llama-gpu <model>` (M1) → **MILESTONE-1-OK**: GGUF parsed, F32 tensor → M40 exact (err=0), cuBLAS GEMM **32.2 GFLOPS** (rel err 2.4e-7) ✓
- `./mini-llama-m2 <model>` (M2) → **MILESTONE-2-OK**: dequant census matches (Q5_0=133, Q8_0=13, Q4_K=12, Q6_K=12, F32=121), 0.630B params → 2.52 GB fp32, real `ffn_up` GEMM on GPU (err 5.6e-6 PASS), VRAM: 573 MB used / 11307 MB free ✓

**Notes:**
- ⚠️ The GPU is now stable (M1+M2 ran clean, no freeze) — but watch it: it hard-froze once during the CUDA install, same card that had D-state lockups before the reboot.
- ℹ️ This M40 reports **12 GB** VRAM (11520 MiB), while the README (written for machine .137) assumes 24 GB — everything fits fine, just so you know for M3+ VRAM budgeting.
- 🚧 Next up per your roadmap: **M3** (RMSNorm/RoPE/attention/KV-cache/SiLU forward pass), **M4** (sampling + CLI), **M5** (speed tuning). Once the forward pass exists, `./mini-llama-m3 <model>` will give you actual tokens out of this box.

Want me to start on M3, or leave it here?
