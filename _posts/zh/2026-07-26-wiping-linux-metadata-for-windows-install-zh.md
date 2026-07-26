---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为Windows安装清除Linux元数据
translated: true
type: note
---

问题：之前用的是联想小新上的Linux Mint系统，现在安装Windows 11时出现"分区类型无法识别"/"卷处于脱机状态"——如何解决？

答案：这几乎总是Linux磁盘元数据残留导致的，Windows分区驱动程序无法解析这些元数据——可能是**mdadm RAID超级块**（Linux Mint安装程序有时会为单磁盘设置创建软件RAID元数据，或是`install_from_iso` GPT+LVM布局残留），或者是分区表上的**LVM/LUKS签名**被Windows误识别为外部/动态磁盘，导致其显示为脱机状态。

由于你要全新安装Windows（无需保留数据），最快的方法是直接清除整个磁盘表，而不是与GUI工具纠缠：

1. 在安装界面按`Shift + F10`打开命令提示符。
2. 运行以下命令：

```
diskpart
list disk
select disk 0          # 选择报错的磁盘，通过容量确认
detail disk             # 确认显示脱机/外部/动态状态
clean
convert gpt
create partition primary
format fs=ntfs quick
exit
```

3. 关闭命令提示符，在安装界面点击**刷新**，选择新创建的分区，点击**下一步**。

这里必须使用`clean`的原因：Windows GUI中的"使磁盘联机"仅能处理简单的脱机状态（如磁盘签名冲突），无法处理分区表或磁盘末尾的Linux RAID/LVM签名。`diskpart clean`会清除MBR/GPT及所有RAID元数据块，让Windows识别到一块真正的空白磁盘，从而停止报错。

如果这台联想小新是**双存储配置**（NVMe + eMMC，常见于小新Air/Pro系列），或曾设置过**Mint的LVM全盘加密**，请在`select disk`前仔细核对`list disk`的磁盘容量——如果你想双系统保留Mint在另一块硬盘上，切勿清理错误的目标盘。

如果你**确实想**在这块磁盘上保留Mint（双系统）而非全部清除，请告诉我，我会提供保留LVM的版本——那是不同的非破坏性路径（仅删除/重建Windows目标分区，保留Mint的LVM物理卷不受影响）。

参考：

- [Diskpart 命令参考 - Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/diskpart)
- [Windows安装程序"无法识别的分区"故障排除](https://learn.microsoft.com/en-us/troubleshoot/windows-client/installing-updates-features-roles/windows-setup-installation-issues)
