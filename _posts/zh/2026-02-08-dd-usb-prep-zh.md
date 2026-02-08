---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: DD 和 USB 准备指南
translated: true
type: note
---

**Question:** 在 Mac 上使用 `dd` 命令之前是否需要抹掉 USB 磁盘？如果需要抹掉，应该选择什么格式？

**Answer:**

在 macOS 上使用 `dd` 命令创建启动 USB（例如写入 Windows ISO 或 Linux ISO）时，**严格来说并不需要预先抹掉或格式化 USB 驱动器**。

`dd` 命令直接写入原始设备（例如 `/dev/diskX` 或 `/dev/rdiskX`），从第一个字节开始完全覆盖整个磁盘——包括分区表、所有现有分区、文件系统和数据。这使得任何先前的格式化在几乎所有情况下都变得无关紧要。

### 为什么通常**不需要**先抹掉/格式化
- 大多数标准混合 ISO (Ubuntu, Fedora, 近期的 Windows 10/11 ISO, 以及许多 Linux 发行版)
- ISO 本身包含了正确的分区表和启动结构
- `dd` 只是逐位（bit-for-bit）拷贝这个结构 → USB 即可变为可启动状态

典型的安全工作流（2025–2026 年最常用且推荐）：
1. 插入 USB
2. 运行 `diskutil list` → 识别正确的磁盘（例如 `/dev/disk4`）
3. 卸载其上的卷：`diskutil unmountDisk /dev/disk4`
4. 运行 dd 命令：  
   `sudo dd if=/path/to/your.iso of=/dev/rdisk4 bs=4m` （或 `bs=1m`, `bs=8m` —— 使用 `rdisk` 通常更快）
5. 等待（如果需要，按 **Ctrl+T** 查看进度）
6. 完成后：`diskutil eject /dev/disk4`

### 为什么有时人们还是会先进行抹掉/格式化
在以下情况下，你可能想要（或需要）这样做：

- 该 USB 之前曾用于不寻常的用途（旧的分区样式、奇特的文件系统、损坏的 MBR/GPT），导致 macOS 报错或 `dd` 表现异常
- 即使在卸载后，你仍收到 "Resource busy" 或权限问题
- 你想额外确保旧的分区表已彻底清除
- 你正在遵循的教程为了安全性/兼容性包含了这一步骤

如果你决定先抹掉它，以下是常见的选择：

| 情况 | Terminal 中的推荐命令 | 格式 / 方案 | 备注 |
|------------------------------------|---------------------------------------------------------------------|----------------------------------|-----------------------------------------------------------------------|
| 快速擦除分区表 | `sudo dd if=/dev/zero of=/dev/diskX bs=1m count=100` | — (原始置零) | 仅清除开头部分 — 通常足以修复“卡住”的驱动器 |
| 标准准备（最常用） | `diskutil eraseDisk FAT32 USBBOOT MBRFormat /dev/diskX` | **MS-DOS (FAT)** + **MBR** | Windows/Linux ISO 非常常见 — 安全且被广泛推荐 |
| 备选方案（macOS 偏好） | `diskutil eraseDisk ExFAT USBBOOT GPT /dev/diskX` | **ExFAT** + **GUID Partition Map** | 运行良好，但 MBR 通常对 Windows 启动兼容性更好 |
| 老牌 Apple 方案 | `diskutil eraseDisk JHFS+ TEMP GPT /dev/diskX` | **Mac OS Extended** + **GPT** | 制作 Windows/Linux USB 时极少需要 |

当人们在 `dd` 之前进行格式化时，**FAT32 + MBR** 是最流行的预格式化选择——它快速、兼容，并且在极少数 ISO 需要特定分区样式的情况下会有所帮助。

**底线 (2026 年视角)**  
在绝大多数实际案例中——尤其是使用现代 Windows 11 ISO（包括 25H2 构建版本）时——你可以完全跳过抹掉/格式化步骤，在卸载后直接进行 `dd`。只需**极其小心**地确认磁盘标识符（`disk2`, `disk3` 等），以避免抹掉你的内置硬盘或其他重要磁盘。

**References:**  

- [https://unix.stackexchange.com/questions/75477/how-should-i-format-a-usb-prior-to-writing-an-iso-to-it](https://unix.stackexchange.com/questions/75477/how-should-i-format-a-usb-prior-to-writing-an-iso-to-it)
- [https://osxdaily.com/2015/06/05/copy-iso-to-usb-drive-mac-os-x-command/](https://osxdaily.com/2015/06/05/copy-iso-to-usb-drive-mac-os-x-command/)
- [https://support.apple.com/en-us/101578](https://support.apple.com/en-us/101578) (相关的 macOS 可启动 USB 背景)
- 各种 2024–2025 年在 macOS 上创建 Windows 11 USB 的社区指南 (GitHub Gists, Reddit 帖子, 博客)