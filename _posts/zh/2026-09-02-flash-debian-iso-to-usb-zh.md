---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将Debian ISO镜像刷写到USB
translated: true
type: note
---

找到了U盘。情况如下：

**U盘：`/dev/disk12`**（外部，物理，15.7 GB，当前装有Ventoy）
**ISO：`/Users/lzwjava/Downloads/debian-live-13.6.0-amd64-xfce.iso`**（3.6 GB）

> ⚠️ 此操作将**擦除U盘上的所有数据**（包括Ventoy）。请确认 disk12 确实是你的U盘。

### 步骤

**1. 卸载磁盘（不要弹出）：**

```bash
diskutil unmountDisk /dev/disk12
```

**2. 使用 dd 写入 ISO（使用 `rdisk12` 可大幅提高写入速度）：**

```bash
sudo dd if=/Users/lzwjava/Downloads/debian-live-13.6.0-amd64-xfce.iso of=/dev/rdisk12 bs=4m status=progress
```

**3. 完成后安全弹出：**

```bash
diskutil eject /dev/disk12
```

说明：

- 使用 `of=/dev/rdisk12`（而非 `disk12s1`）——写入整个磁盘，raw设备速度更快。
- `status=progress` 显示传输进度（适用于较新的macOS）。
- 由于使用了 `sudo`，系统会提示你输入密码。

需要我帮你运行卸载和 dd 吗？
