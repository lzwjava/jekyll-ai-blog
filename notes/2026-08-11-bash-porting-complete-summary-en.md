---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bash Porting Complete Summary
translated: false
type: note
---

Done. Everything is ported and verified working.

## What went into `~/.bashrc`

**Ported from `.zprofile` (Mac) → Linux tweaks:**
- `GLOBAL_PROXY` — points at `127.0.0.1:7890`, which matches your **mihomo** instance already running (7890 mixed / 7891 socks / 9090 dashboard)
- `start_proxy` / `stop_proxy` — stays **off by default** (commented, same as your original); `stop_proxy` now uses `unset` instead of `export VAR=` (cleaner)
- `start_git_proxy` / `stop_git_proxy` — git global config, verified working
- `gitpush` / `gitcommit` + aliases `gpa` / `gca`

**Dropped (don't exist on this machine):**
- `/opt/homebrew` PATH + `brew shellenv` — no Homebrew on Linux
- `SSL_CERT_FILE=~/bin/cacert.pem` — no such file; no ruby/jekyll installed
- `rougify` alias — no rouge project
- The Mac PATH export itself

## Ghostty note
Ghostty runs bash as your shell, and since `.profile` sources `.bashrc`, these load in both login and interactive shells — nothing extra needed. Just **restart ghostty** (or run `source ~/.bashrc`) and you'll have `start_proxy`, `gpa`, etc.

Testing confirmed: aliases, functions, and proxy env set/unset all work in a fresh bash. I also cleaned the git proxy config back to unset after testing.

One thing to be aware of: `gitcommit`/`gitpush` run `git add -A` on everything — same as your original, just flagging since that's a footgun on a shared repo.