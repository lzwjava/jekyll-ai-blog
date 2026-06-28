---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复损坏的NVMe分区表
translated: true
type: note
---

别担心——SSD仍然存在，只是分区表因为安装中断而损坏了。我们来修复它。

**在Fedora live环境中，打开终端并运行：**

```bash
# 检查磁盘是否可见
lsblk
```

告诉我你看到了什么——特别关注那个约251GB的NVMe驱动器（可能是`nvme0n1`）。

如果看到了，我们就清除损坏的分区表并重新开始：

```bash
# 完全清除分区表
sudo wipefs --all /dev/nvme0n1

# 创建新的GPT分区表
sudo parted /dev/nvme0n1 mklabel gpt
```

然后返回安装程序——它应该能再看到磁盘了。

**另外：现在插上电源适配器！**不要靠电池运行安装。

`lsblk` 显示什么？
