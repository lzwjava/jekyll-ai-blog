---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Ubuntu上交换Caps Lock和Ctrl键
translated: true
type: note
---

已完成。现在在 Ubuntu 机器（GNOME/Wayland 会话）上，Caps Lock 和 Ctrl 已互换。

**应用的操作：**

- `gsettings set org.gnome.desktop.input-sources xkb-options "['ctrl:swapcaps']"`
- 结果验证：`['ctrl:swapcaps']` — 在 GNOME 会话中立即生效，重启后保持。

**当前行为：**

- **Caps Lock** 键 → 作为 **Ctrl** 使用
- **左 Ctrl** 键 → 作为 **Caps Lock** 使用

注意：此设置适用于图形化 GNOME 会话。如果希望在登录屏幕或虚拟控制台（tty）也应用该互换，需使用 `sudo` 编辑 `/etc/default/keyboard`（设置 `XKBOPTIONS="ctrl:swapcaps"` 并运行 `setupcon`）——如需此配置，请告知。
