---
audio: false
generated: true
image: false
lang: en
layout: post
title: Caps Lock Swapped to Ctrl Remote
translated: false
type: note
---

Verified — **it's already switched and active on `192.168.1.45`** ✅

Current state on the machine:

- `xkb-options` = `['ctrl:swapcaps']` (persistent in the user's dconf)
- Input layout: `us` (single layout, so the option applies to everything)
- GNOME Wayland session (session 3, tty2) is **active** and gnome-shell is running with the setting loaded (`gsd-keyboard` daemon confirms it)
- The log even proves persistence: the session was re-created at 05:31 today (fresh re-login/reboot) and the setting survived — it's stored in `~/.config/dconf/user`, so it survives reboots

**What's live right now on that machine's keyboard:**

| Key you press | Outputs |
|---|---|
| **Caps Lock** | → **Ctrl** (left control behavior) |
| **Left Ctrl** | → **Caps Lock** |

**Scope**: this applies to the **GNOME desktop session** on that box — i.e. a physical USB keyboard plugged into it, or any input session (GNOME Remote Desktop etc.) attached to that GUI session.

⚠️ Two things to double-check on your end:

1. If you typed on your **laptop's own keyboard** while SSHing in, the swap doesn't apply to the laptop — it applies to the remote machine's keyboard handling.
2. If you meant swap with the **right Ctrl** instead, that's a different option (`ctrl:swapcaps_rctrl`) — say the word and I'll change it.

If it still doesn't feel swapped on the actual hardware keyboard, tell me and I'll dig into whether the physical keyboard is hitting a different input path (e.g., a KVM or wireless dongle session).
