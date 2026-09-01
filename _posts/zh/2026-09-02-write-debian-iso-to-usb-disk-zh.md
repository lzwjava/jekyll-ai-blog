---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将Debian ISO写入USB磁盘
translated: true
type: note
---

以下是将 Debian ISO 写入 USB 磁盘的命令。**⚠️ 这将完全擦除 `/dev/disk12` — 请确保上面没有其他重要数据。**

### 步骤 1 — 卸载磁盘（不要弹出）

```bash
diskutil unmountDisk /dev/disk12
```

### 步骤 2 — 使用 `dd` 写入 ISO

```bash
sudo dd if=/Users/lzwjava/Downloads/debian-live-13.6.0-amd64-xfce.iso \
     of=/dev/rdisk12 \
     bs=4m \
     status=progress
```

注意：

- 使用 **`/dev/rdisk12`**（原始设备）代替 `/dev/disk12` — 在 macOS 上速度更快。
- `bs=4m` 提供良好的吞吐量；`status=progress` 显示传输进度（GNU dd 风格；macOS 的 BSD `dd` 会忽略此参数，但不会报错）。

### 步骤 3 — 刷新并安全弹出

```bash
sync
diskutil eject /dev/disk12
```

### 运行前的快速安全检查

您可以确认目标确实是您的 USB 设备（15.7 GB，外置）：

```bash
diskutil info /dev/disk12 | grep -E "Device/ Media Name|Disk Size|Solid State|Removable"
```

### 单行命令（卸载 → dd → 同步 → 弹出）

```bash
diskutil unmountDisk /dev/disk12 && \
sudo dd if=/Users/lzwjava/Downloads/debian-live-13.6.0-amd64-xfce.iso of=/dev/rdisk12 bs=4m && \
sync && diskutil eject /dev/disk12
```

如果 `status=progress` 不受支持且您想查看进度，可以在另一个终端中运行：

```bash
sudo kill -INFO $(pgrep -n dd)     # macOS：发送 SIGINFO，打印当前进度
```

**在运行 `dd` 之前，请再次确认 `/dev/disk12` 仍然是您的 USB 驱动器** — 磁盘标识符在重新插拔后可能会改变。请立即使用 `diskutil list external` 验证。
