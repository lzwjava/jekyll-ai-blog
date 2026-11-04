---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD 16GB GPU Not Utilized
translated: false
type: note
---

## GPU / VRAM

**No NVIDIA GPU** — `nvidia-smi` fails ("couldn't communicate with the driver"), so CUDA is not usable here.

**AMD GPU via ROCm** (the one you asked about):

| Item | Value |
|---|---|
| Device | `0000:03:00.0`, DID `0x6861` (Vega 10 / Radeon Instinct MI25 class), subsystem `0x0c1e` |
| ROCm name | **AMD Radeon Pro WX 9100** (gfx900, Vega 10) |
| **VRAM total** | **17,163,091,968 B = 15.98 GiB (16 GB HBM2)** |
| VRAM used | 8,318,976 B ≈ **7.9 MiB** (essentially idle) |
| GTT/visible heap | 16,760,832 KB reported by rocminfo |
| VBIOS | 113-D0510100-110 |
| Power cap | 170 W (current draw 6 W) |
| Temp | 41 °C edge / 42 °C junction/mem |
| Max SCLK | 1500 MHz (currently 852 MHz, 0% busy) |

Other GPUs present: Intel HD 530 iGPU (`0x8086:0x1912`, `card1`) — no VRAM, shared system RAM.

System: i5-6500, **11 GiB RAM** total (4.0 GiB used, ~7.1 GiB available), 4 GiB swap.

### Relevant to this repo
Your `build/CMakeCache.txt` has:
```
GGML_HIP=OFF
SD_HIPBLAS=OFF
SD_CUDA=OFF
```
So the current build is **CPU-only** and will not use the 16 GB AMD card. To use it you'd need a HIP build targeting `gfx900`, e.g. `-DGGML_HIP=ON -DSD_HIPBLAS=ON -DAMDGPU_TARGETS=gfx900` (note: gfx900 has no matrix cores, so it's roughly Vega-class throughput — and 11 GB system RAM is the tighter constraint for model loading).