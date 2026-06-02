---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Understanding Ghostty's Configuration File
translated: false
type: note
---

### How the Ghostty Config File Works

Ghostty's configuration file uses a simple, text-based format with key-value pairs in the style of `key = value`. It's designed to be straightforward, letting you override only the defaults you care about—Ghostty ships with sensible built-in defaults for everything else, so a minimal or even empty config file works fine.

#### Quick Syntax Breakdown

- **Keys and values**: Keys are always lowercase and case-sensitive (e.g., `font-family = JetBrains Mono`). Values can be unquoted unless they contain spaces or special characters (e.g., `font-family = "JetBrains Mono Nerd Font"`). Spacing around the `=` doesn't matter.
- **Comments**: Start a line with `#` for notes (e.g., `# My custom theme`). No inline comments after values, or they'll get parsed as part of the value.
- **Reset to default**: Use an empty value like `key =` to revert a setting to Ghostty's built-in default.
- **Special values**: Some options have unique formats, like durations (e.g., `resize-overlay-duration = 4s 200ms`)—check the docs for specifics.
- **File loading**: Ghostty looks for the config at `~/.config/ghostty/config` (Linux/Windows) or `~/Library/Application Support/com.mitchellh.ghostty/config` (macOS). You can include other files with `config-file = path/to/other.conf` for modular setups.
- **CLI overrides**: Any setting can also be set via command-line flags (e.g., `ghostty --font-family="Fira Code"`), which take precedence over the file.

Changes take effect immediately if you reload with the default keybinding (Cmd+Shift+, on macOS or Ctrl+Shift+, on Linux/Windows) or by running `ghostty +reload-config`.

To see all options and defaults, run `ghostty +show-config --default --docs` in your terminal.

### What's a Normal Config?

A "normal" config is often minimal—just tweaking a few things like font, colors, or padding for comfort. Ghostty's defaults include JetBrains Mono as the font family (with built-in Nerd Font support), a clean background/foreground scheme, and no extra padding.

Here's a simple, typical example for a dark-themed setup with a popular font, some padding, and basic keybindings. Save this as your `config` file:

```
# Basic dark theme with padding and custom font
background = 1e1e1e
foreground = f8f8f2
font-family = "JetBrains Mono Nerd Font"
font-size = 14

# Add some breathing room around the text
window-padding-x = 8
window-padding-y = 8

# Custom keybindings (overrides defaults if needed)
keybind = cmd+t=new_tab
keybind = cmd+w=close_tab
keybind = cmd+d=new_split:right
```

This keeps things lightweight while customizing the essentials. You can expand it with more colors (e.g., palette entries like `color0 = 282a36`) or themes from the docs.

[Ghostty Configuration Docs](https://ghostty.org/docs/config)
