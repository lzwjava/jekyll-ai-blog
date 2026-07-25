---
audio: false
generated: true
image: false
lang: en
layout: post
title: ROCm PyTorch GPU Test Summary
translated: false
type: note
---

Now I have the full picture. Here's the summary:

---

## ✅ PyTorch + ROCm — Test Results

| Test | Result |
| ------ | -------- |
| `torch.cuda.is_available()` | ✅ **True** |
| `torch.cuda.device_count()` | ✅ **1** (allocated to this Pod) |
| GPU tensor ops (matmul) | ✅ **Working** (6.25 result) |
| `torch.version.hip` | ✅ **7.2.53211** |
| GPU arch support | `gfx1100`, `gfx90a`, `gfx942`, `gfx950`, ... |
| 4096×4096 matmul benchmark | **24.8ms** per op (~5.5 TFLOPS) |
| vLLM | ✅ **0.16.1.dev0** (ROCm 7.2.1 build) |

### 🖥️ GPU Hardware

```
GPU: AMD Radeon Graphics (gfx1100 / RDNA3)
VRAM: 48 GiB (51,522,830,336 bytes)
PCI: 0000:23:00.0
Node ID: 3
Temp: 27°C (idle)
Power: 14W (idle), cap 241W
```

### 🔍 Why only 1 GPU?

The server has **8 physical GPUs** on the PCI bus, but **only 1 is assigned to this Pod** — the rest are allocated to other tenants:

```
PCI GPUs on bus:   03:00.0  23:00.0*  43:00.0  63:00.0  83:00.0  a3:00.0  c3:00.0  e3:00.0
DRM render nodes:  D128     D129*     D130     D131     D132     D133     D134     D135
/dev/dri access:   ❌      ✅        ❌       ❌       ❌       ❌       ❌       ❌
                              ↑ This one is ours
```

The platform uses **GPU partitioning** — each Pod gets exclusive access to 1 GPU through `/dev/kfd` + a dedicated render node. You get the full 48GiB VRAM to yourself.

### 🚀 Quick usage

```bash
source /opt/venv/bin/activate
python -c "import torch; print(torch.cuda.device_count(), torch.cuda.get_device_name(0))"
# → 1, AMD Radeon Graphics
```
