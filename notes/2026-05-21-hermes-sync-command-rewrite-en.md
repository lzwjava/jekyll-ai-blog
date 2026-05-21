---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Sync Command Rewrite
translated: false
type: note
---

Here's a summary of all changes:

## What changed

### `ww/sync/remote.py` — `sync_hermes()` rewritten

- **Before**: synced only `~/.hermes/config.yaml` to/from a hardcoded remote host (via env vars `WW_REMOTE_IP`/`WW_REMOTE_USER`)
- **After**: syncs the entire `~/.hermes/` directory, with explicit `from_host` and `to_host` params
- Each host is either `localhost` or `user@ip`
- `forth` = `from_host` → `to_host`
- `back` = `to_host` → `from_host`
- Falls back to env vars when `to_host` is empty (backward compat)

### `ww/main.py` — dispatch updated

- Moved `direction = _pop_subcmd() or "forth"` into each subcommand (bashrc, zprofile, ssh) that needs it, instead of at the sync group level
- For `hermes`, uses `argparse` to handle `--from-host`, `--to-host`, and `--help` properly
- Updated help text

## Usage

```
# Push local ~/.hermes/ to remote
ww sync hermes forth --from-host localhost --to-host lzw@192.168.1.36

# Pull remote ~/.hermes/ back to local
ww sync hermes back --from-host localhost --to-host lzw@192.168.1.36

# With env vars (backward compat - no flags needed)
ww sync hermes forth

# Help
ww sync hermes --help
```