---
audio: false
generated: true
image: false
lang: en
layout: post
title: Maps Office Distance Command Added
translated: false
type: note
---

Done. Added `ww maps office` command. Here's the summary:

Files changed:

- ww/maps/maps.py    — added cmd_office(),_haversine_km(), registered in COMMANDS + help
- ww/main.py         — added to Maps help section (alphabetical)
- ~/.zsh/completions/_ww — added 'office' to maps_cmds (alphabetical)

Usage:
  ww maps office <lat,lng>
  ww maps office "22.838889,114.498969"

What it shows:

- Reverse-geocoded FROM address
- TO: OneLink office (万菱国际中心, Tianhe Rd 230-232)
- Straight-line distance (haversine)
- Driving route distance + time (Google Directions API)
- Transit distance + time (if available)
- Route overview with highway names
- Step-by-step directions (first 5 + last 3)
- Driving/straight-line ratio

Run `source ~/.zshrc` or `autoload -Uz compinit && compinit` to pick up tab completion.
