---
audio: false
generated: true
image: false
lang: en
layout: post
title: Device group access fix needed.
translated: false
type: note
---

Confirmed — here's the current state:

### `/dev/ttyUSB0` exists
```
crw-rw---- 1 root dialout 188, 0 Jul  8 19:21 /dev/ttyUSB0
```
The device is present and the CH340 driver is active.

### User `xiaoxin` is **NOT yet in `dialout`** group in this session
```
groups: xiaoxin adm cdrom sudo dip plugdev users lpadmin sambashare
```
`dialout` is **missing** — the `usermod` was applied previously (good), but this shell session still has the old group set. The port is currently **inaccessible** from this terminal.

### What you need to do

**Option A — quick fix in this terminal (no logout):**
```bash
exec su - $USER
```
This starts a fresh login shell with the `dialout` group active. After that, verify with `groups` — you should see `dialout` in the list.

**Option B — logout & login / reboot** (permanent for all new terminals).

### Quick test after either option
```bash
ls -l /dev/ttyUSB0 && screen /dev/ttyUSB0 9600
```
Or just open the Arduino IDE — it should be able to detect and connect to the port now.

Want me to run `exec su - $USER` for you here, or would you prefer to do it yourself?