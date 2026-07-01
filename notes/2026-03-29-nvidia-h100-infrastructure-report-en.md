---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA H100 Machine Infrastructure Report
translated: false
type: note
---

## 🖥️ Machine Report: `162.243.29.96`

| Component | Details |
| ----------- | --------- |
| **OS** | Ubuntu 22.04.4 LTS (Jammy) |
| **Kernel** | 5.15.0-113-generic |
| **Location** | NYC2 (New York) |
| **Type** | KVM Virtual Machine |

### 🧠 CPU

| | |
| --- | --- |
| **Model** | Intel Xeon Platinum 8468 |
| **Cores** | 20 cores, 1 thread per core (no HT) |
| **Architecture** | x86_64, Sapphire Rapids |
| **Cache** | L1d: 640 KiB / L1i: 640 KiB / L2: 80 MiB |
| **ISA** | AVX-512 (full suite), AVX2, VNNI, BF16, FP16 |

### 🎮 GPU

| | |
| --- | --- |
| **Model** | **NVIDIA H100 80GB HBM3** |
| **VRAM** | 81,559 MiB (~80 GB) |
| **Driver** | 575.57.08 |
| **CUDA** | 12.9 |
| **Status** | Idle (0% util, 37°C, 73W / 700W TDP) |
| **MIG** | Disabled |

### 💾 Memory

| | |
| --- | --- |
| **RAM** | 235 GiB total (233 GiB available) |
| **Swap** | None |

### 💿 Disk

| | |
|---|---|
| **Root** | /dev/vda1 — 698 GB (20 GB used, 679 GB free, 3%) |

### 🌐 Network

| Interface | IP |
| --- | --- |
| eth0 (public) | 162.243.29.96/24 |
| eth0 (private) | 10.13.0.5/16 |
| eth1 | 10.100.0.2/20 |
| docker0 | 172.17.0.1/16 |

### Summary

**Beast machine.** H100 80GB + 235GB RAM + 20 Xeon cores + 700GB disk. Ideal for LLM inference — can run large models (70B+) easily. Want me to install Ollama here too?
