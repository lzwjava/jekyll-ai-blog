---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 清理Windows未分配空间
translated: true
type: note
---

问题：我使用安装程序自带的“删除分区”功能删除了磁盘0上476GB的分区，现在显示为未分配空间——接下来该怎么办？

回答：很好，这是最简单的方法，而且成功了。接下来：

1. **选择磁盘0上的未分配空间**。
2. 直接点击**下一步**——不要手动先创建分区。在GPT磁盘的原始未分配空间上操作时，Windows安装程序会自动创建它所需的4个分区（恢复分区、EFI系统分区、MSR分区和实际的Windows分区）。
3. 如果你手动点击**新建分区**，安装程序只会创建一个分区，然后你还需要单独处理EFI/MSR分区——直接让它自动拆分即可。

如果点击“下一步”时不再出现“无法识别的类型/脱机”错误，说明问题已解决——该错误与旧版Linux Mint分区签名（LVM/RAID元数据）有关，删除分区后已清除了混淆Windows磁盘驱动器的元数据。

需要注意：你的照片显示**两块磁盘**（磁盘0和磁盘1），每块各有两个分区。如果磁盘1上也有残留的Mint分区（例如独立的`/home`分区或交换分区），并且你计划全新安装Windows而不使用双系统，建议现在也将这些分区删除，避免日后在磁盘管理中留下多余的Linux分区。如果你想保留磁盘1上的Mint以使用双系统，则无需操作——Windows安装程序不会触碰未选中的其他磁盘。

参考文档：

- [Windows安装程序——创建和格式化硬盘分区](https://learn.microsoft.com/zh-cn/windows-hardware/manufacture/desktop/configure-uefigpt-based-hard-drive-partitions)
