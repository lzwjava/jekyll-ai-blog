---
audio: false
generated: true
image: false
lang: zh
layout: post
title: USB验证，修复BIOS VMD
translated: true
type: note
---

## 分析完成

好消息——**你的 USB 已经正确制作完成**。以下是发现的内容：

### ✅ USB 有效（`/dev/disk12` — 15.7 GB）

| 所需文件 | 状态 | 大小 |
| --- | --- | --- |
| `sources/boot.wim` | ✅ **存在** | 586 MB |
| `sources/install.wim` | ❌ 缺失（预期应 >4GB） | 原大小 7.1 GB |
| `sources/install.swm` | ✅ **存在** | 3.2 GB（第 1 部分） |
| `sources/install2.swm` | ✅ **存在** | 3.7 GB（第 2 部分） |
| `sources/install3.swm` | ✅ **存在** | 79 MB（第 3 部分） |
| `boot/`, `efi/`, `setup.exe` | ✅ **全部存在** | |

一切正常。`boot.wim` 已就位。`install.wim` 被正确分割为 3 个 `.swm` 文件，Windows 安装程序原生支持处理。

### 🎯 真正的问题（并非 USB 问题）

由于 USB 没问题，**重新制作它无法解决 `0xC19001F4` 错误**。问题几乎肯定出在 **联想小新 BIOS 设置** 上：

> BIOS 中启用了 **Intel VMD Controller** 或 **Intel RST**

当 VMD 开启时：

1. Windows PE 能看到 NVMe（安装程序开始复制文件）
2. 第一次重启后，Windows 尝试使用内置的 `stornvme.sys` 从 NVMe 启动
3. 该驱动程序无法通过 VMD 控制器通信 → 硬盘消失
4. Windows 触发恢复 → 安装程序检测到 → 以 `0xC19001F4` 中止

### 步骤 1 — 先修复 BIOS（2 分钟）

在进行其他操作前，重启小新 → 按 **`F2`** → 查找：

| 需要找到的设置 | 更改为 |
| --- | --- |
| **Intel VMD Controller** | **Disabled** |
| **Intel RST / Optane** | **AHCI** |
| **SATA Mode** | **AHCI**（非 RST/Optane） |

保存并退出。然后使用 **同一 USB** 重新尝试安装——应该能成功。

想在重新制作 ISO 之前先试试这个吗？
