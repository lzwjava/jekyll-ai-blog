---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS 下 Ubuntu USB 闪存盘制作说明
translated: true
type: note
---

### 状态：⚠️ 当前未连接任何 USB 驱动器

- ✅ 已找到 ISO：`ubuntu-26.04-desktop-amd64.iso`（6.1 GB）
- ❌ 唯一物理磁盘是 **disk0（内部 500 GB SSD）**。所有“外部”条目均为虚拟磁盘映像（iOS 模拟器），**并非真实的 USB 驱动器**。

**请插入 U 盘，然后运行 `diskutil list`**，查找类似 `/dev/disk2 (external, physical)` 的新条目。

---

### `dd` 命令（macOS）

假设你的 U 盘显示为 `/dev/disk2` **且容量 ≥ 8 GB**：

```bash
# 1. 确认磁盘（确保它是 U 盘，不是 disk0！）
diskutil list

# 2. 卸载该磁盘（不要弹出）
diskutil unmountDisk /dev/disk2

# 3. 写入 ISO（使用原始设备 /dev/rdiskX）
sudo dd if=~/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk2 bs=4m status=progress conv=fsync
```

---

### ⚠️ 关键警告

1. **仔细核对磁盘编号** — `of=/dev/rdisk0` 会覆写系统 SSD，导致设备无法启动。
2. U 盘容量必须 **≥ 8 GB**（ISO 为 6.1 GB）。
3. 如果遇到 `Resource busy`，请确认步骤 2 已成功执行：`diskutil unmountDisk /dev/disk2`。
4. `conv=fsync` 确保数据在拔出 U 盘前完全写入。

写入完成后，可使用以下命令验证：

```bash
diskutil eject /dev/disk2
```

插入 U 盘后告诉我它分配的磁盘编号，我来为你执行操作。