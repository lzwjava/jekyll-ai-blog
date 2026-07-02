---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 内核 7.2.0-rc1 构建完成
translated: true
type: note
---

以下是完整的构建摘要：

---

## 内核构建完成 — Linux 7.2.0-rc1

### 版本信息
```
7.2.0-rc1-00044-g87320be9f0d2
"Baby Opossum Posse" — #1 SMP PREEMPT_DYNAMIC Fri Jul  3 04:37:26 HKT 2026
```

### 构建环境

| 项目 | 详情 |
|------|------|
| **主机** | Fedora 44 (Workstation) |
| **CPU** | Intel Core i5-7360U @ 2.30GHz, 4 核 |
| **内存** | 总计 15 GB，可用 8.8 GB |
| **编译器** | GCC 16.1.1 20260515 (Red Hat 16.1.1-2) |
| **架构** | x86_64 |

### 构建配置

| 选项 | 设置 |
|--------|---------|
| **基础配置** | `x86_64_defconfig` (5,473 行) |
| **内置选项** | 1,632 (`=y`) |
| **可加载模块** | 15 (`=m`) |
| **抢占模式** | `PREEMPT_DYNAMIC` (惰性抢占) |
| **定时器频率** | 1000 Hz |
| **SMP** | 是，最多支持 64 个 CPU |
| **调试信息** | 已禁用 (`DEBUG_INFO_NONE=y`) — 保持构建快速 |

### 生成产物

| 产物 | 大小 | 描述 |
|----------|------|-------------|
| **`arch/x86/boot/bzImage`** | **15 MB** | 可引导的压缩内核镜像 |
| **`vmlinux`** | **53 MB** | 未压缩的 ELF 二进制文件（已剥离调试符号） |
| **`System.map`** | **8.9 MB** | 内核符号表（地址 → 符号映射） |
| **内核模块** | 12 个 `.ko` 文件 | ip_tunnel, sit, efivarfs, nf_log_syslog, x86_pkg_temp_thermal, nf_reject_ipv4/6, tunnel4, xt_addrtype, xt_MASQUERADE, xt_LOG, xt_mark |

### 启用的主要特性
- **架构**: x86_64 (64-bit), EFI 启动 (传统模式 + 混合模式 + handover), ACPI, PCI Express
- **存储**: ext4, SCSI, ATA (PIIX), USB 存储, NVMe (通过 `BLK_DEV_NVME`)
- **图形**: Intel i915 DRM (完整显示管线 — HDMI, DP, LVDS, DSI, eDP, TV-out), VirtIO-GPU
- **网络**: IPv4, IPv6, 桥接, netfilter, 无线 (mac80211), 以太网 (e1000e), USB 网络
- **输入**: USB HID, PS/2, evdev, 触摸屏, 游戏杆
- **音频**: ALSA/OSS 音频子系统
- **虚拟化**: VirtIO (块设备, SCSI, GPU, 输入, balloon)
- **文件系统**: ext4, NFS 客户端, Btrfs, XFS, CIFS/SMB
- **安全**: SELinux, 模块签名基础设施
- **固件**: EFI 运行时服务, ACPI 5+ 特性

### 总磁盘使用量
源码树 + 构建产物: **3.0 GB**