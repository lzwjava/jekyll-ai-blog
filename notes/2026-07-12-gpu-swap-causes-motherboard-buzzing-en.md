---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Swap Causes Motherboard Buzzing
translated: false
type: note
---

Question: Why did my MSI B760M + i9-13900KF + Corsair CX650F system start making a buzzing noise from the motherboard SATA5/6 area after swapping RTX 4070 with a used AMD MI50?

Answer:

From your description, the most likely cause is **not the PSU**. The timing strongly points to the **GPU replacement triggering a motherboard power/PCIe/power-delivery issue**.

Your sequence:

1. System works normally with RTX 4070.
2. Remove RTX 4070.
3. Install used AMD MI50.
4. Immediately motherboard starts buzzing.
5. Buzzing remains after removing MI50 and reinstalling RTX 4070.
6. Sound localized near SATA5/6 area.
7. PSU paperclip test probably passes.

This pattern suggests one of several possibilities.

---

## 1. Most likely: motherboard VRM/choke coil electrical noise (coil whine)

The SATA5/6 area on many mATX boards is close to:

* chipset power circuits
* SATA controller area
* motherboard power filtering components

Small inductors ("chokes") can make a **high-frequency buzzing / whining sound** when current waveform changes.

Example:

```
12V PSU
 |
 +---- CPU VRM
 |
 +---- PCIe slot power
 |
 +---- chipset/SATA power
          |
          +--- coil vibrates
```

A GPU change can alter:

* PCIe power draw
* PCIe signaling
* chipset load
* power-state transitions

and make a previously silent coil start vibrating.

This does **not automatically mean the motherboard is damaged**.

---

## 2. MI50 is a very unusual PCIe device

AMD MI50 is a data-center GPU.

Compared with RTX 4070:

|                 | RTX 4070     | AMD MI50      |
| --------------- | ------------ | ------------- |
| Architecture    | Ada Lovelace | Vega 20       |
| PCIe            | Gen4 x16     | Gen4 x16      |
| Power           | ~200W        | ~300W         |
| Power connector | 8-pin        | 8-pin         |
| Cooling         | consumer fan | blower/server |
| Firmware        | consumer     | enterprise    |

MI50 has much higher transient power behavior.

Your PSU:

Corsair CX650F 650W

is probably enough for RTX 4070:

```
13900KF
~250W peak

RTX4070
~200W

system
~500W peak
```

But MI50:

```
13900KF
250W

MI50
300W+

system
600W+
```

You are very close to PSU limits.

A power transient could stress motherboard power rails.

---

## 3. Possible PCIe slot contact problem

When changing GPUs:

* PCIe slot gets mechanical stress
* GPU bracket may push sideways
* large MI50 is heavier

A slightly bad PCIe contact can create strange symptoms:

* no boot
* motherboard noise
* GPU initialization failure
* PCIe power instability

Try:

1. Remove GPU completely.
2. Blow compressed air into PCIe slot.
3. Inspect slot with flashlight.
4. Install RTX4070 again carefully.

---

## 4. Check EZ Debug LED first

Your MSI board has:

```
CPU
DRAM
VGA
BOOT
```

near top-right.

When powering on:

* CPU light?
* DRAM light?
* VGA light?
* BOOT light?

This is the fastest diagnostic.

Examples:

### VGA LED

Usually:

```
GPU not detected
PCIe problem
GPU power problem
```

### CPU LED

Possible:

```
socket issue
VRM issue
BIOS issue
```

---

## 5. The "SATA5/6 buzzing" may be misleading

Sound travels through PCB.

A coil near PCIe/chipset can sound like it comes from SATA area.

Use:

* paper tube
* screwdriver handle against ear
* stethoscope

Compare:

```
PCIe slot area
|
VRM area
|
SATA area
|
chipset heatsink
```

Do not touch components while powered.

---

## 6. The important question: did MI50 need different power wiring?

MI50 usually expects:

```
8-pin EPS-like PCIe power
```

not motherboard CPU EPS.

If accidentally connected incorrectly:

* wrong cable
* modular PSU cable mismatch
* using another PSU cable

can damage components.

Corsair modular cables are NOT universal.

Never mix:

```
Corsair cable
+
another PSU
```

even if connector fits.

---

## What I would do now (lowest risk)

### Step 1

Disconnect everything unnecessary:

```
Motherboard
CPU
1 RAM stick
RTX4070
PSU 24pin
CPU 8pin
GPU power
```

Remove:

```
SATA cables
NVMe (optional)
USB devices
```

Try boot.

---

### Step 2

Clear CMOS:

1. PSU off
2. Remove AC cable
3. Press power button 10 sec
4. Clear CMOS jumper / remove battery 5 min
5. Boot again

---

### Step 3

Check if buzzing exists without GPU

Only:

```
13900KF
motherboard
PSU
RAM
```

(no GPU)

Since 13900KF is KF:

Important:

```
13900KF has NO integrated GPU.
```

So no display is expected, but check sound.

---

## My probability estimate

Based on your story:

| Cause                                                           | Probability |
| --------------------------------------------------------------- | ----------: |
| Motherboard coil whine triggered by power change                |         50% |
| PCIe slot/contact issue                                         |         20% |
| MI50 power transient damaged/stressed motherboard power circuit |         15% |
| PSU issue                                                       |         10% |
| CPU/water cooling issue                                         |          5% |

The first thing I would not do is keep swapping GPUs repeatedly. Repeated hot plugging / mechanical insertion increases risk.

Your next data point is critical:

1. When pressing power now, do fans spin?
2. Which MSI EZ Debug LED stays on?
3. Does the buzzing happen **with RTX4070 installed**, or only without GPU?
4. Is the buzzing continuous or only during startup?
