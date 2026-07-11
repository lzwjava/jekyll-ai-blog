---
audio: false
generated: true
image: false
lang: en
layout: post
title: Great Wall Power Supplies Quality
translated: false
type: note
---

Question: How good are Great Wall (长城) power supplies?

Answer:

Great Wall Computer Shenzhen Co., Ltd. (长城电源) is actually one of the more mature Chinese PSU brands. It is not just a random domestic brand — it has been making PC power supplies for decades and has OEM experience.

For a normal desktop / AI workstation, a good Great Wall Gold/Platinum PSU is generally **a reasonable choice**.

The key is: **judge the specific model, not only the brand.**

### Great Wall strengths

* ✅ Long history in PSU manufacturing
* ✅ Good domestic supply chain
* ✅ Many models use decent platforms (depending on series)
* ✅ Warranty is often competitive (some high-end models 10 years)
* ✅ Usually cheaper than equivalent Seasonic/Corsair models

For example:

* Platinum efficiency means the PSU wastes less power as heat.
* A 10-year warranty usually indicates the manufacturer has confidence in capacitor life and platform reliability.

### Compared with international brands

Rough ranking:

```
Tier S:
Seasonic high-end
Super Flower high-end
Corsair AX/HX series

Tier A:
Great Wall high-end Platinum
FSP high-end
be quiet! high-end
Cooler Master high-end

Tier B:
Great Wall mainstream
Corsair RM/RMe
Thermaltake Toughpower
```

But some Corsair models are actually made by other OEMs (CWT, Seasonic, HEC, etc.), so the OEM/platform matters more than the logo.

### For your MI50 / AI workstation case

Your situation is different from a gaming PC:

* AMD MI50:

  * ~300W GPU power
  * server/workstation style
  * HBM memory
  * sustained compute load

A cheap gaming PSU is not ideal because AI workloads can run:

```
GPU 300W
CPU 125W+
motherboard + disks + fans 50W
----------------------------
450-550W continuous
```

A good:

* 750W Platinum
* 850W Gold/Platinum

is a comfortable range.

Example:

```
Wall power:
900W PSU @ 60% load
↓
GPU training 24h/day
↓
less heat
less fan noise
better capacitor life
```

### My view

Your friend saying:

> "以后装机买长城吧，长城白金牌，10年质保"

is reasonable.

For AI home lab, I would rather buy:

```
Great Wall Platinum 850W
+
stable motherboard
+
good cooling
```

than save 300 RMB on PSU.

The PSU is the one component that can kill:

* GPU
* motherboard
* SSD

and usually the expensive GPU is the thing you don't want to gamble with.

For your MI50 build, a high-end Great Wall Platinum is actually a better match than many flashy gaming PSUs.
