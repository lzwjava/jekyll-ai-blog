---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: MacOS 可恢复文件拷贝详解
translated: true
type: note
---

**Question: macOS 的可恢复文件复制（resumable file copy）是如何工作的？macOS 又是如何提供这一功能的？**

**Answer:**

macOS 从 **macOS Monterey** (2021) 开始在 **Finder** 中提供了可恢复复制（resumable copy）功能，并延续到了之后的版本，如 Ventura、Sonoma 和 Sequoia。该功能允许你暂停或取消文件/文件夹的复制操作，并在之后从停止的地方恢复，而不是重新开始。

### 如何在 Finder 中使用可恢复复制

1. 开始复制大文件或文件夹（Command+C → Command+V 或拖放）。
2. 在复制进行时，点击复制进度窗口中的 **X** 按钮（或按 Esc 键）来取消/暂停。
3. Finder 会在目标位置保留一个**幽灵化**（ghosted，半透明）的文件/文件夹版本。
4. 当你随后点击这个幽灵化项目时，Finder 会显示两个选项：
   - **继续复制 (Finish Copying)** —— 从上次中断的地方继续。
   - **保留可恢复复件 (Keep Resumable Copy)** —— 保留部分/幽灵化的项目以便稍后恢复（适用于你想在另一个时间或重新连接外部/网络驱动器后完成复制的情况）。

这在本地驱动器、外部驱动器上效果最好，有时也适用于网络共享（尽管网络中断的可靠性较低）。

### 其底层的实际运作机制

Finder **并非**像 HTTP 可恢复下载（例如 URLSession 中的 `Range: bytes=500000-`）那样使用简单的 byte-range 复制。相反，它依赖于以下机制：

- 部分完成的文件/文件夹在复制停止时会完全保留在目标磁盘上。
- Finder 会使用特殊的 metadata（一个 extended attribute，如 `com.apple.metadata:kMDItemResumableCopy` 或类似的内部标识）标记该未完成的项目。
- 当你选择 **Finish Copying** 时，Finder 会智能地比较源路径和目标路径：
  - 跳过已经完成的文件。
  - 仅继续复制缺失或不完整的文件。
  - 对于已部分复制的大文件，它通常会恢复追加数据（但这取决于 file system 和 copy engine 的行为）。
- 幽灵化外观和恢复对话框由 Finder 的内部 copy engine（属于 Finder 进程和 macOS file coordination APIs 的一部分）处理。

在 Monterey 之前，Finder 不支持真正的恢复功能——中断复制通常意味着需要重新开始或手动清理残余文件。可恢复功能是用户针对大型传输（例如 TB 级别的外部驱动器备份）所要求的改进。

### 局限性与说明

- 它不如专业工具（如 `rsync --partial --progress`）或第三方应用（Carbon Copy Cloner, SuperDuper）那样稳健，后者提供更好的验证、重试逻辑和恢复能力。
- 如果连接永久断开，网络复制（SMB/AFP）有时可能无法干净地恢复。
- 如果可恢复复件卡住（变灰且无法访问），常见的解决办法包括创建 alias 以访问内容，或使用 Terminal 命令移除 metadata 标识（例如 `xattr -d com.apple.metadata:kMDItemResumableCopy` 并重置创建日期）。
- 对于非常巨大或关键的传输，许多用户仍然倾向于使用命令行 `rsync` 或付费工具，而不是 Finder 内置的恢复功能。

总结来说，macOS Finder 的可恢复复制是 Monterey 引入的一项便捷的内置功能，它通过 filesystem metadata 和智能比较逻辑追踪部分传输，允许你在不丢失已传输数据的情况下“继续完成”受阻的复制任务。

**References:**

- [https://www.macrumors.com/how-to/pause-copying-file-resume-it-later-monterey/](https://www.macrumors.com/how-to/pause-copying-file-resume-it-later-monterey/)
- [https://apple.stackexchange.com/questions/434544/how-to-remove-the-resumable-copy-flag-of-a-folder](https://apple.stackexchange.com/questions/434544/how-to-remove-the-resumable-copy-flag-of-a-folder)
- [https://discussions.apple.com/thread/253615565](https://discussions.apple.com/thread/253615565)
- [https://developer.apple.com/videos/play/wwdc2023/10006](https://developer.apple.com/videos/play/wwdc2023/10006)（相关的 URLSession 可恢复传输，用于对比）