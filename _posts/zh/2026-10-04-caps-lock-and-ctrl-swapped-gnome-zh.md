---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GNOME 中的 Caps Lock 和 Ctrl 互换
translated: true
type: note
---

完成 ✅ — 在 `192.168.1.45` 上 **Caps Lock ↔ Ctrl 已互换**。

**我做了什么：**

- 检测到桌面环境：**Wayland** 上的 GNOME 46（不是 X11），因此 `setxkbmap`/`xmodmap` 会话 hack 无法正确持久化 —— 改用受支持的 GNOME 方法：
- 通过 dconf（经由位于 `/run/user/1000/bus` 的活动 GNOME 会话总线）设置 XKB 选项 `ctrl:swapcaps`：
  - 键：`/org/gnome/desktop/input-sources/xkb-options` → `['ctrl:swapcaps']` ✓（已验证）
  - 会话 3（tty2 上的活动 GNOME 会话）处于 **Active** 状态，因此它会立即生效

**效果：** 在那台机器的物理键盘上，**Caps Lock 现在充当 Ctrl**，而**右侧的 Ctrl 键充当 Caps Lock**。（`ctrl:swapcaps` 是对称互换。）

这是持久化的 —— 它存储在用户的 dconf 中，因此重启和登录后依然有效。无需重启。如果你想要恢复：`gsettings reset org.gnome.desktop.input-sources xkb-options`。
