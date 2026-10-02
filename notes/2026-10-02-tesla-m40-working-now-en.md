---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla M40 Working Now
translated: false
type: note
---

It's working now. 🎉

```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.178.04             Driver Version: 580.178.04     CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|=========================================+========================+======================|
|   0  Tesla M40                      Off |   00000000:01:00.0 Off |                    0 |
| N/A   28C    P8             15W /  250W |       4MiB /  11520MiB |      0%      Default |
+-----------------------------------------+------------------------+----------------------+
```

**The Tesla M40 is now fully initialized:**
- ✅ `nvidia-smi` works, exit code 0
- ✅ Card recognized: `Tesla M40`, UUID `GPU-9d2f8eda-4ad8-2f53-2959-da07ed35e311`
- ✅ Power: 15W idle / 250W cap — the power-cable problem is fixed
- ✅ Temp: 28°C, P8 idle state, healthy
- ✅ 11520 MiB VRAM (the 12 GB M40), CUDA 13.0

Only thing running on it is `gnome-shell` (1 MiB) — the card is otherwise idle and ready for compute. What did you do, reconnect the EPS 8-pin?