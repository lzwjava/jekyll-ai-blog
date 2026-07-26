---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 清理磁盘0 转换GPT 安装
translated: true
type: note
---

问题：Disk 0 确认为 UMIS NVMe 512GB 驱动器，目标正确 — 是否继续执行 clean？

答案：是的，这是正确的磁盘。已确认：NVMe，在线，476GB NTFS 卷 C，状态健康，非只读。这是你的目标 SSD，不是较小的 Disk 1。

继续：

```cmd
clean
```

等待显示 `DiskPart 已成功清理磁盘。`

```cmd
convert gpt
```

等待显示 `DiskPart 已成功将所选磁盘转换为 GPT 格式。`

```cmd
exit
```

完全关闭命令提示符窗口，然后从修复菜单**重启进入 Windows 11 USB 安装程序**（再次强调，不是修复菜单 — 你需要完整的安装 GUI 才能进入分区选择）。依次通过语言/版本界面到达“选择安装 Windows 11 的位置”，点击**刷新**，选择未分配的 Disk 0，点击**下一步**。

**这次的关键检查点：** 点击下一步后，等待几秒钟让安装程序自动创建分区，如果再次立即报错，则返回分区列表界面查看 — 你应该会在 Disk 0 上看到 4 个条目（系统/EFI、MSR、主分区、恢复分区）。如果这次 EFI 系统分区存在，安装应能在重启后继续执行，而不会像之前那样失败。