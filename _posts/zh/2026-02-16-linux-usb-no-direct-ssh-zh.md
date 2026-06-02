---
audio: false
generated: true
image: false
lang: zh
layout: post
title: USB 上的 Linux 无法作为直接 SSH 目标
translated: true
type: note
---

**Question:** 我可以在 USB 磁盘上安装 Linux 系统，然后从 macOS 访问它（例如通过类似 `ssh /dev/disk10` 的方式），在运行 Mac 硬件的同时使用 Linux 系统文件吗？

**Answer:**

不，你无法直接从 macOS 按照你描述的方式（如 `ssh /dev/disk10`）“SSH”进入 USB 驱动器上的 Linux 安装，从而在保持运行 macOS 的同时，利用 Mac 硬件运行完整的 Linux 环境。

以下是该方法不可行的原因以及你的实际方案建议：

### 为什么提议的方法行不通

- macOS 无法原生地 **chroot** 或完全切换到 Linux root filesystem，因为 macOS（基于 Darwin/BSD kernel）和 Linux 拥有完全不同的 kernel、system calls、libraries（glibc 对比 libSystem）、设备处理方式和二进制格式（ELF 对比 Mach-O）。
- 在 macOS 上挂载 Linux 分区（如 ext4）是可以通过第三方工具如 ext4fuse 或 Paragon 实现的，但这仅允许你读写文件 —— 它**不能**让你运行 Linux binaries 或启动 Linux 环境。
- 并没有类似于 `ssh /dev/disk10` 这种进入 Linux OS 的简单命令。SSH 需要一个正在运行的 Linux 系统，且其 SSH server (sshd) 必须已经处于激活状态，而当 USB 只是插在电脑上且 macOS 正在运行时，情况并非如此。

### 最接近的实际替代方案

1. **从 USB 引导进入 Linux（如果你想在 Mac 硬件上运行完整 Linux，推荐此方案）**
   - 在 USB 驱动器上安装完整的 Linux 系统（不仅是 live 环境）。许多 Linux distros（Ubuntu, Fedora, Debian, Arch 等）都支持像安装到内置硬盘一样安装到 USB。
   - 在 Intel Macs 上：重启，按住 **Option (Alt)** 键 → 选择 USB（通常显示为 "EFI Boot"）。
   - 在 Apple Silicon (M1/M2/M3/M4) 上：Linux 支持有限，通常需要 virtualization（如 UTM, Parallels）或特殊项目如 Asahi Linux —— 目前尚不支持广泛的直接 USB 引导。
   - 这可以让你利用 Mac 全部的 CPU/GPU/RAM 获得原生 Linux 性能。
   - 你可以使其 persistent（更改会被保存）。
   - 缺点：运行 Linux 时你必须完全离开 macOS。

2. **在 macOS 的 virtual machine 中运行 Linux（间接使用 Mac 硬件）**
   - 使用免费工具如 **UTM**、**VirtualBox**，或付费工具如 **Parallels Desktop** 或 **VMware Fusion**。
   - 创建一个从 USB Linux 安装引导的 VM（某些工具允许对 /dev/diskX 进行直接物理磁盘访问）。
   - 或者直接在 VM 内部正常安装 Linux。
   - 优点：留在 macOS 中，方便的文件共享，剪贴板集成，可以与 macOS 应用并排运行 Linux 应用。
   - 性能：配合硬件加速表现良好（尤其是 Apple Silicon 上的 Parallels/UTM），但达不到 100% 的 bare-metal 速度。

3. **高级 / 实验性混合方法（不简单）**
   - 挂载 Linux 分区 → 使用兼容层提取并运行单个 Linux binaries（例如用于在 Linux 上运行 macOS 应用的 Darling —— 但反向的兼容层并不完善）。
   - 在 macOS 上使用 Linux namespaces/containers —— 并不实用。
   - 这些方法通常带来的麻烦远多于收益。

### 总结

如果你的目标是**获得具有 Mac 硬件速度的完整 Linux 体验** → 直接从 USB 引导启动（最适合 Intel Macs）。

如果你想**留在 macOS 中**且仍能使用 Linux → 运行一个 VM（最简单且最实用）。

“从 macOS SSH 进入 USB Linux”的想法遗憾地在简洁性/可行性上并不可行。

**References:**

- <https://askubuntu.com/questions/826943/booting-ubuntu-on-mac-from-usb>
- <https://www.jeffgeerling.com/blog/2024/mounting-ext4-linux-usb-drive-on-macos-2024>
- <https://www.kali.org/docs/usb/live-usb-install-with-mac>
