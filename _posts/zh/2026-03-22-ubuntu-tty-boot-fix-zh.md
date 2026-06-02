---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Ubuntu 启动到 TTY 错误
translated: true
type: note
---

好的，以下是我如何一步步诊断并修复你的“boots to TTY”问题：

## 🔍 诊断

**步骤 1 — 检查显示管理器状态**

```bash
systemctl status gdm3
```

这是第一个警示信号：它显示 `active (exited)` 而不是 `active (running)`。显示管理器应该持续运行——“exited”表示它启动后立即退出。

**步骤 2 — 验证没有 GNOME 进程实际在运行**

```bash
ps aux | grep -i gdm
ps aux | grep -i gnome-shell
```

两者都无输出。没有 GDM 二进制文件，没有 GNOME Shell——图形栈完全不存在。

**步骤 3 — 检查默认引导目标**

```bash
systemctl get-default
```

这显示 `graphical.target`，意味着 systemd *确实* 配置为引导到 GUI 模式。所以配置是正确的——问题是软件缺失。

**步骤 4 — 检查包是否实际已安装**

```bash
dpkg -l | grep -i gdm
```

这是关键证据：`rc  gdm3`。在 dpkg 语言中：

- **`r`** = 包已被**移除**（二进制文件已删除）
- **`c`** = **配置文件**仍存在于磁盘上

`gnome-shell` 也是同样的 `rc` 状态。

**步骤 5 — 确认二进制文件已丢失**

```bash
which gdm3
ls /usr/sbin/gdm3
```

二进制文件不存在。不过旧的 SysV init 脚本（`/etc/init.d/gdm3`）仍存在，这就是为什么 systemd 报告“started”——脚本运行，检查 `test -x /usr/sbin/gdm3`，未找到任何东西，然后静默退出 0。

**步骤 6 — 验证完整范围**

```bash
apt list --installed | grep gnome-shell  # nothing
apt-cache policy ubuntu-desktop          # "Installed: (none)"
apt-cache policy gdm3                    # "Installed: (none)"
apt-cache policy gnome-shell             # "Installed: (none)"
```

整个 GNOME 桌面栈——`ubuntu-desktop`、`gdm3`、`gnome-shell`、`gnome-session`、`gnome-settings-daemon`——都曾在某个时候被卸载。

## 🔧 修复

一条命令：

```bash
sudo apt install ubuntu-desktop -y
```

这是 Ubuntu 元包，它会拉取所有内容：GDM3（显示管理器）、GNOME Shell（桌面）、gnome-session、mutter（窗口管理器）、nautilus（文件管理器），以及约 460 个其他包（~266 MB + 1 GB 磁盘空间）。完成后，GDM3 立即显示为 `active (running)`。

然后 `sudo reboot` 即可回到图形登录界面。

## 🧠 关键要点

当 `systemctl status` 显示某个应长期运行的服务为 `active (exited)` 时，通常意味着二进制文件不存在。`dpkg -l` 状态码（`rc`、`ii`、`iU` 等）是你快速查看已安装、已移除或半配置状态的最佳工具。
