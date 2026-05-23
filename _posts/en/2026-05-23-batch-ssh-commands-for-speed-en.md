---
audio: false
generated: true
image: false
lang: en
layout: post
title: Batch SSH Commands for Speed
translated: false
type: note
---

Pushed. Here's the summary:

Root cause: 9 separate SSH round-trips per remote machine. Each SSH handshake = TCP + key exchange + auth. DMIT alone was ~18s.

Fix: batch all commands into one shell script, pipe via stdin to `ssh ... bash`. One connection, one round-trip.

Results:
  local:       0.1s (unchanged)
  workstation: 0.9s (was ~5s)
  dmit:        2.5s (was ~18s)
  all three:   3.3s (was ~30s+)

Also fixed macOS fallbacks — `cmd | awk` returns 0 even when `cmd` fails, so `|| fallback` never fired. Replaced with explicit `if command -v` checks.