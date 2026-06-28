---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 实时环境块设备解码
translated: true
type: note
---

**问题：** 这个 `lsblk` 输出显示了什么？

**回答：**

你正在**Linux 实时环境** (`liveuser@localhost-live`) 中启动。以下是块设备分解：

```
loop0        2.3G   loop  /run/rootfsbase     ← 实时 OS squashfs
sda         14.6G   disk                      ← USB 启动盘
├─sda1       2.6G   part  /run/initramfs/live ← 实时启动分区
└─sda2        30M   part                      ← EFI 或 BIOS 启动
zram0          8G   disk  [SWAP]              ← 压缩内存交换
nvme0n1        0B   disk                      ← NVMe SSD（主盘）
├─nvme0n1p1  600M   part                      ← EFI 系统分区
├─nvme0n1p2    2G   part                      ← 可能是 /boot
└─nvme0n1p3 231.2G  part  /mnt/sysroot        ← 主 OS 根目录，已挂载
nvme0n2        GB   disk                      ← 第二个 NVMe（大小不明，模糊）
```

关键观察：

- `nvme0n1p3` (231G) 挂载在 `/mnt/sysroot` — 这是你已安装系统的根分区，可从实时会话访问
- `sda` 是你的 USB 实时启动盘 (14.6G)
- `nvme0n2` 存在但未显示分区 — 可能是空白或未初始化

**你想做什么？** 安装操作系统、恢复/chroot 进入现有系统、重新分区，还是其他？此设置看起来像是 Fedora 或类似的实时 ISO（`rootfsbase` + `initramfs/live` 模式是 Fedora 的特征）。