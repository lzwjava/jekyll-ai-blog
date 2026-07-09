---
audio: false
generated: true
image: false
lang: en
layout: post
title: Permission Denied Dialout Group Fix
translated: false
type: note
---

Here's the full picture:

---

## ✅ Problem Found: Permission denied — not in `dialout` group

**The fix is applied**, but here's what was happening and what you need to know:

### Root Cause

- `/dev/ttyUSB0` exists and your Arduino (via **CH340** USB-serial chip, ID `1a86:7523`) is detected
- The port is owned by `root:dialout` with permissions `rw-rw----` (660)
- Your user wasn't in the `dialout` group → **no read/write access**

### What I did

- Added you to the `dialout` group via `usermod -aG dialout xiaoxin`
- Verified with `newgrp dialout` that the port is now accessible

### You still need to

**Log out and log back in** (or reboot) for the group change to stick permanently in your terminal emulator, or do:

```bash
exec su - $USER
```

in the current terminal to get a new login shell with the `dialout` group active.

### Quick test once the group is active

```bash
screen /dev/ttyUSB0 9600
```

Or with your Arduino IDE / app — it should now connect fine.

### Summary

| Item | Status |
| ------ | -------- |
| Device detected | ✅ CH340 on `/dev/ttyUSB0` |
| Driver loaded (`ch341-uart`) | ✅ |
| Permissions | ✅ Fixed (was missing `dialout` group) |
| Port in use by another process | ❌ No — clear to connect |
| App can connect | ⏳ After re-login / `exec su - $USER` |
