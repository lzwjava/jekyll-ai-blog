---
audio: false
generated: true
image: false
lang: en
layout: post
title: Improved Help Messages for Subcommand Groups
translated: false
type: note
---

Done. Here's a summary of what changed in `ww/main.py`:

Every group that has subcommands (`github`, `macos`, `image`, `proc`, `utils`, `java`, `network`, `git`, `pdf`, `copilot`, `sync`, `cloudflare`, `clash`, `llm`, `env`, `latest`) now shows a help message when run with no subcommand (or `--help`/`-h`), instead of printing the unhelpful "Unknown X command: ".

Groups that don't have subcommands (`note`, `screenshot`, `search`, `read`, `marp`, `whisper`, etc.) were already handled correctly — they run their default action or have their own argument parsing. No change needed there.