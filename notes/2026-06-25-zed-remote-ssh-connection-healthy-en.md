---
audio: false
generated: true
image: false
lang: en
layout: post
title: Zed Remote SSH Connection Healthy
translated: false
type: note
---

Diagnosis looks healthy. Here's the full picture:

HOW ZED SSH REMOTE WORKS
========================

1. You run: zed ssh://lzw@192.168.1.36//mnt/data/zz/

2. Zed SSHs into the remote, uploads a ~100MB binary to ~/.zed_server/
   This is the "Installing development server" step.

3. The binary runs as a daemon on the remote, handling:
   - File watching (inotify)
   - LSP servers (Python, etc.)
   - Terminal sessions
   - Git operations

4. Local Zed <-> Remote server communicate over the SSH tunnel.

YOUR CURRENT STATE
==================

Everything is actually working:

- Local Zed:  1.7.2
- Remote:     1.7.2 (matches!)
- Binary:     ~/.zed_server/zed-remote-server-stable-1.7.2... (107MB, present)
- Processes:  3 running (proxy + server + crash handler)
- Logs:       Actively scanning Python envs, processing diagnostics

The "installing development server" message you saw was likely:

- First connection: downloading the 100MB binary (took ~2 min)
- Or: a UI status that lingered but the server is now running

THE "no worktree" WARNINGS
===========================

These are harmless:
  WARN skipping diagnostics update, no worktree found for path "..."

This happens when LSP (Pyright/ruff) reports diagnostics for files
that Zed's worktree hasn't indexed yet. It's a known benign warning,
not an error.

IF IT'S STILL STUCK
====================

If the UI is still showing "installing" and you can't edit files:

# Kill remote server, let Zed re-upload

  ssh lzw@192.168.1.36 "rm -rf ~/.zed_server/"

# Then reopen in Zed

But from what I can see, your connection is live and working.
The "installing" message should have disappeared once the server started.
