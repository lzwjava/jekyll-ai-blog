---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ghostty User-Space Install Guide
translated: false
type: note
---

Ghostty is installed and working. Because `sudo` requires a TTY (unavailable to me), I did a **user-space install** — no root needed.

## What I installed
- **Ghostty 1.3.0** from Ubuntu 26.04's universe repo (deb)
- Extracted into `~/.local` instead of `/usr`, plus the one missing dependency `libgtk4-layer-shell0`

## Layout

| Path | Purpose |
|------|---------|
| `~/.local/bin/ghostty` | Launcher wrapper (sets env vars, on your `PATH`) |
| `~/.local/opt/ghostty/` | Ghostty binary + resources (themes, shell integration, docs) |
| `~/.local/lib/ghostty-deps/` | Bundled `libgtk4-layer-shell.so.0` |
| `~/.local/share/terminfo/x/xterm-ghostty` | Terminfo entry |
| `~/.local/share/icons/hicolor/...` | App icon |
| `~/.local/share/applications/com.mitchellh.ghostty.desktop` | Desktop entry (patched to use the wrapper) |

The wrapper handles the two things a system install would normally do:
```bash
export GHOSTTY_RESOURCES_DIR="$HOME/.local/opt/ghostty/usr/share/ghostty"
export LD_LIBRARY_PATH="$HOME/.local/lib/ghostty-deps/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
```

## Verified
- `ghostty --version` → `Ghostty 1.3.0-dev+0000000`
- All shared libs resolve (`ldd` clean)
- `xterm-ghostty` terminfo loads
- **Live GUI smoke test**: opened a Wayland window and ran a command successfully
- Appears in your app launcher

## Notes
- Config goes in `~/.config/ghostty/config`.
- `ghostty` launches like any other terminal (e.g. from your launcher, or `ghostty` in a shell).
- The `ww/ghostty/` module (`ww ghostty list`, etc.) is **macOS-only** — it uses Swift/Cocoa `CGWindowList`/`AXUIElement`, so it won't function on this Linux box regardless of this install.
- If you'd prefer the clean system-wide install instead (into `/usr` with proper apt tracking), run:
  ```bash
  sudo apt install ghostty
  ```
  then remove the user-space copy: `rm -rf ~/.local/opt/ghostty ~/.local/lib/ghostty-deps ~/.local/bin/ghostty`.