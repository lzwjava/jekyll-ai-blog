---
audio: false
generated: true
image: false
lang: en
layout: post
title: Alacritty Supports macOS Windows and Linux
translated: false
type: note
---

Yes, Alacritty is cross-platform. Evidence from the codebase:

1. **Self-described** in `Cargo.toml` and the man page: *"A fast, cross-platform, OpenGL terminal emulator"*

2. **Three platform targets** in the code via `#[cfg(...)]`:
   - `target_os = "macos"` — native macOS (Cocoa, Metal/OpenGL)
   - `windows` — Windows (ConPTY)
   - Linux/Unix with two display backends:
     - `feature = "x11"` — X11
     - `feature = "wayland"` — Wayland

3. **TTY layer** has platform-specific implementations:
   - `tty/unix.rs` — macOS + Linux (pty via posix_openpt)
   - `tty/windows/mod.rs` + `conpty.rs` — Windows ConPTY

4. **Font defaults** are per-platform (`font.rs:105-110`):
   - macOS: `Menlo`
   - Windows: `Consolas`
   - Linux: `monospace`

5. **Display server selection** in `main.rs:12-25`:
   ```
   #[cfg(not(any(feature = "x11", feature = "wayland", target_os = "macos", windows)))]
   compile_error!("...");  // won't compile without at least one platform
   ```

So it supports macOS, Windows, and Linux (X11 or Wayland).