---
audio: false
generated: true
image: false
lang: en
layout: post
title: Shift+F10 Not Working During Setup
translated: false
type: note
---

Question: Shift+F10 isn't doing anything — how to get a command prompt?

Answer: Click **OK** on that error dialog first — Setup will roll back and drop you to the "Select location to install Windows" screen again. Shift+F10 only works when focus is on an actual Setup screen, not while that modal error box is up.

Once you're back at the partition screen:

1. Press `Shift + F10` again — should open cmd.
2. If it still doesn't respond, make sure you're pressing both keys on the **laptop's physical keyboard** (not through a remote/KVM/virtual keyboard if you're using one — Shift+F10 sometimes doesn't pass through those).
3. If truly nothing happens, try `Shift + Fn + F10` — on Lenovo laptops F-keys often default to media/function mode, so you may need Fn to get the actual F10 signal through.

Once cmd opens, run:

```cmd
notepad X:\Windows\Panther\setupact.log
```

(drive letter might be X: or another letter — if X: doesn't work, run `wpeutil` or just check `dir C:\`, `dir D:\` etc. to find the Windows PE / setup drive)

Scroll to the very bottom, find the last `Error` line, and paste it here.
