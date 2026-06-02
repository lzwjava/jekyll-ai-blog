---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Ghostty Window Cycling Shortcuts
translated: false
type: note
---

Yeah, I totally get it—Cmd + ` (tilde/backtick) for cycling through windows in Ghostty feels snappy and intuitive, especially if you're treating them like lightweight, independent sessions instead of cramming everything into tabs. It's got that nice cyclic flow without the mental overhead of tab bar clutter. The default Cmd + Shift + [ / ] for tab navigation (or pane focus with Cmd + [ / ]) does feel clunky on Mac, since you're juggling Shift on top of Cmd, and those brackets aren't the most thumb-friendly without stretching.

You're spot on: a single Cmd + key combo is way cleaner for most folks—ergonomic, quick to hit, and less error-prone than multi-modifier mashups. Ghostty's defaults already lean into that for tab selection (Cmd + 1–8 jumps straight to specific ones), but if you're all-in on windows over tabs, you could remap cycling to something even simpler like Cmd + J/K (Vim-style) or Cmd + ←/→ for prev/next window. It's super easy to customize in the config file—just add lines like:

```
keybind = "cmd-j", "window:previous"
keybind = "cmd-k", "window:next"
```

That keeps it to one modifier + one key, no fuss. What setup are you running mostly—multiple Ghostty windows across spaces, or all pinned to one desktop? If you've got a specific action you wanna bind (like quick pane swaps), I can brainstorm more tweaks.
