---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla P100 needs forced airflow
translated: false
type: note
---

Question: Does the Tesla P100 have a cooling fan, and will it work in a B150M Pro + i5-6500?

Answer: **Yes electrically, but cooling is the big catch.**

### 1. P100 PCIe normally has **no fan**

The NVIDIA **Tesla P100 PCIe is passively cooled**. It has a large heatsink but **no onboard blower/fan**. NVIDIA explicitly specifies the thermal solution as *passive* and says it requires system airflow. ([NVIDIA Images][1])

It also draws up to **250 W** and requires substantial airflow through the heatsink. ([NVIDIA][2])

So:

```text
P100
 ┌─────────────────┐
 │  huge heatsink  │
 │ ███████████████ │
 │     GP100       │
 └─────────────────┘
        ↑
   NO onboard fan
```

A normal desktop case with just one weak exhaust fan is **not a good idea**. You need strong airflow directed through the P100 heatsink, or an aftermarket shroud/fan setup.

### 2. B150M + i5-6500: **yes**

Assuming your motherboard is one of the MSI **B150M PRO** models with a PCIe x16 slot, the P100 will work at the hardware/PCIe level.

For example, the B150M PRO-VHL has:

```text
PCIe 3.0 x16
```

and the P100 is:

```text
PCIe Gen3 x16
```

so they match perfectly. ([MSI][3])

Your **i5-6500 is also a 6th-gen LGA1151 CPU**, exactly the generation these B150 boards support. ([ASUS Global][4])

The CPU itself isn't a compatibility problem.

### 3. The real problem: PSU

This is what I'd pay attention to.

P100:

```text
GPU power:       250 W
PCIe interface:  x16
External power:  up to ~240 W via 8-pin
```

NVIDIA's specifications show the P100 can draw up to **250 W**, with the auxiliary 12 V input accounting for most of that. ([NVIDIA][2])

I'd use at least:

```text
quality 650 W PSU
        +
proper 8-pin PCIe GPU power cable
```

For a cheap/old PSU, I would **not** put a 250 W P100 on it.

### 4. One more important thing: P100 is a compute card

The P100 is not like a GTX 1080. It is a **Tesla compute accelerator**.

For your setup:

```text
B150M
  │
  ├── i5-6500
  │
  ├── P100 12/16 GB
  │      └── PCIe 3.0 x16
  │
  └── PSU ── 8-pin ── P100
```

For **CUDA / PyTorch / model inference / training**, that's exactly the kind of use case it was designed for.

But don't expect the P100 to behave like a normal gaming GPU with display outputs. The PCIe P100 is primarily a **headless compute accelerator**.

### My recommendation

If you're considering buying a cheap used P100 for an old desktop, I'd say:

**B150M + i5-6500 + P100 = viable**, provided you have:

* ✅ PCIe x16 slot
* ✅ Good **650 W+ PSU**
* ✅ Correct **8-pin PCIe power**
* ✅ Full-height / dual-slot clearance
* ⚠️ **Strong case airflow**
* ⚠️ Linux is preferable for a CUDA compute box

The **passive cooling is the thing I'd solve first**. A P100 running at 250 W continuously without adequate airflow will throttle badly or hit its thermal limit. NVIDIA specifies an operating limit around 80°C and slowdown around 82°C. ([Scribd][5])

If you're buying one for **LLM inference/training**, tell me the **exact P100 listing (12GB/16GB, PCIe/SXM2)** and your **PSU model**, and I can tell you whether I'd buy it.

[1]: https://images.nvidia.com/content/tesla/pdf/nvidia-tesla-p100-PCIe-datasheet.pdf?utm_source=chatgpt.com "Data Sheet: Tesla P100"
[2]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "Specifications"
[3]: https://www.msi.com/Motherboard/B150M-PRO-VHL/Specification?utm_source=chatgpt.com "Specification B150M PRO-VHL | MSI Global - The Leading Brand in High-end Gaming & Professional Creation"
[4]: https://www.asus.com/us/supportonly/b150m-et-v5/helpdesk_cpu/?utm_source=chatgpt.com "B150M-ET/V5 - Support"
[5]: https://www.scribd.com/document/738724628/NV-tesla-p100-pcie-PB-08248-001-v01?utm_source=chatgpt.com "NV Tesla p100 Pcie PB 08248 001 v01 | PDF | Graphics Processing Unit | Computing"
