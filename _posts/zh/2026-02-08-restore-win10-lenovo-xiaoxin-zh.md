---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-haiku
title: 在联想小新上还原 Windows 10
translated: true
type: note
---

如果您在 Lenovo Xiaoxin 上安装了 Ubuntu 并想换回 Windows 10，以下是您的主要选择：

**选项 1：Dual Boot（保留两个系统）**
如果您想在机器上同时保留 Windows 10 和 Ubuntu，可以使用 bootloader 在它们之间切换。当您重启电脑时，应该会看到一个启动菜单（通常是 GRUB），让您选择加载哪个 OS。如果您想保留两个系统，这是最简单的方法。

**选项 2：重新安装 Windows 10（擦除 Ubuntu）**
如果您想让 Windows 10 成为唯一的 OS，您需要：
1. 首先备份 Ubuntu 中的所有重要文件
2. 在另一台电脑上使用 Windows Media Creation Tool（可从 Microsoft 下载）制作一个 Windows 10 安装 USB 驱动器
3. 从该 USB 驱动器启动并重新安装 Windows 10，这将覆盖 Ubuntu
4. 在安装过程中，您可以格式化硬盘以完全删除 Ubuntu 分区

**选项 3：使用原始 Recovery Partition**
Lenovo 笔记本电脑通常带有 recovery partition 或 recovery media。检查您是否有：
- Lenovo Vantage 应用（如果 Windows 仍然可以访问）
- 笔记本电脑附带的原始恢复 DVD 或 USB
- 硬盘上的隐藏 recovery partition

如果您有这些，您可能无需安装盘即可将 Windows 10 恢复到出厂设置。

**您需要准备：**
- Windows 10 安装介质或 recovery media
- 另一台用于制作安装 USB 的电脑
- 安装过程所需的时间

哪种方案最适合您的需求？