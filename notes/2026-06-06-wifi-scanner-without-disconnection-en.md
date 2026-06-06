---
audio: false
generated: true
image: false
lang: en
layout: post
title: WiFi Scanner Without Disconnection
translated: false
type: note
---

Done. Here's the summary:

Created `ww network wifi-scan-best` — a WiFi signal scanner that works without disconnecting.

Files changed:

- NEW:  ww/network/wifi_scan_best.py — CoreWLAN (macOS) + nmcli (Linux) scanner
- MOD:  ww/main.py — wired `wifi-scan-best` subcommand + help text
- MOD:  pyproject.toml — added pyobjc-framework-CoreWLAN dependency
- MOD:  ~/.zsh/completions/_ww — tab completion entry

Usage:
  uv run ww network wifi-scan-best

Features:

- macOS: CoreWLAN via PyObjC (real RSSI, noise, SNR, channel, bandwidth)
- Linux: nmcli fallback
- Groups networks by 2.4GHz vs 5GHz
- Sorts by signal strength
- Marks current network with <-- YOU
- Recommends best network with actionable switch command
