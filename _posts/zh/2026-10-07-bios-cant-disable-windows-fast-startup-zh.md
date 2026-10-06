---
audio: false
generated: true
image: false
lang: zh
layout: post
title: BIOS无法禁用Windows快速启动
translated: true
type: note
---

**问题：** 如何从BIOS而不是从Windows内部禁用Fast Startup/Hibernate？

**答案：**

你**无法直接从BIOS禁用Windows Fast Startup**——这是一个Windows操作系统设置。然而，你可以通过BIOS以以下方式达到同样的效果：

---

**选项1：禁用Secure Boot（有帮助的BIOS设置）**
1. 重启 → 按`Del`、`F2`或`F12`（取决于主板）进入BIOS
2. 进入**Boot**或**Security**选项卡
3. 找到**Secure Boot** → 设置为**Disabled**
4. 保存并退出（`F10`）

---

**选项2：通过BIOS行为强制正常关机**
- 在BIOS中找到**"Fast Boot"**（不同于Windows Fast Startup）
- 将其设置为**Disabled**
- 这会在每次启动时强制进行完整的POST检查，有助于确保磁盘状态干净

---

**真正的解决方案——你必须在Windows中执行此操作：**

由于你仍然可以看到启动信息，Kali **实际上正在启动**。所以：

1. 在Kali登录屏幕，打开终端
2. 运行：
```bash
sudo fsck -y /dev/sdb4
```
3. 重启

**或者** —— 在不进入Windows的情况下强制Windows关机：
- 在Windows启动菜单中，按住**Shift**点击关机
- 这会绕过Fast Startup并完全关机

---

**要点：** BIOS "Fast Boot" ≠ Windows "Fast Startup"。你需要在Windows端修复它，或者直接从Kali运行`fsck`。

---

**参考：**
- [Windows Fast Startup 与 BIOS Fast Boot 的区别解释](https://www.howtogeek.com/243901/the-difference-between-fast-startup-hibernate-and-sleep-in-windows-10/)
- [fsck 手册页面](https://man7.org/linux/man-pages/man8/fsck.8.html)