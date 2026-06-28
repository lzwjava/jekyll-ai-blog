---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过SSH在GNOME上交换Caps Lock键
translated: true
type: note
---

在Fedora 44（GNOME/Wayland）上，我通过 SSH 运行了以下命令：

```bash
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus
gsettings set org.gnome.desktop.input-sources xkb-options "['ctrl:swapcaps']"
```

**工作原理：**

1. **`DBUS_SESSION_BUS_ADDRESS`** — SSH 会话无法访问 GNOME 桌面总线。设置此环境变量指向当前用户的 D-Bus 套接字，使得 `gsettings` 能够与 GNOME 会话通信。

2. **`gsettings set org.gnome.desktop.input-sources xkb-options`** — GNOME 的键盘设置存储在 dconf 中。`xkb-options` 键接受一个 XKB 选项列表。

3. **`ctrl:swapcaps`** — 来自 `xkeyboard-config` 的 XKB 选项，在输入层交换 Caps Lock 和左 Ctrl 键的键码。在 Wayland 和 X11 上均有效。

此设置会跨重启持久化，因为它存储在 GNOME 的 dconf 数据库（`~/.config/dconf/user`）中。
