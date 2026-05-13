---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Health Summary Under Power Cap
translated: false
type: note
---

GPU is healthy. Quick read:

```
RTX 4070 (12 GB)
─────────────────────────────
Temp:       66 °C    ✓ (throttle starts ~83 °C → 17 °C headroom)
Power:      208 / 215 W  → at the power cap, normal for sustained training
Fan:        56 %     ✓ moderate, room to spin up if temp rises
GPU-Util:   100 %    ✓ pegged
Memory:     7.5 / 12.0 GiB (61 %) ✓ comfortable, no OOM risk
Perf state: P2       ✓ max performance
ECC errors: none reported
```

Training process (PID 1200744, python3.11) is the only meaningful workload — 7.36 GiB. Xorg + gnome-shell take <120 MiB combined, no issue.

**Why MFU is "only" 12.86%:** the card is hitting its **215W power cap**, not thermal limits. That's the bottleneck — there's no fix without raising the cap (which on a 4070 isn't meaningful) or undervolting. Step time of 11.11 s/iter is what this card can do at this power budget, and it's been rock-stable for ~5 hours.

**Bottom line:** nothing concerning. Temps are good, power is steady, memory has headroom, no errors. Run can finish.