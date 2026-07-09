---
audio: false
generated: true
image: false
lang: en
layout: post
title: Serial Port Access Confirmed
translated: false
type: note
---

## ✅ Confirmed — everything is working

| Check | Result |
| ------- | -------- |
| User in `dialout` group | ✅ Yes (via `sg dialout`) |
| `/dev/ttyUSB0` device | ✅ Present, CH340 active |
| Port permissions | ✅ `rw-rw----`, owned by `root:dialout` (20) |
| Read/write access | ✅ **Success** — port opened with `O_RDWR` |

The `usermod -aG dialout xiaoxin` was applied correctly. Your current shell just hadn't picked up the new group yet. Running commands via `sg dialout` (or `newgrp dialout`) activates it immediately.

### Two ways to make this permanent for new terminals

1. **Log out and log back in** (or reboot) — every new terminal will have `dialout` automatically.
2. **Or** just run this once in any new terminal you open:

   ```bash
   exec su - $USER
   ```

   (it'll prompt for your password, then start a fresh login shell)

Either way, the Arduino IDE and any serial tool (`screen`, `minicom`, `arduino-cli`) will now be able to connect to `/dev/ttyUSB0` without issues.
