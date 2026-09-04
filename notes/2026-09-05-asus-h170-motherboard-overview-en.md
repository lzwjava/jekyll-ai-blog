---
audio: false
generated: true
image: false
lang: en
layout: post
title: ASUS H170 Motherboard Overview
translated: false
type: note
---

Question: **Intro to ASUS H170 motherboards**

Answer:

![Image](https://images.openai.com/static-rsc-4/HGvWQGRzHHPZcD5asqbaX4UnE_dOvzOfJoD1PD2tqOqUmnf5dp8QD5bSNOfdshFqGKew7t1CWN1t3RJmvHBTUW2tKxFvn6Uc4qBMoUZwXN60vpPi1P9W0mvmX8RZBFoh_k9_FsM_HgFH4DXw_1ga2oKu_3QAi0SxGHmSLLvneh88ldxA-8cLAmta1qVyJnKb?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/N7ibr4zFWwHtQJQV5GL7cBdhnqbHMH79p-VrjsF1t3CVK5ri5PKU_nRxPJjFuLQFOd6kkn4sV1xRTRzO__TtQ5jUaXyuNa_dzMHX8TOkA955STCKGg6S3_MCPsFzG5IjxDD-Gb6LLyr7GGn5_UGOE2Ftv3KCvYT2ZtyQ1RIFNPe2pptjhdZPi5jNIecy8VzD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/bRKF1Kxyif3PdTAVqdQqntK7OFcR5IhqiTS231-p4KEyAp8ul7ktq7HRR9ZiTuFolJnKxXmxlzwamh5VdGXR20FoUys3OEXGMDVQcZg6LG4cKk0vN-36WfdZ9rXgaJxRqF6GWpsDqmxoeml-YhCXeccvKoho7MPjNSYhN8rFzDAl4Wv3a6O4QM0sKm0Lj9iw?purpose=fullsize)

The **ASUS H170 series** is Intel's **100-series motherboard platform**, released around **2015–2016**, primarily for 6th-gen Skylake CPUs.

### Core specs

| Feature             | ASUS H170                     |
| ------------------- | ----------------------------- |
| CPU socket          | **LGA1151**                   |
| CPU generation      | Intel 6th gen Core (Skylake)  |
| Chipset             | Intel H170                    |
| RAM                 | DDR4, typically 2133 MHz      |
| Memory channels     | Dual-channel                  |
| CPU overclocking    | ❌ No                          |
| RAM overclocking    | Generally ❌                   |
| PCIe x16            | Usually 1 × x16               |
| M.2                 | Depends on exact ASUS model   |
| SATA                | Up to 6 × SATA 6 Gb/s         |
| USB                 | USB 3.x + USB 2.0             |
| Integrated graphics | Outputs depend on board       |
| Form factors        | ATX / mATX depending on model |

### CPU compatibility

The interesting part is that H170 uses **LGA1151**, so you can commonly pair it with:

```text
Celeron G39xx
Pentium G44xx/G45xx
Core i3-6100 / 6300
Core i5-6400 / 6500 / 6600
Core i7-6700
```

Some ASUS H170 boards can also support **7th-gen Kaby Lake** CPUs after a BIOS update, e.g.:

```text
i7-7700
i5-7500
i3-7100
```

But you should check the **exact ASUS model + BIOS version** before assuming 7th-gen support.

### H170 vs B150 vs Z170

The three common 100-series chipsets are roughly:

```text
                    H170       B150       Z170
------------------------------------------------
CPU OC               No         No         Yes
PCIe CPU lanes       16         16         16
Chipset PCIe lanes   16         8          20
SATA                 6          6          6
M.2                  Depends    Depends    Depends
Target               Mid        Budget     Enthusiast
```

For your current **GPU testing / repair bench**, H170 is actually a pretty useful cheap platform.

You don't need an expensive modern motherboard just to test a GPU:

```text
H170 + cheap Skylake CPU
       │
       ├── PCIe x16
       │      │
       │      └── GPU under test
       │
       ├── PSU
       ├── RAM
       └── monitor
```

The important thing is having a **known-good PCIe x16 slot, PSU, CPU and RAM**. That gives you a controlled environment for distinguishing:

```text
GPU problem
   vs
motherboard PCIe problem
   vs
PSU problem
   vs
CPU/BIOS problem
```

If you mean a **specific ASUS H170 board**, send me a photo of the motherboard/model label. I can identify the exact model and walk through its **PCIe slots, power connectors, front-panel pins, M.2/SATA, BIOS, and GPU-testing points**.

I can also map an H170 board into a **practical GPU diagnostic bench** and show exactly what to measure with your multimeter.
