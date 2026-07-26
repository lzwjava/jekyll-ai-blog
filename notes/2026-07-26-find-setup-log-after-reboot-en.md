---
audio: false
generated: true
image: false
lang: en
layout: post
title: Find Setup Log After Reboot
translated: false
type: note
---

Question: setupact.log isn't there anymore after reboot — where else can I find the failure log?

Answer: Right — that log lived on the temporary WinPE RAM disk (`X:`), which gets wiped every time you reboot into a fresh Setup session. But Setup usually copies its logs onto your target drive before failing. Check there instead:

```cmd
Shift + F10
notepad C:\$WINDOWS.~BT\Sources\Panther\setupact.log
```

If that path doesn't exist, try:

```cmd
dir C:\$WINDOWS.~BT\Sources\Panther\
```

to see what log files actually got written, then open whichever `setup*.log` is there.

If `C:\$WINDOWS.~BT` doesn't exist at all (meaning Setup failed before it even got that far this time), just check what's on C: currently:

```cmd
dir C:\
```

Given this is getting to be a repeat generic failure with no clear disk-related cause left, honestly at this point I'd skip further log digging and just **rule out the USB media** directly, since that's the most likely remaining culprit:

1. Re-download the Windows 11 ISO from Microsoft's official page (fresh copy).
2. Re-flash with **Rufus**: GPT partition scheme + UEFI target.
3. Try a different USB stick if you have one, in a rear USB port directly on the laptop (not a hub).

That combination — bad ISO, bad USB write, or a flaky drive — accounts for the vast majority of "generic install failed" dialogs when the disk/partition side is already confirmed clean, which yours now is.
