---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rain Detector for Windshield View
translated: false
type: note
---

Done. Here's what was added:

**New file:** `ww/weather/rain.py`

- Records 3s video from webcam via ffmpeg (avfoundation)
- Extracts 5 frames (1 per second)
- Sends all frames to vision model (VISION_MODEL or MODEL from .env) via OpenRouter
- Rates rain on a 0-5 scale with detail and advice
- Designed for in-car use: prompt tells the model the webcam faces the windshield, window may be closed

**Usage:**

```
ww rain              # 3-second video, analyze rain
ww rain --seconds 5  # longer capture
ww rain --keep       # keep the video file
ww rain --debug      # show model/request info
ww weather rain      # also works
```

**Files modified:**

- `ww/main.py` — routing for `ww rain` (top-level) and `ww weather rain`, help text, all_groups
- `~/.zsh/completions/_ww` — `rain` in top-level commands + `weather_cmds` array with rain subcommand

**How it works in the car:** Point the laptop webcam at the windshield. Run `ww rain`. It captures a short video, extracts frames, and tells you the rain intensity (0=clear to 5=torrential) with a practical advice line like "close window" or "safe to open window slightly".
