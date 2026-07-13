---
audio: false
generated: true
image: false
lang: en
layout: post
title: "'ll uno' Arduino Serial Monitor"
translated: false
type: note
---

Here's a comprehensive summary of everything done in this session:

---

## Session Summary: `ll uno` subcommand — Arduino UNO serial monitor

### Project context

`ll` is a Rust CLI tool (`/home/xiaoxin/projects/ll/`) with a ratatui TUI interface. It already had `info` (system info), `gcloud`, and `word2vec` subcommands. The repo had an Arduino sketch (`sketch_jul9a/sketch_jul9a.ino`) that reads a microphone on A0 and outputs amplitude values over serial at 9600 baud.

### Goal

Add a `cargo run -- uno status` command that reads the Arduino's serial output and displays it in a live TUI.

### Changes made

**1. `Cargo.toml`** — added `serialport = "4.7"` dependency for serial port access.

**2. `src/uno.rs`** (new, 232 lines) — two subcommands:

- **`uno listen`** — raw serial dump to stdout. Tested and working: reads amplitude values (44–65 range from the mic) at 9600 baud from `/dev/ttyUSB0`.
- **`uno status`** — TUI with:
  - Header bar showing port/baud
  - Live amplitude display (turns green bold when >30 threshold)
  - Rolling line chart (200 samples, auto-scaling Y axis)
  - Stats bar: min, max, avg, sample count
  - Quit with `q` or `Esc`

**3. `src/main.rs`** — wired in the module, match arm, and updated help text.

### Issues encountered and resolved

| Issue | Cause | Fix |
| ------- | ------- | ----- |
| Rust toolchain not installed | Fresh dev machine | Installed via rustup |
| `libudev-dev` missing | `serialport` crate needs it | `apt install libudev-dev` |
| Permission denied on `/dev/ttyUSB0` | User not in `dialout` group | Use `sg dialout` (same pattern user already used) |
| ENXIO error running through `sg` | `sg` detaches stdin from the TTY, so `enable_raw_mode()` fails | Rewrote the read loop to use `BufReader` (same pattern as `listen`); added a helpful error message directing the user to `sudo usermod -a -G dialout` |

### How to use

```bash
# Recommended: add user to dialout group once, then run directly
sudo usermod -a -G dialout $USER
# log out & back in

cargo run -- uno status          # TUI with chart
cargo run -- uno listen          # raw serial dump
```

### Git

```
b2b62f8  feat: add uno subcommand for Arduino serial monitor
  5 files changed, 433 insertions(+), 12 deletions(-)
  create mode 100644 src/uno.rs
```
