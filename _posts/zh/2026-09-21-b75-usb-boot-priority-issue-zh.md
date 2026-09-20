---
audio: false
generated: true
image: false
lang: zh
layout: post
title: B75 USB启动优先级问题
translated: true
type: note
---

USB 现在已拔出（所以你把它移到了 B75 电脑上）。"一直启动 Ubuntu" = B75 跳过了 USB。这是启动优先级/启动模式的问题，不是 USB 坏了。按顺序修复如下：

## 1. 确认你正在哪台机器上操作

该 USB 是为 **B75 PC** 制作的，不是这台 MSI B760M 机器。请确保你在 B75 板上启动它。

## 2. 使用启动菜单键（先试这个——最快）

开机后（从按下电源键那一刻起）**反复按**以下某个键：

- **F11** —— 大多数通用 AMI 主板上的常见键（你的 B75 BIOS 是 AMI Aptio）
- **F12**、**F8**、**Esc**、**F9**、**F7** —— 其他常见键

你应该会看到“请选择启动设备”列表。选择 USB 对应的条目。寻找**前面没有“UEFI:”**的条目（例如 `USB HDD: ...`，而不是 `UEFI: USB`）。

## 3. 进入 BIOS 设置（开机时按 **Del** 或 **F2**）

如果启动菜单没用，进入设置并检查以下选项（这些通常是 B75/AMI 上的常见原因）：

1. **禁用“Fast Boot”/“Quick Boot”** —— 如果启用，BIOS 会跳过 USB 初始化，导致 USB 无法启动。
2. **启用“Legacy USB Support”**（在 Advanced → USB Configuration 中）。
3. **Boot Mode / CSM** —— 设置为 **Legacy**（或“Legacy + UEFI”）。FreeDOS USB 仅支持传统模式；如果主板处于纯 UEFI 模式，它将被忽略。
4. **启动优先级**（Boot 标签）：
   - 将 **Boot Option #1 设为 USB** 或 **USB HDD**
   - 同时检查 **“Hard Disk Drive BBS Priorities”** —— USB 经常在这里作为“硬盘”出现，你需要把它移到 #1。
5. 保存并退出（**F10**）。

## 4. 使用 USB 2.0 端口（黑色）

旧主板通常无法从 **蓝色 USB 3.0** 端口启动。请插入后 I/O 面板上的 **黑色 USB 2.0** 端口。

---

有两个问题可以快速缩小范围：

1. 你是在 **B75 PC** 上测试，还是在这台 MSI 机器上（只是试一下）？
2. 当你开机 B75 时，启动画面显示什么（是否有“按 Fxx 进入启动菜单”的提示，以及 BIOS 品牌是什么）？

如果你能告诉我屏幕上显示的启动菜单键，或者发一张 BIOS **Boot** 标签的照片，我可以直接指出需要更改的具体设置。