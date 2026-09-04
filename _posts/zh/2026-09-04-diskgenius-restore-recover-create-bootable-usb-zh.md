---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'DiskGenius: 还原、恢复、创建可启动U盘'
translated: true
type: note
---

**问题：** 如何在 Windows 上使用 DiskGenius — 具体来说，将 disk image 恢复到 USB 驱动器、恢复文件以及其他常见操作？

**回答：**

DiskGenius 是一款功能强大的 Windows 全能磁盘工具。以下是其最常见的用途：

---

### 🔁 将 Disk Image 恢复到 USB 驱动器

此操作将 image 文件（备份）写回到物理磁盘（如 USB 驱动器）：

1. 在左侧面板中 **右键单击** 目标磁盘（你的 USB）→ 选择 **"Restore Image File To Disk"**，或者进入菜单 **Disk → Restore Image File To Disk**。
2. 在文件对话框中 **定位并选择** 你的 disk image 文件 → 点击 **Open**。
3. **确认** 目标磁盘正确无误 → 点击 **Start**。
4. 弹出警告提示 USB 上所有数据将被覆盖 — 点击 **OK** 确认。
5. 等待恢复完成。

> ⚠️ 执行此操作前请备份 USB 上的现有数据 — 它将被清空！

---

### 💾 从 USB 恢复丢失/删除的文件

打开 DiskGenius 后，所有连接的存储设备都会显示在左侧面板中。如果 USB 驱动器已连接，它会出现在那里（例如显示为 "RD1"）。如果 DiskGenius 完全无法检测到该设备，则可能物理损坏，软件恢复将无法生效。

恢复文件步骤：
1. 在左侧面板中选择 USB 驱动器或分区。
2. 点击 **File → Recover Lost Files**（或右键单击该驱动器）。
3. 选择扫描模式 — 可以启用 **"Search For Known File Types"** 来逐扇区扫描特定文件类型（照片、视频、文档等）。注意，此模式恢复的文件将丢失原始名称和文件夹结构。
4. 预览并将恢复的文件保存到 **另一个** 驱动器。

---

### 📀 创建可启动的 WinPE USB 驱动器

1. 插入 USB 驱动器并启动 DiskGenius。
2. 点击 **Tools → Create WinPE Bootable USB Drive of DiskGenius**。
3. 点击 **OK**，等待数秒即可创建完成。

要求：USB 必须格式化为 FAT32、exFAT 或 NTFS，且至少拥有 **800 MB** 可用空间。对于 UEFI 计算机，请事先将 USB 格式化为 **FAT32**。

---

### 🗂️ 其他常用功能

DiskGenius 还支持：partition recovery、克隆磁盘、将磁盘备份为 image 文件、重建 MBR、快速分区、校验和修复坏道、将 dynamic disk 转换为 basic disk，以及系统迁移。

---

**参考链接：**
- [DiskGenius Official User Guide](https://www.diskgenius.com/manual/)
- [Restore Disk From Image File – DiskGenius Manual](https://www.diskgenius.com/manual/restore-disk-from-image-file.php)
- [How to Recover Lost Data with DiskGenius](https://www.diskgenius.com/how-to/recover-lost-data-with-diskgenius.php)
- [Create WinPE Bootable USB – DiskGenius Manual](https://www.diskgenius.com/manual/create-winpe-bootable-disk-for-diskgenius.php)