---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Windows 11安装盘脱机错误
translated: true
type: note
---

问题：Windows 11 安装程序显示“分区类型无法识别”/“所选卷处于脱机状态”——如何解决？

答案：当磁盘处于 RAID/动态磁盘状态，或存在外部磁盘签名（常见于从另一台 RAID 配置的机器中取出硬盘，或曾属于 Intel RST/VROC 的磁盘）时，会出现此问题。安装程序的 GUI 中的“使磁盘联机”按钮呈灰色不可用状态，因为它无法处理这种情况——请使用 diskpart 解决。

1. 在安装界面按下 `Shift + F10` 打开命令提示符。
2. 运行：

```
diskpart
list disk
select disk 1          # 根据图片选择对应的磁盘索引
detail disk             # 查看是否显示“状态：脱机”及原因
attributes disk clear readonly
online disk
```

3. 如果磁盘仍无法联机（外部/动态磁盘）：

```
list volume
select volume 1
attributes volume clear readonly
```

4. 如果磁盘显示为**动态**而非**基本**，安装程序将完全无法在此安装——必须转换磁盘。此操作具有破坏性：

```
clean
convert basic
create partition primary
format fs=ntfs quick
```

`clean` 会清除选定磁盘上的分区表——请确保选择了*正确*的磁盘编号，而非源数据盘。在 `select disk` 后再次运行 `list disk` 确认，然后再执行 `clean`。

5. 退出 diskpart（`exit`），关闭命令提示符，在安装界面点击**刷新**，然后再次尝试下一步。

根本原因通常是：磁盘之前曾在 RAID 阵列（Intel RST）中使用，或是存储空间中的动态磁盘，亦或是因其他操作系统导致 GPT 保护性 MBR 混乱。如果这是一块全新的 NVMe 硬盘，请检查 BIOS SATA 模式（RAID 与 AHCI）——在安装过程中切换模式会直接导致此问题。

参考资料：

- [Diskpart 命令参考 - Microsoft Learn](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/diskpart)
- [修复：Windows 安装程序无法在此计算机硬件上配置 Windows](https://learn.microsoft.com/zh-cn/troubleshoot/windows-client/installing-updates-features-roles/windows-setup-installation-issues)