---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 显卡BIOS刷写修复
translated: true
type: note
---

BIOS 文件在远程机器上，已验证（md5 `611b0eb7e20d4c489a0d9195352170df` 匹配，16MB）。

以下是刷写并完成 GPU 修复的计划：

## 第 1 步 — 将 BIOS 文件复制到 U 盘

**最简单的方式：** 将一个 **FAT32 格式的 U 盘** 插入 Debian 机器，然后告诉我。我会远程挂载它，将 `~/E7978IMS.AA0` 复制进去，然后安全卸载——全程远程操作。

（或者使用桌面文件管理器自行将 `E7978IMS.AA0` 复制到 U 盘。）

## 第 2 步 — 使用 M-Flash 刷写

1. 重启，连续按 **DEL** 进入 BIOS（Click BIOS 5）。
2. 点击 **M-FLASH**（底部按钮；或在高级模式下按 F7 → 位于左侧菜单 / “Utilities” 中）。
3. 系统将重启进入刷写模式。
4. 选择 **“Select one file to update BIOS”**。
5. 浏览到你的 U 盘 → 选择 **`E7978IMS.AA0`**。
6. 确认 **Yes**。⚠️ **刷写过程中切勿断电或重启**（大约需要 1–2 分钟）。
7. 系统会自动重启。

## 第 3 步 — 启用 “Above 4G Decoding”

刷写完成后，BIOS 设置将恢复为默认值。再次进入 BIOS（按 DEL）：

1. 按 **F7** 进入高级模式。
2. 进入 **Settings → Advanced → PCI Subsystem Settings**（或 “PCIe/PCI Subsystem”）。
3. **“Above 4G Decoding” → Enabled**。
4. **F10 → Save & Exit**。

## 第 4 步 — 验证

启动进入 Debian 后告诉我——我会检查 BAR 并运行 `nvidia-smi`。驱动程序（550.163.01）已安装并准备就绪。

---

⚠️ **重要提示：**
- BIOS 刷写存在一定风险。请确保电源稳定，不要中断刷写过程。
- 刷写后如果仍然找不到该选项，我们会一起检查确切的菜单路径——但 A.A 版本发布说明（“Support multi graphic cards”）表明该选项是存在的。

你手边有 U 盘吗？如果插入 Debian 机器，我会帮你把文件复制进去。