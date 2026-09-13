---
audio: false
generated: true
image: false
lang: en
layout: post
title: SXM2 GPU Interface Guide
translated: false
type: note
---

**Question:** What is the SXM2 interface on Tesla GPUs, and how do you use it?

No search needed — this is well-established hardware knowledge.

**What is SXM2?**

SXM2 (Server PCI Express Module 2) is NVIDIA's proprietary high-bandwidth mezzanine socket designed for data center use. It's **not a standard PCIe slot** — it plugs directly into a specially designed board/baseplate on compatible server platforms.

**Why SXM2 exists:**
The whole point is bandwidth. SXM2 delivers more power and NVLink lanes directly to the GPU, enabling the full HBM2 bandwidth potential that a standard PCIe slot would bottleneck.

| Feature | PCIe Version | SXM2 Version |
| --- | --- | --- |
| Interface | PCIe x16 | Proprietary mezzanine |
| Memory Bandwidth (P100) | ~549 GB/s | **~732 GB/s** |
| Memory Bandwidth (V100) | ~900 GB/s | **~900 GB/s** |
| NVLink support | No | **Yes** |
| Power delivery | Via PCIe slot + aux | **Direct from board** |
| Cooling | Own heatsink/fan | **Server chassis airflow** |
| Consumer motherboard compatible | ✅ Yes | ❌ No |

---

**How to actually use an SXM2 GPU:**

You need one of these compatible platforms — there is no adapter that works reliably:

- **NVIDIA DGX-1** (P100 or V100)
- **NVIDIA HGX-1 / HGX-2** baseboard
- **Supermicro SYS-4028GR-TRT2** (P100 SXM2)
- **Dell EMC DSS 8440** (V100 SXM2)
- **IBM Power Systems AC922**

You cannot plug an SXM2 card into a regular desktop or server motherboard. The SXM2 socket is on a **dedicated GPU baseplate/board**, which then connects to the host system via PCIe or NVLink fabric.

---

**Practical advice for secondhand buyers:**

If you're seeing SXM2 P100 or V100 cards sold cheaply on Xianyu/Taobao, be aware:

- ⚠️ **Useless without a compatible SXM2 host board** — the card alone does nothing
- ⚠️ Compatible host boards (HGX baseplates) are expensive and rare secondhand
- ⚠️ No display output, no PCIe adapter exists that works at full speed
- ✅ **PCIe versions** of P100/V100 are far more practical for individual buyers — they plug straight into any server or workstation with a PCIe x16 slot

**Bottom line:** Unless you already have an SXM2-compatible server platform, always buy the **PCIe variant** of P100 or V100 instead. The SXM2 cards are essentially unusable outside their intended server chassis.
