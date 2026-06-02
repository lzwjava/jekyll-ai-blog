---
audio: false
generated: true
image: false
lang: en
layout: post
title: Terminal Git Tools Versus GitHub Desktop
translated: false
type: note
---

**Question:** The file viewer in GitHub Desktop is great, right? You can directly navigate to files when checking them?

**Answer:**

GitHub Desktop's file viewer is decent but honestly pretty limited compared to what you probably want. Here's the real breakdown:

**What GitHub Desktop does well:**
- Side-by-side or unified diff view for changed files
- Click a file in the changed files list → jump to its diff
- Syntax highlighting on diffs

**Where it falls short:**
- You're only seeing *diffs*, not the full file in context
- No search across files
- No tree navigation for the full repo
- Slow for large changesets

**Better alternatives for your workflow (terminal-first):**

```bash
# See all changed files
git status

# Diff a specific file
git diff path/to/file.py

# Open changed files directly in your editor
git diff --name-only | xargs code  # VSCode
git diff --name-only | xargs nvim  # neovim

# Interactive diff browser (best CLI option)
git diff | delta        # https://github.com/dandavison/delta
git diff | tig         # ncurses git browser
```

**`delta`** is the biggest upgrade — it gives you syntax-highlighted, side-by-side diffs right in the terminal, line numbers, and even hyperlinks to files. Install:

```bash
brew install git-delta
```

```ini
# ~/.gitconfig
[core]
    pager = delta
[delta]
    side-by-side = true
    navigate = true
    line-numbers = true
```

**`tig`** gives you a full ncurses TUI for browsing commits, diffs, file trees — closer to what GitHub Desktop offers but in terminal.

Given you're terminal-first on M2, `delta` + `tig` will beat GitHub Desktop's file view every time. GitHub Desktop is mostly useful for people who avoid the terminal — not your case.
