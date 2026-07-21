---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enter MSI BIOS & Disable Secure Boot
translated: false
type: note
---

## MSI MAG B760M Mortar — Enter BIOS

**Key: DEL (Delete)**

Here's the exact sequence:

1. **Shut down** the machine completely (or reboot)
2. **Press the power button**
3. **Immediately start tapping the DEL key** repeatedly — once per second, don't hold it
4. You'll see the MSI Click BIOS interface

> Note: On MSI boards, you'll usually see "Press DEL to enter BIOS Setup" at the bottom of the screen during POST. If you miss it, just reboot and try again — tap earlier.

---

## Once inside BIOS → Disable Secure Boot

The menu path on your B760M Mortar:

1. **Settings** (or **Security** tab if visible — older MSI BIOS had it here; on Click BIOS 5 it's under **Settings**)
2. → **Security**
3. → **Secure Boot**
4. → Set to **Disabled**
5. Press **F10** → **Yes** to Save & Exit

Alternative path on some MSI BIOS versions:

- **Boot** → **Secure Boot** → **Disabled**

---

## If you have the new MSI Click BIOS (UEFI/GUI style)

Look for the **Settings** icon (gear icon at top or side), then:

- **Security** → **Secure Boot** → **Disabled**

---

One reboot later, `nvidia-smi` will work. Let me know if you get into BIOS and can't find the Secure Boot option — I can look up the exact menu screenshots for this board.
