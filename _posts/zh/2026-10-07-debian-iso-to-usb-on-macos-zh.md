---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 macOS 上将 Debian ISO 写入 USB
translated: true
type: note
---

您的 ISO 已确认：`debian-13.7.0-amd64-netinst.iso`（756 MB），我找到了您的 USB 闪存盘：**/dev/disk12**（4 GB，USB，标签为 EAGET）。

**⚠️ 请再次确认这是正确的 U 盘——dd 会毫无警告地擦除其上的所有数据。**

在 macOS 上，运行：

```bash
# 1. 卸载 USB（如果已卸载，请忽略错误）
sudo diskutil unmountDisk /dev/disk12

# 2. 将 ISO 写入原始设备（注意 rdisk12 中的 "r"）
sudo dd if=/Users/lzwjava/Downloads/debian-13.7.0-amd64-netinst.iso of=/dev/rdisk12 bs=4m status=progress conv=fsync

# 3. 完成后弹出
sudo diskutil eject /dev/disk12
```

关键点：
- `of=/dev/rdisk12`（原始设备）——**切勿**写入 `/dev/disk12`（逻辑设备），否则 macOS 可能无法正确刷新数据。
- `conv=fsync` 可确保在 dd 退出前所有数据都已刷新到 U 盘。
- `bs=4m` 可加快速度；整个写入过程应在一分钟内完成。
- `status=progress` 标志会显示实时进度（GNU dd / 较新版本的 macOS dd）。如果报错 "invalid status"，请去掉该参数，并在另一个终端中运行 `pkill -USR1 -n -x dd` 查看进度。

如果希望在步骤 2 之前格外谨慎，请确认目标确实是该 U 盘：`diskutil info /dev/disk12` 应显示与您的 U 盘相同的大小（4 GB）。