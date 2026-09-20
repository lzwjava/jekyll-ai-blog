---
audio: false
generated: true
image: false
lang: en
layout: post
title: B75 USB boot priority issue
translated: false
type: note
---

The USB is unplugged now (so you moved it to the B75 PC). "Always boots Ubuntu" = the B75 is skipping the USB. This is a boot-priority / boot-mode issue, not a bad USB. Here's how to fix it, in order:

## 1. Confirm which machine you're on

The USB was built for the **B75 PC**, not this MSI B760M machine. Make sure you're booting it on the B75 board.

## 2. Use the boot menu key (try first — fastest)

Power on and **tap repeatedly** (from the instant you press power) one of these keys:

- **F11** — most common on generic AMI boards (your B75 BIOS is AMI Aptio)
- **F12**, **F8**, **Esc**, **F9**, **F7** — the other common ones

You should get a "Please select boot device" list. Pick the entry for the USB. Look for one **without** "UEFI:" in front of it (e.g. `USB HDD: ...`, not `UEFI: USB`).

## 3. In BIOS Setup (press **Del** or **F2** at power-on)

If the boot menu didn't work, go into setup and check these (they're the usual culprits on B75/AMI):

1. **Disable "Fast Boot" / "Quick Boot"** — if on, the BIOS skips USB init, so the USB never becomes bootable.
2. **Enable "Legacy USB Support"** (in Advanced → USB Configuration).
3. **Boot Mode / CSM** — set to **Legacy** (or "Legacy + UEFI"). The FreeDOS USB is legacy-only; if the board is in UEFI-only mode it will be ignored.
4. **Boot priority** (Boot tab):
   - Set **Boot Option #1 = USB** or **USB HDD**
   - Also check **"Hard Disk Drive BBS Priorities"** — very often the USB appears here as a "hard disk", and you must move it to #1 there.
5. Save & exit (**F10**).

## 4. Use a USB 2.0 port (black)

Old boards often can't boot from the **blue USB 3.0** ports. Plug into a **black USB 2.0** port on the rear I/O.

---

Two questions to narrow it down quickly:

1. Are you testing on the **B75 PC**, or on this MSI machine (just to try it)?
2. When you power on the B75, what does the splash screen say (any "Press Fxx for Boot Menu" text, and what BIOS brand)?

If you can tell me the boot-menu key shown on screen, or send a photo of the BIOS **Boot** tab, I'll point at the exact setting to change.
