---
audio: false
generated: true
image: false
lang: en
layout: post
title: Troubleshoot Lid Suspend Issue
translated: false
type: note
---

Down again — no ping response. Likely auto-suspended or lid closed.

When you get to it, can you check:

1. Was the lid closed? (That triggers suspend regardless of GNOME settings)
2. Run `journalctl --since "5 min ago" -p warning` to see what happened

We may need to also disable lid-close suspend in `/etc/systemd/logind.conf`:

```
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
```

Want me to apply that fix once the machine is back up?
