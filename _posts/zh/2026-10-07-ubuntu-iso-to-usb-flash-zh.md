---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu ISO 写入 U 盘
translated: true
type: note
---

全部确认：

- **ISO**：`/Users/lzwjava/Downloads/ubuntu-26.04.1-desktop-amd64.iso`（6.0G）✓
- **USB**：`/dev/disk12` — “OnlyDisk”，15.7 GB，外部，当前**未挂载** ✓

运行以下命令：

```bash
# 1. 卸载以防万一有自动挂载（目前 disk12 未挂载，这步只是保险）
diskutil unmountDisk /dev/disk12

# 2. 写入 ISO（使用原始设备 /dev/rdisk12；原始 dd 写入时不会有挂载干扰）
sudo dd if=/Users/lzwjava/Downloads/ubuntu-26.04.1-desktop-amd64.iso of=/dev/rdisk12 bs=4m conv=sync

# 3. 刷新缓冲区并弹出
sync && diskutil eject /dev/disk12
```

注意事项：

- 在 macOS 上，优先使用 `/dev/rdisk12`（原始设备）而不是 `/dev/disk12`，以避免写入缓存带来的意外；ISO 为 6.0G，U 盘为 15.7G，容量足够。
- `dd` 在完成前不会输出任何内容 — 在终端按 **Ctrl+T** 查看进度，或使用 `pv /Users/lzwjava/Downloads/ubuntu-26.04.1-desktop-amd64.iso | sudo dd of=/dev/rdisk12 bs=4m` 显示进度条（如果已安装 `pv`）。
- ⚠️ 这是破坏性操作 — `/dev/disk12` 上的所有内容都将被覆盖。使用 `diskutil list external` 确认是正确的 U 盘（只有 `disk12` 显示为外部/物理设备；其他磁盘是镜像/虚拟机设备）。
