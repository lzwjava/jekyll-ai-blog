---
audio: false
generated: true
image: false
lang: en
layout: post
title: Terminal Task Prioritization via Font Sizing
translated: false
type: note
---

**Question:** Can using different font sizes across terminal windows/sessions be another way to visually distinguish multiple tasks — not just window position?

**Answer:**

Yes, exactly. Font size is an underutilized dimension for terminal multitasking. Here's the full picture of what you can do:

## Font Size as a Visual Signal

The idea: assign semantic meaning to font size across windows.

| Font Size | Use Case |
|-----------|----------|
| Large (18–24pt) | Main focus task — the thing you're actively coding |
| Medium (13–14pt) | Secondary monitor — logs, watchers, test runners |
| Small (9–11pt) | Background processes — LLM streaming, build CI, agent loops |

Your eyes instantly know where to look without reading anything.

## How to Set It Per Window

**iTerm2** (most flexible):

```bash
# Via AppleScript — set font size of current window
osascript -e 'tell application "iTerm2"
  tell current session of current window
    set font size to 18
  end tell
end tell'
```

Or create **Profiles** in iTerm2 (Preferences → Profiles) — one per task type — each with its own font size, color scheme, and badge. Then launch with:

```bash
# Open new window with a specific profile
osascript -e 'tell application "iTerm2" to create window with profile "Focus"'
```

**Kitty** (config-based, fast):

```bash
# In kitty.conf or via remote control
kitty @ set-font-size 20        # current window
kitty @ --to unix:/tmp/kitty-focus set-font-size 20  # specific instance
```

You can launch separate kitty instances with different configs:

```bash
kitty --config ~/.config/kitty/focus.conf &
kitty --config ~/.config/kitty/monitor.conf &
```

**Wezterm** (Lua-scripted, most programmable):

```lua
-- wezterm.lua
local wezterm = require 'wezterm'

return {
  font_size = 14.0,  -- default
  -- override per-pane via events or window decorations
}
```

## Combine Font Size + Color Theme + Badge

The real power is stacking signals:

```
Window 1: Large font + dark theme + badge "FOCUS"     → active coding
Window 2: Medium font + blue theme + badge "LOGS"      → streaming output
Window 3: Small font + dim theme + badge "AGENT"       → background LLM agent
```

In iTerm2, badges show in the top-right corner of each pane — set via:

```bash
printf "\e]1337;SetBadgeFormat=%s\a" $(echo -n "AGENT" | base64)
```

## My Suggested Layout for Your Workflow

Given you run CLI agents (`ww`, `zz`, `iclaw`) + LLM streaming + active coding:

```
┌─────────────────────────────────┐  ┌──────────────────┐
│  FOCUS (20pt, light theme)      │  │ AGENT (10pt, dim)│
│  $ vim / claude-code / cursor   │  │ $ ww run loop... │
│                                 │  │ streaming tokens │
├─────────────────────────────────┤  ├──────────────────┤
│  LOGS (12pt, blue tint)         │  │ BUILD (11pt)     │
│  $ tail -f / pytest -s          │  │ $ gh run watch   │
└─────────────────────────────────┘  └──────────────────┘
```

Font size alone tells you the priority of each window at a glance — no reading required.