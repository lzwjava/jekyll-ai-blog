---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X Status and Setup Steps
translated: false
type: note
---

Looks good — that's a clean readout of the MI300X.

**The card in plain terms:**
- **AMD Instinct MI300X** — 256 GB HBM3, PCIe 5.0 x16, fully allocated to this VM as a VF (dedicated, not shared)
- It's sitting at max link speed (32 GT/s x16), in D0 power state, ready to use

**The catch**: it's a VF, so you don't have temperature/clock/power telemetry or the ability to run compute workloads yet — those require the full ROCm stack. Right now you have the driver but not the runtime.

**To make it compute-ready**, you'd need:
```
apt install rocm-hip-sdk
```
That pulls in HIP (AMD's CUDA equivalent), ROCm libraries, and should wire up KFD so `rocm-smi` works too. It's a heavy install (~several GB) but it's the standard path.

Want me to kick that off, or are you good with the current visibility?
