---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows 11 FAT32 USB 安装
translated: true
type: note
---

## ✅ 完成！以下是总结

### 已完成的操作

| 步骤 | 状态 |
| --- | --- |
| **1. 格式化 USB**（`MS-DOS FAT32` + `GPT`） | ✅ 完成 |
| **2. 复制所有 ISO 文件**（除 `install.wim` 外） | ✅ 完成 |
| **3. 拆分 `install.wim`**（7.1 GB → 3 个 FAT32 友好的块） | ✅ 完成 |

### 最终 USB 结构

```
/Volumes/WIN11/
 ├── autorun.inf
 ├── boot/              ← Windows 启动管理器
 ├── bootmgfw.efi       ← UEFI 启动加载器
 ├── bootmgr / bootmgr.efi
 ├── efi/               ← EFI 启动文件
 ├── setup.exe
 ├── sources/
 │    ├── install.swm   ← 3.2 GB（第 1 部分）
 │    ├── install2.swm  ← 3.7 GB（第 2 部分）
 │    ├── install3.swm  ← 79 MB（第 3 部分）
 │    └── ... （所有其他源文件）
 └── support/
```

**使用了 7.9 GB / 总共 14 GB** — 还有剩余空间。

### 使用方法

1. **安全弹出 USB** 从 Finder（或 `diskutil eject /dev/disk13`）
2. **将其插入您的 Lenovo Xiaoxin**
3. **启动** → 按 `F2` / `F12`（或 `Fn+F2`）→ 选择 USB 作为启动设备
4. Windows 11 25H2 安装程序将自动加载 — 它原生识别 `.swm` 文件

无需 Etcher。没有"缺少分区表"错误。这是官方微软兼容的 UEFI 启动方法。
