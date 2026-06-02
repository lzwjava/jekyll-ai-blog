---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD MI300X GPU Server Analysis and Test
translated: false
type: note
---

Here's the full comprehensive breakdown of everything on that server:

---

## Server Profile: 165.245.137.138

| Attribute | Value |
|---|---|
| Hostname | `7` (Ubuntu 24.04) |
| Kernel | `6.8.0-106-generic` |
| CPU arch | x86_64 |
| RAM | 235 GB total (230 GB free) |
| Disk | 697 GB (611 GB free) |
| SSH auth | Public key (passwordless) |

---

## GPU: AMD Instinct MI300X (Virtual Function)

| Attribute | Value |
|---|---|
| PCI device | `0000:83:00.0` |
| Device ID | `0x74b5` (MI300X VF) |
| GFX version | `gfx942` |
| HBM3 memory | 256 GB (BAR at `0x4000000000`) |
| PCIe link | 5.0 x16 @ 32 GT/s |
| NUMA node | 0 |
| Partition | 0 (full GPU) |
| ROCm | **7.2.0** installed at `/opt/rocm-7.2.0` |
| GPU firmware | loaded (amdgpu v6.16.13 in-kernel) |
| RAS | GFX+SDMA+UMC all ENABLED |
| Power state | D0 (active, was in low-power before first use) |

---

## ROCm Stack Health

| Component | Status |
|---|---|
| `amdgpu` kernel module | Loaded (in-kernel) |
| `rocm-smi` | Works — detects GPU correctly |
| `rocminfo` | At `/opt/rocm-7.2.0/bin/rocminfo` |
| `hipcc` | Available (`/opt/rocm-7.2.0/bin/hipcc`) |
| KFD topology | Nodes 0 and 1 present (GPU is enumerated) |
| KFD simd | GPU visible through KFD (not a blind VF) |

---

## llama.cpp Build Details

| Attribute | Value |
|---|---|
| Source | `https://github.com/ggerganov/llama.cpp.git` |
| Commit | `b39a7bf` (v0.12.0) |
| Build dir | `/root/llama.cpp/build/` |
| CMake flags | `-DGGML_HIP=ON -DAMDGPU_TARGETS=gfx942` |
| Backends | CPU + HIP/ROCm |
| HIP compiler | Clang 22.0.0 (ROCm) |
| Output binary | `/root/llama.cpp/build/bin/llama-cli` |
| Model downloaded | Qwen2.5-0.5B-Instruct Q4_K_M (469 MB) |

---

## Smoke Test Results

Ran Qwen2.5-0.5B with all layers offloaded to GPU (`-ngl 99`):

```
Prompt: "Hello, could you introduce yourself briefly?"

Response: Of course! I am Qwen, a large language model created by Alibaba Cloud...

Performance:
  Prompt processing:  748.7 tokens/second
  Text generation:    484.2 tokens/second
```

Both prompt ingestion and token generation ran on the MI300X via the HIP backend — confirmed fully functional.

---

## Quick Reference Commands (for future use)

```bash
# Rebuild (if needed)
cd /root/llama.cpp
export ROCM_PATH=/opt/rocm-7.2.0 && export HIP_PATH=$ROCM_PATH && export PATH=$ROCM_PATH/bin:$PATH
cmake -B build -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx942
cmake --build build -j$(nproc) --target llama-cli

# Run inference
./build/bin/llama-cli -m models/tiny-model.gguf -ngl 99 -p "Your prompt" -n 200
```

Everything is ready to go. You can run larger models on that 256 GB HBM3 — it'll handle pretty much any open-weight model you throw at it.
