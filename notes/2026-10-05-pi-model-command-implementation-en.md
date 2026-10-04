---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pi Model Command Implementation
translated: false
type: note
---

Done. The `ww pi set-model` command is implemented, wired in, and the pi agent's default model is set to `openrouter/xiaomi/mimo-v2.6-flash`.

## What pi actually reads

Pi's startup model comes from `defaultProvider` + `defaultModel` in `<agent-dir>/settings.json` (default `~/.pi/agent/settings.json`, overridable via `PI_CODING_AGENT_DIR`).

## Changes

**New files**
- `ww/pi/__init__.py`
- `ww/pi/set_model.py` — parses `<provider>/<model>` (split at first `/`), or a full model id with `--provider`, merges into `settings.json` preserving other keys, prints previous → new value
- `ww/pi/show_model.py` — prints current `provider/model`

**`ww/main.py`**
- New `elif group == "pi":` dispatch block (`set-model`, `show-model`)
- Help text section `Pi:` in `_print_help()`
- Added `"pi"` to the unknown-command suggestion list

**`completions/_ww`** (repo source; refresh your shell with `ww completion install` then `autoload -Uz compinit && compinit`)
- `pi` entry in top-level `commands` array
- `pi_cmds` subcommand array
- `pi)` case in the subcommand dispatcher
- `subcmd2` case giving `set-model` its `--provider` flag completion

## Verified

```
$ uv run ww pi set-model openrouter/xiaomi/mimo-v2.6-flash
Previous: openrouter/xiaomi/mimo-v2.6-flash
Set:      openrouter/xiaomi/mimo-v2.6-flash
Saved to: /home/lzw/.pi/agent/settings.json

$ uv run ww pi show-model
openrouter/xiaomi/mimo-v2.6-flash
```

`~/.pi/agent/settings.json` now has `defaultProvider: openrouter`, `defaultModel: xiaomi/mimo-v2.6-flash` (it was already at that value; the write is confirmed). Ruff check + format pass on `ww/pi` and `ww/main.py`.

Note: AGENTS.md mentions `~/.zsh/completions/_ww`, but that installed copy doesn't exist on this machine — the repo file `completions/_ww` is the source that `ww completion install` copies, so I updated that.