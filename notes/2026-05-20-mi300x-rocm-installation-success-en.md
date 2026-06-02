---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X ROCm Installation Success
translated: false
type: note
---

Everything works now. Here's the final result:

---

## ROCm Stack — Fully Operational

**`rocm-smi`** (AMD's nvidia-smi):
```
GPU  Temp    Power   SCLK    MCLK   PwrCap   VRAM%  GPU%
0    37.0°C  154.0W  139MHz  900MHz 750.0W   0%     0%
```

**`rocminfo`** — full GPU specs:
```
AMD Instinct MI300X VF (gfx942)
  304 Compute Units | 1216 SIMDs | 32 Shader Engines
  191 GB HBM3 | 2100 MHz max clock
  Wavefront: 64 | Workgroup: 1024
```

**HIP compute test:**
```
HIP devices: 1
Device 0: AMD Instinct MI300X VF
  Memory: 191 GB
  Compute units: 304
  Clock: 2100 MHz
```

---

## What was broken & how it was fixed

| Step | Problem | Fix |
|------|---------|-----|
| 1 | `rocm-smi` not installed | `apt install rocm-smi` from AMD repo |
| 2 | `rocm-smi` shows "No AMD GPUs" | MI300X was missing firmware |
| 3 | Versioned vs non-versioned package conflicts | Force-purged, installed versioned `*7.2.3` packages |
| 4 | `libxml2.so.2` missing (Ubuntu 25.10 has `.so.16`) | Symlink: `libxml2.so.2 → libxml2.so.16` |
| 5 | Firmware files missing (psp/gc/sdma/vcn) | `apt install linux-firmware` + GPU rebind |
| 6 | GPU driver init failed → HIP saw 0 devices | After firmware + rebind: GPU initialized, HIP sees 1 device |

## Commands available now

```
rocm-smi              # GPU status (temp, power, clocks, utilization)
rocminfo              # Full hardware topology
amd-smi               # Your original PCI-level info tool (still works)
hipcc                 # HIP C++ compiler
rocm_agent_enumerator # List GPU architectures
```

The environment is set permanently via `/etc/profile.d/rocm.sh` (PATH, ROCM_PATH, LD_LIBRARY_PATH).
