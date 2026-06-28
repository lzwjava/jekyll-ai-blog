---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 准备刷写Fedora
translated: true
type: note
---

USB是`/dev/disk13`——同一个15.7 GB的驱动器。它上面有：

```
disk13s128  Bios Boot Partition     245 KB    (GRUB bootloader)
disk13s1    Linux Filesystem       16.8 MB   (很可能是OpenWrt内核)
disk13s2    Linux Filesystem       109 MB    (很可能是OpenWrt根文件系统)
(空闲空间)                          15.6 GB   (未使用)
```

这看起来像是通过`dd`刷写的**OpenWrt固件镜像**——很小的内核和根文件系统分区，其余为空。对MacBook没有用。

**准备刷写Fedora。命令：**

```bash
# 卸载USB
diskutil unmountDisk /dev/disk13

# 刷写Fedora ISO（这会擦除USB上的所有内容）
sudo dd if=/Users/lzwjava/Downloads/Fedora-Workstation-Live-44-1.7.x86_64.iso of=/dev/rdisk13 bs=4m status=progress

# 完成后弹出
diskutil eject /dev/disk13
```

现在要执行这些命令吗？