---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Syslinux XZ解压失败
translated: true
type: note
---

**问题：** 从 MOD 50 系列（或类似）映像启动时，Syslinux 中出现“XZ compressed data is corrupt — System halted”是什么意思？是什么原因造成的？

---

**答案：**

## 此错误的含义

当 Syslinux 加载 Linux 内核或 initramfs 时，这些文件通常使用 XZ（或类似格式）压缩。错误“XZ-compressed data is corrupt — System halted”发生在内核解压缩阶段——Syslinux 成功加载了文件，但当内核尝试将其解压到内存时，数据未通过完整性检查，系统完全停止。

这**通常不是**软件缺陷——它最常表明存在**硬件或介质问题**。

---

## 根本原因（按常见程度从高到低排序）

### 1. 内存故障（最常见）

一个已确认的原因是内存模块故障——更换故障内存后，更新即可顺利安装。解压缩过程要求内存稳定可靠；即使一个比特位翻转也会导致输出损坏。

### 2. USB 驱动器损坏或写入错误

劣质 U 盘可能导致此错误。某案例中，将同一 ISO 写入另一 U 盘后问题解决。即使物理介质看似正常，也可能存在坏扇区。

### 3. 老旧或不兼容的硬件

在老机器上，该错误可能间歇出现。ACPI 设置也可能引发此错误，有时可通过在内核启动参数中添加 `acpi=off` 来解决。

### 4. 光驱故障（如果从 CD/DVD 启动）

至少有一个案例确认故障 DVD 光驱是原因之一。

### 5. 写入不完整或中断

即使 ISO 校验和正确且在其他机器上可正常启动，也可能出现此错误，表明问题与特定硬件相关，而非映像文件损坏。

---

## 故障排除步骤

| 步骤 | 操作 |
| --- | --- |
| 1 | 运行 **Memtest86+** 测试内存 |
| 2 | 尝试 **不同的 U 盘** 或闪存介质 |
| 3 | 使用已验证的工具重新写入映像 |
| 4 | 尝试在 **另一台机器** 上启动以隔离问题 |
| 5 | 在内核启动参数中添加 `acpi=off` |
| 6 | 逐一重新插拔或更换内存模块 |

---

## 关于“仅限 MOD 50 系列映像”的说明

如果你使用的是特定的嵌入式设备映像（例如标有“MOD 50”的 NAS、UPS 控制器或网络设备），并且只有该特定映像会触发此错误，那么可能的元凶是：映像写入不完整、设备的闪存存储存在坏块，或者设备内存中用于解压缩的地址范围存在故障。建议优先通过制造商的恢复方法重新刷写映像。

---

**参考资料：**

- [LibreELEC Forum — 内存故障导致 XZ 损坏错误](https://forum.libreelec.tv/thread/9589-solved-update-to-8-1-0-on-generic-failed-xz-compressed-data-is-corrupt-system-ha/)
- [Arch Linux Forums — XZ 压缩数据损坏](https://bbs.archlinux.org/viewtopic.php?id=144116)
- [Arch Linux Forums — 旧硬件的 ACPI 解决方法](https://bbs.archlinux.org/viewtopic.php?id=144116)
- [Linux Mint Forums — USB 驱动器损坏为根本原因](https://forums.linuxmint.com/viewtopic.php?t=204857)
- [Gentoo Forums — 硬件相关的 XZ 损坏错误](https://forums.gentoo.org/viewtopic.php?t=987516)
