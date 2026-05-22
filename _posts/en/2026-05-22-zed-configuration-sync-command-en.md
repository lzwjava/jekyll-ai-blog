---
audio: false
generated: true
image: false
lang: en
layout: post
title: Zed Configuration Sync Command
translated: false
type: note
---

Done. Here's what happened:

**`~/.config/zed/settings.json`** — set `"existing_window"` → `"new_window"` so CLI/double-click always spawns a new window.

**`ww sync zed`** — new subcommand added. Pattern matches `sync_ssh` / `sync_bashrc`:

```
ww sync zed          sync ~/.config/zed/ local → remote
ww sync zed back     sync ~/.config/zed/ remote → local
```

Files changed (commit `210276a`, pushed to `main`):

| File | Change |
|---|---|
| `ww/sync/remote.py` | +`sync_zed()` function — syncs `~/.config/zed/` via scp |
| `ww/main.py` | +help text line, +dispatch block for `zed` |
| `README.md` | +row in sync table |
| `~/.config/zed/settings.json` | `existing_window` → `new_window` |

To test it works:

```
ww sync --help       # confirm zed shows up in the list
ww sync zed forth    # pushes local zed config to remote
```

(It'll time out on scp unless a remote is reachable via `WW_REMOTE_IP` — the dispatch itself is confirmed working.)