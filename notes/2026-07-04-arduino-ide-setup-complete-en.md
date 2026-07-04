---
audio: false
generated: true
image: false
lang: en
layout: post
title: Arduino IDE Setup Complete
translated: false
type: note
---

Done. Arduino IDE **2.3.10** installed and configured. Here's the summary:

**What was installed:**

- `~/Apps/arduino-ide.AppImage` (193M) — downloaded from GitHub releases
- `~/.local/share/applications/arduino-ide.desktop` — shows up in your app menu under "Development" / "Electronics"
- `~/.local/share/icons/.../arduino-ide.png` — app icon

**What was configured:**

- **dialout group** — you're already a member (active immediately for new logins)
- **brltty removed** — that braille display daemon was installed and would've grabbed CH340 clone ports. It's gone now.
- **libfuse2** was already installed, so the AppImage can run

**To launch:**

- From app menu: search "Arduino IDE"
- From terminal: `~/Apps/arduino-ide.AppImage &`

**When plugging in an Arduino Uno:**

- Genuine Uno → `/dev/ttyACM0`
- CH340 clone → `/dev/ttyUSB0` (driver is kernel-built-in, no install needed)
- Check with `ls /dev/tty{ACM,USB}*`

**Note:** The dialout group change takes effect on next login. If you want to use it in this session without logging out, run `newgrp dialout` in the terminal where you'll start the IDE.
