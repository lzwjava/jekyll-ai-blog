---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Linux 内核 7.2 构建摘要
translated: true
type: note
---

编译完成！以下是摘要：

**内核：Linux 7.2.0-rc1**（`Baby Opossum Posse`）

**构建产物：**

| 文件 | 大小 | 路径 |
|------|------|------|
| **bzImage** | **15 MB** | `arch/x86/boot/bzImage` |
| **vmlinux** | **53 MB** | `vmlinux`（未压缩的ELF文件） |

**构建信息：** `#1 SMP PREEMPT_DYNAMIC`，x86_64架构，gzip压缩，可重定位，支持EFI和传统引导。

该构建在配备15GB内存的4核i5-7360U处理器上，使用`x86_64_defconfig`作为基础配置成功完成。
