---
audio: false
generated: true
image: false
lang: en
layout: post
title: Troubleshooting Qwen 3.5 Server Setup
translated: false
type: note
---

Got it, you want the comprehensive review of the whole process. Here goes:

---

## 🦞 Full Review: Getting Qwen 3.5 9B Running on This Server

### The Goal
Download and run `aravhawk/qwen3.5-opus-4.6:9b` locally on this server (RTX 4070, 62GB RAM).

### What Happened

**1. Model Download (~90 min)**
- Pulled via Ollama: 5.6 GB main layer + 921 MB secondary layer
- Speed was all over the place: started at 3.5 MB/s, crawled to 90 KB/s at times
- Model file is GGUF Q4_K-M quantized, 5.23 GB, architecture `qwen35` (hybrid SSM+Attention)

**2. Ollama Couldn't Load It**
- Server has Ollama v0.18.2 — too old for the `qwen35` architecture
- Error: `unknown model architecture: 'qwen35'`
- Needed v0.20.2+
- Tried updating Ollama — GitHub downloads from this server were ~30 KB/s. Every attempt failed or timed out
- Install script (`curl | sh`) got truncated at 0.6% and killed

**3. Pivoted to llama.cpp**
- Found existing llama.cpp build at `~/projects/llama.cpp` but it was from October 2025 — also didn't support `qwen35`
- Git fetch was also painfully slow without proxy
- **Key breakthrough:** Mihomo proxy on port 7890 — set `http.proxy`/`https.proxy` for git, and fetches flew
- `git fetch origin master` via proxy, `git reset --hard origin/master`
- New code has `qwen35` support (added line 42 in `llama-arch.cpp`)
- Rebuilt llama-server from source with CUDA support (`cmake .. -DGGML_CUDA=ON`)
- Build completed successfully

**4. First Launch — CPU Only**
- CUDA driver (535) too old for CUDA 13.2 toolkit: `CUDA driver version is insufficient for CUDA runtime version`
- Fell back to CPU: 32 threads, ~10 tok/s
- Model loaded fine, responded correctly via OpenAI-compatible API at `http://127.0.0.1:11435`

**5. Driver Upgrade (nvidia-driver-535 → 570)**
- Old driver: 535.288.01 (supports up to CUDA 12.2)
- New driver: 570.211.01 (supports CUDA 13.2)
- DKMS kernel modules built for both 6.8.0-106 and 6.8.0-107 kernels
- **Reboot required** to load new kernel modules

### Current State

| Component | Status |
|-----------|--------|
| Model file | ✅ Downloaded (5.23 GB GGUF) |
| llama.cpp | ✅ Updated & rebuilt (latest master) |
| llama-server | ⏸️ Killed before driver upgrade |
| NVIDIA driver | ✅ Installed 570.211.01 (needs reboot) |
| GPU offloading | 🔜 After reboot |

### After Reboot
Start the server with:
```bash
LD_LIBRARY_PATH=~/projects/llama.cpp/build/bin \
  ~/projects/llama.cpp/build/bin/llama-server \
  -m /usr/share/ollama/.ollama/models/blobs/sha256-d0ecd80b0e45b0d9e49c8cd1527b7f7d52d8d3bde2c569ab36aac59bb78f53f7 \
  -ngl 99 -c 8192 --host 0.0.0.0 --port 11435
```

Expected: ~60-100+ tok/s with all 32 layers on the RTX 4070.

### Lessons Learned
- **GitHub from this server is unusable without proxy** — ~30 KB/s raw, instant with mihomo on 7890
- **Ollama's versioning is a pain** — each new model architecture needs a specific Ollama version
- **llama.cpp is more resilient** — just rebuild from source and it works
- **CUDA driver/toolkit version mismatch** is a classic gotcha — always check `nvidia-smi` CUDA version vs `nvcc --version`

---

Now reboot and let's see it fly 🦞
