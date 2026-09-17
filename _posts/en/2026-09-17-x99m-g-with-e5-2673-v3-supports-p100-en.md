---
audio: false
generated: true
image: false
lang: en
layout: post
title: X99M-G with E5-2673 v3 Supports P100
translated: false
type: note
---

Question: **Can the JGINYUE X99M-G D3 ARGB + Xeon E5-2673 v3 run an NVIDIA Tesla P100 PCIe?**

Answer: **Yes. Electrically/PCIe-wise, this combination should work.** There are a few important caveats.

The exact motherboard in your listing is **JGINYUE X99M-G D3 ARGB**. JGINYUE specifies:

* LGA2011-3
* Xeon E5-2673 v3 supported
* **1× PCIe 3.0 x16**
* DDR3, dual-channel, up to 64 GB
* 24-pin ATX + 8-pin CPU power
* Windows 7/10 officially listed ([jginyue][1])

The **Tesla P100 PCIe** is also:

* PCIe **3.0 x16**
* 250 W maximum board power
* Requires an auxiliary **CPU 8-pin** power connector
* Passive heatsink
* Full-height, dual-slot
* UEFI supported ([NVIDIA][2])

So the basic path is:

```text
E5-2673 v3
     │
LGA2011-3
     │
JGINYUE X99M-G D3 ARGB
     │
PCIe 3.0 x16
     │
Tesla P100 PCIe 16GB/12GB
```

### ⚠️ The big issue: cooling

This is the thing I'd worry about **more than compatibility**.

The P100 PCIe is a **passive** 250 W accelerator. NVIDIA explicitly specifies that the card requires system airflow to stay within its thermal limits. ([NVIDIA Images][3])

So you **cannot treat it like a normal gaming GPU** with its own fan.

You want something like:

```text
[front intake fan]
       ↓↓↓↓↓
┌───────────────────────┐
│ CPU          P100     │
│ cooler       █████    │
│              █████    │
│              █████    │
└───────────────────────┘
       ↓↓↓
[rear exhaust]
```

With a normal desktop case and weak airflow, the P100 can get extremely hot.

### ⚠️ Power supply

P100 is rated at **250 W**. NVIDIA specifies up to 240 W through its auxiliary CPU 8-pin input and up to 66 W through the PCIe slot. ([NVIDIA][4])

I'd use at least a **quality 550–650 W PSU** for:

```text
E5-2673 v3     ~105 W TDP
Tesla P100     250 W
motherboard    ~40–60 W
RAM/SSD/fans   ~30–50 W
----------------------
realistic      ~425–465 W
```

Don't use a random cheap "500 W" PSU.

### ⚠️ BIOS

Interestingly, JGINYUE currently provides both **original BIOS and "chicken blood" BIOS** for this board. ([jginyue][1])

For a Tesla compute box, I'd start with the **original BIOS**, not a modded/"鸡血" BIOS.

You don't need some special Tesla BIOS on the motherboard. The P100 itself has UEFI support. ([NVIDIA][2])

### One more important distinction

Make sure the listing says:

> **Tesla P100 PCIe**

and **not**

> Tesla P100 SXM2

They are completely different physical interfaces.

```text
P100 PCIe       → YES, this motherboard
P100 SXM2       → NO, cannot plug into PCIe slot
```

NVIDIA's documentation identifies the PCIe version as PCIe Gen3 x16, while the SXM2 version is a completely different form factor. ([NVIDIA Images][3])

### My take on this ¥230-ish platform

For a cheap CUDA machine, the architecture is actually quite interesting:

```text
E5-2673 v3
12C / 24T
     +
64GB DDR3
     +
Tesla P100 16GB HBM2
     ↓
CUDA / PyTorch / inference
```

The **P100 is the valuable part**. The X99 + Xeon platform is basically just a cheap PCIe host.

One caveat: **P100 is Pascal (compute capability 6.0)**, so before buying one specifically for modern AI workloads, check whether the exact CUDA/PyTorch stack you intend to run still supports `sm_60`. That's potentially more important in 2026 than whether the motherboard can electrically run the card.

[1]: https://www.jginyue.com.cn/index/Article/show/cat_id/48/id/222?utm_source=chatgpt.com "精粤X99M-G D3 ARGB主板 - Intel LGA 2011-3 - 精粤JGINYUE官网"
[2]: https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "SPECIFICATIONS"
[3]: https://images.nvidia.com/content/grid/pdf/DA-09018-001_v07.pdf?utm_source=chatgpt.com "Tesla P100

The NVIDIA Tesla P100 GPU Accelerator"
[4]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "Specifications"
