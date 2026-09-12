---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TinyLinux启动错误修复
translated: true
type: note
---

**问题：** 这些 Linux 启动错误是什么意思，我该如何修复？

**回答：**

屏幕上显示的是 TinyLinux 20.10 启动失败，包含两个不同的问题：

**1. ACPI BIOS 错误（非关键）**

```
ACPI BIOS Error: Could not resolve symbol [\_SB.PCI0.SAT0.SPT0._GTF.DSSP], AE_NOT_FOUND
ACPI Error: Aborting method \_SB.PCI0.SAT0.SPT0._GTF due to previous error
```

这些是固件中与 SATA/存储设备初始化相关的 ACPI 表错误。它们是警告信息，并非启动失败的根本原因——系统通常仍能启动。

**2. 根文件系统未找到（关键——这是导致进入 shell 的原因）**

```
Partition with root filesystem not found. Waiting...
Giving up...
/bin/sh: can't access tty: job control turned off
```

内核无法找到应该启动的分区。这是实际的失败原因。

---

**常见原因及修复方法：**

| 原因 | 修复方法 |
| --- | --- |
| 引导加载器中 `root=` 参数错误 | 编辑 GRUB：将 `root=UUID=...` 或 `root=/dev/sdXY` 改为正确的分区 |
| 驱动器被识别为不同的设备名称（例如 `sda` → `nvme0n1`） | 在紧急 shell 中使用 `lsblk` 检查，然后更新 GRUB |
| initramfs 损坏或缺失 | 从 live USB chroot 中重新构建：`update-initramfs -u` |
| 引导加载程序安装到错误的磁盘 | 将 GRUB 重新安装到正确的磁盘 |
| 磁盘更换后 UUID 不匹配 | 更新 `/etc/fstab` 和 GRUB 配置为正确的 UUID |

**紧急操作步骤：**

由于你已进入紧急 shell（`/ #`），请运行：

```sh
lsblk        # 查看所有检测到的分区
blkid        # 查看所有分区的 UUID
cat /proc/cmdline   # 查看内核接收到的 root= 参数
```

这些命令会告诉你分区是否存在但名称不同，或者确实丢失。

---

**参考资料：**

- [Linux Kernel Boot Parameters](https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html)
- [GRUB2 Recovery – Arch Wiki](https://wiki.archlinux.org/title/GRUB/Restore_GRUB_Legacy)
- [initramfs troubleshooting – Ubuntu Docs](https://wiki.ubuntu.com/Initramfs)
