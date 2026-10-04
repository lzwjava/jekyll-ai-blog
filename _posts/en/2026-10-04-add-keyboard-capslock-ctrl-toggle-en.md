---
audio: false
generated: true
image: false
lang: en
layout: post
title: Add keyboard capslock-ctrl toggle
translated: false
type: note
---

Done. I added a new `keyboard` command group with a `capslock-ctrl` subcommand that toggles the Caps Lock ↔ Ctrl swap on Ubuntu.

## What was added

**New files**
- `ww/keyboard/__init__.py`
- `ww/keyboard/main.py` — group dispatcher (`ww keyboard capslock-ctrl`)
- `ww/keyboard/capslock_ctrl.py` — the actual toggle logic

**Edited files**
- `ww/main.py` — help text, dispatch branch, and the "did you mean" suggestion list
- `completions/_ww` — zsh tab-completion entries

## How it works

On Ubuntu, it uses **`gsettings`** against `org.gnome.desktop.input-sources xkb-options` (works on both GNOME Wayland and X11 — the existing `ww linux switch-keys` only handled X11). It falls back to `setxkbmap` for plain X11 sessions.

Toggle behavior, exactly as requested:
- No swap → enables `ctrl:swapcaps`
- Already swapped → removes it (back to default)
- Other xkb options are preserved (only `ctrl:swapcaps` is added/removed)

Bonus explicit modes:
```
ww keyboard capslock-ctrl            # toggle
ww keyboard capslock-ctrl on         # force on
ww keyboard capslock-ctrl off        # force off
ww keyboard capslock-ctrl status     # show state
```

## Verified

Your machine already had `['ctrl:swapcaps']` set, so I tested the full cycle — status showed `ON`, toggle flipped it to `OFF`, a second toggle restored it to `ON`. Original state (`['ctrl:swapcaps']`) is preserved.