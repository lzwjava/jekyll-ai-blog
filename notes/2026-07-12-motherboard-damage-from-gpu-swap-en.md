---
audio: false
generated: true
image: false
lang: en
layout: post
title: Motherboard Damage from GPU Swap
translated: false
type: note
---

Question: Analyze why MSI B760M + i9-13900KF + Corsair CX650F started making buzzing noise after swapping RTX4070 to AMD MI50, and now cannot boot.

Answer:

From your description, the key timeline is:

1. System was stable:

```
MSI B760M Mortar WiFi
i9-13900KF
Corsair CX650F
RTX4070
```

2. You removed RTX4070.

3. Installed used AMD MI50.

4. Immediately:

* motherboard area started "滋滋" electrical noise
* no display / cannot boot
* noise localized near SATA5/SATA6 area
* even after removing water cooling, noise remains
* reinstall RTX4070, still abnormal

This strongly suggests **a motherboard power rail problem or motherboard damage**, not the PSU.

---

## 1. The most likely event: MI50 caused a PCIe power fault

AMD MI50 is a server GPU:

* Vega 20 architecture
* PCIe 4.0 x16
* 300W TDP
* 8-pin EPS-style power connector (not normal gaming GPU behavior)
* Designed for workstation/server platforms

The important part:

**MI50 is not a normal RTX4070 replacement.**

RTX4070:

```
PCIe slot:
75W

12VHPWR:
up to 200W+
```

MI50:

```
PCIe slot:
75W

8-pin:
~225W
```

But the board design, firmware, power sequencing, and cooling assumptions are different.

A used MI50 may have:

* damaged VRM
* shorted capacitor
* failed power stage
* damaged PCIe edge connector

When inserted, the motherboard PCIe 12V rail may have been stressed.

---

## 2. Why noise comes from SATA5/SATA6 area?

This is interesting.

On the MSI B760M Mortar:

The SATA ports are physically close to:

* chipset (PCH)
* PCIe power distribution
* motherboard VRM auxiliary circuits

The noise you hear is probably not SATA itself.

Likely sources:

```
24-pin ATX
     |
     |
 motherboard power plane
     |
     +---- PCH/chipset power VRM
     |
     +---- SATA controller
```

High frequency switching noise:

```
VRM coil
   |
   |
  ~~~~~
  electrical vibration
```

is called:

**coil whine**

A damaged VRM can produce:

```
ziiiiiiiiii
buzz buzz
```

even without booting.

---

## 3. The PSU paperclip test is not enough

Corsair instruction:

Short:

```
PS_ON
(pin 16 usually)
+
Ground
```

means:

```
PSU turns on
```

It only proves:

* standby circuit works
* PSU can start

It does NOT prove:

* voltage stability under load
* transient response
* PCIe power quality

However:

Your symptom points away from PSU because:

> noise is physically located on motherboard

---

## 4. Important test: minimal motherboard boot

Do this:

Remove:

* GPU
* SSD
* SATA devices
* USB devices
* RGB controllers

Only:

```
Motherboard
+
CPU
+
CPU cooler
+
1 RAM stick
+
24-pin ATX
+
8-pin CPU EPS
```

Then power on.

Expected:

13900KF has no iGPU:

```
no GPU = no display
```

but:

* EZ Debug LED should show VGA error

You should NOT hear motherboard buzzing.

If buzzing remains:

=> motherboard damaged.

---

## 5. Check EZ Debug LED

MSI board has:

```
CPU
DRAM
VGA
BOOT
```

Usually top-right.

Meaning:

### CPU red

Possible:

* CPU power problem
* motherboard VRM issue

### DRAM yellow

RAM initialization failure

### VGA white

GPU problem

### BOOT green

POST succeeded, storage problem

Your case likely:

```
VGA LED
or
CPU LED
```

---

## 6. Possible damage scenarios ranked

My probability estimate:

### #1 Motherboard PCIe/power circuit damaged

Probability: 60%

Reason:

* happened exactly during GPU swap
* noise from motherboard
* persists after GPU replacement

### #2 MI50 itself defective and damaged motherboard

Probability: 25%

Used MI50 cards are risky.

Possible:

```
MI50 VRM short
        |
        |
PCIe 12V rail
        |
        |
motherboard damage
```

### #3 PSU damaged

Probability: 10%

Less likely because:

* CX650F protections probably triggered
* noise location inconsistent

### #4 CPU/water cooling issue

Probability: <5%

Removing water cooling changed nothing.

---

## 7. Do NOT repeatedly power cycle

If a motherboard power component is damaged:

Every power-on:

```
12V
 |
VRM
 |
heat
 |
possible further damage
```

Avoid:

* plugging MI50 again
* repeated boot attempts

---

## 8. What I would do next

Order:

### Step 1

Remove GPU completely.

Clear CMOS:

```
PSU off
AC unplug
press power button 10 seconds
remove CMOS battery 5 minutes
```

Boot minimal config.

---

### Step 2

Listen again.

If:

```
buzz still exists
```

RMA motherboard.

---

### Step 3

Test RTX4070 in another machine if possible.

Do not test MI50 again until motherboard confirmed healthy.

---

## My conclusion

The most likely story:

```
RTX4070 removed
        |
        v
MI50 inserted
        |
        v
MI50 had abnormal power behavior
        |
        v
PCIe power rail / motherboard VRM stressed
        |
        v
B760M motherboard now has coil whine / power fault
        |
        v
No POST
```

The fact that you can localize the noise near SATA5/SATA6 is a strong clue: the sound is probably coming from motherboard inductors/chipset power circuitry, not the GPU or PSU.

Your MSI B760M + 13900KF is a high-end enough platform that a motherboard failure is unfortunately plausible after an abnormal PCIe device event. I would stop testing and focus on confirming motherboard health first.
