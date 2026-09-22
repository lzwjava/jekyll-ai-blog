---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用dd将ISO写入U盘
translated: true
type: note
---

在 **`/dev/disk12`** 找到了您的USB磁盘（15.7 GB 外部存储，FAT32 格式）。

以下是 `dd` 命令：

```bash
# ⚠️ 警告：此操作将销毁 /dev/disk12 上的所有数据！
# 首先，卸载所有已挂载的卷
sudo diskutil unmountDisk /dev/disk12

# 将 ISO 写入 USB 磁盘（使用原始磁盘以加快速度）
sudo dd if=/Users/lzwjava/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=1m
```

**关键说明：**
- 使用 `/dev/rdisk12`（原始磁盘）→ 比 `/dev/disk12` 快得多
- `bs=1m` → 1 MB 块大小，性能更佳
- macOS 的 `dd` 默认不显示进度；要查看进度，请另开一个终端并运行：
  ```bash
  sudo killall -INFO dd
  ```
  （或者，如果您安装了 `pv`，可以使用 `sudo pv -tpreb /Users/lzwjava/Downloads/ubuntu-26.04-desktop-amd64.iso | sudo dd of=/dev/rdisk12 bs=1m`）

然后耐心等待——约 6.1 GB 数据，以 30–50 MB/s 的速度需要 **2–3 分钟**。完成后，安全弹出：

```bash
sudo diskutil eject /dev/disk12
```

**运行前请再次确认** `/dev/disk12` 确实是您的 USB 设备——确保没有连接其他外部磁盘！