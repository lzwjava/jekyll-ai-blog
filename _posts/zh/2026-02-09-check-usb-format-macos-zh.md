---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 如何在 macOS 上检查 USB 格式
translated: true
type: note
---

Question: 在 macOS 中，如何知道 USB 磁盘的格式（FAT32 或其他）？

Answer: 

以下是在 macOS 上检查 USB 驱动器文件系统格式（例如 FAT32, exFAT, APFS, Mac OS Extended, NTFS 等）最简单的方法：

### Method 1: 使用 Finder（最快 – 推荐）

1. 插入您的 USB 驱动器。
2. 打开 **Finder**。
3. 在侧边栏中找到您的 USB 驱动器（通常显示在 "Locations" 下）。
4. 右键点击（或按住 Control 点击）该 USB 驱动器名称。
5. 选择 **Get Info** (显示简介)。
6. 在 Info 窗口中，找到名为 **Format** 的行（靠近顶部，在 General 下）。
   - 您会看到类似以下内容：
     - **MS-DOS (FAT32)** → 也就是 FAT32
     - **ExFAT** → 现代的大文件兼容格式
     - **Mac OS Extended (Journaled)** → 也被称为 HFS+
     - **APFS**
     - **Windows (NTFS)**
     - 等等。

此方法适用于任何近期的 macOS 版本，对大多数用户来说也是最快的方法。

### Method 2: 使用 Disk Utility（更详细的视图）

1. 插入您的 USB 驱动器。
2. 打开 **Disk Utility**：
   - 前往 Applications → Utilities → Disk Utility
   - 或使用 Spotlight (Cmd + Space) 并输入 "Disk Utility"
3. 在左侧边栏中，选择您的 USB 驱动器（点击实际的设备名称，而不只是卷标 —— 如果看不到完整的设备列表，请前往菜单 **View → Show All Devices**）。
4. 查看主区域显示的信息：
   - 您会看到清晰列出的 **Format** 或 **File System**（例如 "MS-DOS (FAT32)", "ExFAT", "APFS" 等）。
   - 您还可以点击顶部的 **Info** 按钮（i 图标）查看更多详情。

### Method 3: 使用 Terminal（适用于命令行用户）

1. 打开 **Terminal** (Applications → Utilities → Terminal)。
2. 运行此命令列出所有磁盘：
   ```
   diskutil list
   ```
   → 找到您的 USB 驱动器（通常是类似 `/dev/disk2` 或 `/dev/disk3` —— 通过容量和名称来识别它）。
3. 然后运行（将 `disk3` 替换为您实际的磁盘编号）：
   ```
   diskutil info disk3s1
   ```
   （使用对应卷的分区，如 `diskXs1` 或 `diskXs2`）
   → 寻找 **File System Personality** 或 **Type (Bundle)** 这一行 —— 它会显示 FAT32, ExFAT, Journaled HFS+, APFS 等。

**Quick tip**: 在 macOS 中，FAT32 通常显示为 **MS-DOS (FAT32)**。如果您只看到 "MS-DOS (FAT)"，那是较旧的 16-bit FAT（在现代 USB 驱动器上很少见）。

这些方法适用于 macOS Ventura, Sonoma, Sequoia 及更早的版本。

References:  

- [How to Determine File System of a Drive on Mac - OS X Daily](https://osxdaily.com/2023/01/30/how-to-determine-file-system-of-a-drive-on-mac)
- [Server Fault - How do I identify the file system of a drive in Mac OS?](https://serverfault.com/questions/276091/how-do-i-identify-the-file-system-of-a-drive-in-mac-os)