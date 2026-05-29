---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disabling Approvals in Hermes
translated: false
type: note
---

Here's what I found:

Three ways to skip approvals, from easiest to most permanent:

1. **`/yolo` slash command** (easiest, per-session)
   Just type `/yolo` inside a hermes session. Toggles YOLO mode on/off. All dangerous commands auto-approved for that session. Does NOT persist to config — resets when you restart hermes.

2. **`HERMES_YOLO_MODE=1` env var** (per-process, no config edit)
   ```bash
   HERMES_YOLO_MODE=1 hermes
   ```
   Frozen at module import time (line 29 of `tools/approval.py`) — can't be flipped mid-session even by prompt injection. Good for "always skip in this shell".

3. **Edit `~/.hermes/config.yaml`** (permanent, all sessions)
   ```yaml
   approvals:
     mode: off
   ```
   The code at `tools/approval.py:825-837` handles YAML 1.1's quirk where bare `off` is parsed as boolean `False` — it normalizes that to the string `"off"` correctly, so both `mode: off` and `mode: "off"` work.

**Do you need to manually edit config.yaml?** No. The `/yolo` command is the fastest way — one keystroke in-session. But it's per-session only. If you want it permanent without editing the file, you'd need to use the env var approach or add `export HERMES_YOLO_MODE=1` to your shell profile.

There's no `hermes config set approvals.mode off` CLI subcommand exposed — the `/config` command is read-only (shows current config). The `save_config_value()` function exists internally and is used by commands like `/reasoning`, but no slash command wraps it for arbitrary config keys. That would actually be a nice addition — a generic `/config set <key> <value>` command.

**My recommendation:** Just type `/yolo` at the start of each session. It's one command, zero config changes, and the status bar shows `⚠ YOLO` so you know it's active.