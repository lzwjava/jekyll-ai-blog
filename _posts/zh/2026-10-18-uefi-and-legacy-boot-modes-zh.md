---
audio: false
generated: true
image: false
lang: zh
layout: post
title: UEFI与Legacy启动模式
translated: true
type: note
---

**问题：** 在计算机启动模式的上下文中，UEFI 和 Legacy（BIOS）是什么意思？

---

**答案：**

## Legacy（BIOS）

- 自 1980 年代以来计算机启动的**旧**方式
- 代表 **Basic Input/Output System**（基本输入/输出系统）
- 简单、有限——仅支持最大 **2 TB** 的硬盘
- 使用 **MBR**（主引导记录）分区样式
- 基于文本的界面，鼠标通常无法使用
- 启动速度较慢

## UEFI

- Legacy BIOS 的**现代**替代品
- 代表 **Unified Extensible Firmware Interface**（统一可扩展固件接口）
- 支持大于 **2 TB** 的驱动器
- 使用 **GPT**（GUID 分区表）分区样式
- 图形界面，鼠标可以使用
- **启动更快**（支持快速启动 / 安全启动）
- Windows 11 和现代 Linux 安装所需

---

## 简单类比

| | Legacy BIOS | UEFI |
| -- | ------------- | ------ |
| 类似于... | 老式翻盖手机 | 现代智能手机 |
| 速度 | 慢 | 快 |
| 磁盘大小限制 | 最大 2 TB | 9 ZB（实际上无限制） |
| 安全性 | 无 | Secure Boot ✓ |
| 界面 | 仅文本 | 图形化（鼠标可用） |

---

## 对于 Ubuntu，你应该使用哪一个？

✅ **使用 UEFI** — 这是现代 Dell 笔记本默认使用的模式，Ubuntu 在这种模式下安装效果最佳。

> 当你使用 Rufus 刷写 USB 驱动器时，请确保选择：
>
> - 分区方案：**GPT**
> - 目标系统：**UEFI（非 CSM）**

“CSM”（兼容性支持模块）是允许 Legacy 模式的选项——对于现代 Ubuntu 安装，**请将其关闭**。

---

**参考资料：**

- [UEFI vs Legacy BIOS – How-To Geek](https://www.howtogeek.com/56958/htg-explains-how-uefi-will-replace-the-bios/)
- [Ubuntu UEFI 安装指南](https://help.ubuntu.com/community/UEFI)
