---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 云虚拟机紧急恢复控制台
translated: true
type: note
---

**问题：** 在 AMD Developer Cloud / DigitalOcean 实例管理界面中，“Recovery Console”是什么意思？

**答案：**

这是标准的云虚拟机紧急访问工具。以下是对各项功能的说明：

**Recovery Console（恢复控制台）**
一种基于浏览器的串行/VNC 控制台，直接连接到虚拟机的虚拟显示输出——完全绕过 SSH。相当于物理上坐在服务器前。在以下情况下使用：

- SSH 无法工作（sshd 配置错误、防火墙阻止登录、密钥错误）
- 网络堆栈配置错误
- 虚拟机陷入启动循环或内核恐慌
- 需要运行 `fsck`、编辑 `/etc/fstab` 或修复 GRUB

**Recovery ISO（恢复 ISO）**
将实例启动到一个临时救援操作系统（最小化 Linux），而非你安装的系统。你原有的磁盘会被挂载到 `/mnt` 或类似路径。在以下情况下使用：

- 操作系统本身无法启动
- 需要 `chroot` 进入并修复损坏的系统
- 文件系统损坏，需要从外部修复

**Password Authentication（密码认证）**
SSH 通常使用密钥认证。恢复控制台需要密码（因为你无法通过浏览器串行终端传递 SSH 密钥）。因此，你需要设置或启用 root 密码登录才能使用此控制台。

**Reset Root Password（重置 root 密码）**
通过虚拟机管理程序（cloud-init 或类似机制）注入新 root 密码，即使你无法登录。这是在你完全失去访问权限时的逃生出口。

---

**对你情况的简要总结：**

如果你的 AMD Dev Cloud 实例无法通过 SSH 访问：

1. 启动 Recovery Console → 浏览器终端，无需 SSH
2. 修复问题（sshd、防火墙、网络等）
3. 或者启动 Recovery ISO → 挂载磁盘 → `chroot` → 修复

这相当于裸机上的 IPMI/iDRAC/iLO——一种在操作系统损坏时仍可使用的带外访问。
