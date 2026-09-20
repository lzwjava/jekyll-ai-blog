---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hardware programmer recovers bricked BIOS
translated: false
type: note
---

That confirms it — `fpt -f` wrote the **entire** chip, including the boot-block, so the built-in recovery is gone. No software trick will bring it back; you need a **hardware programmer**. This is very recoverable and cheap (~$5).

## What to buy

- **CH341A programmer** (the common black PCB, ~$5) — *or* the green "CH341A 24/25 series" one
- **SOIC8 test clip** (~$2) — clips onto the chip without soldering
- Optional: **1.8V adapter** (most B75 BIOS chips are 3.3V, so usually not needed)

## Steps (I've already got `flashrom` installed and the original BIOS ready here)

**1. Find the BIOS chip** on the B75 board (power off, unplug PSU):

- It's an **8-pin** chip near the southbridge/CMOS battery.
- Label usually **Winbond `W25Q32`/`W25Q64`**, **MXIC `MX25L32`/`MX25L64`**, **GigaDevice `GD25Q32/64`**, or **EN/EON**.
- 📸 **Read the exact marking on the chip and tell me** — I'll prepare the exact flashrom command and confirm pin 1 orientation.

**2. Connect the programmer:**

- Clip the SOIC8 clip onto the chip (pin 1 = the **dot** on the chip → align with pin 1 on the clip/adapter).
- CH341A **jumper to 3.3V** (not 5V!) — important.
- Plug the CH341A into **this MSI machine's USB**.

**3. I'll run flashrom here** to write `B75V101_original.bin` back — board restored to stock.

## Then we flash again, more cautiously

I suspect the **rebuilt DSDT** (which came out 104 bytes larger than the original and forced the AmiBoardInfo PE to expand) is what killed POST. Next attempt, I'll do it in safe stages so a bad step can't brick it:

1. **Stock** → verify it POSTs after recovery.
2. **ReBarDxe only** (no UEFIPatch, no DSDT) → flash → test POST.
3. **+ UEFIPatch** → flash → test.
4. **+ DSDT patch only if needed**, with the DSDT **shrunk to fit** the original size (removing `_OSI` entries, etc.) so the PE never has to expand.

---

**Next action for you:** open the B75 case and read the BIOS chip label (photo if you can). Tell me what it says, and order the CH341A + SOIC8 clip. Once it arrives, we'll have you back to stock in minutes.
