---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD MI300X Server GPU Details
translated: false
type: note
---

Done. Here's the summary:

---

**Server**: `ssh root@134.199.199.108`

**GPU**: AMD Instinct MI300X (Aqua Vanjaram) — Virtual Function passthrough

| Item | Detail |
|------|--------|
| GPU | AMD Instinct MI300X VF (0x74b5) |
| PCIe | Gen 5.0 x16 (32 GT/s) |
| Memory | 256 GB HBM3 |
| Driver | in-kernel amdgpu |
| Host | ubuntu-gpu-mi300x1-192gb-devcloud-atl1 |

**Command to check GPU** (nvidia-smi equivalent):
```
amd-smi
```

I installed it at `/usr/local/bin/amd-smi` on the server. It reads sysfs/lspci directly since the GPU is an SR-IOV virtual function and the KFD (compute) interface isn't exposed — `rocm-smi` shows "No AMD GPUs specified" for the same reason. 

For full compute access (HIP, ROCm libraries, etc.), you'll need:
```
apt install rocm-hip-sdk
```

But that's a big install — let me know if you want to go that route.