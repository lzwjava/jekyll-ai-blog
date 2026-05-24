---
audio: false
generated: true
image: false
lang: en
layout: post
title: Warp Vertical Tabs Configuration Guide
translated: false
type: note
---

**Question:** How does Warp's vertical tabs layout work, and how do you configure it?

**Answer:****Answer:**

Vertical tabs is a **recently shipped feature** (docs updated ~3 days ago). Here's the full breakdown:

---

## Enable It

Navigate to `Settings → Appearance → Tabs` and toggle **"Use vertical tab layout"** on.

That's it. The horizontal tab bar disappears and a **resizable left sidebar** takes its place.

---

## What the Sidebar Shows

The vertical tabs panel replaces the horizontal tab bar with a sidebar showing rich metadata, drag-and-drop management, and display options for tabs and panes.

Key UX features inside the panel:

- **Compact vs expanded mode** — choose between a dense single-line view (default) or a detailed multi-line layout with full metadata.
- **Configurable pane titles** — control which metadata appears first: last command or conversation, working directory, or Git branch.
- **Hover detail sidecar** — hover any pane row to see full, un-clipped metadata in a floating detail card without changing focus.
- **Search + drag-and-drop + rename** — filter panes by title, directory, or branch; reorder tabs or move panes between tabs by dragging; double-click a tab to rename it inline.

---

## Toolbar Control

The "Tabs panel" button in the configurable toolbar toggles the vertical tabs sidebar. The side a button lives on determines which side of the window its panel opens on — so you can move the toggle to the right side if you want the sidebar on the right instead.

The configurable toolbar works with both horizontal tabs and vertical tabs.

---

## Tab Configs (TOML — Reusable Layouts)

This is the power-user feature that pairs well with vertical tabs. Save a tab layout as a `.toml` file:

```toml
# ~/.local/share/warp-terminal/tab_configs/workstation.toml
[[panes]]
cwd = "~/projects/myrepo"
command = "ssh lzw@192.168.1.36"

[[panes]]
cwd = "~/projects/myrepo"
split_direction = "horizontal"
```

Right-click any tab in the vertical tabs panel or horizontal tab bar, then click **"Save as new config"** — Warp generates a `.toml` file from the tab's layout, commands, and directory.

Tab configs live at:
```
~/.local/share/warp-terminal/tab_configs/   # stable
~/.local/share/warp-terminal-preview/tab_configs/  # preview
```

The new config appears in the `+` menu automatically.

---

## Practical Layout for Your Workflow

Given you have MacBook Air (daily) + workstation at `192.168.1.36`:

```
Vertical sidebar tabs:
├── [local] ~/projects          ← daily coding
├── [ssh] lzw@192.168.1.36     ← GPU workstation
├── [monitor] nvidia-smi -l 1  ← training watcher
└── [logs] tail -f train.log   ← model output
```

Each of these as a saved Tab Config → one click from the `+` menu to restore the full layout. This is the real win over iTerm2 — no session manager plugin, no tmux on local, just TOML files you can version control.

---

## Why Vertical > Horizontal at Scale

- Horizontal tabs truncate past ~6 tabs — you lose tab names
- Vertical sidebar scales to 20+ tabs with full metadata visible
- Git branch + working directory visible per tab without switching — critical when you're juggling multiple model training runs or agent sessions

References:

- [Vertical Tabs - Warp docs](https://docs.warp.dev/terminal/windows/vertical-tabs/)
- [Tab Configs - Warp docs](https://docs.warp.dev/terminal/windows/tab-configs/)
- [Configurable toolbar - Warp docs](https://docs.warp.dev/terminal/windows/configurable-toolbar/)