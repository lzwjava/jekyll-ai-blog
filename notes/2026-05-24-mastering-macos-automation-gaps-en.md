---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mastering macOS Automation Gaps
translated: false
type: note
---

Now I have a clear picture. You already have 12 `ww macos` commands covering a solid surface area. Here's my analysis of what you already know, and what open-source projects would level you up next.

---

## What Your Code Already Tells Me

You're comfortable with:
- **plistlib** — reading binary plists (Dock)
- **networksetup** — system proxy config
- **pmset** — power/battery management
- **diskutil** — disk enumeration
- **sysctl** — kernel parameters (hw.memsize, hw.model, etc.)
- **vm_stat** — virtual memory pages
- **PyObjC** — `UserNotifications` (toast.py), `CoreText` (list_fonts.py)
- **osascript** — AppleScript bridge for System Events
- **stat -f** — BSD stat for file timestamps
- **du** — disk usage

Gaps I see — no window management, no accessibility API usage, no `screencapture`, no `shortcuts` CLI, no IOKit, no `launchctl` deep usage. That's where the interesting stuff lives.

---

## Recommendations, Matched to Your Gaps

### 1. yabai — Window Management (fills your biggest gap)

Your `ww macos open-terminal` just opens Ghostty windows. yabai gives you programmatic control over every window's position, size, space, and stacking — via a CLI and IPC socket.

```bash
# Install
brew install koekeishiya/formulae/yabai
yabai -m signal --add event=dock_did_restart action="sleep 1; yabai -m config ..."

# Example: move focused window to right half
yabai -m window --grid 1:2:1:0:1:1

# Example: query all windows as JSON
yabai -m query --windows

# Example: focus window by direction
yabai -m window --focus east
```

What you'll learn: macOS Accessibility API, SIP (System Integrity Protection) — yabai needs partial SIP disable for full features, which teaches you exactly what SIP protects and how. Also teaches you macOS Spaces (virtual desktops) at the API level.

https://github.com/koekeishiya/yabai

### 2. skhd — Global Hotkey Daemon (pairs with yabai)

```bash
brew install koekeishiya/formulae/skhd

# ~/.config/skhd/skhd.conf
alt - h : yabai -m window --focus west
alt - j : yabai -m window --focus south
alt - k : yabai -m window --focus north
alt - l : yabai -m window --focus east
```

What you'll learn: how macOS captures keyboard events at the system level (CGEventTap, IOKit HID), how Input Monitoring permission works.

https://github.com/koekeishiya/skhd

### 3. screencapture + Shortcuts CLI — fill your screenshot pipeline

You already have screenshot → LLM vision in `ww note screenshot-log`. But you're not using the full power of macOS's native tools:

```bash
# screencapture is incredibly capable
screencapture -i ~/Desktop/capture.png          # interactive selection
screencapture -R 0,0,1920,1080 ~/full.png       # specific region
screencapture -v ~/capture.mp4                   # screen recording (macOS 15+)
screencapture -C                                 # capture cursor

# Shortcuts CLI — Apple's automation framework
shortcuts list
shortcuts run "Get Text From Image" -i photo.png
shortcuts run "Remove Background" -i photo.png -o output.png

# Create a shortcut programmatically
shortcuts create "My Workflow" --workflow workflow.json
```

What you'll learn: macOS Shortcuts framework, Quick Actions, and how to bridge CLI ↔ GUI automation.

### 4. IOKit via PyObjC — Hardware-Level Access

Your `get_system_info.py` uses `sysctl` and `system_profiler`. IOKit goes deeper:

```python
# IOKit battery info (raw, not pmset)
import subprocess
import plistlib

# IORegistry — the kernel's device tree
result = subprocess.run(
    ["ioreg", "-r", "-c", "AppleSmartBattery", "-a"],
    capture_output=True, text=True
)
# Parse the plist output to get:
# - CycleCount, DesignCapacity, MaxCapacity, Temperature
# - Serial, ManufactureDate, CellVoltage

# IOKit display info
result = subprocess.run(
    ["ioreg", "-r", "-c", "IODisplayConnect", "-a"],
    capture_output=True, text=True
)

# IOKit USB devices
result = subprocess.run(
    ["ioreg", "-r", "-c", "IOUSBDevice", "-a"],
    capture_output=True, text=True
)
```

