---
audio: false
generated: true
image: false
lang: zh
layout: post
title: U盘报告无介质
translated: true
type: note
---

我检查了连接的存储设备。以下是我的发现：

## USB 磁盘状态

**有**一个 USB 设备已连接，但它显示为**空/不可读**：

| 属性 | 值 |
|---|---|
| 设备 | `/dev/sdb` |
| 厂商 / 型号 | NAND / USB2DISK |
| 接口 | USB |
| 可移动 | 是 |
| 大小 | **0 字节** |
| 分区表 | 无 |
| 文件系统 | 无 |

内核报告 `/dev/sdb` **"未找到介质"**：

```
fdisk: cannot open /dev/sdb: No medium found
Error: Error opening /dev/sdb: No medium found
```

这通常意味着以下情况之一：
1. USB 驱动器是一个**未插入存储卡的读卡器**（"NAND" 厂商和 "USB2DISK" 型号常见于 SD/microSD 适配器）。
2. 驱动器是**空白/从未格式化**的——不过这种情况下它仍会报告一个大小。
3. 驱动器的闪存控制器**未响应**操作系统。

## 其他磁盘（供参考）

这些是系统的常规磁盘，不是 USB：

- **`/dev/sda1`** — 1.8 TB ext4，挂载在 `/mnt/data`（标签 `data`）——这是你当前项目所在的磁盘。
- **`/dev/nvme0n1`** — 931 GB NVMe SSD（系统根目录 + `/boot/efi`）。

## 我可以进一步检查的内容

由于 `/dev/sdb` 报告未找到介质，因此没有可读取的文件系统。如果你愿意，我可以：

1. **重新扫描设备**，看看它是否变得可读：
   ```bash
   echo 1 | sudo tee /sys/block/sdb/device/rescan
   ```
2. **检查是否有卡**——如果这是读卡器，请插入 SD/microSD 卡，我会重新检测它。
3. **用 `dmesg`/`udevadm` 检查原始设备**，获取关于介质未被检测到的更多诊断细节。

需要我尝试重新扫描或收集更多诊断信息吗？