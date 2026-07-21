---
audio: false
generated: true
image: false
lang: en
layout: post
title: BIOS Fan Curve Too Aggressive
translated: false
type: note
---

Good news — the system is thermally fine. The fan noise is a BIOS behavior issue, not a cooling problem. Here's the diagnosis:

**Temperatures (all cool):**

- CPU package: 38°C (max core 35°C)
- GPU: 33°C, 11W, fan at 0% (passive)
- NVMe: 39.9°C
- Ambient/chassis: 27.8°C

**No thermal reason for fans to be loud.**

**The problem:**
The system has a PWM fan controller (`INTC1085:00` on Intel chipset) but the OS never exported the pwm0 channel — it's at `npwm=1` (1 fan header detected) but `pwm0/` directory doesn't exist. This means the OS isn't driving the fans at all. They're running at **BIOS/UEFI default**, which is typically 100% or a very aggressive curve. This is common on desktop boards where the BIOS handles fan control without handing it off to the OS.

`lm-sensors` found no fan speed sensors anywhere — the board's super I/O isn't exposing RPM readings either.

**Likely cause:**
The machine just booted 3 minutes ago. The BIOS fan curve is set to aggressive (possibly full speed at all temps), and `thermald` is running in polling mode with no config file (`/etc/thermald/thermal-conf.xml` doesn't exist), so it's not doing anything useful.

**Things you can try:**

1. **Enter BIOS/UEFI** (usually Del/F2 at boot) and adjust the fan curve — set a silent/profile or manual curve. Since the OS can't control fans, this is the place to fix it.

2. **Check if the noise is actually the HDD** — the 1.8TB WD20EZBX (7200RPM) at `/mnt/data` is a mechanical drive and makes audible seek/rotation noise. Unmount it temporarily to test if the noise stops.

3. **If you want OS-level fan control**, you'd need to export the PWM channel:

   ```bash
   echo 0 | sudo tee /sys/devices/platform/INTC1085:00/pwm/pwmchip0/export
   ```

   Then set duty cycle. But this is board-specific and might not work if the BIOS doesn't allow OS fan control.

4. **Create a thermald config** at `/etc/thermald/thermal-conf.xml` to give it proper thermal policies, though this won't help if the BIOS isn't surfacing fan control to the OS.

The quickest fix: **go into BIOS and set a silent fan profile**. The system is cool enough to run fans at minimum speed.
