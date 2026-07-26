---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ventoy Windows 11 USB 方案
translated: true
type: note
---

一切就绪。以下是完整的分步计划：

---

## 完整计划：Ventoy v1.1.17 → Windows 11 USB

### 当前状态

| 项目 | 详情 |
| --- | --- |
| **USB 设备** | `/dev/sdb`（14.6G） |
| **ISO** | `~/Downloads/Win11_25H2_English_x64_v2.iso`（7.9G） |
| **Ventoy** | `/tmp/ventoy-1.1.17/`（已解压） |
| **USB 分区** | 已卸载 ✅ |

### ⚠️ 这将擦除 `/dev/sdb` 上的所有内容

当前的 EFI/WIN11 分区将被销毁。

### 步骤（按顺序）

| 步骤 | 命令 |
| --- | --- |
| **1. 安装 Ventoy** | `sudo /tmp/ventoy-1.1.17/Ventoy2Disk.sh -i /dev/sdb` |
| **2. 确认** | 当提示时输入 `y` |
| **3. 等待完成** | 约 10 秒 |
| **4. 复制 ISO** | `cp ~/Downloads/Win11_25H2_English_x64_v2.iso /media/$USER/Ventoy/` |
| **5. 验证** | `ls /media/$USER/Ventoy/` → 应显示 `.iso` 文件 |
| **6. 同步并弹出** | `sync && sudo umount /media/$USER/Ventoy` |

### 步骤 4 之后 — Ventoy 功能解锁

- ✅ **无 4GB FAT32 限制** — Ventoy 使用 `exFAT`，因此 `install.wim` 原生适配
- ✅ **多 ISO** — 可添加更多 ISO（Linux、救援盘等）
- ✅ **持久化** — 支持为 Linux ISO 提供持久存储
- ✅ **Legacy + UEFI** — 同时兼容两种 BIOS 模式

### 特别针对联想小新

从 USB 启动后 → Ventoy 菜单 → 选择 ISO → 如果安装程序未检测到 SSD，请在磁盘选择界面 **加载 Intel RST/VMD 驱动**。

---

**是否继续执行步骤 1（将 Ventoy 安装到 `/dev/sdb`）？** 这将 **擦除当前 USB 数据**。
