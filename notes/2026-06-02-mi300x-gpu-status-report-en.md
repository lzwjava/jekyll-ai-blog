---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X GPU Status Report
translated: false
type: note
---

Here's the quick GPU status:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  MI300X GPU Status — rocm-smi
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GPU Utilization:  100%       ← fully saturated
VRAM Used:        63.5 GB / 192 GB  (33%)
Power:            747W / 750W cap    ← running at limit
Junction Temp:    75°C
Memory Temp:      50°C
SCLK (GPU):       1351 MHz
MCLK (Memory):    900 MHz
Fan:              0% (passive/server cooling)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Key commands for future reference:

  rocm-smi                              # quick overview (like nvidia-smi)
  rocm-smi -a                           # all details
  rocm-smi --showuse --showmeminfo vram # GPU% + VRAM
  rocm-smi --showtemp --showpower       # thermal + power
  rocm-smi --showclocks                 # clock speeds
  watch -n1 rocm-smi                    # live monitoring

GPU is at 100% utilization, 747W power draw (near the 750W cap), junction temp 75°C — all normal for a sustained training workload. VRAM is only 33% used, so you have plenty of room to scale batch size or model size if needed.