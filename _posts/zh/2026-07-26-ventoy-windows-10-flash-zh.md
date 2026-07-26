---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ventoy Windows 10 启动盘
translated: true
type: note
---

## ✅ 完成 — 通过 Ventoy 刷入 Windows 10

### 操作过程

| 步骤 | 操作 | 耗时 |
|---|---|---|
| 1 | 卸载旧的 FAT32 分区 | 瞬间 |
| 2 | 将 **Ventoy v1.1.17** 安装到 `/dev/sdb`（擦除并重新分区） | 约15秒 |
| 3 | **复制** `Win10_22H2_English_x64v1.iso`（5.8G）到 Ventoy 分区 | 约2分钟 |
| 4 | 同步、卸载、关机 | 瞬间 |

### 最终 USB 布局

| 分区 | 大小 | 文件系统 | 标签 | 内容 |
|---|---|---|---|---|
| `/dev/sdb1` | 14.6G | **exFAT** | `Ventoy` | `Win10_22H2_English_x64v1.iso` (5.8G) |
| `/dev/sdb2` | 32M | **vfat** | `VTOYEFI` | Ventoy EFI 引导加载程序 |

### USB 现在有 2 个 ISO

由于你之前复制了 Windows 11 ISO……等等——那是在 **旧** USB 上，后来它被重新分区为 `DISK_IMG`。这是一个全新的 Ventoy 安装，仅包含：

- **Windows 10 22H2** (5.8G) ← 刚刚添加

如果你也想在这里放 Windows 11：

```bash
sudo mount /dev/sdb1 /mnt
sudo cp ~/Downloads/Win11_25H2_English_x64_v2.iso /mnt/
sync; sudo umount /mnt
```

两个 ISO 文件都会在启动时的 Ventoy 引导菜单中显示。**安全拔出。**