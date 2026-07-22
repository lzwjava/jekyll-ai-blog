---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI B760M Mortar BIOS Quiet Guide
translated: false
type: note
---

Here's the detailed walkthrough for your MSI MAG B760M Mortar BIOS:

---

## 🛠 How to Fix: Step-by-Step BIOS Guide

### 1. Enter BIOS

- Restart your PC
- Repeatedly press **Del** (Delete) key immediately when the MSI logo appears
- Or press **F2** if Del doesn't work

### 2. Set AIO_PUMP to 100% Fixed Speed

```
- Press F7 to switch to Advanced Mode (if you're in EZ Mode)
- Go to: Hardware Monitor (or Settings → Hardware Monitor)
- Find: PUMP_FAN (or AIO_PUMP header entry)
- Set: DC Mode (not PWM)
- Set temperature source: CPU
- Set the fan curve to a flat line:
    Drag all points to 100%
    Or manually set:
        0°C → 100%
        100°C → 100%
  This locks the pump at full speed always.
```

**Why:** The Thermalright Frozen Prism 240 pump should run at constant speed. Varying pump speed causes water flow changes → temperature oscillation → fan ramping noise.

### 3. Set CPU_FAN Custom Curve

```
- Stay in: Hardware Monitor
- Find: CPU_FAN (or FAN1)
- Set: PWM Mode (not DC)
- Temperature source: CPU
- Select: "Custom" or "User" curve (not "Smart Fan" default)

  Set these points:
       ┌──────────┬──────────┐
       │ Temp (°C) │ Duty (%) │
       ├──────────┼──────────┤
       │    30    │    30    │
       │    50    │    50    │
       │    70    │    75    │
       │    85    │    100   │
       └──────────┴──────────┘

  On MSI boards, you typically:
    - Select a point on the graph
    - Press +/- or type the value
    - Move to the next point
```

**Why this curve matters:**

| Current (idle) | After fix |
| --- | --- |
| 31% PWM → **1546 RPM** | 30% PWM at 30°C → **~550 RPM** |
| CPU at 35°C, fan loud | CPU at 35°C, fan quiet |

The Thermalright prism fans have a **high minimum speed** (~1000-1200 RPM minimum). So setting 30% at 30°C will likely get you ~1000-1200 RPM instead of the theoretical 550 RPM — but that's still **much quieter than 1546 RPM**.

### 4. (Optional but Recommended) Undervolt + Power Limiting

```
BIOS path:
    Overclocking → Advanced CPU Configuration

Set:
    CPU Lite Load: Mode 5-7 (Mode 7 is more aggressive undervolt)
    → This reduces voltage = less heat = fans don't need to ramp

    Long Duration Power Limit (PL1): 200W
    Short Duration Power Limit (PL2): 200W
    Tau: 56 seconds or Auto
    → Limits max heat output without noticeable gaming performance loss
```

**Expected improvement:**

| Setting | Cinebench R23 | Max Temp | Noise |
| --------- | ---------------- | ---------- | ------- |
| Default (253W) | ~40000 pts | 100°C | Loud |
| CPU Lite Load Mode 7 + 200W limit | ~37000 pts | 80-85°C | Quiet |

### 5. Also Check Your HDD

You have a **WD20EZBX 1.8TB** (7200 RPM) mechanical hard drive at `/mnt/data`. This is a **physical noise source** separate from fans.

**Quick test:**

```bash
# Unmount to see if noise disappears
sudo umount /mnt/data
sudo hdparm -Y /dev/sda   # park the drive
# Listen — if noise stops, that's your HDD
```

### 6. Apply and Exit

```
Press F10 → Save Changes & Reset → Yes
```

After reboot, run `ww linux check-fan` again to verify fan1 RPM dropped.

### Summary Checklist

| Step | What | Expected Result |
| ------ | ------ | ----------------- |
| ✅ 1 | AIO_PUMP → 100% DC fixed | Stable water flow, no pump ramping |
| ✅ 2 | CPU_FAN → custom PWM curve | fan1 drops from 1546 to ~1000-1200 RPM at idle |
| ✅ 3 | CPU Lite Load Mode 7 | Less voltage, lower temps |
| ✅ 4 | PL1/PL2 = 200W | Max heat capped, fans stay quieter under load |
| ✅ 5 | Check HDD noise | Eliminate mechanical noise confusion |
