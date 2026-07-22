---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI B760M Mortar Noisy AIO Solution
translated: false
type: note
---

**Question: Why is my MSI MAG B760M Mortar + Thermalright Frozen Prism 240 AIO fan so loud?**

Answer:

Your motherboard is probably not the noisy part. The usual causes are:

1. **AIO pump/fan curve is too aggressive**

The Thermalright Frozen Prism 240 uses:

* 2 × 120mm PWM radiator fans
* up to ~1850 RPM
* AIO pump

At default BIOS settings, many boards run CPU cooling fans based on CPU temperature spikes. Modern Intel CPUs (especially i9-13900KF on B760M) have very fast temperature jumps:

```
idle:
CPU 35-45°C

open browser/build code:
CPU spike → 70-90°C in milliseconds

BIOS sees spike:
fan jumps 1000 → 1800 RPM
```

Result: annoying "jet engine" behavior.

---

2. **i9-13900KF is a very hot CPU**

Your setup:

```
CPU: i9-13900KF
Board: MSI MAG B760M Mortar
Cooler: Thermalright Frozen Prism 240
```

The 13900KF can easily hit:

```
PL2 power:
~250W+

Cinebench:
90-100°C possible
```

A 240mm AIO is borderline for this CPU.

The cooler can handle gaming/workloads, but heavy all-core loads will make fans ramp.

---

3. **MSI default BIOS fan mode**

MSI often ships with:

```
CPU Fan:
Smart Fan Mode ON

Temperature source:
CPU

Curve:
aggressive
```

Try:

BIOS:

```
Hardware Monitor
    CPU Fan:
        PWM mode

    Fan curve:
        30°C -> 20%
        50°C -> 40%
        70°C -> 70%
        85°C -> 100%
```

Do not let it instantly jump to 100%.

---

4. **AIO pump connected incorrectly**

Check cables.

Typical:

```
Pump power:
AIO_PUMP header

Radiator fans:
CPU_FAN header

ARGB:
JRAINBOW header
```

If pump is connected to CPU_FAN and controlled badly:

```
pump speed changes
↓
water flow changes
↓
temperature oscillation
↓
fan noise
```

Better:

```
AIO_PUMP = 100% fixed
CPU_FAN = temperature controlled
```

---

5. **13900KF motherboard power limits**

B760 boards often allow unlimited Intel turbo:

```
PL1 = 253W
PL2 = 253W
Tau = unlimited
```

For a quieter machine:

BIOS:

```
CPU Lite Load:
Mode 5-7

or

Long Duration Power Limit:
125-200W
```

Performance loss is small, noise reduction is large.

Example:

```
Cinebench R23:

253W:
40000 pts
100°C
loud

180W:
36000-38000 pts
80-90°C
much quieter
```

---

6. **Check whether the noise is actually the pump**

AIO noises:

### Fan noise

```
whoosh / air noise
changes with RPM
```

Fix:

* lower fan curve
* replace fans

### Pump noise

```
buzzing
rattling
water sound
constant
```

Fix:

* set pump to fixed 100%
* check mounting orientation
* remove air bubbles

---

For your exact hardware, I would do:

```
1. BIOS:
   AIO_PUMP = 100%

2. CPU fan curve:
   40% until 60°C
   70% at 80°C

3. Enable Intel power limits:
   PL1/PL2 = 200W

4. Undervolt:
   CPU Lite Load Mode 5-7

5. Use MSI Center only for monitoring, not fan control
```

A 13900KF + 240mm AIO can be quiet, but not with unlimited turbo + aggressive fan curves. The B760M Mortar is actually a good board; the noise is mostly the combination of **13900KF power behavior + 240mm radiator + default curves**.
