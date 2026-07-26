---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows 11 USB安装指南
translated: true
type: note
---

针对您的具体情况（在联想小新上安装Windows 11），以下是我之前的操作及推荐方法：

## 之前的方法（Mac上使用wimlib）

```bash
# 1. 将U盘格式化为FAT32并采用GPT分区
diskutil eraseDisk MS-DOS WIN11 GPT /dev/disk13

# 2. 挂载ISO镜像
hdiutil attach Win11_25H2_English_x64_v2.iso

# 3. 复制除install.wim外的所有文件（该文件7.1GB，超过FAT32的4GB限制）
rsync -av --exclude='sources/install.wim' /Volumes/CCCOMA_X64FRE_EN-US_DV9/ /Volumes/WIN11/

# 4. 将大型install.wim分割为小于4GB的块
wimlib-imagex split \
  /Volumes/CCCOMA_X64FRE_EN-US_DV9/sources/install.wim \
  /Volumes/WIN11/sources/install.swm \
  3800

# 5. 完成后弹出U盘
diskutil eject /dev/disk13
```

这将生成一个**支持UEFI启动**的U盘，Windows安装程序可原生识别。`.swm`分割文件由安装程序自动处理。

## 备选方案（如有Windows电脑）

**Rufus** — 最简便的选择：
- 选择ISO → 勾选 **GPT + UEFI（非CSM）** → 点击开始
- 自动处理`install.wim`大小问题

## 备选方案（如继续使用Mac）

**balenaEtcher** — **不推荐**用于Windows ISO（如前所述，镜像类型错误）。

## 针对联想小新的关键点

不过——目前**更大的问题**是您遇到的`0xC19001F4`错误。在重新刷写U盘前，建议先检查以下BIOS设置：

> **Intel VMD控制器** 或 **Intel RST** → 设置为 **禁用** / **AHCI**

这比U盘本身更可能是实际障碍。需要我指导您在BIOS中查找该选项吗？