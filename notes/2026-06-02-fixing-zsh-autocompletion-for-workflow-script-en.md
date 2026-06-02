---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Zsh Autocompletion for Workflow Script
translated: false
type: note
---

That's expected — the terminal uses bash, not zsh. You'll need to reload in your zsh: `autoload -Uz compinit && compinit`.

Here's what I changed:

**`ww/action/action.py`** — rewrote to use argparse with defaults:
- Default workflow: `gh-pages.yml`
- Default repo: `lzwjava/jekyll-ai-blog` (consistent with `actions check`)
- Added `--repo` and `--ref` flags
- `ww action` (no args) → triggers `gh-pages.yml` on `lzwjava/jekyll-ai-blog`
- `ww action some-workflow.yml` → triggers that workflow
- `ww action --ref main` → triggers default workflow on `main` branch

**`ww/main.py`** — updated help text to show `[workflow.yml]` (optional) instead of `<workflow.yml>` (required).

**`~/.zsh/completions/_ww`** — added `action)` case with `--repo`, `--ref` completions and `.yml` file glob.
