---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rust TUI Runs Inside Terminal
translated: false
type: note
---

Question: Is Rust TUI always popping up a separate window instead of directly showing the result in the terminal?

Answer:

No — most Rust TUI libraries do **not** create a separate desktop window.

A Rust TUI (Terminal User Interface) usually runs **inside the existing terminal** itself.

For example, libraries like:

* [ratatui](https://ratatui.rs/?utm_source=chatgpt.com)
* [crossterm](https://github.com/crossterm-rs/crossterm?utm_source=chatgpt.com)
* [termion](https://github.com/redox-os/termion?utm_source=chatgpt.com)

typically:

* switch the terminal into an “alternate screen buffer”
* redraw the screen continuously
* hide the normal shell prompt temporarily
* capture keyboard events interactively

So it *looks* like a fullscreen app “popped up,” but it is still just inside your terminal.

Examples:

```bash
cargo run
```

Then your terminal becomes something like:

```text
┌────────────────────────────┐
│   System Monitor           │
│ CPU: 32%                   │
│ Memory: 5.2 GB             │
│                            │
│ Press q to quit            │
└────────────────────────────┘
```

When you quit (`q`), the normal shell returns.

---

What you are probably comparing:

| Type        | Behavior                          |
| ----------- | --------------------------------- |
| CLI program | Prints result and exits           |
| TUI program | Takes over terminal interactively |
| GUI program | Opens actual OS window            |

So:

```rust
println!("Hello");
```

→ direct output

while TUI:

```rust
terminal.draw(|f| {
   // render UI
});
```

→ interactive terminal screen

---

Some TUIs can also behave more like a normal CLI.

For example:

```bash
git log
htop
btop
lazygit
```

These are all terminal-based interfaces, not separate windows.

---

Technically, most Rust TUI apps use:

```text
Alternate Screen Buffer
```

via ANSI escape sequences.

That means:

* your old terminal content is preserved
* the app gets a clean temporary screen
* after exit, the old screen restores

This is why it feels like a “popup mode.”

---

If you want:

## 1. Direct output only

Use normal CLI:

```rust
println!("result");
```

or libraries like:

* [clap](https://github.com/clap-rs/clap?utm_source=chatgpt.com)
* [indicatif](https://github.com/console-rs/indicatif?utm_source=chatgpt.com)

---

## 2. Interactive terminal UI

Use TUI:

* [ratatui](https://ratatui.rs/?utm_source=chatgpt.com)
* [cursive](https://github.com/gyscos/cursive?utm_source=chatgpt.com)

---

## 3. Actual graphical windows

Use GUI frameworks:

* [egui](https://github.com/emilk/egui?utm_source=chatgpt.com)
* [iced](https://github.com/iced-rs/iced?utm_source=chatgpt.com)
* [tauri](https://tauri.app/?utm_source=chatgpt.com)

These create real desktop windows.

References:

* [https://ratatui.rs/](https://ratatui.rs/)
* [https://github.com/crossterm-rs/crossterm](https://github.com/crossterm-rs/crossterm)
* [https://github.com/gyscos/cursive](https://github.com/gyscos/cursive)
* [https://github.com/emilk/egui](https://github.com/emilk/egui)
* [https://tauri.app/](https://tauri.app/)
