---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复cd命令以在cmd中切换驱动器
translated: true
type: note
---

问题：在 Windows cmd 中，`cd E:\` 只会打印出 `E:\`，但不会实际切换当前驱动器/目录——如何解决？

答案：在 cmd.exe 中，仅使用 `cd` 无法切换驱动器——它只能改变当前驱动器*内部*的目录。要同时切换驱动器，请使用 `/d`：

```cmd
cd /d E:\
```

或者两步法（这是经典技巧）：

```cmd
E:
cd \
```

原因：cmd 会为每个驱动器字母单独记录一个“当前目录”。`cd E:\` 设置了 E 盘的当前目录，但因为你仍在 C 盘，所以视觉上没有变化——这就是为什么它只是把 `E:\` 回显给你（实际上，`cd` 后面只跟了驱动器字母而没有目录参数，相当于确认）。`cd /d` 强制同时切换驱动器并改变目录。

参考文献：

- [CD command - Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cd)
