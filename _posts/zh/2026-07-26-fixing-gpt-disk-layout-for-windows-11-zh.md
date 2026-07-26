---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Windows 11的GPT磁盘布局
translated: true
type: note
---

问题：分析 `diskpart list partition` — 磁盘布局是否导致 Windows 11 安装失败？

回答：

这张截图非常有帮助。你的 SSD 布局如下：

```
Disk 0 (476 GB GPT)

Partition 1   Reserved   16 MB
Partition 2   Primary    476 GB
```

这**不是正常的 Windows 11 UEFI 布局**。

一个正确干净的 Windows 11 GPT 磁盘通常应该是：

```
Partition 1   EFI System      ~100 MB   FAT32
Partition 2   Microsoft MSR    16 MB
Partition 3   Windows          NTFS
Partition 4   Recovery         ~500 MB-1GB
```

你目前的磁盘是：

```
MSR 16 MB
+
一个巨大的主分区
```

缺失：

* EFI 系统分区 (ESP) ❌
* 恢复分区 ❌

这比 VMD 更能解释安装失败的原因。

---

## 修复方法

既然你是全新安装，请清空磁盘。

在同一个命令提示符中：

```cmd
diskpart

select disk 0

clean

convert gpt

exit
```

然后关闭 CMD。

在 Windows 安装程序中：

1. 点击**刷新**
2. 选中**未分配空间**
3. 点击**下一步**

**不要**手动创建分区。

Windows 安装程序会自动创建：

```
EFI
MSR
Windows
Recovery
```

---

## 原因分析

很可能之前的分区是由以下方式创建的：

* 旧的 Linux 安装
* 之前的 Windows 克隆
* 联想恢复修改
* 手动分区

安装程序尝试升级/安装到现有的 GPT 布局中，但没有有效的 EFI 启动分区，随后失败并报错：

```
0xC19001F4
```

---

目前来看：

* USB ✅ 确认正常
* SSD ✅ 已检测到
* VMD ❌ 可能性较小
* 磁盘布局 ❌ 很可能是根本原因

我建议现在执行 `clean + convert gpt`。这是最高概率的修复方法。