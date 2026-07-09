---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu截图快捷键指南
translated: true
type: note
---

**问题：** 如何在 Ubuntu 中截图？我想找与 macOS 快捷键 `⌘ + Ctrl + 4` 或 `⌘ + 5` 等效的操作。

**回答：**

在现代 Ubuntu（GNOME）上，截图快捷键与 macOS 非常相似。

| 操作                           | Ubuntu                        | macOS                                      |
| ------------------------------ | ----------------------------- | ------------------------------------------ |
| 全屏截图                       | `PrtSc`                       | `⌘ + Shift + 3`                            |
| 选择区域截图                   | `Shift + PrtSc`               | `⌘ + Shift + 4`                            |
| 当前窗口截图                   | `Alt + PrtSc`                 | `⌘ + Shift + 4`，然后按空格键              |
| 截图界面（录制/截图）          | `PrtSc`（Ubuntu 22.04+）      | `⌘ + Shift + 5`                            |
| 复制到剪贴板                   | 按住 `Ctrl` 再加任意快捷键    | 按住 `Ctrl` 再加 macOS 截图快捷键          |

### 最常用的快捷键

```text
PrtSc
```

打开 Ubuntu 的截图界面（类似 macOS 的 `⌘ + Shift + 5`），你可以：

* 截取整个屏幕
* 截取一个窗口
* 截取选定区域
* 开始屏幕录制（Ubuntu 22.04+）

---

```text
Shift + PrtSc
```

选择一个矩形区域进行截图。

相当于 macOS 中的：

```text
⌘ + Shift + 4
```

---

```text
Alt + PrtSc
```

仅截取当前活动窗口。

---

```text
Ctrl + Shift + PrtSc
```

将选定区域截图**复制到剪贴板**，而不是保存。

相当于 macOS 中的：

```text
⌘ + Ctrl + Shift + 4
```

同样地：

* `Ctrl + PrtSc` → 全屏截图到剪贴板
* `Ctrl + Alt + PrtSc` → 活动窗口截图到剪贴板

### 截图保存位置

默认情况下：

```text
~/Pictures/Screenshots/
```

（在较旧的 Ubuntu 版本中，有时直接保存在 `~/Pictures` 中）。

### 命令行截图

如果你更喜欢终端：

```bash
gnome-screenshot
```

截取区域：

```bash
gnome-screenshot -a
```

截取活动窗口：

```bash
gnome-screenshot -w
```

延迟 5 秒：

```bash
gnome-screenshot -d 5
```

### 如果你使用的是笔记本电脑

许多笔记本电脑需要按住 **Fn** 键，因为 `PrtSc` 与其他键共用：

```text
Fn + PrtSc
```

或

```text
Fn + Shift + PrtSc
```

具体取决于键盘布局。

**参考文档：**

* Ubuntu GNOME 截图文档：[https://help.gnome.org/users/gnome-help/stable/screen-shot-record.html](https://help.gnome.org/users/gnome-help/stable/screen-shot-record.html)
* Ubuntu 桌面指南：[https://help.ubuntu.com/stable/ubuntu-help/screen-shot-record.html](https://help.ubuntu.com/stable/ubuntu-help/screen-shot-record.html)