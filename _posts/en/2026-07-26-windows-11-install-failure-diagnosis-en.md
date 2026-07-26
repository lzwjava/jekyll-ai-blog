---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows 11 Install Failure Diagnosis
translated: false
type: note
---

Question: Generic "Windows 11 installation has failed" dialog, no error code — disk/partition setup was correct this time, so what's actually failing?

Answer: Since the disk now has a proper GPT layout and you selected the right unallocated space, this generic failure (no error code, immediate small dialog rather than the earlier detailed error) points away from partitioning and toward **installation media or hardware**:

**1. Check the actual log first — don't guess blind:**

```cmd
Shift + F10
notepad X:\Windows\Panther\setupact.log
```

Scroll to the bottom (most recent entries) — look for lines with `Error` or a hex code like `0x8007...`. This tells you exactly what failed instead of the vague dialog. Paste me the last 20-30 lines around the error if you want me to read it.

**2. Most common cause of this generic failure: corrupt/bad USB installer.**

- Re-download the Windows 11 ISO fresh from Microsoft (don't reuse a possibly corrupted download).
- Re-flash the USB with **Rufus**, explicitly set: Partition scheme = **GPT**, Target system = **UEFI (non-CSM)**.
- Try a **different USB port** — front-panel/USB-A ports on some Lenovo laptops have flaky UEFI driver support during Setup; try a rear/USB 3.0 port directly if you're on a hub or different port.
- Try a **different USB drive** if you have one — a flaky/aging USB stick is a very common cause of exactly this failure with no useful error message.

**3. Less likely but possible:** RAM issue. If you have a spare stick or can test, a single stick reseated properly rules this out.

Check `setupact.log` first — that'll save us guessing. What's in the tail of that file?
