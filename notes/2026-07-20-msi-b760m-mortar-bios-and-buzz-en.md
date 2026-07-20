---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI B760M Mortar BIOS and Buzz
translated: false
type: note
---

**Question: MSI MAG B760M Mortar — how to reset/install new BIOS, and is the “滋滋” (buzzing/zizzing) sound when plugging power related?**

## 1. Reset BIOS (clear CMOS)

For the **MSI MAG B760M Mortar** (DDR4 or DDR5 version), you have three ways:

### Method A — Clear CMOS jumper (recommended)

1. Shut down PC.
2. Turn off PSU switch (`0`).
3. Remove AC power cable.
4. Press case power button for ~10 seconds (discharge capacitors).
5. Find the **JBAT1** pins on motherboard.
6. Short the two pins with a screwdriver for ~5–10 seconds.
7. Reconnect power and boot.

This resets:

* XMP memory settings
* CPU overclock/undervolt
* fan curves
* boot order
* BIOS settings

---

### Method B — Remove CMOS battery

1. Power off completely.
2. Remove the round CR2032 battery.
3. Wait 5 minutes.
4. Put battery back.
5. Boot.

Same result.

---

## 2. Install / update new BIOS

MSI boards have **M-FLASH** and **Flash BIOS Button**.

### Option 1: M-FLASH (normal)

1. Download BIOS:

[MSI MAG B760M Mortar Support Page](https://www.msi.com/Motherboard/MAG-B760M-MORTAR/support?utm_source=chatgpt.com)

2. Format USB stick as **FAT32**.
3. Extract BIOS file.
4. Copy BIOS file to USB root.
5. Enter BIOS:

```
DEL key during boot
```

6. Select:

```
M-FLASH
→ select BIOS file
→ confirm
```

Do not:

* remove power
* reset PC
* touch USB

Usually takes 5–10 minutes.

---

### Option 2: Flash BIOS Button (even without CPU/RAM)

This is useful if:

* motherboard does not POST
* CPU unsupported by old BIOS
* BIOS corrupted

Steps:

1. Download BIOS.
2. Rename file:

Usually MSI requires:

```
MSI.ROM
```

3. Put only that file on FAT32 USB.
4. Insert into special USB port:

```
Flash BIOS USB port
```

5. Connect:

* 24-pin motherboard power
* 8-pin CPU power

6. Press:

```
Flash BIOS Button
```

LED blinking = flashing.

---

# 3. About the "滋滋" sound when plugging power

This is interesting.

A small **buzzing / zzz sound immediately when PSU power is connected** can come from several places.

## Case 1: Normal coil whine (possible)

Modern motherboards have:

* VRM inductors
* standby 5V circuits
* capacitors

When AC enters PSU, motherboard gets:

```
AC 220V
   ↓
PSU standby 5V
   ↓
motherboard standby circuit
   ↓
EC / RGB controller / LAN chip
```

Some inductors can vibrate:

```
current → magnetic field → coil vibration → "滋滋"
```

genui{"physics_electricity_magnetism_learning_block":{"type_id":"CURRENT_TO_MAGNETIC_FIELD"}}

A very faint high-frequency sound is usually harmless.

---

## Case 2: PSU issue

More concerning if:

* sound comes from PSU itself
* crackling
* electrical smell
* sound changes with GPU load

Example:

```
Plug AC
 ↓
PSU standby circuit
 ↓
capacitor charging
 ↓
buzz/crackle
```

A cheap/aging PSU can do this.

---

## Case 3: Short circuit / motherboard problem

Bad signs:

* motherboard LED flashes strangely
* PSU clicks repeatedly
* PC turns on/off loop
* burning smell
* USB devices behave weirdly

Then disconnect everything:

Only connect:

```
Motherboard
CPU
CPU cooler
1 RAM stick
PSU
```

No GPU, no SSD.

Try boot.

---

# 4. BIOS reset vs buzzing relationship

Usually:

```
BIOS corruption
       ❌
       |
       no relation
       |
Power plug buzzing
```

BIOS is firmware stored in SPI flash.

Buzzing happens in the **power delivery analog hardware**, not BIOS.

However, if BIOS settings are wrong:

* extreme RAM voltage
* overclock
* unstable CPU voltage

it can cause startup problems, but not usually a buzzing sound when AC is plugged in.

---

## For your specific board + i9-13900KF

You mentioned before you have:

```
MSI MAG B760M Mortar
Intel i9-13900KF
RTX 4070
```

This board should support 13900KF, but I would still:

1. Clear CMOS.
2. Update latest BIOS.
3. Load optimized defaults.
4. Enable XMP only after stable boot.

For a used motherboard, I would also inspect:

* VRM area (burn marks)
* swollen capacitors
* bent CPU socket pins
* 8-pin CPU power connector

The **exact location of the zizz sound** matters a lot:

* near PSU → PSU suspicion
* near CPU VRM → coil whine
* near rear I/O → standby circuit

If you record a 5–10 second audio/video clip when plugging AC, the source can usually be identified.
