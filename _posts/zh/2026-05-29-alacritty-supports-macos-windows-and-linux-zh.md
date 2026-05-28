---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Alacritty 支持 macOS、Windows 和 Linux
translated: true
type: note
---

是的，Alacritty 是跨平台的。以下是代码库中的证据：

1. **自述** 在 `Cargo.toml` 和 man 页面中：*"一个快速、跨平台、基于 OpenGL 的终端模拟器"*

2. **三个平台目标** 通过 `#[cfg(...)]` 在代码中体现：
   - `target_os = "macos"` — 原生 macOS（Cocoa，Metal/OpenGL）
   - `windows` — Windows（ConPTY）
   - Linux/Unix 拥有两种显示后端：
     - `feature = "x11"` — X11
     - `feature = "wayland"` — Wayland

3. **TTY 层** 具有平台特定的实现：
   - `tty/unix.rs` — macOS + Linux（通过 posix_openpt 的 pty）
   - `tty/windows/mod.rs` + `conpty.rs` — Windows ConPTY

4. **字体默认值** 按平台设置（`font.rs:105-110`）：
   - macOS：`Menlo`
   - Windows：`Consolas`
   - Linux：`monospace`

5. **显示服务器选择** 在 `main.rs:12-25` 中：
   ```
   #[cfg(not(any(feature = "x11", feature = "wayland", target_os = "macos", windows)))]
   compile_error!("...");  // 至少需要一个平台才能编译
   ```

因此它支持 macOS、Windows 以及 Linux（X11 或 Wayland）。