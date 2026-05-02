---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mint系统下交换大写锁定键与控制键
translated: true
type: note
---

## 评测：Linux Mint 上的 CapsLock ↔ Ctrl 键位互换

### 我们做了什么

**`~/.Xmodmap`** — 用于告知 X11 如何重映射按键：
1. 将 CapsLock 从 “Lock” 修饰键组中移除
2. 将 Ctrl_L 从 “Control” 修饰键组中移除
3. 将物理 CapsLock 键重新分配为 `Control_L` 键码
4. 将物理 Ctrl_L 键重新分配为 `Caps_Lock` 键码
5. 将两者重新添加到各自对应的修饰键组中

这是一个完整而干净的键位互换 — 两个按键在所有应用中都能完全替代对方的功能。

**`~/.config/autostart/xmodmap.desktop`** — 一个 Cinnamon 自动启动项，用于在每次桌面会话启动时运行 `xmodmap ~/.Xmodmap`。无需 root 权限；Cinnamon 会在登录时自动处理 `~/.config/autostart/` 中的内容。

**`DISPLAY=:0 xmodmap ~/.Xmodmap`** — 将此映射实时应用到正在运行的 X 会话中，无需注销或重启。

---

### 优点

- 无需 root/sudo 权限 — 完全在用户空间操作
- 立即生效，无需重启系统
- 通过自动启动机制实现跨重启持久化
- Xmodmap 方法是 X11 环境下所有桌面环境（Cinnamon、XFCE、MATE 等）中最可靠的解决方案

### 潜在脆弱性

- **Wayland**：`xmodmap` 在 Wayland 下无效。Linux Mint Cinnamon 目前默认使用 X11，因此现阶段没有问题 — 但仍值得留意。
- **替代方案**：更干净的系统级解决方案是在 `/etc/default/keyboard` 中设置 `XKBOPTIONS="ctrl:swapcaps"`，但这需要 sudo 权限。我们采用的方法是无需 root 权限的最佳选择。