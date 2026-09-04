---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 恢复.pmfx磁盘映像到磁盘
translated: true
type: note
---

**问题：**如何将 `.pmfx`（DiskGenius 磁盘映像）文件恢复到磁盘？

**答案：**

`.pmfx` 文件是 DiskGenius 专有的磁盘映像格式——它是整个磁盘的压缩备份，包含所有分区和文件。你可以用它做两件事：**恢复到磁盘**，或**在不恢复的情况下浏览/提取文件**。

---

### ✅ 方法一 — 将 .pmfx 映像恢复到磁盘（完全恢复）

1. 在 DiskGenius 中**右键点击**目标磁盘 → 选择 **“将映像文件恢复到磁盘”**，或前往菜单 **磁盘 → 将映像文件恢复到磁盘**。
2. 在文件对话框中，找到并选择你的 `.pmfx` 文件 → 点击 **打开**。
3. 确认目标磁盘正确无误 → 点击 **开始**。
4. 将出现警告提示目标磁盘上的所有分区和数据将被覆盖。请确保任何重要数据已提前备份 → 点击 **确定**。
5. 等待恢复完成。

> ⚠️ 重要提示：恢复时，目标磁盘的大小不应小于源磁盘。

---

### ✅ 方法二 — 仅从 .pmfx 文件恢复单个分区

较新版本的 DiskGenius 支持从 `.pmfx` 磁盘映像文件中恢复单个分区，因此如果你只需要一个分区，则无需恢复整个磁盘。

---

### ✅ 方法三 — 不恢复，直接浏览和提取文件

如果你只想从 `.pmfx` 映像中取出特定文件，而无需将其写入磁盘：

1. 点击 **工具** 菜单 → 选择 **“加载磁盘/分区映像”**。
2. 浏览并找到 `.pmfx` 映像文件 → 点击 **打开**。
3. 选择你想要查看的时间点 → 点击 **开始**。DiskGenius 将加载备份映像中的文件。
4. 选择你要找回的文件，并将其复制到所需位置。

---

### 💡 小贴士

- `.pmfx` 扩展名是 DiskGenius（也称为 Eassos DiskGenius）专用的，你只能在 Windows 上使用 DiskGenius 打开/恢复 `.pmfx` 文件。
- 较新版本支持对 `.pmfx` 磁盘映像文件进行扇区编辑，适用于高级用户。

---

**参考资料：**

- [从映像文件恢复磁盘 – DiskGenius 手册](https://www.diskgenius.com/manual/restore-disk-from-image-file.php)
- [加载并浏览分区映像文件 – DiskGenius 手册](https://www.diskgenius.com/manual/explorer-partition-img.php)
- [.PMFX 文件扩展名信息 – FileInfo.com](https://fileinfo.com/extension/pmfx)
- [DiskGenius 版本历史](https://www.diskgenius.com/version-history.php)
