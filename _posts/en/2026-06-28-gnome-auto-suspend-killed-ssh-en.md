---
audio: false
generated: true
image: false
lang: en
layout: post
title: GNOME auto-suspend killed SSH
translated: false
type: note
---

All good. Here's what happened and what I fixed:

**Root cause:** GNOME auto-suspended the machine after 15 minutes idle (`sleep-inactive-ac-type: suspend`). This killed SSH and all running processes (including mihomo).

**Fixes applied:**
- Disabled auto-suspend on both AC and battery (`sleep-inactive-*-type: nothing`)
- Restarted mihomo (it doesn't survive reboot since it's `nohup`, not systemd)

**Verified:**
- Hermes v0.17.0 running on Fedora ✅
- Mihomo proxy working (exit IP 69.63.219.52) ✅
- `hermes chat -q` works end-to-end ✅

**Note:** mihomo still won't auto-start on reboot. Want me to create a systemd service for it so it persists across reboots?
