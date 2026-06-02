---
audio: false
generated: true
image: false
lang: en
layout: post
title: Warp Terminal Modern UX Features
translated: false
type: note
---

**Question:** How do people use Warp as a more convenient terminal manager (not as an AI agent session)?

**Answer:**

Warp's core value beyond AI is as a **modern terminal UX** — here's what people actually use it for:

---

## 1. Blocks — The Killer Feature

Every command + its output is a **discrete "block"**. This means:

- Click any block to select/copy just that output — no mouse-drag hell
- Scroll through history block-by-block, not line-by-line
- Share a block as a permalink (useful for async debugging with teammates)
- Re-run any past block from history without retyping

This alone replaces most of what people use tmux scrollback + mouse copy for.

---

## 2. Tabs + Split Panes (Without tmux Config Hell)

```
Cmd+T          → new tab
Cmd+D          → split right
Cmd+Shift+D    → split down
Cmd+[ / Cmd+] → switch panes
```

No `.tmux.conf`, no prefix key, no muscle memory rewiring. For someone who just wants splits without learning tmux keybindings.

---

## 3. Input Editor That Behaves Like a Real Editor

- **Multi-line editing** natively — paste a 10-line bash script, edit it inline before running
- Cursor movement with arrow keys, home/end, Option+arrow for word jump
- No more `set -o vi` hacks just to edit a long command
- Syntax highlighting in the prompt itself

---

## 4. Command History Search (Better Than `Ctrl+R`)

- `Ctrl+R` in Warp opens a fuzzy-search history panel with full output preview
- Filter by directory, time, exit code
- For you specifically — with 1.5B tokens/yr of LLM usage, your shell history is a knowledge base. Warp makes it searchable.

---

## 5. Workflows (Saved Commands with Parameters)

```yaml
# Stored as a workflow
name: SSH to workstation
command: ssh lzw@192.168.1.36
tags: [infra, remote]
```

- Fill-in-the-blank parameterized commands
- Shared across machines via Warp account sync
- Think of it as a personal runbook, but in-terminal
- `Ctrl+Shift+R` to open workflow browser

For your setup: SSH to workstation, `scp` patterns, `nvidia-smi` watchers, model training launchers — all saveable.

---

## 6. Session Restoration

Unlike iTerm2, Warp restores open tabs/panes and their working directories on restart. No session manager plugin needed.

---

## 7. Theme + Prompt (Without Oh-My-Zsh Overhead)

- Built-in theme editor (GUI, not config files)
- Works with existing Starship/p10k prompt — doesn't override it
- Font rendering is noticeably sharper (GPU-accelerated, written in Rust/Metal)

---

## What People DON'T Use It For (vs. tmux)

| Feature | tmux | Warp |
|---|---|---|
| Remote session persistence (SSH detach) | ✅ | ❌ |
| Works on remote server | ✅ | ❌ (local only) |
| Scriptable via config | ✅ | Partial |
| Pair/share terminal session | ✅ | ❌ |

**Bottom line:** Warp doesn't replace tmux for remote server work. For your workstation at `192.168.1.36` — you still want tmux there. Warp is the local terminal that replaces iTerm2 + a bunch of plugins.

---

## Practical Config for Your Workflow

Turn off the AI noise if you just want the terminal UX:

```
Settings → AI → Disable AI suggestions
Settings → Features → Turn off Warp Drive if not needed
```

Then you have a fast, block-based, GPU-rendered terminal with good splits and searchable history — no agent involved.
