---
audio: false
generated: true
image: false
lang: en
layout: post
title: SAMA 600W PSU for GPU Testing
translated: false
type: note
---

Question: What is this **SAMA 战旗750 / 额定600W PSU**, and is it suitable for your GPU testing/build?

Answer:

This is a **SAMA (先马) 战旗 750** power supply. The important point is:

* **Model/series:** SAMA 战旗 750
* **Rated output:** **600 W** — despite the “750” in the product name
* **CPU power:** **2 × 8-pin EPS**
* **GPU power:** **2 × 6+2-pin PCIe** = can power a GPU requiring 6-pin or 8-pin PCIe
* **Condition:** seller claims nearly-new, personally used, upgraded/replaced
* **Warranty:** seller says there is still official replacement service
* **“包点亮”** = seller guarantees that a normal system will power on/display

### For your GPU repair/testing work

The connector configuration is actually quite useful:

```text
PSU
 ├── 24-pin ATX ─────── motherboard
 ├── 8-pin EPS ──────── CPU
 ├── 8-pin EPS ──────── optional second CPU connector
 ├── 6+2 PCIe ───────── GPU #1
 └── 6+2 PCIe ───────── GPU #2
```

But **600 W is the real limitation**.

For example:

| GPU              | Typical board power | 600W PSU           |
| ---------------- | ------------------: | ------------------ |
| GT 630           |             ~30–65W | ✅ Easily           |
| Quadro 4000      |               ~140W | ✅                  |
| RTX 4070         |               ~200W | ✅                  |
| RTX 4090         |               ~450W | ⚠️ Not recommended |
| RTX 5090         |               ~575W | ❌                  |
| 2 × RTX 4070     |     ~400W GPU alone | ⚠️                 |
| 2 × high-end GPU |               500W+ | ❌                  |

For **your current use case of testing broken GPUs**, I'd actually prefer a PSU with **more independent PCIe cables and 750–1000W capacity**, because you're likely to encounter cards with abnormal power consumption or short circuits.

One particularly important thing: **don't judge a PSU by “750” in the name**. Here the seller explicitly says **额定600瓦**, so treat it as a **600W PSU**.

If you send me the **actual label/photo of the SAMA PSU**, I can identify the exact OEM, 12V rail rating, protections, and whether I'd buy it for GPU repair work.

I can also compare this directly against the **Corsair CX650F RGB 750W** you were looking at and tell you which is better for GPU testing.
