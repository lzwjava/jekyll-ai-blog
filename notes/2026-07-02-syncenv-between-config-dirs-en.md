---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sync.env between config dirs
translated: false
type: note
---

Done. Here's the full summary:

## Changes

### New file: `ww/sync/ww.py`
- `sync_ww_env(direction="forth")` — copies `.env` between `~/.config/ww/.env` and `$CONFIG_DIR/ww/.env`
- `forth` (default): canonical → config dir
- `back`: config dir → canonical
- Uses `shutil.copy2` to preserve metadata, creates parent dirs if needed
- Prints a confirmation line on success

### Modified: `ww/main.py`
- Added `ww sync ww` handler in the sync dispatch block (same pattern as bashrc/zprofile — `direction` param with `forth` default)
- Added help text to both the main help page and the sync subcommand help

### Modified: `~/.zsh/completions/_ww`
- Added `'ww:Sync .env to/from CONFIG_DIR'` to the `sync_cmds` array
- Run `autoload -Uz compinit && compinit` in your zsh to pick it up
