---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS重启后释放16 GB
translated: true
type: note
---

这是 macOS/APFS 的正常行为：

**~16 GB 的差异（从 490 GB 变为 474 GB）来自于：**

1. **Swap 文件** — 你的 M2 Air 有 16 GB 内存。重启前，在高负载（挂载了多个 iOS 模拟器磁盘映像、运行 LLM 工具等）下，macOS 会向磁盘进行交换。重启后 Swap 被清空。目前只有 2 GB 的 sleepimage 存在，但重启前 Swap 很容易达到 8-12 GB。

2. **APFS 本地时间机器快照** — macOS 会定期创建本地快照，这些快照会计入“已用”空间，但在 Finder 中不可见。当前快照数量为零，证实重启前它们存在，并在重启后被释放。每个快照可能有几 GB。

3. **可清除空间** — macOS 会将缓存的 iCloud 内容、系统缓存和临时数据标记为“可清除”。这在磁盘工具中显示为“已用”，但重启后会被回收。

4. **/private/var/folders/** — 正在运行的进程的临时文件（当前为 942 MB，重启前可能达到几 GB）。

**结论：** 这 16 GB 一直都在——macOS 只是将你的磁盘用作内存压力溢出和缓存的缓冲区。重启清除了 Swap、快照和临时文件。这是预期的行为，随着你继续使用电脑，这种情况会再次发生。

**提示：** 目前只有 54 GB 可用空间（数据卷上现在约 18 GB 可用），你的空间相当紧张。如果需要空间，你可以通过删除用户缓存来回收 14 GB（`rm -rf ~/Library/Caches/pip`、`Homebrew`、`JetBrains`、`LarkShell` 等）。
