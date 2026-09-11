---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 用dd将ISO写入U盘
translated: true
type: note
---

你的U盘显示为 **`/dev/disk12`**（外部、物理、15.7 GB）。以下是macOS上的操作步骤：

**1. 首先卸载磁盘**（不要弹出，仅卸载）：

```bash
diskutil unmountDisk /dev/disk12
```

**2. 使用 `dd` 写入ISO镜像**（使用 `rdisk` 可大幅提升原始写入速度）：

```bash
sudo dd if=/Users/lzwjava/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=4M status=progress
```

如果你的 `dd` 不支持 `status=progress`，请使用：

```bash
sudo dd if=/Users/lzwjava/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=4m
```

写入过程中没有可见输出——它可能会看起来卡住几分钟。你可以在终端中按 `Ctrl+T` 显示进度。

**3. 完成后弹出：**

```bash
diskutil eject /dev/disk12
```

⚠️ **警告：** 此操作将完全擦除 `/dev/disk12` 上的所有数据。仔细检查目标设备——如果插拔了其他驱动器，请再次运行 `diskutil list` 以确认U盘的标识符，然后再执行 `dd` 命令。