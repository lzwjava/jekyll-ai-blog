---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重启后查找设置日志
translated: true
type: note
---

问题：重启后 setupact.log 不见了——还能在哪里找到失败日志？

回答：没错——那个日志存在于临时的 WinPE RAM 磁盘（`X:`）上，每次重新启动进入新的安装会话时都会被清空。但安装程序通常会在失败前将日志复制到目标驱动器上。请改到以下位置查看：

```cmd
Shift + F10
notepad C:\$WINDOWS.~BT\Sources\Panther\setupact.log
```

如果该路径不存在，请尝试：
```cmd
dir C:\$WINDOWS.~BT\Sources\Panther\
```
查看实际写入的日志文件，然后打开其中存在的 `setup*.log` 文件。

如果 `C:\$WINDOWS.~BT` 完全不存在（意味着安装程序本次甚至还没进行到这一步就失败了），直接检查当前 C 盘的内容：
```cmd
dir C:\
```

考虑到这已经是一个重复出现的通用失败，且没有明确的磁盘相关原因，说实话，到此为止我建议跳过进一步翻日志，直接**排除 USB 介质**的问题，因为这是最可能的剩余原因：

1. 从微软官方页面重新下载 Windows 11 ISO（全新副本）。
2. 使用 **Rufus** 重新写入：GPT 分区方案 + UEFI 目标。
3. 如果有的话，换一个不同的 U 盘，插入笔记本电脑后置的 USB 端口（不要用集线器）。

当磁盘/分区方面已经确认干净（你的情况现在就是这样）时，上述组合——损坏的 ISO、错误的 U 盘写入或故障的驱动器——是导致“通用安装失败”对话框的绝大多数原因。