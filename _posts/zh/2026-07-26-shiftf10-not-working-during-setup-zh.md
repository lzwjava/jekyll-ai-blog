---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Shift+F10在安装过程中无效
translated: true
type: note
---

**问题：** Shift+F10 没反应 —— 如何打开命令提示符？

**回答：** 先点击那个错误对话框上的 **确定** —— 安装程序会回退，并再次将你带到“选择要安装 Windows 的位置”屏幕。Shift+F10 只在焦点处于实际的安装程序屏幕时有效，而当这个模态错误框弹出时则无效。

回到分区屏幕后：
1. 再次按下 `Shift + F10` —— 应该会打开 cmd。
2. 如果仍然没有响应，请确保你在 **笔记本电脑的物理键盘** 上同时按下这两个键（不要通过远程/KVM/虚拟键盘，因为 Shift+F10 有时无法通过这些方式传递）。
3. 如果确实没反应，尝试 `Shift + Fn + F10` —— 在联想笔记本上，F 功能键通常默认为媒体/功能模式，因此你可能需要按 Fn 键才能真正触发 F10 信号。

cmd 打开后，运行：
```cmd
notepad X:\Windows\Panther\setupact.log
```
（驱动器号可能是 X: 或其他字母 —— 如果 X: 无效，请运行 `wpeutil` 或直接检查 `dir C:\`、`dir D:\` 等来找到 Windows PE / 安装驱动器）

滚动到最底部，找到最后一行带 `Error` 的内容，并将其粘贴到这里。