---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tabby Terminal for Senior Devs
translated: false
type: note
---

**Question:** What is the Terminus app for terminal, and why do some senior developers use it?

**Answer:**

You're likely thinking of **Tabby** (formerly Terminus) — it was renamed. It's an open-source, cross-platform terminal emulator built on Electron + web technologies.

**GitHub:** https://github.com/Tabby/tabby

### What it is

- Electron-based terminal (like VS Code's terminal, but standalone)
- Cross-platform: macOS, Windows, Linux
- SSH client built-in with connection manager
- Plugin ecosystem (written in TypeScript/Angular)
- Supports serial port connections (embedded/hardware devs love this)

### Why some senior devs use it

| Feature | Why it matters |
|---|---|
| **Built-in SSH manager** | Save and organize connections without maintaining `~/.ssh/config` manually |
| **Serial port support** | Rare among terminals — useful for firmware/embedded work |
| **Cross-platform parity** | Windows devs get a Unix-like terminal experience without WSL friction |
| **Plugin API** | Extend with TypeScript — some devs build internal tooling on top |
| **Split panes + tabs** | Standard now, but well-implemented |

### Honest take for you specifically

Given you're on **Warp** already — Tabby doesn't obviously beat it for your workflow. Warp has:
- AI command completion
- Block-based output (much better for LLM/agent output parsing)
- Better macOS native feel (not Electron)

Tabby's real niche is **Windows users** and **SSH-heavy workflows** where you want a unified terminal + connection manager without reaching for PuTTY or a separate SSH GUI.

Senior devs who swear by it are often on mixed OS environments or doing embedded/serial work. For pure AI engineering on macOS, Warp or even iTerm2 + tmux beats it.
