---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ReBarUEFI B75 BIOS 闪存盘
translated: true
type: note
---

以下是U盘中的内容：

## `/dev/sdb` — 14.65 GiB U盘（型号“YGS”）

**分区：** `sdb1` — 32 MB FAT16，可引导，标签 `FD13-LITE`（其余14.6 GB未分配）

## 这是什么

一个**可引导的FreeDOS 1.3“Lite”U盘**，专为**BIOS固件刷写**而构建——具体来说是一个**“ReBarUEFI - B75 BIOS刷写”**工具。

**根目录下的关键文件：**
- `flash.bat` — 主脚本：将当前BIOS备份到 `BACKUP.BIN`，然后使用Intel Flash Programming Tool（`fpt.exe`）刷写 `NEWBIOS.BIN`
- `fpt.exe` — Intel Flash Programming Tool
- `NEWBIOS.BIN` / `OLDBIOS.BIN` — 新版/旧版BIOS镜像（各4 MB）
- `BACKUP.BIN` — 原始BIOS的备份（4 MB）
- `fparts.txt` — 闪存芯片部件列表
- `KERNEL.SYS` + `COMMAND.COM` + `fdconfig.sys` + `fdauto.bat` — FreeDOS启动环境
- `setup.bat` — FreeDOS安装程序
- `freedos/` — FreeDOS系统文件
- `packages/` — FreeDOS软件包存档（.zip）

## `flash.bat` 的作用

1. 备份当前BIOS：`fpt -d BACKUP.BIN`
2. 刷写新BIOS：`fpt -f NEWBIOS.BIN`
3. 成功时：提示您关机/开机。失败时：警告您**不要**关机并重试。

## ⚠️ 警告

这是一个**BIOS固件刷写盘**（适用于Intel B75主板，添加ReBar/UEFI支持）。刷写错误的BIOS或中断该过程可能导致**机器变砖**。仅可在目标硬件上使用。

需要我详细检查某个文件吗（例如查看 `fparts.txt` 以了解支持的闪存芯片，或比较 `NEWBIOS.BIN` 与 `OLDBIOS.BIN`）？