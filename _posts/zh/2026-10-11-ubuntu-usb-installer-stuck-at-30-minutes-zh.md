---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu USB 安装程序卡在30分钟
translated: true
type: note
---

问题：你的 Ubuntu USB 启动/安装盘已插入，进度条已运行约 30 分钟。发生了什么？

答案：**30 分钟异常漫长**，如果进度条确实卡住的话。最可能发生以下情况之一：

1. **USB 驱动器速度极慢或已损坏**

   * 老旧/廉价的 USB 闪存盘持续写入速度可能非常糟糕。
   * 损坏的闪存盘可能表面上有进展，随后停滞。

2. **Ubuntu 正在验证/写入 USB**

   * 如果你正在*创建* Ubuntu 启动 USB，工具可能正在写入 ISO 文件并进行验证。
   * 正常的 USB 通常应在几分钟内完成，而非半小时。

3. **USB 端口或控制器存在问题**

   * 尝试另一个 USB 端口，最好是主板后置 I/O 端口。
   * 避免使用 USB 集线器。

4. **如果你已经正在从 USB 启动 Ubuntu**

   * 长时间停顿可能是由硬件初始化、GPU 驱动或文件系统错误引起的。
   * 按 `Esc` 键查看 Ubuntu 是否在图形化进度屏幕下隐藏了启动信息。

### 如果你当前正在创建 Ubuntu USB

在另一台 Linux 机器上，我会检查：

```bash
lsblk
sudo dmesg -w
```

然后插入 USB，观察类似以下错误：

```text
I/O error
Buffer I/O error
device descriptor read error
reset SuperSpeed USB device
```

如果你在使用 `dd` 且它看起来卡住了，可以通过以下命令检查进度：

```bash
sudo kill -USR1 $(pgrep '^dd$')
```

你会得到类似这样的输出：

```text
2147483648 bytes copied, 120 s, 17.9 MB/s
```

**不要在 `dd` 仍在写入时拔掉它。**

如果你告诉我**具体是哪个界面显示进度条**（Ubuntu 安装器、Rufus、启动盘创建器、Ventoy 或 Ubuntu 启动屏幕），我可以更精确地告诉你发生了什么。