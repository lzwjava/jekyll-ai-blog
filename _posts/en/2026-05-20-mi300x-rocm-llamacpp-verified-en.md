---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X ROCm llama.cpp Verified
translated: false
type: note
---

All done. Here's the full summary:

---

**SSH'd to** `root@165.245.137.138` — Ubuntu 24.04, 235 GB RAM, 611 GB free disk

**GPU detected**: **AMD MI300X VF** (device `0x74b5`, gfx942)

- 256 GB HBM3, PCIe 5.0 x16 at 32 GT/s
- ROCm 7.2.0 installed, `rocm-smi` sees the GPU
- `amdgpu` kernel module loaded (version 6.16.13)

**llama.cpp setup**:

1. Cloned `https://github.com/ggerganov/llama.cpp.git` to `/root/llama.cpp/`
2. Installed `cmake` (was missing)
3. Built with `-DGGML_HIP=ON -DAMDGPU_TARGETS=gfx942` — **HIP backend detected and compiled**
4. Downloaded Qwen2.5-0.5B Q4_K_M (469 MB) to `/root/llama.cpp/models/`

**Smoke test result** — inference on MI300X via ROCm:

```
Of course! I am Qwen, a large language model created by Alibaba Cloud...

[ Prompt: 748.7 t/s  |  Generation: 484.2 t/s ]
```

**Confirmed**: HIP/ROCm backend works end-to-end. The MI300X is fully operational for inference with llama.cpp.
