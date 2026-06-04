---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixed Tailscale Version Mismatch
translated: false
type: note
---

Done. Here's the final state:

```
══════════════════════════════════════════
  Tailscale — Cleaned Up
══════════════════════════════════════════

Before:
  Homebrew CLI:   v1.96.4  (old, mismatched)
  GUI app:        v1.98.5  (running tailscaled)
  Warning:        version mismatch on every command

After:
  Single install: v1.98.5  (GUI app + wrapper script)
  Binary:         /opt/homebrew/bin/tailscale → wrapper
                  → /Applications/Tailscale.app/Contents/MacOS/Tailscale
  Daemon:         GUI app's system extension (no sudo needed)
  Warning:        gone ✓

Status:
  lzw-mac → to:   8ms, direct LAN, WireGuard encrypted
  SSH:            public key auth, working
══════════════════════════════════════════
```

The wrapper script at `/opt/homebrew/bin/tailscale` forwards all args to the GUI app's binary, so `tailscale status`, `tailscale ping`, etc. all work as expected — version-matched and no warnings.
