---
audio: false
generated: true
image: false
lang: en
layout: post
title: Zed Emacs-Style Navigation Keybindings
translated: false
type: note
---

Done. Here's what I set up:

**`~/.config/zed/keymap.json`**

| Keys | Action | Style |
|---|---|---|
| `Ctrl+x Ctrl+←` / `Ctrl+x Ctrl+→` | Go Back / Go Forward | **Emacs-like** (`C-x` prefix) |
| `Ctrl+x ←` / `Ctrl+x →` | Go Back / Go Forward | Emacs-like (shorter) |
| `Alt+←` / `Alt+→` | Go Back / Go Forward | Editor standard (fallback) |

### How it works

After you **Alt+click** a variable/function to jump to its definition:

1. **`Ctrl+x ←`** (or `Alt+←`) → jump back to where you came from
2. **`Ctrl+x →** (or `Alt+→`) → jump forward again

### Why these bindings

Since you mentioned Emacs: `Ctrl+x` (`C-x`) is the canonical Emacs prefix key, so `C-x ←` / `C-x →` feels natural for an Emacs user. `Alt+←`/`Alt+→` is also added as a familiar fallback that works across many editors.

### If you use Vim mode in Zed

If you ever enable `vim_mode` in settings, the context won't match. For Vim users, Zed defaults to `Ctrl+o` (go back) and `Ctrl+i` (go forward) — already Vim-standard. Let me know if you want those too.