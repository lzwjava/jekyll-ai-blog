---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 清理转换GPT并重装Windows
translated: true
type: note
---

问题：现在在命令提示符中（通过“修复你的电脑”）——接下来该做什么？

回答：运行 diskpart 并重新执行 clean/convert 操作，和之前一样：

```cmd
diskpart
list disk
```

确认哪个磁盘是你的主 SSD（大约 476GB 的那个）。

```cmd
select disk 0
detail disk
```

检查它显示的是 **分区样式：MBR** 还是 **GPT**，并确认这是正确的磁盘（不是那个小的 14GB 磁盘 1）。

```cmd
clean
convert gpt
exit
```

关闭命令提示符窗口，返回主修复/设置菜单，然后再次从 **Windows 11 安装 U 盘**启动（不是修复——你需要实际的设置流程来选择安装位置）。接着：

1. 进入“选择要安装 Windows 11 的位置”
2. 点击 **刷新**
3. 选择现在未分配的磁盘 0
4. 点击 **下一步**——让它自动创建分区

然后立即在再次点击下一步之前检查分区列表——确认 **EFI 系统分区**与 MSR/主分区/恢复分区一起出现。这就是上次缺失并导致启动失败的东西。
