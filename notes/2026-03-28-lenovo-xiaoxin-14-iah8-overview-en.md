---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lenovo XiaoXin 14 IAH8 System Overview
translated: false
type: note
---

Here's the full rundown of the laptop at `192.168.1.47`:

---

## 🖥️ Lenovo XiaoXin 14 IAH8 — System Overview

### 💻 Laptop
- **Model:** Lenovo XiaoXin 14 IAH8 (also known as IdeaPad Slim 5 14 in some markets)
- **Chassis:** Laptop (14-inch)
- **Firmware:** LACN36WW (June 2024)

---

### 🧠 CPU — Intel Core i5-12450H

| Spec | Value |
|------|-------|
| **Architecture** | Alder Lake-H (12th Gen, Intel 7 / 10nm) |
| **Total Cores** | 8 (4 P-cores + 4 E-cores) |
| **Total Threads** | 12 (P-cores have Hyper-Threading) |
| **P-core Base / Turbo** | 2.0 GHz → **4.4 GHz** |
| **E-core Base / Turbo** | 1.5 GHz → 3.3 GHz |
| **L3 Cache** | 12 MB Smart Cache |
| **L2 Cache** | 7 MB |
| **TDP** | 45W base / 95W turbo |
| **Current Temp** | ~28-32°C (idle, very cool) |
| **Current Freq** | 400-860 MHz (idle, power saving) |

**Performance context:**
- Cinebench R23 Multi: ~10,043 pts
- Cinebench R23 Single: ~1,596 pts
- Comparable to older Ryzen 7 5700U / i7-10750H in multi-thread
- Solid mid-range mobile CPU — great for daily tasks, coding, light-medium workloads
- The 4 E-cores handle background tasks efficiently while P-cores do the heavy lifting

---

### 🎮 GPU — Intel UHD Graphics (Alder Lake-P GT1)

| Spec | Value |
|------|-------|
| **Chip** | Intel UHD Graphics (48 EUs, Xe architecture) |
| **Max Frequency** | 1.2 GHz |
| **Driver** | i915 (kernel) + Mesa 25.2.8 |
| **Renderer** | Mesa Intel Graphics (ADL GT2) |
| **Display** | 1920×1200 via X.org + Xwayland |
| **Vulkan** | 1.3.275 |

This is integrated graphics only — no discrete GPU. Fine for desktop use, video playback, and light GPU-accelerated tasks. Not a gaming GPU.

---

### 🧮 Memory (RAM)

| Spec | Value |
|------|-------|
| **Total** | 16 GB (16,093 MB) |
| **Used** | 4.0 GB |
| **Available** | 11 GB |
| **Swap** | 2 GB (unused) |

Likely DDR5 4800 MHz (supported by this platform). 16 GB is comfortable for multitasking.

---

### 💾 Storage — NVMe SSD

| Spec | Value |
|------|-------|
| **Device** | `/dev/nvme0n1p2` |
| **Total** | 468 GB |
| **Used** | 12 GB (3%) |
| **NVMe Temp** | ~27°C |

Nearly empty — barely anything installed beyond the base system.

---

### 🐧 Operating System — Linux Mint 22.3 "Zena"

| Spec | Value |
|------|-------|
| **OS** | Linux Mint 22.3 (Zena) |
| **Base** | Ubuntu 24.04 (Noble) |
| **Kernel** | 6.14.0-37-generic |
| **Architecture** | x86_64 |
| **Desktop** | Cinnamon (running in X11/Xwayland) |

Linux Mint is a great choice for this hardware — lightweight, stable, beginner-friendly, and well-supported on Lenovo laptops. The 6.14 kernel has solid Alder Lake support with proper P-core/E-core scheduling.

---

### 🔋 Current Status

| Metric | Value |
|------|-------|
| **Uptime** | 15h 41m |
| **Load Average** | 0.03 / 0.08 / 0.13 (essentially idle) |
| **CPU Usage** | ~21% scaling, mostly Firefox |
| **Battery** | 0% (likely on AC power, battery reading unreliable) |
| **CPU Temp** | 28-32°C (very cool) |
| **NVMe Temp** | 27°C |

---

### 📊 Verdict

A solid mid-range ultrabook. The i5-12450H with 16 GB RAM and NVMe storage makes for a snappy daily driver. Linux Mint runs beautifully on it. The only real limitation is the lack of a discrete GPU — if you need heavy graphics work or gaming, that's the bottleneck. For everything else — coding, browsing, office work, media — it's more than enough.