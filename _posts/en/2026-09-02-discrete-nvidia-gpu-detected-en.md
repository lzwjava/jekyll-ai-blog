---
audio: false
generated: true
image: false
lang: en
layout: post
title: Discrete NVIDIA GPU Detected
translated: false
type: note
---

Your system has a **discrete NVIDIA GPU**:

| Property | Value |
| --- | --- |
| **GPU** | NVIDIA GeForce GT 730 (GK208B) |
| **Vendor** | ASUS (`1043:84f7`) |
| **PCI Address** | `01:00.0` |
| **Driver** | `nouveau` (open-source) |

It’s **not an integrated card** — it sits on its own PCIe slot with dedicated memory regions (128MB + 32MB prefetchable, 16MB non-prefetchable), and the system routes display interrupts to it.

If you want to switch to the proprietary NVIDIA driver, install `nvidia-driver-XXX` (where `XXX` matches your distro’s package) and reboot. With the proprietary driver loaded, `nvidia-smi` will work.
