---
audio: false
generated: true
image: false
lang: en
layout: post
title: Zed SSH Remote Path Canonicalization Fix
translated: false
type: note
---

Here's the full summary:

## Problem

Zed SSH remote opened `ssh://lzw@192.168.1.36/mnt/data/deepseek-v4-inference/` but showed an empty project — directory existed with 8 files (model.py, kernel.py, generate.py, etc.) but nothing appeared in the editor.

## Root Cause

Two issues found in `~/Library/Logs/Zed/Zed.log`:

1. **Path canonicalization failure** (primary):
   ```
   ERROR [worktree] failed to canonicalize root path "/mnt/data/deepseek-v4-inference": 
   canonicalizing "/mnt/data/deepseek-v4-inference": No such file or directory (os error 2)
   ```
   The Zed remote server process could see the path (it attempted file watching) but failed during `std::fs::canonicalize()`. Likely a stale remote server binary that had cached bad state.

2. **inotify watch limit exhausted** (secondary):
   ```
   ERROR [crates/worktree/src/worktree.rs:5018] (remote server) OS file watch limit reached.
   ```
   Remote had `max_user_watches=65536` (default) — too low for Zed's file watcher.

## Fixes Applied

| Fix | Command | Effect |
|-----|---------|--------|
| Bump inotify | `echo 'fs.inotify.max_user_watches=524288' \| sudo tee -a /etc/sysctl.conf && sudo sysctl -p` | 65536 → 524288 |
| Delete stale server | `rm -rf ~/.zed_server/` | Forces Zed to re-upload fresh binary (~100MB) |

## Key Takeaways

- Zed SSH remote auto-downloads a server binary to `~/.zed_server/` on the remote host. If it gets stale or corrupted, delete it and let Zed re-download.
- Always check `~/Library/Logs/Zed/Zed.log` on the client side — it logs remote server errors too (prefixed with `(remote server)`).
- Absolute paths in Zed SSH URLs need double slash: `ssh://host//absolute/path` not `ssh://host/absolute/path`.
- Default inotify limit (65536) is too low for Zed. Bump to 524288 on any machine used as Zed remote.
- The remote machine (Ubuntu 24.04, x86_64) needs no Zed installed — the server binary is self-contained.

## Note

Saved to `notes/2026-05-25-zed-remote-ssh-canonicalization-bug-fixes-en.md` (was already there from earlier diagnosis).