---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA GPU and GGUF support added
translated: false
type: note
---

Done. All changes on `lzw@192.168.1.137:~/mini-llama.cpp` are committed and pushed:

- **`.gitignore`**: added `mini-llama-gpu` (the compiled ELF binary that was previously untracked)
- **`Makefile`**: nvcc target for the GPU build
- **`src/gguf.c`, `src/gguf.h`**: GGUF file parsing
- **`src/gpu_mm.cu`**: GPU matrix multiplication via cuBLAS

Commit `a835b6c` — `feat: add CUDA GPU attention with gguf loader` pushed to `origin/main` on GitHub (5 files, +315/-6).

One note: the branch's upstream tracking is gone (`based on 'origin/main', but the upstream is gone`). Since the push was to a newly-created remote `main` branch, you may want to re-link locally:

```bash
git branch --set-upstream-to=origin/main main
```
