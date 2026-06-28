---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 擦除NVMe并重新安装Fedora
translated: true
type: note
---

根据您照片中的 `lsblk` 输出，NVMe 已经可见：

```
nvme0n1      259:0    0    0B   0 disk          ← 显示 0B = 分区表损坏
├─nvme0n1p1  259:1    0  600M   0 part
├─nvme0n1p2  259:2    0    2G   0 part
└─nvme0n1p3  259:4    0  231.2G 0 part  /mnt/sysroot
```

实际上它显示了分区，并且 `/mnt/sysroot` 已挂载 —— 分区表并未完全损坏，而是之前的安装部分写入导致。磁盘本身显示 `0B` 只是模糊照片带来的显示伪影。

**以下是逐步操作步骤：**

**第一步 —— 先卸载 sysroot（重要）**

```bash
sudo umount /mnt/sysroot
```

**第二步 —— 擦除所有数据**

```bash
sudo wipefs --all /dev/nvme0n1
sudo wipefs --all /dev/nvme0n1p1
sudo wipefs --all /dev/nvme0n1p2
sudo wipefs --all /dev/nvme0n1p3
```

**第三步 —— 创建新的 GPT 标签**

```bash
sudo parted /dev/nvme0n1 mklabel gpt
```

**第四步 —— 验证**

```bash
lsblk
```

现在应显示 `nvme0n1` 且没有任何子分区。

**第五步 —— 重新启动 Fedora 安装程序**

```bash
sudo anaconda
```

或者点击桌面上的安装程序图标。它将识别到干净的磁盘，并允许您进行自动分区。

擦除后 `lsblk` 显示什么？
