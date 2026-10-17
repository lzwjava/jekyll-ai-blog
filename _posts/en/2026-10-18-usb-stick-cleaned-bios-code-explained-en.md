---
audio: false
generated: true
image: false
lang: en
layout: post
title: USB stick cleaned, BIOS code explained
translated: false
type: note
---

Done. The USB stick is now clean:

- **/dev/disk14** — 4.0 GB USB stick
- Erased, repartitioned (GUID scheme + EFI), formatted as **FAT32**, volume name **"USB"**, mounted and ready to use.

---

## What does `E7978IMS.AA0` mean?

That's an **MSI motherboard BIOS firmware version string**. MSI names their BIOS files with a strict convention:

| Part | Meaning |
|------|---------|
| `E` | Prefix used by MSI for all BIOS image files |
| `7978` | **Board model code** — the internal MSI model identifier for that specific motherboard |
| `IMS` | **Intel MSI** — the BIOS vendor/format marker (MSI's Intel-platform BIOS builds) |
| `AA0` | **BIOS revision/version** — e.g. `AA0`, `140`, `1A0`; later letters/numbers = newer builds |

So `E7978IMS.AA0` = the BIOS image for MSI board model **7978**, version **AA0**. If you see this string, it's the firmware file for that specific MSI motherboard — you'd flash it via M-FLASH or MSI Center, and it must match your exact board model (flashing the wrong model's BIOS can brick the board).

Want me to look up which specific MSI board model 7978 corresponds to, or check anything else on the disk?
