---
audio: false
generated: true
image: false
lang: en
layout: post
title: Caps Lock and Ctrl Swapped on Ubuntu
translated: false
type: note
---

Done. Caps Lock and Ctrl are now swapped on the Ubuntu machine (GNOME/Wayland session).

**What was applied:**

- `gsettings set org.gnome.desktop.input-sources xkb-options "['ctrl:swapcaps']"`
- Result verified: `['ctrl:swapcaps']` — takes effect immediately in the GNOME session, persists across reboots.

**Behavior now:**

- **Caps Lock** key → acts as **Ctrl**
- **Left Ctrl** key → acts as **Caps Lock**

Note: this applies to the graphical GNOME session. If you also want the swap on the login screen or a virtual console (tty), that needs `sudo` editing of `/etc/default/keyboard` (`XKBOPTIONS="ctrl:swapcaps"` + `setupcon`) — let me know if you'd like that too.
