---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix tmux xterm-ghostty problem
translated: false
type: note
---

**Question:** Why is tmux complaining about `xterm-ghostty` being an unsuitable terminal?

**Answer:**

tmux is checking the `TERM` environment variable (which your shell set to `xterm-ghostty` because you're using Ghostty terminal) against its database of known terminal capabilities. The issue: tmux doesn't recognize `xterm-ghostty` in its terminfo database — either because:

1. **Ghostty's terminfo isn't installed** — Ghostty is newer, and your system's terminfo database doesn't have an entry for it yet
2. **TERM mismatch** — Your shell exported `TERM=xterm-ghostty`, but tmux only knows about standard terms like `xterm-256color`, `screen`, etc.

**Fix (ranked by preference):**

```bash
# Option 1: Use a compatible TERM value (simplest)
TERM=xterm-256color tmux

# Option 2: Set TERM in your shell profile (~/.zshrc or ~/.bash_profile)
export TERM=xterm-256color

# Option 3: Install Ghostty's terminfo (proper solution)
# In Ghostty's repo or check their docs for installation
# Usually something like:
tic -xe ghostty ~/.config/ghostty/terminfo  # if Ghostty provides this
```

**What I'd do:** Use `TERM=xterm-256color` as a quick fix. If Ghostty is your daily driver, add `export TERM=xterm-256color` to your shell config. This is safe — most modern terminals (including Ghostty) are compatible with xterm-256color's capability set.

Then:

```bash
lzw@to:~/projects/private-projects/whisper-playground/yangyang2$ tmux
```

Should work. If you want native Ghostty support in tmux long-term, check Ghostty's docs for terminfo installation — but honestly, xterm-256color works fine.