---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pi Installation via SSH Workaround
translated: false
type: note
---

Done. Pi is installed on `lzw@192.168.1.137` and verified working.

## What I did

**The obstacle:** the official installer (`curl -fsSL https://pi.dev/install.sh | sh`) requires Node.js ≥ 22.19 + npm and a real terminal — over SSH without a TTY it refuses to install Node ("No terminal detected"), and Debian 13's apt only offers Node 20.19 (too old) while `sudo` needs a password. So I replicated its non-sudo path deterministically:

1. **Standalone Node.js v22.23.3** — downloaded from `nodejs.org/dist/latest-v22.x`, sha256-verified, extracted to `~/.local/share/pi-node/` with a `current` symlink (same method/location the official installer uses; no sudo required).
2. **Ran the official Pi installer** with Node on PATH — it completed fully non-interactively: managed install of **Pi 1.2.0** with 119 pinned dependencies, smoke-test verified, activated.
3. **PATH setup** — installer put the launcher in `~/.local/bin` (already added by Debian's `~/.profile` for login shells); I appended a guarded line to `~/.bashrc` so non-login interactive shells also find `pi` plus the standalone Node.

## Result

```
$ ssh lzw@192.168.1.137
$ pi --version
1.2.0
```

- Binary: `/home/lzw/.local/bin/pi` (managed install in `~/.pi/agent/`)
- Node: `~/.local/share/pi-node/current` (the pi launcher auto-adds it to PATH at runtime)
- Verified: `bash -lc "pi --version"` → 1.2.0, `bash -ic "pi --version"` → 1.2.0
- Update later with: `pi update`
