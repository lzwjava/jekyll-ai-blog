---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GNOME 桌面已从您的机器卸载
translated: true
type: note
---

好了，我已经完全了解情况了。以下是发生的事情：

**这个机器上的 GNOME 桌面环境已被完全卸载。**

以下是证据：

| Package | Status | Notes |
|---------|--------|-------|
| `ubuntu-desktop` | **未安装** | 拉取整个桌面的元包 |
| `gdm3` | **`rc`** (已移除，配置保留) | 显示管理器二进制文件已删除 |
| `gnome-shell` | **`rc`** (已移除，配置保留) | GNOME shell 本身已删除 |
| `gnome-session` | **未安装** | 已删除 |
| `gnome-settings-daemon` | **`rc`** | 已删除 |

启动时发生的情况：systemd 尝试通过旧的 SysV init 脚本 (`/etc/init.d/gdm3`) 启动 gdm3，该脚本检查 `test -x /usr/sbin/gdm3` — 二进制文件不存在 — 因此静默退出 0。这就是为什么 `systemctl status gdm3` 显示 `active (exited)` 且无错误。它“启动”了但立即退出，因为没有可运行的内容。

同时 `/etc/X11/default-display-manager` 仍指向 `/usr/sbin/gdm3`，并且 `graphical.target` 是默认目标 — 但没有显示管理器或 shell，你就会直接进入 TTY。

**要修复它，请运行：**

```bash
sudo apt install ubuntu-desktop
```

这将重新拉取 gdm3、gnome-shell 和所有其他组件。之后，重启应该会带你进入图形登录界面。

**或者**，如果你有意移除桌面以节省这台服务器（它正在运行 Docker/Jellyfin/OpenClaw）的资源，并且只想保持 headless 模式 — 也没问题，只需告诉我。
