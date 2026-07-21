---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fan Diagnosis Tool
translated: false
type: note
---

Done. Saved at `~/projects/ww/ww/linux/check_fan.py` and registered as `ww linux check-fan`.

Next time you hear a loud fan, just run:

```
ww linux check-fan
```

It collects in one shot:

- **Temperatures** — CPU cores, GPU, NVMe, chassis via lm-sensors + sysfs
- **Fan controllers** — PWM chips, exported channels, duty cycles, or detects "BIOS controls fans"
- **GPU fan** — nvidia-smi fan speed %, temp, power draw
- **Spinning disks** — lsblk ROTA flag to flag HDDs
- **thermald** — whether the thermal daemon has a config file or is running in polling mode
- **CPU load/frequency** — top consumers + per-core MHz
- **Disk I/O** — iostat snapshot showing util%, await, iowait
- **Summary verdict** — tells you if OS has no fan control (BIOS fix needed), or flags HDD noise

Committed and pushed as `c9cca06`.