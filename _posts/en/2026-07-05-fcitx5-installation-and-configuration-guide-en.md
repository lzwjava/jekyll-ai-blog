---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fcitx5 Installation and Configuration Guide
translated: false
type: note
---

Done. Fcitx5 is installed and running on this machine.

## Summary

**Installed packages**: fcitx5, fcitx5-chinese-addons (includes pinyin engine + cloudpinyin + pinyinhelper), fcitx5-config-qt (GUI config tool), all frontends (GTK3/4, Qt5/6).

**Config**:

- im-config set to fcitx5
- `~/.config/fcitx5/profile` configured with `keyboard-us` + `pinyin`
- IBus daemon killed (they conflict — don't run both)
- Fcitx5 daemon running on X11

**How to use**:

- `Ctrl+Space` toggles between English (keyboard-us) and Chinese Pinyin
- Or run `fcitx5-config-qt` for GUI settings
- Or toggle programmatically: `fcitx5-remote -s pinyin` / `fcitx5-remote -s keyboard-us`

**Note**: This is running on the server (192.168.1.36 workstation) via SSH. Fcitx5 needs a running X11 session — it works if you SSH with X forwarding or use it directly on the workstation's display. On your MacBook Air you'd install it via `brew install fcitx5` if needed there too.
