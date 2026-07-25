---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD ROCm PyTorch Diagnostic Report
translated: false
type: note
---

Here's the full diagnostic report:

---

## ✅ PyTorch + ROCm Status

| Component | Status |
|-----------|--------|
| **PyTorch** (system venv) | ✅ **2.9.1+rocm** installed at `/opt/venv` |
| **torchaudio** | ✅ 2.9.0 |
| **torchvision** | ✅ 0.24.1 |
| **vLLM** | ✅ 0.16.1.dev0 (ROCm 7.2.1 build) |
| **APEX** | ✅ 1.9.0+rocm7.2.1 |
| **amdsmi** | ✅ 26.2.2 |
| **amd-aiter** | ✅ 0.1.7 |

### 🖥️ GPU Hardware — **8× AMD Radeon (gfx1100 / RDNA3)**

```
Device ID:  1002:744b → gfx1100 (AMD Radeon RX 7000 series)
VRAM each:  48 GiB (51,522,830,336 bytes)
Total VRAM: ~384 GiB
```

Full GPU list from `lspci`:
```
03:00.0, 23:00.0, 43:00.0, 63:00.0
83:00.0, a3:00.0, c3:00.0, e3:00.0
```

Plus one ASPEED BMC for display (`1a03:2000`).

### 🧠 ROCm Stack

| Component | Version |
|-----------|---------|
| ROCm | **7.2.1** (`/opt/rocm → /opt/rocm-7.2.1`) |
| hipconfig | 7.2.53211 |
| Kernel driver | ROCk module 6.16.13 loaded |
| HSA Runtime | 1.18 |

### ⚙️ System Specs

- **CPU:** AMD EPYC 9334 (2× 32-core = 128 threads)
- **RAM:** 503 GiB
- **Swap:** none

### 📍 How to use PyTorch with ROCm

The PyTorch is in the system venv — activate it:

```bash
source /opt/venv/bin/activate
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.device_count())"
# → True, 8
```

If your current shell can't `import torch`, you're likely running outside the venv. Just `source /opt/venv/bin/activate` first.