What you'll learn: IORegistry — the kernel's device tree. This is how `system_profiler` gets its data, but raw. You can add `ww macos hardware` that goes deeper than your current `system-info`.

### 5. launchctl — Process Management (complement your process_analyze.py)

Your `process_analyze.py` uses `ps aux` + LLM. But macOS process management lives in launchd:

```bash
# List ALL services (not just user agents)
launchctl print system/
launchctl print gui/$(id -u)/

# Detailed info about a service
launchctl print gui/$(id -u)/com.apple.Spotlight

# See what a service's PID is, its exit status, last crash
launchctl list | grep -v com.apple

# Disable a service (persistent across reboots)
launchctl disable gui/$(id -u)/com.some.background.agent

# Enable it back
launchctl enable gui/$(id -u)/com.some.background.agent

# Kickstart (restart) a service
launchctl kickstart -k gui/$(id -u)/com.apple.Finder
```

What you'll learn: the entire macOS service lifecycle — LaunchDaemons (system-level, root), LaunchAgents (user-level, per-session), XPC services, and how `launchd` replaces both `cron` and `inetd`.

A natural `ww macos services` command would list all non-Apple agents with their status, last run time, and exit codes.

### 6. m-cli — The Swiss Army Knife You Should Study

Not just use — **read the source**. It's a single bash script:

```bash
brew install m-cli
# The source is just:
cat $(which m)
```

It wraps ~200 macOS admin tasks: Airport, Bluetooth, DNS, firewall, Time Machine, FileVault, parental controls, screen sharing, etc. Every command teaches you a native macOS tool you didn't know existed.

https://github.com/rgcr/m-cli

### 7. osx-cpu-temp / iStats — Thermal Monitoring

```bash
brew install osx-cpu-temp
osx-cpu-temp  # reads from IOKit SMC (System Management Controller)
```

What you'll learn: SMC (System Management Controller) — the embedded chip that manages thermals, fans, battery charging. IOKit SMC access is how you read CPU die temperature, fan RPM, and battery health at the hardware level.

Source: https://github.com/lavoiesl/osx-cpu-temp

### 8. macos-defaults — Configuration Catalog

```bash
# Every macOS `defaults write` command, documented
open https://github.com/yannbertrand/macos-defaults

# Examples you can add to ww:
defaults read com.apple.dock tilesize              # dock icon size
defaults read -g AppleFontSmoothing                # font rendering
defaults read com.apple.finder ShowPathbar         # Finder path bar
defaults read com.apple.Spotlight orderedItems     # Spotlight config
```

A `ww macos defaults` command that reads/displays/searches your current non-default settings would be very useful.

---

## What I'd Build Next in ww

Based on your gaps, here are the highest-value additions:

| Command | What it does | What you learn |
|---|---|---|
| `ww macos services` | List non-Apple launchd agents/daemons | launchctl, XPC |
| `ww macos hardware` | Deep IOKit hardware info (battery cycles, thermal, USB) | ioreg, IORegistry |
| `ww macos defaults` | Show/search all non-default system preferences | defaults CLI, plist domains |
| `ww macos snapshot` | screencapture with region/recording support | screencapture flags |
| `ww macos permissions` | Show TCC database (what apps have camera/mic/files access) | TCC.db, sqlite3 |

The `permissions` one is especially interesting — TCC (Transparency, Consent, and Control) is macOS's privacy framework. Reading it teaches you how Apple sandboxes app access:

```bash
# TCC database location (SIP-protected, need to copy)
cp ~/Library/Application\ Support/com.apple.TCC/TCC.db /tmp/
sqlite3 /tmp/TCC.db "SELECT client, service, auth_value FROM access;"

# Shows which apps have camera, microphone, screen recording,
# file access, etc.
```

---

## TL;DR Priority

1. **yabai + skhd** — install today, use daily, biggest productivity unlock
2. **read m-cli source** — 30 min investment, 200 new macOS commands in your mental model
3. **build `ww macos services`** — launchctl is the most underused macOS tool
4. **build `ww macos hardware`** — ioreg gives you data sysctl can't
