---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows 11 25H2 可启动 U 盘已创建
translated: true
type: note
---

## 摘要 — Windows 11 25H2 可启动 USB 已创建 ✅

### 问题

`Win11_25H2_English_x64_v2.iso` 是一个 **DVD 镜像**（ISO9660），而非原始磁盘镜像。Etcher 期望镜像中包含分区表（如 Ubuntu ISO 那样），因此会报错 *"missing partition table"*。即使绕过此问题，7.1 GB 的 `install.wim` 也超出了 FAT32 的 4 GB 文件大小限制——USB 将无法启动。

### 我们的操作

| # | 操作 | 命令/工具 |
| --- | --- | --- |
| 1 | **分析** ISO 和 USB | `diskutil list`、`hdiutil imageinfo`，确认 `install.wim` 为 7.1 GB |
| 2 | **格式化** 15.7 GB 的 USB 为 FAT32 + GPT | `diskutil eraseDisk MS-DOS WIN11 GPT /dev/disk13` |
| 3 | **复制** ISO 中除 `install.wim` 外的所有文件到 USB | `rsync -av --exclude='sources/install.wim'` |
| 4 | **拆分** 7.1 GB 的 `install.wim` 为 3 个 FAT32 安全块（`.swm` 文件） | `wimlib-imagex split ... 3800` |

### 最终 USB 驱动器 `/Volumes/WIN11`

- **文件系统：** FAT32 + GPT
- **大小：** 已用 7.9 GB / 总计 14 GB
- **结构：** `boot/`、`efi/`、`sources/`、`setup.exe`、`support/`
- **安装文件：** `install.swm`（3.2 GB）+ `install2.swm`（3.7 GB）+ `install3.swm`（79 MB）

这是 **微软官方兼容方法**，适用于 UEFI Windows 安装介质。USB 已安全弹出，可用于启动 **联想小新**。
