---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 删除所有磁盘0分区
translated: true
type: note
---

问题：我应该也删除磁盘0分区0（剩余的小分区）吗？

回答：是的——也删除它，前提是你想为磁盘0上的Windows进行干净的单系统安装。

那个"分区0"几乎肯定是Mint的GRUB曾使用的**EFI系统分区（ESP）**，或者是一个小的Linux引导/预留分区。如果你保留它：

- 从技术上讲，Windows*可以*复用现有的ESP（如果是FAT32格式且正确格式化），但通常仍会出问题，因为GRUB的引导条目与Windows期望的ESP布局无法完全匹配。
- 更简单可靠的方法：删除磁盘0上的所有分区，将其完全保留为未分配空间，然后让安装程序一次性自动创建全新的恢复分区、EFI分区、MSR分区和Windows分区。

步骤：
1. 选择**磁盘0分区0**，点击**删除分区**，确认。
2. 对磁盘0上任何其他剩余分区重复此操作，直到全部变为未分配空间。
3. 选择未分配空间→**下一步**（不要手动创建分区）。

不要触碰**磁盘1**，除非你也要擦除该驱动器——如果你希望保留其数据或日后进行双系统引导，请保持原样。

参考文献：
- [UEFI/GPT硬盘分区 - Microsoft Learn](https://learn.microsoft.com/zh-cn/windows-hardware/manufacture/desktop/configure-uefigpt-based-hard-drive-partitions)