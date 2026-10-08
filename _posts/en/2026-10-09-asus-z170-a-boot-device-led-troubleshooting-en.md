---
audio: false
generated: true
image: false
lang: en
layout: post
title: "ASUS Z170-A Boot Device LED Troubleshooting"
translated: false
type: note
---

Question: **What is wrong with this ASUS Z170-A?**

Answer: **The red LED in your photo is the `BOOT_DEVICE_LED`.** That is a very useful clue.

ASUS documents the Z170-A as having four POST LEDs: **CPU, DRAM, VGA, and BOOT_DEVICE**. If one remains lit, POST has detected a problem with that component. ([ASUS Download Center][1])

In your photo:

* CPU LED: apparently **not lit**
* DRAM LED: apparently **not lit**
* VGA LED: apparently **not lit**
* **BOOT_DEVICE_LED: RED → lit**
* The motherboard is therefore getting through CPU/RAM/VGA initialization and is stopping at the **boot-device stage**.

### Most likely: no bootable SSD/HDD

I can see the SATA ports on the right side of the board, but I don't see a SATA drive connected.

If you're testing this board **without an SSD/HDD**, this behavior is expected.

The POST sequence is roughly:

```text
Power on
   ↓
CPU initialization       ✓
   ↓
DRAM initialization      ✓
   ↓
PCIe / VGA initialization ✓
   ↓
Find boot device         ← RED LED
   ↓
Boot Windows/Linux
```

So this **doesn't look like a dead motherboard**.

ASUS specifically says that a boot-device failure should be checked by reconnecting the SATA/M.2 drive, SATA cable/port, and trying a known-good drive. ([ASUS Global][2])

### If your goal is just to test the motherboard

You don't actually need a hard disk just to determine whether the board can POST.

Connect:

```text
Z170-A
├── 24-pin ATX
├── 8-pin CPU EPS
├── CPU + cooler
├── 1 DIMM
├── PSU
└── GPU only if your CPU has no usable iGPU
```

Then power it on.

If you get **BIOS/UEFI screen**, the core platform is basically alive.

If you're using an Intel CPU with integrated graphics, you can also test the motherboard video output directly.

### One important thing I notice

Your cooler is huge and is sitting very close to the DIMM area. That's fine, but for troubleshooting I'd simplify the system:

```bash
# Minimum POST test
CPU
1 × RAM
PSU
motherboard
monitor
```

Then add GPU / SSD / other PCIe cards one at a time.

If you tell me **which CPU + RAM you put in this Z170-A**, and whether you're getting **display output or just the red BOOT LED**, I can give you the exact next diagnostic step.

References:

* [ASUS Z170-A User Manual](https://www.asus.com/supportonly/z170-a/helpdesk_manual/?utm_source=chatgpt.com)
* [ASUS Q-LED troubleshooting](https://www.asus.com/us/support/faq/1043948/?utm_source=chatgpt.com)

[1]: https://dlcdnets.asus.com/pub/ASUS/mb/LGA1151/Z170-A/E10611_Z170-A_UM_V2_WEB.pdf?model=z170-a&utm_source=chatgpt.com "1.8 Onboard LEDs"
[2]: https://www.asus.com/us/support/faq/1043948/?utm_source=chatgpt.com "[Motherboard] Common Q-CODE(Error CODE) and Troubleshooting | Official Support | ASUS USA"
