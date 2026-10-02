---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla M40 power cable error
translated: false
type: note
---

Yes — there **is** a Tesla M40 in that machine, but it's **not powered properly**, so the driver can't bring it up.

**What I found on `192.168.1.34`:**

| Item | Result |
| ------ | -------- |
| GPU | `NVIDIA GM200GL [Tesla M40]` at `0000:01:00.0` ✅ |
| Driver | 580.178.04 loaded (kernel modules `nvidia`, `nvidia_uvm`, etc.) |
| `nvidia-smi` | ❌ `No devices were found` |

**The actual error** (from `journalctl`):

```
NVRM: GPU 0000:01:00.0: GPU does not have the necessary power cables connected.
NVRM: GPU 0000:01:00.0: RmInitAdapter failed! (0x24:0x1c:1603)
NVRM: GPU 0000:01:00.0: rm_init_adapter failed, device minor number 0
```

The card is detected on the PCIe bus and the driver enumerates it (`Model: Tesla M40` in `/proc/driver/nvidia/gpus/`), but the GPU UUID reads as `GPU-????-????-...` because it never completes initialization — it's a **power delivery problem, not a driver/software problem**.

**Important note about the Tesla M40:** it does **not** use a standard PCIe 8-pin GPU cable. It uses an **8-pin EPS (CPU) power connector** (250W card). This is the most common reason for exactly this error on M40s — people plug in a PCIe 8-pin (or leave it unplugged) and the card reports "power cables not connected."

**To fix:**

1. Power off the machine.
2. Connect a proper **EPS 8-pin** cable from the PSU to the M40's power connector (M40 has a single 8-pin EPS connector).
3. Make sure the PSU can supply ~250W for the card.
4. Power on and check `nvidia-smi` again.

Want me to check the PSU/cabling info or anything else on that box?
