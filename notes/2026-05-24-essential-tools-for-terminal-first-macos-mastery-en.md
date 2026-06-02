---
audio: false
generated: true
image: false
lang: en
layout: post
title: Essential Tools for Terminal-First macOS Mastery
translated: false
type: note
---

Good question. Given your profile — terminal-first, builds CLI tools, wants deep OS understanding — here's what I'd actually recommend, prioritized by impact:

---

## Tier 1: Use Daily, Learn by Osmosis

### Homebrew

You already use it, but studying its formula system teaches you macOS packaging, code signing, sandboxing, and how Apple's dependency ecosystem works.

```
# Peek at a formula's internals
brew cat fd
brew info --json=v2 jq
```

Source: <https://github.com/Homebrew/brew>

### iTerm2

If you're on Terminal.app, switch. iTerm2 is massively more configurable and open source. Triggers, profiles, scripting API, tmux integration.

<https://github.com/gnachman/iTerm2>

### skhd / yabai

**skhd** = hotkey daemon. **yabai** = tiling window manager. Together they give you i3-like control over macOS windows, entirely keyboard-driven. Studying yabai's source teaches you how macOS WindowServer, accessibility APIs, and SIP work.

```bash
brew install koekeishiya/formulae/skhd
brew install koekeishiya/formulae/yabai
```

<https://github.com/koekeishiya/skhd>
<https://github.com/koekeishiya/yabai>

This is the single biggest productivity unlock on macOS for someone with your workflow.

---

## Tier 2: Deepen OS Understanding

### XNU Kernel Source

You mentioned it — actually reading it is different. Start with:

```bash
# Your kernel version
uname -a
# Match to https://github.com/apple-oss-distributions/xnu/tags
```

Read these files in order:

1. `osfmk/kern/startup.c` — boot sequence
2. `bsd/kern/kern_proc.c` — how processes work
3. `osfmk/ipc/` — Mach IPC (how macOS IPC actually works)

### launchd

Understanding launchd is understanding macOS process management, scheduling, and daemon lifecycle. Read the source, then use `launchctl` fluently:

```bash
# List all user agents
launchctl list | grep -v apple

# Inspect a specific service
launchctl print gui/$(id -u)/com.apple.Finder
```

<https://github.com/apple-oss-distributions/launchd>

### libdispatch (GCD)

GCD is everywhere in macOS. Reading its source teaches you concurrency primitives, thread pools, and how Apple thinks about parallelism.

<https://github.com/apple/swift-corelibs-libdispatch>

---

## Tier 3: Tools That Teach You What macOS Can Do

### m-cli

Swiss-army knife for macOS admin tasks. Study it to learn what `defaults`, `profiles`, `diskutil`, `scutil`, `networksetup`, and dozens of other native commands can do:

```bash
brew install m-cli
m --help
```

<https://github.com/rgcr/m-cli>

### macos-defaults

Comprehensive catalog of `defaults write` commands. Every option is documented with what it does. You'll discover features you didn't know existed.

<https://github.com/yannbertrand/macos-defaults>

```bash
# Example: disable the "are you sure you want to open this" dialog
defaults write com.apple.LaunchServices LSQuarantine -bool false
```

### osx-serial-number / powermetrics / fs_usage

Not projects, but native tools most people never touch:

```bash
# Real-time power/CPU/GPU metrics (needs sudo)
sudo powermetrics --samplers cpu_power,gpu_power -i 1000

# Watch every filesystem syscall in real-time
sudo fs_usage -w -f filesys

# Watch every network connection
sudo nettop -m tcp

# DTrace (SIP allows some, but you can use Instruments)
sudo dtrace -n 'syscall::open*:entry { printf("%s", copyinstr(arg0)); }'
```

---

## Tier 4: Security & Internals Research

### The Objective-See Foundation

Patrick Wardle's tools — free, open-source macOS security. Studying these teaches you how macOS malware works, what the TCC database is, how entitlements work, and how to audit your own system.

- **KnockKnock** — what persists on your Mac
- **BlockBlock** — monitors persistence locations
- **RansomWhere?** — ransomware detection
- **OverSight** — mic/camera access monitor

<https://objective-see.org/products.html>

### macOS Security (on GitHub)

Community-maintained docs on every macOS security mechanism: SIP, TCC, entitlements, AMFI, Gatekeeper, XProtect, MRT.

<https://github.com/drduh/macOS-Security-and-Privacy-Guide>

---

## Tier 5: Build Something

Given your skill set, the fastest way to learn macOS deeply is to build a small tool. Ideas:

1. **A `top`-like tool for macOS** using `libproc` + IOKit — teaches you process internals
2. **A clipboard manager** (you already have clipboard handling in `ww`)
3. **A window automation CLI** wrapping macOS Accessibility APIs via PyObjC

```bash
# PyObjC gives you access to almost all macOS frameworks from Python
pip install pyobjc-framework-Cocoa pyobjc-framework-Quartz

# Example: list all windows
python3 -c "
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly
for w in CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, 0):
    print(w.get('kCGWindowOwnerName', '?'), '-', w.get('kCGWindowName', ''))
"
```

---

## My Recommendation for You Specifically

Start with **yabai + skhd** (Tier 1) — immediate productivity gain, and you'll learn macOS window management internals by configuring them. Then read **XNU's process management code** (Tier 2) to understand what `ps`, `top`, and `Activity Monitor` are actually querying.

The combination of using yabai daily + reading XNU source gives you both practical skill and deep understanding faster than any other approach.
