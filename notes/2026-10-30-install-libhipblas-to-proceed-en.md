---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install libhipblas to proceed
translated: false
type: note
---

The model is downloading (~4.36 GB, ETA ~10 min).

 Now the build blocker: llama.cpp's HIP backend requires libhipblas-dev, which isn't installed, and sudo here needs a password. I can't type it.

 Please either run this yourself:

 ```bash
   sudo apt-get install -y libhipblas-dev
 ```

 …or paste your sudo password and I'll continue (install → build with -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx900 → run inference).

 Everything else is ready:
 - ✅ ~/projects/llama.cpp cloned (eb4e244)
 - ✅ cmake 4.4.4 installed via uv
 - ✅ ROCm/HIP 7.1 detected at /usr, GPU gfx900 (WX 9100, 16 GB VRAM)
 - ⏳ Model downloading → ~/projects/llama.cpp/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf

 Once you unblock the package, I'll finish the build and run a test inference.