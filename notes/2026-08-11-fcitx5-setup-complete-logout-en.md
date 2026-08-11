---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fcitx5 Setup Complete – Logout
translated: false
type: note
---

Everything is installed and pre-configured. Here's the full picture:

## ✅ What I did

| Step | Status |
| ------ | -------- |
| Installed `fcitx5`, `fcitx5-chinese-addons`, `fcitx5-config-qt` | ✅ 5.1.19 / 5.1.12 |
| Set Fcitx5 as default (`im-config -n fcitx5` → `~/.xinputrc`) | ✅ |
| Masked IBus GNOME autostart (prevents conflict) | ✅ |
| Pre-wrote `~/.config/fcitx5/profile` — IM list: `keyboard-us` (default), **双拼**, 拼音 | ✅ |
| Pre-wrote `~/.config/fcitx5/conf/pinyin.conf` — **小鹤双拼** (`ShuangpinProfile=4`), mode on | ✅ |

Auto-start on login is handled by `im-config`'s phase-2 hook (`/usr/share/im-config/data/23_fcitx5.rc` runs `fcitx5 -d` and sets `GTK_IM_MODULE`/`QT_IM_MODULE`/`XMODIFIERS=@im=fcitx`), so no extra steps needed.

## 🚪 The only remaining step: log out and log back in

Fcitx5 can't be hot-loaded into a running GNOME session. After you log in again:

1. Click the tray icon (or `Ctrl+Space`) in any text field
2. Type `xm` + `space` → should produce **小明** — that's 小鹤双拼 working

## Verify / tune afterwards

```bash
fcitx5-diagnose        # health check
fcitx5-configtool      # GUI — tweak schemes, toggle 全拼 fallback
```

Want a different scheme instead of 小鹤? Edit `~/.config/fcitx5/conf/pinyin.conf` (or use the GUI):
`ShuangpinProfile=0` 自然码 · `1` 微软双拼 · `2` 紫光 · `3` 智能ABC · `4` 小鹤

⚠️ One warning: I can trigger the logout for you (`gnome-session-quit --logout --no-prompt`) — but it will **close all your open apps/windows without saving**. Want me to do that, or will you log out yourself?
