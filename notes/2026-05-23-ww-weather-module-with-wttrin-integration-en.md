---
audio: false
generated: true
image: false
lang: en
layout: post
title: ww Weather Module with wttr.in Integration
translated: false
type: note
---

All good. Here's what was added:

**New file:** `/Users/lzwjava/projects/ww/ww/weather/weather.py`
- Uses `wttr.in` (free, no API key) for weather data
- Supports three modes:
  - `ww weather` — full weather report for auto-detected location
  - `ww weather <city>` — full report for a specific city
  - `ww weather <city> --oneline` — one-line summary (e.g. `guangzhou: ☁️  +81°F`)
  - `ww weather <city> --json` — structured JSON output

**Modified:** `/Users/lzwjava/projects/ww/ww/main.py`
- Added `weather` to help text and dispatch

Note: auto-detect location is IP-based, so it shows the proxy location (Los Angeles) when the VPN is on. For accurate local weather, pass `Guangzhou` explicitly.