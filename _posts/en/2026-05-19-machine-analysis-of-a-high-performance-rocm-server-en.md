---
audio: false
generated: true
image: false
lang: en
layout: post
title: Machine Analysis of a High-Performance ROCm Server
translated: false
type: note
---

Here's the complete machine analysis:

---

## Machine Analysis: `129.212.178.209`

### Overview

| Property | Value |
|---|---|
| Hostname | `7` |
| OS | Ubuntu 24.04.4 LTS (Noble Numbat) |
| Kernel | 6.8.0-106-generic (x86_64) |
| Uptime | ~54 minutes (fresh) |
| Virtualization | **KVM/QEMU** (pc-q35-6.1) |

---

### CPU — Intel Xeon Platinum 8568Y+ (virtualized)

| Property | Value |
|---|---|
| vCPUs | **20 cores**, 1 socket, 1 thread/core |
| ISA | x86_64, AVX-512 (full: VL, DQ, BW, BF16, VNNI, VBMI, FP16, etc.) |
| L1 cache | 640 KB (32 KB × 20 instances) |
| L2 cache | 80 MB total (4 MB × 20) |
| BogoMIPS | 4600.00 |
| Hypervisor | KVM, full virtualization with VT-x |

This is a cloud VM slice of a real Intel Xeon — you get 20 dedicated cores with heavy AVX-512 support, which matters for token embedding throughput and prefill in LLM serving.

---

### GPU — AMD Instinct **MI300X VF** (gfx942 / CDNA3)

| Property | Value |
|---|---|
| Model | AMD Instinct MI300X VF |
| Architecture | **gfx942** (CDNA3) |
| Compute Units | **304** (32 SE × ~9.5 CU/SE) |
| SIMDs | 1,216 (4 per CU) |
| Max Clock | **2,100 MHz** |
| **VRAM** | **191.7 GiB** (205,822,885,888 bytes) |
| VRAM Used | ~286 MB (essentially idle) |
| GTT Memory | ~118 GiB available |
| L2 Cache | 4 MB |
| L3 Cache | **256 MB** |
| PCIe | **Gen5 x16 @ 32 GT/s** |
| Compute Partition | SPX (single GPU) |
| Memory Partition | NPS1 (single partition, not NUMA-split) |
| Temperature | 43°C junction / 38°C memory |
| Power Draw | **157W idle** |
| GPU Utilization | **0%** (completely idle) |
| State | **Low-power mode** (auto-sleeping) |

This is the top-tier AMD datacenter GPU — 192 GB HBM3, ideal for large model inference (Llama-405B, DeepSeek-V3 at FP8). The low-power state just means no workload is running; it'll ramp up to full clocks when loaded.

---

### ROCm Software Stack

| Component | Version |
|---|---|
| **ROCm** | **7.2.0** (70200-43) |
| Driver | 6.16.13 |
| HIP SDK | 7.2.26015 (AMD clang 22.0.0) |
| rocm-smi-lib | 7.8.0 |
| ROCm LLVM | 22.0.0 |
| ROCgdb | 16.3 |
| MIOpen | ✓ installed |
| MIGraphX | ✓ installed |
| RCCL (NCCL equivalent) | ✓ installed |
| OpenCL | ✓ 2.0 |
| OpenMP | ✓ installed |

Full ROCm toolchain is installed — HIP compiler, debugger, ML libraries (MIOpen, MIGraphX, RCCL). You can compile HIP/C++ kernels or run PyTorch with ROCm backend.

**Missing**: No PyTorch or any Python ML packages installed (only PyYAML). You'll need to install `torch` with ROCm support.

---

### Memory & Storage

| Resource | Total | Used | Free |
|---|---|---|---|
| System RAM | **235 GiB** | 5.7 GiB | 229 GiB |
| Swap | 0 (none configured) | — | — |
| OS Disk (vda1) | 719 GB | 87 GB | **610 GB free** |
| **Data Disk (vdc1)** | **5 TB** | — | **unmounted** |

Key observation: the **5TB data disk is formatted (ext4) but not mounted**. You'll want to mount it — great for model weights, datasets, or Docker volumes.

---

### Docker

| Property | Value |
|---|---|
| Docker | 29.3.0 + Compose v5.1.0 |
| Running container | `rocm` — port **8888** (likely Jupyter) |
| GPU access | ✓ confirmed (/dev/kfd, /dev/dri accessible) |

---

### Network

| Interface | IP | Purpose |
|---|---|---|
| eth0 | 129.212.178.209/20 | Public / AMD DevCloud |
| eth1 | 10.128.0.2/20 | Private/internal |
| docker0 | 172.17.0.1/16 | Docker bridge |

---

### Overall Assessment

This is an **AMD DevCloud ATL1 instance** — a cloud-allocated MI300X node for development. It's freshly booted, completely idle, with a massive 192 GB GPU ready for large-model work.

**Immediate recommendations:**

1. **Mount the 5TB disk** — `mount /dev/vdc1 /data` or similar, then add to fstab
2. **Install PyTorch for ROCm** — `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm7.2`
3. **Wake the GPU** — the low-power state is normal; it auto-wakes on workload
4. Consider switching memory partition to **NPS4** if you need NUMA-aware multi-process access (currently NPS1, which treats the GPU as one monolithic memory pool — fine for single-process inference)

Want me to mount the 5TB disk and install PyTorch?
