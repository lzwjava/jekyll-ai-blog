---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Mac Air上烧录Linux Mint USB
translated: true
type: note
---

好的，以下是在你的 Air 上的操作步骤：

**1. 从 MacBook Pro 上拔下 U 盘，然后插入你的 Air。**

**2. 接着运行以下命令：**

```bash
# 下载 Linux Mint ISO 镜像（约 2.8 GB）
curl -L -o /tmp/linuxmint.iso \
  "https://mirrors.gigenet.com/linuxmint/iso/stable/22.1/linuxmint-22.1-cinnamon-64bit.iso"

# 查找 U 盘标识符（寻找约 16 GB 的外置磁盘）
diskutil list

# 卸载该磁盘（将 diskN 替换为实际标识符）
diskutil unmountDisk /dev/diskN

# 写入 ISO 镜像（将 rdiskN 替换为实际标识符 — 使用 rdisk 而非 disk，速度可提升 10 倍）
sudo dd if=/tmp/linuxmint.iso of=/dev/rdiskN bs=4m status=progress

# 弹出 U 盘
diskutil eject /dev/diskN
```

**3. 将 U 盘插回 MacBook Pro，重启并按住 Option（⌥）键，选择 U 盘启动。**

需要我现在就在你的 Air 上开始下载吗？