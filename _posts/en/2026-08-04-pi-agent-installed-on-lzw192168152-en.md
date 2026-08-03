---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pi Agent Installed on lzw@192.168.1.52
translated: false
type: note
---

Pi agent is installed and working on `lzw@192.168.1.52` (the warnings are just from `-i` without a TTY, harmless).

**What was done:**

1. **Node.js 22.23.2 + npm 10.9.8** installed standalone (no sudo) at `~/.local/share/pi-node/current/` — matching pi's own installer convention. Downloaded via wget since `curl` isn't on the remote (the installer's own node-bootstrap used curl, so I did this manually).
2. **PATH persisted**: `~/.local/share/pi-node/current/bin` added to both `~/.bashrc` and `~/.profile`.
3. **pi 0.83.0 installed** via the official installer (`pi.dev/install.sh`):
   - Ran without a TTY → auto-selected install, used npm to install `@earendil-works/pi-coding-agent` (132 packages).
   - Binary at `~/.local/share/pi-node/current/bin/pi` — verified `pi --version` → `0.83.0` in a fresh login shell.

**Remote summary so far:**
- `~/bin/mihomo` + config, running in tmux session `mihomo` (proxy working via Hysteria2)
- `~/bin/tmux` 3.5a (AppImage-extracted, rootless)
- `~/.local/share/pi-node/current/bin/pi` 0.83.0

Run `pi` in a new SSH session on that machine to start using it.