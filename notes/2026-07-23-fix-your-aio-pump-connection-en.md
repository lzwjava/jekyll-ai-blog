---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Your AIO Pump Connection
translated: false
type: note
---

**AIO_PUMP** = **All-In-One Pump header** on your motherboard.

It's a dedicated 4-pin fan header labeled specifically for AIO (All-In-One) liquid cooler pumps.

### On your MSI MAG B760M Mortar board:

The motherboard has these relevant headers:

| Header | Label on board | Purpose |
|--------|----------------|---------|
| **AIO_PUMP** | top edge, near CPU socket | For the **pump** of your liquid cooler |
| **CPU_FAN** | right of CPU socket | For the **radiator fans** (or air cooler fan) |
| **PUMP_FAN** | sometimes same as AIO_PUMP | Alternate pump header |
| **SYS_FAN1-4** | around the board | For case fans |

### Your current setup (likely wrong):

```
AIO pump cable  ──→  CPU_FAN     ← pump controlled by CPU temp curve (bad)
Radiator fans   ──→  ???
```

This causes:
- Pump speed fluctuates with CPU temp spikes
- Water flow changes → temperature oscillation
- Fans ramp up and down → annoying noise

### Should be:

```
AIO pump cable  ──→  AIO_PUMP    ← pump runs at 100% fixed (good)
Radiator fans   ──→  CPU_FAN     ← fans controlled by CPU temp curve
```

### How to tell which cable is which on your Thermalright Frozen Prism 240:

The AIO has **two cables** coming from the pump block:

1. **Pump power cable** (3-pin or 4-pin, thicker wire) — labeled "PUMP" or comes from the pump housing
2. **Fan cables** — come from the two radiator fans, often daisy-chained together into one connector

Check your cable routing and make sure:
- The **pump cable** goes to **AIO_PUMP** header on the motherboard
- The **radiator fan cables** go to **CPU_FAN** header (or via a splitter to CPU_FAN)