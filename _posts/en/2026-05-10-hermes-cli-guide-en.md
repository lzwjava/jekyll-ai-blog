---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Model CLI Usage Guide
translated: false
type: note
---

`hermes model` is interactive only — there's no `set` subcommand and no `--global` flag. It only takes auth/portal flags (`--portal-url`, `--no-browser`, etc.) and then drops you into the picker (`hermes_cli/main.py:9161-9201`).

Two options:

1. Run the picker:
   ```
   hermes model
   ```

2. Set it non-interactively via `config set` (`hermes_cli/main.py:10108-10112`):
   ```
   hermes config set model anthropic/claude-opus-4.7
   ```

There's no `--global` switch anywhere in the parser — `hermes config set` writes to the single user config (`hermes config path` shows where). If you want to scope it per-project, you'd have to manage that with env/working dir, not a CLI flag.
