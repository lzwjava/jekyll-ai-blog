---
audio: false
generated: true
image: false
lang: en
layout: post
title: IBus Chinese Input Configuration Guide
translated: false
type: note
---

Here's the summary:

**IBus + libpinyin** is now installed and configured.

**What was set up:**
- `ibus-libpinyin` (Pinyin input engine) installed
- Engine set to `libpinyin` — press **Ctrl+Space** to toggle between English and Chinese
- IBus daemon restarted
- Environment variables added to `~/.bashrc`:
  - `GTK_IM_MODULE=ibus`
  - `QT_IM_MODULE=ibus`
  - `XMODIFIERS=@im=ibus`
- Default preload engines saved: `[libpinyin, xkb:us::eng]`

**⚠️ Caveats (terminal-only session):**

This system doesn't have a desktop environment running in this session — it's a CLI/SSH session. The IM environment variables will work in **GUI apps** launched from this shell (e.g. `gedit`, `libreoffice`, `vscode`), but **not in this terminal** itself. Terminal-based Chinese input needs either:
1. **Terminal app with IM support** (GNOME Terminal, Konsole, kitty — not plain TTY or tmux without X)
2. Or use `fbterm` + `ibus` for TTY-level input

If you're on the **TTY** (Ctrl+Alt+F1–F6, no X server), Chinese input won't work without `fbterm` + `ibus-fbterm`. If you're on **SSH** from a Mac (using Terminal.app or iTerm2), the input is handled on the **client side** — set up Chinese input on the Mac side and it'll Just Work in any remote shell.