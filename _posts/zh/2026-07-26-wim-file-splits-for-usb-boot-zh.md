---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WIM文件拆分为USB启动
translated: true
type: note
---

## 分析完成 — 整体情况如下

### ✅ 已发现的内容

| 项目 | 状态 |
| --- | --- |
| **ISO 文件** | ✅ 位于 `/Users/lzwjava/Downloads/Win11_25H2_English_x64_v2.iso` — **7.9 GB** |
| **ISO 内容** | ✅ 标准 Windows 11 DVD 布局 — `boot/`, `efi/`, `sources/`, `setup.exe` |
| **`install.wim`** | ⚠️ **7.1 GB** — 超过 FAT32 的 **4 GB 文件大小限制** |
| **USB 驱动器** (`/dev/disk13`) | ✅ **15.7 GB** — 已检测到，但 **无分区表，无文件系统**（"内容：无"） |
| **`wimlib`** | ✅ 已安装于 `/opt/homebrew/bin/wimlib-imagex` |

### 🔍 Etcher 报错的根本原因

USB 驱动器 (`/dev/disk13`) 完全是一块裸盘 — **无 MBR，无 GPT，无文件系统**。当 Etcher 检查 Windows ISO 时，它会看到：

- **ISO 格式**（ISO9660/UDF）— **不是带有分区表的混合磁盘映像**
- Windows ISO 是 **DVD 映像**，而非 Ubuntu/Raspberry Pi ISO 那样的原始磁盘映像
- Etcher 期望映像内部包含 `GPT/MBR → 分区 → 文件系统`

因此 Etcher 提示 *"缺少分区表"* — 这个说法没错，但真正的问题在于 Etcher 不适合此任务。

### 🚨 真正的问题

即使格式化 USB，`install.wim` 大小为 **7.1 GB** — FAT32 单文件上限为 4 GB。你**必须**将其拆分为 `.swm` 文件。

### ✅ 建议操作：`wimlib` 方法

你回答中的步骤是正确的。既然一切已就绪：

1. **格式化 USB** 为 FAT32（GPT）
2. **复制所有 ISO 文件**，除 `install.wim` 外
3. **拆分 `install.wim`** 为 `install.swm`、`install2.swm`、`install3.swm`
4. **弹出**两个驱动器

---

**现在要执行完整设置吗？** 我将：

1. `diskutil eraseDisk MS-DOS WIN11 GPT /dev/disk13` — 格式化 USB
2. `cp -av` 复制文件
3. `rm /Volumes/WIN11/sources/install.wim`
4. `wimlib-imagex split` 拆分为 3800 MB 的分块

完成后，USB 将能在你的 **Lenovo Xiaoxin UEFI 笔记本电脑**上完美启动。
