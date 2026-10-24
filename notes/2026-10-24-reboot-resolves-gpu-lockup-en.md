---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reboot resolves GPU lockup
translated: false
type: note
---

✅ **Reboot complete and healthy.** Summary:

**What happened:**
- `shutdown -r +1` was scheduled at ~19:43, box went down, and has been back up for **1:10** (was 10 days up before)
- SSH is responding, load average dropped from **4.00 → 0.09**

**GPU — fixed** 🎉:
| Metric | Before | After |
|---|---|---|
| nvidia-smi | hung (D-state lockups, ~18min stuck procs) | responds instantly |
| Temp | 41°C | **32°C** |
| Power | 62W (P0) | **15W (P8, idle)** |
| Stuck processes | multiple D-state | **0** (no D/Z state procs) |
| Driver/CUDA | 580.178.04 / 13.0 | unchanged ✓ |

**System state:**
- Kernel: 7.0.0-38-generic ✓
- GPU: Tesla M40, 4 MiB / 11520 MiB used, 0% util, idle ✓
- 1 user logged in (was 6 — the desktop session from before came back under the boot)

The restart cleared the GPU I/O lockup that was making `nvidia-smi` hang. Everything's back to normal — anything else you want me to check?
