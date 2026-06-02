---
audio: false
generated: true
image: false
lang: en
layout: post
title: Homebrew-pip binary symlink conflict
translated: false
type: note
---

**Problem**
`brew install hf` installed successfully into the Cellar but failed at the `brew link` step — it couldn't create symlinks into `/opt/homebrew/bin/` because `hf` and `tiny-agents` were already there.

**Root Cause**
A pip-installed `huggingface-hub` package (v0.29.3) had already placed console scripts at:
- `/opt/homebrew/bin/hf` — Python script targeting `python3.14`
- `/opt/homebrew/bin/tiny-agents` — Python script targeting `python3.14`

The Homebrew `hf` formula (v1.8.0) tries to symlink the exact same paths, so linking failed with a conflict.

**Why This Happens**
Both pip and Homebrew manage files in `/opt/homebrew/bin/` on your setup because Homebrew's Python is the system Python. When you `pip install` a package with CLI entry points, pip writes scripts into Homebrew's bin directory. Homebrew doesn't know about these pip-managed files and vice versa — no conflict detection exists between the two.

**Options Considered**
1. `brew link --overwrite hf` — forces Homebrew's symlinks, but leaves two copies of huggingface-hub installed (brew + pip). Maintenance headache.
2. `pip uninstall huggingface-hub && brew link hf` — clean, but swaps pip for brew as the manager. Downgrade from 1.12.0 → 1.8.0.
3. `brew uninstall hf` — remove the brew copy entirely, keep pip. **Chosen approach.**

**Resolution**
`brew uninstall hf` removed the brew Cellar copy (1,140 files, 19.3MB). The pip-installed `hf` CLI remained functional at version 1.12.0 — actually newer than the brew version 1.8.0.

**Takeaway**
When a CLI tool is available via both pip and brew, pick one manager and stick with it. Mixing them causes symlink conflicts. For Python-native tools like `huggingface-hub`, pip/uv is usually the better choice — faster updates, fewer dependencies, and no brew formula maintenance lag.
