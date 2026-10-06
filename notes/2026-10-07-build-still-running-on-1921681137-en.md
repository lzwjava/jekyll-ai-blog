---
audio: false
generated: true
image: false
lang: en
layout: post
title: Build Still Running on 192.168.1.137
translated: false
type: note
---

The build is **still running** on 192.168.1.137 (I used `.137` — same host as before; `.37` may have been a typo).

Status from `ps aux`:

- **Your original command is alive** — PID 9650 started at **16:01** (the `bash -c` wrapper)
- `cmake --build build -j 2` → `gmake` → running (PIDs 9651/9653/9656/9894)
- **Currently in the CUDA compilation phase** — two `nvcc` processes (PIDs 13014, 13032, started 16:09) are compiling `mmq-instance-iq3_s.cu` and `mmq-instance-iq3_xxs.cu`

This is the slowest part of a llama.cpp build — it loops through hundreds of CUDA template instances (mmq, fa, etc.) for both `compute_52` and sm_52. With `-j 2`, this CUDA stage can take a while.

If you want, I can keep monitoring (e.g., check the count of compiled `.o` files in `build/ggml/src/ggml-cuda` to gauge progress), or just re-check `ps` in a bit. Want me to check progress percentage?
