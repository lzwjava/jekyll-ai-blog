---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想小新 14 IAH8 系统概览
translated: true
type: note
---

以下是位于 `192.168.1.47` 的笔记本电脑详细报告：

---

## 🖥️ Lenovo XiaoXin 14 IAH8 — 系统概览

### 💻 Laptop
- **Model:** Lenovo XiaoXin 14 IAH8 (在某些市场也称为 IdeaPad Slim 5 14)
- **Chassis:** Laptop (14-inch)
- **Firmware:** LACN36WW (2024年6月)

---

### 🧠 CPU — Intel Core i5-12450H

| Spec | Value |
|------|-------|
| **Architecture** | Alder Lake-H (12th Gen, Intel 7 / 10nm) |
| **Total Cores** | 8 (4 P-cores + 4 E-cores) |
| **Total Threads** | 12 (P-cores 支持 Hyper-Threading) |
| **P-core Base / Turbo** | 2.0 GHz → **4.4 GHz** |
| **E-core Base / Turbo** | 1.5 GHz → 3.3 GHz |
| **L3 Cache** | 12 MB Smart Cache |
| **L2 Cache** | 7 MB |
| **TDP** | 45W base / 95W turbo |
| **Current Temp** | ~28-32°C (idle，非常凉爽) |
| **Current Freq** | 400-860 MHz (idle，节能模式) |

**性能说明：**
- Cinebench R23 Multi: ~10,043 pts
- Cinebench R23 Single: ~1,596 pts
- 多线程性能与旧款 Ryzen 7 5700U / i7-10750H 相当
- 优秀的中端移动端 CPU — 适合日常任务、Coding 以及中轻度工作负载
- 4 个 E-cores 高效处理后台任务，而 P-cores 则负责重度计算

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

仅配备 Integrated Graphics — 无独立 GPU。足以胜任桌面使用、视频回放和轻度 GPU 加速任务。并非游戏用途 GPU。

---

### 🧮 Memory (RAM)

| Spec | Value |
|------|-------|
| **Total** | 16 GB (16,093 MB) |
| **Used** | 4.0 GB |
| **Available** | 11 GB |
| **Swap** | 2 GB (未使用) |

可能为 DDR5 4800 MHz (该平台支持)。16 GB 对于多任务处理非常充裕。

---

### 💾 Storage — NVMe SSD

| Spec | Value |
|------|-------|
| **Device** | `/dev/nvme0n1p2` |
| **Total** | 468 GB |
| **Used** | 12 GB (3%) |
| **NVMe Temp** | ~27°C |

几乎为空 — 除了基础系统外几乎没有安装任何内容。

---

### 🐧 Operating System — Linux Mint 22.3 "Zena"

| Spec | Value |
|------|-------|
| **OS** | Linux Mint 22.3 (Zena) |
| **Base** | Ubuntu 24.04 (Noble) |
| **Kernel** | 6.14.0-37-generic |
| **Architecture** | x86_64 |
| **Desktop** | Cinnamon (运行在 X11/Xwayland) |

Linux Mint 是这款硬件的理想选择 — 轻量、稳定、新手友好，且在 Lenovo 笔记本上支持良好。6.14 Kernel 拥有成熟的 Alder Lake 支持，具备完善的 P-core/E-core 调度机制。

---

### 🔋 当前状态

| Metric | Value |
|------|-------|
| **Uptime** | 15h 41m |
| **Load Average** | 0.03 / 0.08 / 0.13 (基本处于 idle) |
| **CPU Usage** | ~21% scaling, 主要来自 Firefox |
| **Battery** | 0% (可能正使用 AC 电源，电池读数不可靠) |
| **CPU Temp** | 28-32°C (非常凉爽) |
| **NVMe Temp** | 27°C |

---

### 📊 总结

一款表现稳健的中端 Ultrabook。i5-12450H 配合 16 GB RAM 和 NVMe 存储使其成为响应迅速的日常主力机。Linux Mint 在其上运行非常完美。唯一的限制是缺乏独立 GPU — 如果你需要进行重度图形工作或游戏，这将是瓶颈。对于其他所有需求 — Coding、浏览网页、办公、多媒体 — 它都绰绰有余。
