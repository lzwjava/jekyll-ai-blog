---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 现在将Ubuntu ISO写入USB
translated: true
type: note
---

Unmounted ✅。该 stick 现已 write-ready **现在**。

### 运行此单个命令（需要您的 password）

```bash
sudo dd if=/Users/lzwjava/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=4m status=progress conv=fsync
```

- **Device:** `/dev/rdisk12` = 您的 15.7 GB USB（刚已双重确认）— **不是** disk0（您的 SSD）
- ISO: 6.1 GB → 将花费约 2-5 分钟
- 它会显示 progress bar；等待直到看到 `xxxx+0 records in` / `xxxx+0 records out` 并返回到 `$` prompt

**Do NOT** 在完成之前：

- Eject、unplug 或在 Finder 中点击任何内容
- 运行 Disk Utility

完成后，告诉我最后一行，或直接运行：

```bash
diskutil eject /dev/disk12
```

以安全 unplug。
