---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpCore-Simplify Automated EFI Builder
translated: false
type: note
---

**Question:** Give me an intro to the OpCore-Simplify project (github.com/lzhoang2801/OpCore-Simplify).

**Answer:**

**OpCore-Simplify** is a Python CLI tool (~6.4k stars, 592 forks, BSD-3-Clause) that automates the most tedious part of Hackintoshing: building an OpenCore EFI folder tailored to your exact hardware, instead of hand-assembling it by following the Dortania guide.

### The problem it solves

Building an OpenCore EFI manually means: dumping ACPI tables, figuring out which SSDT patches your motherboard needs, picking the right kexts (Lilu, WhateverGreen, VirtualSMC, audio codec, NIC driver...), choosing an SMBIOS, and hand-editing a `config.plist` with hundreds of keys. One wrong quirk = kernel panic. OpCore-Simplify turns this into a pipeline: **hardware report in → bootable EFI out**.

### How it works (the pipeline)

1. **Hardware detection** — on Windows it can export a hardware report directly; otherwise you feed it a `Report.json` + ACPI dump from its companion tool Hardware-Sniffer.
2. **Compatibility check** — a `Compatibility Checker` tells you which devices and macOS versions your hardware supports.
3. **ACPI patching** — integrates SSDTTime for common patches (FakeEC, FixHPET, PLUG, RTCAWAC) plus custom ones: fixing _PRW sleep-state values to prevent immediate wake, disabling unsupported PCI devices, adding devices like PNLF, MCHC, USBX, and HEDT-specific kernel panic fixes.
4. **Kext + bootloader fetching** — automatically checks and downloads current OpenCorePkg and kexts from Dortania Builds and GitHub releases before each build.
5. **config.plist generation** — applies opinionated defaults: GPU ID spoofing for unrecognized AMD cards, CpuTopologyRebuild for Intel P/E-core CPUs, ResizeAppleGpuBars configuration, SMBIOS selection optimized for power management and performance, and itlwm WiFi profiles for auto-connect at boot.

### Hardware coverage

Intel Nehalem (1st gen) through Arrow Lake (15th gen/Core Ultra 2), AMD Ryzen/Threadripper via AMD Vanilla patches; GPUs from Intel iGPUs (Iron Lake → Ice Lake), AMD Navi 21/22/23 and Vega APUs, to legacy NVIDIA (Kepler/Pascal/Maxwell); macOS High Sierra → Tahoe 26 — the Tahoe support leaning on the author's own fork of OpenCore Legacy Patcher 3.0.0, since official Dortania releases won't work with Tahoe early patches.

### Repo structure

Minimal and readable — `OpCore-Simplify.py` is the entry point, `Scripts/` holds the logic (including `datasets/kext_data.py`, essentially a curated knowledge base mapping hardware IDs → kexts), plus `.bat`/`.command` launchers. 96% Python, no heavy dependencies — it's in the same spirit as corpnewt's tooling (SSDTTime, UnPlugged), which it builds on.

### Caveats

The author is explicit that it doesn't guarantee a first-attempt successful install — you still need Dortania-guide basics, USB port mapping afterward, and troubleshooting patience. It gets you a *very good starting EFI*, not a turnkey install.

Worth noting for your context: the interesting engineering here is the encoded expert knowledge — years of Hackintosh community heuristics compressed into rule-based Python (hardware fingerprint → patch set). It's a classic expert system; a fun thought experiment is how much of `kext_data.py` + the ACPI patch heuristics could be replaced by an agent that reads the ACPI dump directly.

**References:**

- [OpCore-Simplify — GitHub](https://github.com/lzhoang2801/OpCore-Simplify)
- [Dortania OpenCore Install Guide](https://dortania.github.io/OpenCore-Install-Guide/)
- [Hardware-Sniffer (companion tool)](https://github.com/lzhoang2801/Hardware-Sniffer)
