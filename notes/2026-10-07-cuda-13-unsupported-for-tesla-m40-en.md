---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA 13 Unsupported for Tesla M40
translated: false
type: note
---

I checked both against NVIDIA's official docs — and got a clear, mixed answer:

## 1. Driver → 580.178.04: ✅ Yes, supported

NVIDIA 580.178.04's supported-chips list explicitly includes your card:
```
Tesla M40        (17FD)
Tesla M40 24GB   (17FD 10DE 1173)   ← yours
```
So the driver itself can be upgraded and the M40 will still work.

**But** there's an important caveat: Debian trixie only packages **550.163.01**. To get exactly 580.178.04 I'd have to install NVIDIA's `.run` installer (or add NVIDIA's repo), which is riskier than apt and needs re-doing manually on every kernel update. For this old card, 550 vs 580 makes **zero functional difference**.

## 2. CUDA → 13.0: ❌ Not possible for this GPU

NVIDIA's own CUDA 13.0 release notes say:

> "Removed support for **Maxwell**, Pascal, and Volta GPUs, corresponding to compute capabilities earlier than Turing."
> "Dropped support for **pre-Turing** architectures."

Your Tesla M40 is **Maxwell (compute capability 5.2)** — it was removed in CUDA 13.0. The maximum CUDA toolkit that can target the M40 is **CUDA 12.x**.

> Note: if you upgrade the *driver* to 580.178.04, `nvidia-smi` will show "CUDA Version: 13.0" — but that's just the driver's API level. It does **not** mean you can run CUDA 13.0 apps on the M40. CUDA 13.0-compiled code simply won't run on Maxwell.

## What I recommend

| Goal | Action |
|---|---|
| Match the other desktop's driver (580.178.04) | Possible, but **not worth it** for the M40 — 550.163.01 is stable, apt-managed, and fully supports the card |
| Actually run CUDA compute on the M40 | Install **CUDA 12.x toolkit** (Debian's `nvidia-cuda-toolkit`) — this is the real "upgrade" that matters |

So the honest answer:
- **CUDA 13.0: can't use with the M40, period.**
- **Driver 580.178.04: can do it, but I'd advise keeping 550.**

How would you like to proceed?

1. **Install CUDA 12.x toolkit** (recommended — makes the M40 actually useful for PyTorch etc.)
2. **Still upgrade the driver to 580.178.04** (I'll do the `.run` install, but I'll flag the maintenance cost)
3. **Both** (580 driver + CUDA 12.x toolkit)
