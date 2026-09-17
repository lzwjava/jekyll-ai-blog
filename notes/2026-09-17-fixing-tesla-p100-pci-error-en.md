---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Tesla P100 PCI Error
translated: false
type: note
---

Question: **The A68HM-E still reports `PCI Resource ERROR / PCI OUT OF RESOURCES CONDITION` with the Tesla P100. What should I change?**

Answer: **This is probably not a PCIe Gen1/2/3 or PCI Latency Timer problem.** The P100 has a very large PCI BAR requirement. NVIDIA documents the P100's compute-mode **BAR1 as 16 GB**. ([NVIDIA Images][1])

The first thing I'd investigate is **64-bit PCI MMIO / Above 4G decoding**.

### 1. Try this BIOS configuration

On the A68HM-E, look for:

```text
Advanced
 └─ PCI / PCIe / PnP Configuration
      Above 4G Decoding       -> Enabled
```

If you have it, also try:

```text
PEG Link Speed               -> Gen3
PCI Latency Timer            -> 64
CSM                          -> Enabled
Fast Boot                    -> Disabled
```

**Do not change PCI Latency Timer to 128/256 hoping to fix this.** That isn't where the resource problem is.

`Above 4G Decoding` is specifically intended to allow 64-bit-capable PCI devices to be mapped above the 4-GB address boundary, and PCI resource exhaustion with NVIDIA GPUs is a known symptom when this isn't available/configured correctly. ([Supermicro][2])

### 2. But there's a bigger problem with this motherboard

The **A68HM-E is a 2014-era FM2+ board**. ASUS still lists the A68HM-E manual/support page, but this platform predates the kind of large PCIe MMIO allocation that modern accelerator cards commonly need. ([ASUS Global][3])

Your P100 is unusual compared with a normal GeForce card:

```text
Tesla P100 PCIe
PCIe interface: Gen3 x16
BAR0: 16 MB
BAR1: 16 GB  <-- important
BAR3: 32 MB
```

([NVIDIA Images][1])

So the situation can be:

```text
A68HM-E BIOS
      │
      ├── PCIe Gen3 negotiation       ✓
      │
      ├── PCI Latency Timer           ✓
      │
      └── PCI resource allocation
                │
                └── cannot allocate P100's BAR/MMIO
                              ↓
                    PCI OUT OF RESOURCES
```

This happens **before Linux/Windows/NVIDIA drivers even matter**.

### 3. Very useful test

Remove the P100.

Enter BIOS and enable:

```text
Above 4G Decoding = Enabled
```

Save, power off completely.

Then install **only the P100**.

Also disconnect/remove unnecessary PCIe devices temporarily:

* Wi-Fi card
* PCIe sound card
* extra SATA/RAID controller
* other GPUs
* PCIe capture cards
* anything else occupying PCI resources

Then boot.

### 4. If A68HM-E doesn't have "Above 4G Decoding"

This is the critical case.

If your BIOS **doesn't expose Above 4G Decoding / 64-bit PCI resource allocation**, then changing:

```text
Gen1
Gen2
Gen3
PCI Latency 32
PCI Latency 64
PCI Latency 128
```

probably won't solve the fundamental problem.

There are documented cases where enabling Above 4G decoding resolves exactly this `PCI OUT OF RESOURCES` condition. ([Supermicro][2])

And NVIDIA's P100 documentation confirms why this card is much more demanding in PCI address space than an ordinary GPU. ([NVIDIA Images][1])

### 5. One thing I want to see

**Take a photo of your A68HM-E BIOS `Advanced` menu**, especially anything containing:

```text
PCI
PCIe
PCI PnP
North Bridge
South Bridge
MMIO
Above 4G
64-bit
PEG
CSM
```

Send me that photo.

I can tell you **exactly which BIOS options to change**. The important question now isn't Gen1 vs Gen2 vs Gen3 — it's whether this old AMD BIOS can allocate the P100's **large 64-bit PCI MMIO/BAR space**.

[1]: https://images.nvidia.com/content/pdf/tesla/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "Specifications"
[2]: https://www.supermicro.com/en/support/faqs/faq.php?faq=15556&utm_source=chatgpt.com "FAQ Entry | Online Support | Support - Super Micro Computer, Inc."
[3]: https://www.asus.com/us/supportonly/a68hm-e/helpdesk_manual/?utm_source=chatgpt.com "A68HM-E - Support"
