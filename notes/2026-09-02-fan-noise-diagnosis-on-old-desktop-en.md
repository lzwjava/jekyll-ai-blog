---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fan Noise Diagnosis on Old Desktop
translated: false
type: note
---

Here's a complete **fan source diagnosis**:

---

## Hardware Summary

| Item | Details |
| ------ | --------- |
| **CPU** | Intel Celeron E3400 @ 2.60GHz (dual-core) |
| **GPU** | Intel G41 Integrated Graphics (`i915` driver) — **no discrete card** |
| **Board** | Lenovo with Intel 4 Series / ICH7 chipset |
| **Fan sensors** | **None detected** |
| **Current temps** | CPU Core 0: **43°C**, Core 1: **37°C**, ACPI: **30°C** |

---

## Fan Check Results

### 1. No hardware fan speed sensors

`/sys/class/hwmon/` only shows:

- `hwmon0` = `acpitz` (motherboard temp)
- `hwmon1` = `coretemp` (CPU core temps)

**No `fan1_input`, `fan2_input`, or `pwm*` files exist.** The system cannot report fan RPM to software.

### 2. No ACPI fan devices

```
/proc/acpi/fan → does not exist
/sys/bus/acpi/devices/*FAN* → none found
```

### 3. No GPU thermal zone

```
/sys/class/drm/card0/device/hwmon/ → does not exist
```

The Intel integrated GPU does not expose a hwmon interface.

### 4. Thermal policy

- Critical trip point: **110°C**
- Current temps are **~70°C below critical** — the CPU is basically idle/cool.
- Cooling devices (`Processor`) show `cur_state=0` (not throttling).

---

## What plugin are you seeing?

Your XFCE panel config (`xfce4-panel.xml`) shows **no GPU/sensor plugin** is active. The running plugins are:

| Plugin | Purpose |
| -------- | --------- |
| applicationsmenu | Start menu |
| tasklist | Window list |
| pager | Workspace switcher |
| systray | System tray |
| clock | Time |
| actions | Shutdown/etc |
| showdesktop | Minimize all |
| launcher x4 | App shortcuts |
| directorymenu | File manager menu |

If you see a "GPU" or "graphics card" icon somewhere, it might be:

- A **generic monitor widget** (e.g., Conky, a custom script, or a system tray icon from a GPU tool you installed previously)
- A **status icon** for a VM/emulator software

---

## Why is the fan loud?

Even though temps read ~37–43°C, the fan on this older Lenovo desktop is likely **BIOS-controlled** (not OS-controlled), and it may run at a fixed or aggressive curve. Common causes:

1. **Dust / clogged heatsink** — old Intel G41/Celeron systems easily accumulate dust, making the CPU fan spin high.
2. **Dried thermal paste** — 10+ year old machine; thermal paste on the Celeron E3400 may be degraded, causing the fan to work harder.
3. **Case/chassis fan** — the loud noise might be a cheap sleeve-bearing case fan, not the CPU fan.

---

## Recommendation

If the noise is bothering you:

```bash
# Check if any hidden GPU monitoring process is running
ps aux | grep -iE "nvidia|amd|gpu|temp|sensor|fan"
```

Since the system has **no discrete GPU and no fan sensors**, a "GPU graphical card plugin" showing data is either:

- **Reading Intel iGPU stats** (which has no fan/temp sensor), or
- **A leftover artifact** from software that expects an NVIDIA/AMD card

**For the physical noise:** Open the case and clean the CPU heatsink/fan with compressed air. If it's a Lenovo G41-era desktop, the CPU fan is likely a small 65W Intel stock cooler that gets noisy with age.

Would you like a command to check if any hidden background process is pretending to monitor a GPU?
