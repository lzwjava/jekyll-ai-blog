---
audio: false
generated: true
image: false
lang: en
layout: post
title: BIOS recovery steps for Huanan B75
translated: false
type: note
---

Question: Your Huanan B75 now powers on with fans running, but there is no video output after the BIOS flash; the keyboard briefly lights up.

Answer:

That symptom strongly suggests the CPU/PSU are not the immediate problem. **Treat this as a failed BIOS initialization first.** Don't keep reflashing modified images yet.

### 1. Do the simplest POST test first

Power completely off and unplug it.

Disconnect/remove:

* SSD
* discrete GPU
* all USB devices except keyboard
* any extra PCIe cards

Leave only:

* B75 motherboard
* CPU + cooler
* **one DDR3 stick**
* PSU
* monitor connected to the motherboard video output

Your CPU model matters here: the motherboard VGA/DVI outputs only work if the CPU has usable Intel integrated graphics.

Then clear CMOS:

1. PSU switch OFF.
2. Remove AC power.
3. Remove CMOS battery.
4. Hold the case power button ~10 seconds.
5. Wait a few minutes.
6. Reinstall battery.
7. Power on.

Try each RAM stick individually and, if necessary, different DIMM slots.

### 2. Then try AMI recovery

Since you have the untouched `B75V101_original.bin`, this is the thing I'd try **before buying a programmer**.

AMI's documented recovery mechanism uses the boot block to load a BIOS image, commonly named `AMIBOOT.ROM`, and `Ctrl+Home` is the standard recovery hotkey. USB recovery is supported on some AMI implementations, but whether this particular Huanan board exposes it depends on its firmware implementation. ([Futura Sciences Forums][1])

Make the USB as simple as possible:

```text
USB
└── AMIBOOT.ROM
```

Where:

```text
AMIBOOT.ROM = B75V101_original.bin
```

I would **not** put multiple BIOS files on it for the first attempt. Use a small FAT32 USB stick if possible.

Then:

```text
1. PC OFF
2. USB inserted
3. Hold Ctrl + Home
4. Press power
5. Keep Ctrl + Home held for ~10–15 seconds
6. Release
7. Wait
```

**Do not reset or power it off once recovery appears to start.**

AMI documentation says the recovery process can operate without a functioning display and uses beep/access activity to indicate that the ROM is being loaded/programmed. ([Futura Sciences Forums][1])

### 3. The important diagnostic: what does it do with the USB?

Listen carefully.

| Behavior                                                              | Meaning                                                                            |
| --------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| USB LED flashes/accesses                                              | Very promising — boot block is probably alive                                      |
| Several beeps                                                         | Recovery routine may have started                                                  |
| 4-ish recovery beeps                                                  | Strong indication the ROM programming completed on implementations using that code |
| Absolutely no USB activity, no beeps                                  | Recovery path may not be enabled, or boot block itself may be damaged              |
| Fans run forever, keyboard briefly flashes, completely dead afterward | Consistent with BIOS not reaching normal POST                                      |

**Don't assume "no display = dead motherboard."** A functioning recovery boot block can exist even when the normal BIOS cannot POST.

### 4. One thing I want you to check before doing anything else

You said:

> keyboard will light up a bit

That's useful.

Tell me exactly what happens when you press power:

```text
Fans:        stay spinning / spin then stop
Keyboard:    flashes once / stays lit / completely off
USB stick:   LED flashes? yes/no
Beep:        0 / 1 / 2 / 4 / continuous
Monitor:     "No signal" immediately / wakes then no signal
GPU:         installed / removed
CPU model:   exact model
```

Also, **don't flash the enlarged/custom image again yet**. First attempt to restore the known-good original `B75V101_original.bin`.

If `Ctrl+Home` produces **zero USB activity and zero beeps**, then I'd move to reading the SPI chip directly with a CH341A/SOIC8 clip. That gives us a much more deterministic recovery path than repeatedly guessing at keyboard recovery combinations.

### References

* [AMI AMIBIOS8 Flash Update & BIOS Recovery Methods](https://forums.futura-sciences.com/attachments/materiel-hardware/58894d1225034379-flash-bios-rate-amibios8_flash_recovery_whitepaper_v10.pdf) ([Futura Sciences Forums][1])
* [BIOSTAR: How to recover AMI BIOS if update fails](https://www.biostar-usa.com/app/en-us/support/faq.php?page=12&searchfaq=bios) ([Biostar USA][2])

I can also walk you through the **CH341A read → verify → backup → write → verify** procedure if the Ctrl+Home recovery doesn't respond.

[1]: https://forums.futura-sciences.com/attachments/materiel-hardware/58894d1225034379-flash-bios-rate-amibios8_flash_recovery_whitepaper_v10.pdf?utm_source=chatgpt.com "AMIBIOS Whitepaper"
[2]: https://www.biostar-usa.com/app/en-us/support/faq.php?page=12&searchfaq=bios&utm_source=chatgpt.com "BIOSTAR Technical Support & FAQ | Expert Solutions for Motherboards & IPC"
