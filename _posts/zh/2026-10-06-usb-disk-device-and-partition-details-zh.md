---
audio: false
generated: true
image: false
lang: zh
layout: post
title: USB磁盘设备与分区详细信息
translated: true
type: note
---

您的 USB 磁盘在这里：

**Device: `/dev/disk12`** — 一个通用的 **"OnlyDisk"** USB 闪存盘，**15.7 GB**，可移动，当前**未挂载**。

它有一个 GPT 分区表，包含 4 个分区：

| Partition | Type | Size | Filesystem |
| --- | --- | --- | --- |
| `s1` | Microsoft Basic Data | 6.5 GB | MS-DOS (FAT) |
| `s2` | EFI | 5.3 MB | — |
| `s3` | Microsoft Basic Data | 307 KB | — |
| `s4` | Linux Filesystem | 9.2 GB | 未检测到 |

它看起来像一个**可引导/多引导 USB 闪存盘**（EFI 分区 + FAT 数据分区 + 一个原始 Linux 分区），可能是由 Ventoy 或 Linux 安装程序之类的工具创建的。不支持 SMART，因此无法检查其健康状况。

需要我挂载分区 `s1`（FAT 分区）以便您可以浏览其内容吗？
