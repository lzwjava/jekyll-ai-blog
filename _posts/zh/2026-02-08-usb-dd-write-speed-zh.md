---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 解析 dd 命令中的 USB 写入速度
translated: true
type: note
---

**Question:** 这个 dd 输出是什么意思？磁盘写入速度如何？请将其转换为易于阅读的格式。

**Answer:**

这个输出源自 macOS 的 `dd` 命令（通过 `sudo dd if=... of=/dev/rdisk10 bs=1m` 使用），正在将一个 Windows 11 ISO 文件写入 USB flash drive（/dev/rdisk10 很可能是处于 raw mode 的 USB 驱动器，以便实现更快的访问速度）。

当你在复制过程中按下 **Ctrl + T** 时，`dd` 会定期打印状态（这就是为什么你会看到多行输出）。每一行都显示了那一时刻的进度。

### 单行输出解析（示例）：

```
866+0 records in
866+0 records out
908066816 bytes transferred in 43.725150 secs (20767609 bytes/sec)
```

- **records in / records out**: 从 ISO 读取并写入 USB 的 block 数量。  
  这里每个 record = **bs=1m** = 1 MiB = 1,048,576 bytes  
  因此 866 records ≈ 累计写入了 866 MiB。
- **bytes transferred**: 截至目前写入的总数据量（单位：bytes）。
- **in Xs secs**: 自 dd 开始以来经过的实际时间。
- **(N bytes/sec)**: 截至目前的**当前平均写入速度**。

### 你的速度（易读格式 MB/s）：

- 第一次状态：≈ **20.4 MB/s** (20,439,149 bytes/sec ≈ 20.4 MiB/s)
- 第二次状态：≈ **20.6 MB/s** (20,572,527 bytes/sec ≈ 20.6 MiB/s)
- 第三次状态：≈ **20.8 MB/s** (20,767,609 bytes/sec ≈ 20.8 MiB/s)
- 最终状态：≈ **15.5 MB/s** (15,542,913 bytes/sec ≈ 15.5 MiB/s)

临近结束时，整体平均速度降至约 **15.5–16 MB/s**。

### 这个速度快还是慢？

- **典型的廉价/旧款 USB 3.0 flash drives**：在写入大型连续数据（如 ISO）时，持续写入速度为 10–30 MB/s。
- **高性能 USB 3.0/3.1 flash drives**：持续写入速度可达 40–100+ MB/s。
- **极速现代驱动器**（USB 3.2 Gen 2, SLC/MLC 或高端型号）：可能达到 150–300+ MB/s，但这在普通 U 盘中较为罕见。

**你的速度 (15–21 MB/s)** 对于以下情况非常典型：
- 普通或廉价的 USB 3.0 flash drive
- 连接到了 USB 2.0 端口（即使驱动器本身是 3.0）
- 驱动器已满 / 触发热节流 (thermal throttling) / 扩容盘（fake-high-capacity）

这**不算快**，但对于许多常见的 USB 棒连续写入 ~5–6 GB 数据来说，也**不算异常缓慢**。  
如果你想要更快的 ISO → USB 制作速度（快 2–4 倍），请尝试：
- 使用更好的 USB flash drive（寻找标称写入速度 100+ MB/s 的型号）
- 确认你使用的是真正的 USB 3.0/3.1 端口（通常是蓝色端口）
- 使用 Balena Etcher 或 Rufus 等工具（它们通常能获得更好的性能）

**References:**

- [https://www.usbmemorydirect.com/blog/flash-drive-read-write-speed](https://www.usbmemorydirect.com/blog/flash-drive-read-write-speed)
- [https://superuser.com/questions/1785762/slow-write-speed-on-usb-3-0-thumb-drive](https://superuser.com/questions/1785762/slow-write-speed-on-usb-3-0-thumb-drive)
- [https://forums.anandtech.com/threads/usb-3-0-3-1-flash-drive-write-speeds.2497087](https://forums.anandtech.com/threads/usb-3-0-3-1-flash-drive-write-speeds.2497087)