---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kernel 7.2.0-rc1 Build Complete
translated: false
type: note
---

Here's the comprehensive build summary:

---

## Kernel Build Complete — Linux 7.2.0-rc1

### Version
```
7.2.0-rc1-00044-g87320be9f0d2
"Baby Opossum Posse" — #1 SMP PREEMPT_DYNAMIC Fri Jul  3 04:37:26 HKT 2026
```

### Build Environment

| Item | Detail |
|------|--------|
| **Host** | Fedora 44 (Workstation) |
| **CPU** | Intel Core i5-7360U @ 2.30GHz, 4 cores |
| **RAM** | 15 GB total, 8.8 GB available |
| **Compiler** | GCC 16.1.1 20260515 (Red Hat 16.1.1-2) |
| **Arch** | x86_64 |

### Build Configuration

| Option | Setting |
|--------|---------|
| **Base config** | `x86_64_defconfig` (5,473 lines) |
| **Built-in options** | 1,632 (`=y`) |
| **Loadable modules** | 15 (`=m`) |
| **Preemption** | `PREEMPT_DYNAMIC` (lazy preemption) |
| **Timer frequency** | 1000 Hz |
| **SMP** | Yes, up to 64 CPUs |
| **Debug info** | Disabled (`DEBUG_INFO_NONE=y`) — kept build fast |

### Produced Artifacts

| Artifact | Size | Description |
|----------|------|-------------|
| **`arch/x86/boot/bzImage`** | **15 MB** | Bootable compressed kernel image |
| **`vmlinux`** | **53 MB** | Uncompressed ELF binary (debug symbols stripped) |
| **`System.map`** | **8.9 MB** | Kernel symbol table (address → symbol mapping) |
| **Kernel modules** | 12 `.ko` files | ip_tunnel, sit, efivarfs, nf_log_syslog, x86_pkg_temp_thermal, nf_reject_ipv4/6, tunnel4, xt_addrtype, xt_MASQUERADE, xt_LOG, xt_mark |

### Key Features Enabled
- **Architecture**: x86_64 (64-bit), EFI boot (legacy + mixed mode + handover), ACPI, PCI Express
- **Storage**: ext4, SCSI, ATA (PIIX), USB storage, NVMe (via `BLK_DEV_NVME`)
- **Graphics**: Intel i915 DRM (full display pipeline — HDMI, DP, LVDS, DSI, eDP, TV-out), VirtIO-GPU
- **Networking**: IPv4, IPv6, bridging, netfilter, wireless (mac80211), Ethernet (e1000e), USB net
- **Input**: USB HID, PS/2, evdev, touchscreen, joystick
- **Audio**: ALSA/OSS sound subsystem
- **Virtualization**: VirtIO (block, SCSI, GPU, input, balloon)
- **Filesystems**: ext4, NFS client, Btrfs, XFS, CIFS/SMB
- **Security**: SELinux, module signing infrastructure
- **Firmware**: EFI runtime services, ACPI 5+ features

### Total Disk Usage
Source tree + build artifacts: **3.0 GB**