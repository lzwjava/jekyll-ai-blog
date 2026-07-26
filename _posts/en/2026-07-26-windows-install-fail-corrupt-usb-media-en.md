---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Windows Install Fail: Corrupt USB Media"
translated: false
type: note
---

Question: Do you need to extend the partition before installing, and why does it keep failing with the same "recovery environment" trigger?

Answer: No — extending partition isn't relevant here. Your Disk 0 layout is already fine (Setup auto-creates EFI/MSR/Primary/Recovery from unallocated space; extend/create partition manually would only cause problems).

Since it failed again with the **exact same `0xC19001F4` trigger**, this is probably not an accidental keypress — a repeat identical failure at the same point suggests either:

1. **Genuinely corrupt USB media** — same failure every time at the same phase strongly points to a bad file on the USB stick that Setup can't read, and Setup's fallback behavior (misleadingly logged as "user requested recovery") kicks in when it hits that bad read.
2. **A physical trigger you're not noticing** — some Lenovo laptops have a **Novo button** or **OneKey Recovery** combo that can register a press from vibration/bag pressure if it's exposed, or a stray touch on a touchscreen if this model has one.

**Do this next, skip more log-reading:**
1. Re-download the Windows 11 ISO fresh from Microsoft (don't reuse the current one).
2. Re-flash a **different USB stick** if you have one — use Rufus, GPT + UEFI target.
3. During the whole install, **don't touch the keyboard, trackpad, or touchscreen at all** once "Installing Windows" progress starts — hands off completely until OOBE.
4. If you have a second USB port (avoid USB hubs), plug directly into a rear port.

If it fails identically a third time with a fresh ISO + fresh USB + zero touching, that would point to a hardware issue (bad RAM or a flaky NVMe controller) rather than media — but let's rule out the USB first since that's the most common cause of a repeatable, otherwise-unexplained abort like this.
