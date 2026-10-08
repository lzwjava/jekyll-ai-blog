---
audio: false
generated: true
image: false
lang: en
layout: post
title: BOOT LED Red Even With HDD
translated: false
type: note
---

Question: **The BOOT_DEVICE LED is still red even though you connected the HDD — why?**

Answer: Yes — in this second photo I can see the **HDD is connected by SATA power + SATA data**, but the important question is whether the motherboard can actually detect it.

The red LED is definitely labeled **`BOOT_DEVICE_LED`** on your Z170-A. ASUS says this LED means the board cannot find a usable boot device. ([@ROG][1])

### Do this exact test

**1. Disconnect the HDD completely.**

Leave only:

```text
Z170-A
├── CPU + cooler
├── 1 RAM stick
├── PSU 24-pin
├── PSU 8-pin CPU
└── monitor
```

No HDD, no USB drives, no other PCIe cards.

Then power on and repeatedly press:

```text
DEL DEL DEL DEL ...
```

You should normally get into **UEFI/BIOS** even with zero storage devices.

The BOOT LED can remain lit because there is no boot device, but **you should still be able to enter BIOS**.

---

### If you get BIOS

Then the motherboard is probably fine.

Connect the HDD:

```text
HDD
 ├── SATA power
 └── SATA data → SATA6G_1
```

Then in BIOS check:

```text
Advanced Mode
    ↓
Advanced
    ↓
SATA Configuration
```

See whether the HDD appears.

If it **doesn't appear**, suspect:

1. bad SATA data cable
2. bad SATA port
3. bad HDD
4. SATA power problem
5. BIOS SATA configuration

Try:

```text
SATA6G_1 → SATA6G_2
```

and another SATA cable.

ASUS specifically recommends reconnecting the SATA cable and storage device when the BOOT LED stays on. ([@ROG][1])

### But there's an even more important test

Your photo appears to show **no display cable connected to the motherboard**, and I don't see a discrete GPU in the setup.

If your CPU is something like:

```text
i5-6500
i5-6600
i7-6700
i7-6700K
```

it has Intel integrated graphics, so connect your monitor to the **motherboard's HDMI/DVI/DisplayPort output**.

If your CPU is an **F-series** or otherwise has no iGPU, you'll need a discrete GPU.

---

### The key distinction

If you have:

```text
BOOT_DEVICE_LED = red
+
BIOS appears
```

→ **storage/boot problem**, not a motherboard POST failure.

If you have:

```text
BOOT_DEVICE_LED = red
+
NO BIOS / NO display
```

→ we need to investigate further. The BOOT LED may be the *last* LED in the POST sequence rather than the actual root cause.

The Z170-A's POST LEDs are designed to run through CPU → DRAM → VGA → boot-device checks, with the problematic LED remaining lit. ([motherboarddb.com][2])

**Tell me the exact CPU model** installed in this Z170-A (e.g. `i7-6700K`), and whether your monitor currently shows **anything at all**. Then I can narrow this down substantially.

[1]: https://rog.asus.com/us/support/faq/1042678/?utm_source=chatgpt.com "[Motherboard] ASUS motherboard troubleshooting via Q-LED indicators | Official Support | ROG USA"
[2]: https://motherboarddb.com/media/manuals/Asus/Z170-A/Z170-A.pdf?utm_source=chatgpt.com "1.8 Onboard LEDs"
