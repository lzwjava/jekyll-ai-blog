---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Cloud GPU OOM Report
translated: false
type: note
---

Here's a comprehensive summary of everything:

---

## AMD Radeon Cloud Server — Complete Status

### Server Specs

| Component | Value |
| ----------- | ------- |
| **Host** | 36.150.116.206 |
| **SSH Port** | 31154 (currently down) |
| **OS** | Ubuntu 24.04.4 LTS |
| **CPU** | 2× AMD EPYC 9334 (128 threads) |
| **RAM** | 503 GiB |
| **GPU** | AMD Radeon Graphics (gfx1100 / RDNA 3) |
| **VRAM** | 48 GiB |
| **ROCm** | 7.2.1, Driver 6.16.13 |
| **PyTorch** | 2.9.1+git (ROCm 7.2 in `/opt/venv`) |
| **Disk** | `/` = 3.5TB overlay (2.8TB free), `/workspace` = 98GB loop (19GB free) |

### GPU Compute Test

✅ **Passed** — HIP vector add (1M elements) computed correctly, all 48GB VRAM accessible, 96 CUs, 1760 MHz clock.

### What We Did

1. **Diagnosed connectivity** — Found SSH port 31094 wrong; actual SSH ports are 31090, 31098, 31100 (default), 31154 (ours)
2. **Added your SSH key** to the server
3. **Downloaded FLUX.2-dev** (166GB, 39 files) to `/FLUX.2-dev` — **completed successfully** in 252s
4. **Attempted inference** — OOM crashed the instance. FLUX.2-dev is a **32B parameter model** — the transformer alone is 60GB, cannot fit in 48GB VRAM even with CPU offloading

### Current State

- **Instance: DOWN** — OOM killed the SSH daemon on port 31154
- **Model files**: 166GB of FLUX.2-dev safely saved at `/FLUX.2-dev` on the overlay filesystem
- **Jupyter Lab**: Running on port 8888 (token: `amd-oneclick`) but not accessible through cloud proxy
- **Other SSH ports** (31090, 31098, 31100): Still responding but our key isn't authorized

### Next Steps (after restart)

| Step | Action | Why |
| ------ | -------- | ----- |
| 1 | Restart instance from cloud console | Get SSH back on port 31154 |
| 2 | Remove FLUX.2-dev files | Free 166GB disk |
| 3 | Download **FLUX.1-dev** (~35GB) | 12B params, needs ~24GB VRAM at FP16 |
| 4 | Run with `enable_sequential_cpu_offload()` | Fits in 48GB VRAM ✅ |

**FLUX.1-dev** is the right choice for your 48GB GPU — it's a 12B parameter model that needs ~24GB VRAM for the transformer plus ~10GB for the T5 text encoder. With CPU offloading, it'll run comfortably.
