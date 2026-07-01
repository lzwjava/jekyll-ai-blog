---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVMe 分区与磁盘工具
translated: true
type: note
---

问题：`lsblk` 是什么？在安装 Fedora 时如何分区？有哪些磁盘工具？为什么 NVMe 驱动器（例如 `nvme0n1`）看起来被分割成了多个设备？

答案：

你很可能指的是 `lsblk`（"list block devices" 的缩写），而不是 `lbdisk`。它显示块设备的树状结构以及它们是如何被分区的。

```bash
lsblk
# NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
# nvme0n1     259:0    0 931.5G  0 disk
# ├─nvme0n1p1 259:1    0   600M  0 part /boot/efi
# ├─nvme0n1p2 259:2    0     1G  0 part /boot
# └─nvme0n1p3 259:3    0 929.9G  0 part /
```

### NVMe 命名 —— 为什么看起来“被分割”

命名规则编码了 NVMe 的拓扑结构，而不是多个磁盘：

```
nvme0  n1   p3
 │     │    └─ 分区 3
 │     └────── 命名空间 1
 └──────────── 控制器 0（物理 SSD）
```

- `nvme0` = 控制器（一个物理 SSD）。
- `n1` = 命名空间 1。NVMe 驱动器将存储暴露为 *命名空间*；消费级 SSD 几乎总是只有一个（`n1`）。企业级驱动器可以将一个 SSD 划分成多个命名空间，这些命名空间看起来就像独立的磁盘（`nvme0n1`、`nvme0n2`）。
- `p1/p2/p3` = 该命名空间内的分区。

因此，`nvme0n1p1 … p3` 是 **一个** SSD、一个命名空间、三个分区。与 SATA 相比，SATA 会是 `sda` → `sda1, sda2, sda3`。“额外”的字母（`n1`）是唯一的区别。你看到的是分区，而不是多个磁盘。

### 分区实际是什么

分区只是在分区表（现代 UEFI 系统上为 GPT）中记录的连续字节范围。内核读取磁盘开头的 GPT 标头并创建 `pN` 设备节点。没有任何物理分割 —— 它只是指向偏移量的元数据。

典型的 Fedora UEFI 布局：

| 分区 | 大小 | 文件系统 | 挂载点 | 用途 |
| ------ | ------ | ---------- | -------- | ------ |
| p1 | ~600M | FAT32 | `/boot/efi` | EFI 系统分区（引导加载程序） |
| p2 | ~1G | ext4 | `/boot` | 内核 + initramfs |
| p3 | 剩余空间 | btrfs | `/` | 根目录（Fedora 默认使用 btrfs） |

Fedora 的默认设置还会将 `/home`、`/` 等作为 p3 内部的 **btrfs 子卷**，而不是单独的分区 —— 灵活，无需固定大小分割。

### Fedora 安装过程中分区（Anaconda）

在安装程序中：**安装目标 → 存储配置**。

- **自动** —— Anaconda 会为你创建 ESP + `/boot` + btrfs 根目录。除非有特殊原因，否则选择此项。
- **自定义** —— 你定义挂载点；它构建分区/子卷。
- **高级（Blivet-GUI）** —— 原始分区编辑器，完全手动控制。

### 命令行分区

如果你想手动（或通过脚本）操作，现代工具：

```bash
# 检查
lsblk -f                      # 设备 + 文件系统 + UUID
sudo fdisk -l /dev/nvme0n1    # 分区表转储

# GPT 分区，可脚本化
sudo sgdisk -n 1:0:+600M -t 1:ef00 /dev/nvme0n1   # ESP
sudo sgdisk -n 2:0:+1G   -t 2:8300 /dev/nvme0n1   # /boot
sudo sgdisk -n 3:0:0     -t 3:8300 /dev/nvme0n1   # 根目录，使用剩余磁盘空间

# 交互式替代方案
sudo gdisk /dev/nvme0n1       # GPT 感知的 fdisk
sudo cfdisk /dev/nvme0n1      # curses TUI，最简单的交互方式
sudo parted /dev/nvme0n1      # 支持调整大小和脚本化操作

# 格式化
sudo mkfs.fat -F32 /dev/nvme0n1p1
sudo mkfs.ext4 /dev/nvme0n1p2
sudo mkfs.btrfs /dev/nvme0n1p3
```

`sgdisk` 分区类型代码值得了解：`ef00` = EFI 系统，`8300` = Linux 文件系统，`8200` = 交换分区，`8e00` = LVM。

对你理解模型的关键点：单个 NVMe 下出现的“多个磁盘”外观只是 `控制器 → 命名空间 → 分区`。一个 SSD，通过 GPT 表分割。如果你看到 `nvme0n2`，那才是一个真正独立的命名空间，只有企业/数据中心驱动器才会暴露。

参考：

- [lsblk(8) 手册页](https://man7.org/linux/man-pages/man8/lsblk.8.html)
- [NVMe 命名空间与设备命名 — Arch Wiki](https://wiki.archlinux.org/title/NVMe)
- [Fedora 安装指南 — 手动分区](https://docs.fedoraproject.org/en-US/fedora/latest/install-guide/install/Installing_Using_Anaconda/)
- [sgdisk / gdisk 文档](https://www.rodsbooks.com/gdisk/)
