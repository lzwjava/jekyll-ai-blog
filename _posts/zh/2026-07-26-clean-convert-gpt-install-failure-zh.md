---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Clean Convert GPT安装失败
translated: true
type: note
---

问题：执行 clean/convert gpt 并让安装程序自动创建分区后，Windows 11 安装失败——需要实际错误信息才能诊断。

回答：仅凭“安装失败”不足以确定原因——安装程序失败时会给出特定的错误代码或信息（通常发生在“正在复制文件”阶段或首次重启后）。针对联想小新 + 全新 clean/convert 操作的常见错误包括：

- **“Windows 无法安装到此磁盘。选中的磁盘具有 MBR 分区表...”** → 你已转换为 GPT，但 BIOS 仍处于 Legacy/CSM 引导模式而非 UEFI。解决方法：进入 BIOS (`F2`)，将 **Boot Mode 设置为 UEFI**（非 Legacy），如有必要请关闭 CSM/安全启动兼容模式。
- **“我们无法创建新分区或找到现有分区... 0x80300001”** → USB 启动介质未被识别为 UEFI，或缺少存储驱动程序。请使用 Rufus 以 **GPT + UEFI** 模式重新制作 Windows 11 USB 启动盘。
- **文件复制期间出错，然后重启再次失败** → USB 介质损坏（写入错误）或 ISO 镜像损坏。请重新下载 ISO 并重新制作 USB 启动盘。
- **首次自动重启后卡住或失败** → BIOS 启动顺序仍指向 USB 而非内部磁盘上的新 Windows 分区——请进入 BIOS 将 NVMe/SSD 设为第一启动设备（或拔掉 USB，安装应能继续）。

能否告诉我：
1. 确切的错误信息/代码（有照片更佳）
2. 失败发生在哪个阶段——是文件复制期间，还是重启之后

这样我就能准确判断属于上述哪种情况。