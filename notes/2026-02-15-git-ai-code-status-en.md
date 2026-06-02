---
audio: false
generated: true
image: false
lang: en
layout: post
title: Git Status for AI Code Changes
translated: false
type: note
---

Question: What is the usage and benefit of running "git status" when working with coding assistants like Claude or Codex, especially in the context of modified and untracked files?

Answer:

Yes — using `git status` is one of the most effective and lightweight ways to quickly understand **what a coding assistant (Claude, Cursor, Windsurf, Aider, Codex, etc.) has actually changed** in your project.

### Typical workflow when using AI coding assistants

1. You ask the AI to implement a feature / fix a bug / refactor something
2. The assistant either:
   - writes code in chat → you copy-paste
   - directly edits files (Claude in IDE, Cursor, Aider, continuedev, etc.)
3. After the AI finishes → **immediately** run:

```bash
git status
# or shorter
git st
# or even
git diff --stat
```

This gives you instant visibility:

| What git status shows          | Meaning in AI coding context                                 | Common next action                          |
|-------------------------------|---------------------------------------------------------------|---------------------------------------------|
| `modified: path/to/file.py`   | AI changed existing file                                      | `git diff path/to/file.py` to review        |
| `Untracked files: scripts/...`| AI created new file(s)                                        | `git add` if good, or `rm` if unwanted      |
| `deleted: oldfile.js`         | AI removed file (sometimes by accident)                       | `git restore --staged` or `git rm --cached` |
| nothing to commit, working tree clean | AI made no file changes (maybe only printed code in chat)    | check chat / terminal output                |

### Your concrete example

```
Changes not staged for commit:
  modified: .claude/settings.local.json

Untracked files:
  scripts/clash/clash_select_provider.py
```

Interpretation:

- Claude (or a Claude-powered tool) most likely **changed its own config** → `.claude/settings.local.json` (very common)
- Claude / you / another tool **created a new Python script** → `scripts/clash/clash_select_provider.py`

So the fastest way to verify whether the new script works:

```bash
# Review what was created
cat scripts/clash/clash_select_provider.py

# Or open in editor
code scripts/clash/clash_select_provider.py     # VS Code
nvim scripts/clash/clash_select_provider.py     # Neovim

# Run & test
python scripts/clash/clash_select_provider.py
# or
python3 scripts/clash/clash_select_provider.py
# or with arguments if needed
python scripts/clash/clash_select_provider.py --help
```

### Recommended 10-second checklist after AI finishes working

```bash
git status -s          # compact view
git diff --stat        # summary of changes
git diff               # if you want to see everything (sometimes too much)
```

Then decide:

- Good changes → `git add . && git commit -m "feat: add clash provider selector (Claude)"`
- Bad changes → `git restore .` or `git restore --staged .` or even `git reset --hard` (careful!)
- Only want some files → `git add scripts/clash/clash_select_provider.py`

So yes — `git status` is probably **the most valuable 5-character command** when you frequently use AI assistants to write or modify code.

References:

- None required for this git usage explanation.
