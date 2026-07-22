---
audio: false
generated: true
image: false
lang: en
layout: post
title: "MSI Fan Diagnostic: High Idle RPM"
translated: false
type: note
---

Here's the complete English summary of your fan diagnostic:

---

## Fan Check Results — MSI MAG B760M Mortar + Thermalright Frozen Prism 240

### Hardware Monitor Chip

Loaded **NCT6687D** driver (`nct6683 force=1`) — configured to auto-load on boot.

### Current Fan Status

| Channel | RPM | PWM | Notes |
|---------|-----|-----|-------|
| **fan1** | **~1546 RPM** | **81/255 (31%)** | **Only active fan** |
| fan2-fan10 | 0 RPM | various | Unconnected headers or no feedback |

### Temperatures (all excellent)

```
CPU (PECI):      35°C
PCH (Chipset):   49°C
GPU (RTX 4070):  39°C (fans stopped)
NVMe (980 1TB):  40°C
HDD (WD20EZBX):  active/idle
```

### Key Findings

**1. ⚠️ Fan runs high at idle**

- PWM 31% should map to ~590 RPM if linear, but you're getting **1546 RPM**
- The Thermalright Prism 240 fans (max ~1850 RPM) are running at ~83% of max speed at just 31% PWM
- Likely: the fan's PWM response has a high minimum floor, OR the BIOS minimum duty cycle is set too high

**2. 🔇 OS has no PWM control**

- PWM controller (`INTC1085:00`, `npwm=1`) shows 0/1 channels exported
- **BIOS is in full control** of fan curves — typical for MSI boards

**3. 🔊 HDD mechanical noise contributor**

- **WD20EZBX** (1.8TB, 7200 RPM) spinning drive — continuous rotation/seek noise

**4. 🎯 Pump likely not reporting speed**

- The AIO pump is probably on the **AIO_PUMP** header, which reports 0 RPM to the NCT6687 chip — it's likely running at full speed but the sensor doesn't capture it

---

## 🛠 Recommended Fixes

### Enter BIOS (Del/F2) → Hardware Monitor

```
1. Set AIO_PUMP header to 100% fixed (DC full speed)
   This keeps water flowing consistently regardless of CPU temp

2. Set CPU_FAN to PWM mode with a custom curve:
     30°C → 30%  (~550 RPM)
     50°C → 50%  (~920 RPM)
     70°C → 75%  (~1400 RPM)
     85°C → 100% (~1850 RPM)
```

### For Quieter Operation

**BIOS → Overclocking → CPU Lite Load**: Set to **Mode 5-7**. This **undervolts** the 13900KF — minimal performance loss, 10-15°C temperature reduction.

**BIOS → Tools → Custom Turbo**: Set **Long Duration Power Limit to 200W**. This significantly reduces heat output with only ~5% performance loss in heavy workloads.

### 📊 Your Hardware Summary

| Component | Status |
| ----------- | -------- |
| CPU | i9-13900KF @ 35°C idle (powersave governor) |
| Motherboard | MSI MAG B760M Mortar (NCT6687D chip) |
| Cooler | Thermalright Frozen Prism 240 (fan1: ~1546 RPM) |
| GPU | RTX 4070 @ 39°C (fans stopped) |
| Storage | WD20EZBX 1.8TB HDD + Samsung 980 1TB NVMe |
| Thermal status | ✅ All temperatures well within limits |

Run `ww linux check-fan` anytime to re-check fan status and temperatures.
