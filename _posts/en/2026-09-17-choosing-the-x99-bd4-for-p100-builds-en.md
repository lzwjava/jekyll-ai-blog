---
audio: false
generated: true
image: false
lang: en
layout: post
title: Choosing the X99-BD4 for P100 Builds
translated: false
type: note
---

Question: **How does the Huananzhi X99-BD4 compare with the Kenao X99-D4 for a Tesla P100 build?**

Answer: **For your P100 use case, I would pick the Huananzhi X99-BD4 if the prices are close.** The reason is mostly the documented PCIe layout and BIOS support, not raw CPU performance.

### Side-by-side

|                             | Kenao X99-D4          | Huananzhi X99-BD4                              |
| --------------------------- | --------------------- | ---------------------------------------------- |
| CPU                         | LGA2011-3             | LGA2011-3                                      |
| RAM                         | DDR4                  | **4× DDR4, up to 128GB**                       |
| PCIe                        | Need exact revision   | **2× PCIe 3.0 x16 + 1× x4 + 1× x1**            |
| NVMe                        | Depends on revision   | **M.2 PCIe 3.0 x4**                            |
| BIOS                        | Unknown               | **AMI UEFI**                                   |
| Above-4G / ReBAR            | Need verify           | Huananzhi provides BIOS with **ReBAR support** |
| GPU use                     | Probably fine         | **Better documented**                          |
| Build quality / consistency | Unknown               | More established model                         |
| Bulk availability           | Your listing: 200 pcs | Usually easier to find individually            |

Huananzhi officially specifies **two PCIe 3.0 x16 slots**, plus x4 and x1, and an M.2 PCIe 3.0 x4 slot. It also officially publishes BIOS versions, including one adding Resizable BAR. ([Huananzhi][1])

### For 1× P100

Both should work:

```text
E5-26xx v3/v4
       │
       └── X99 motherboard
              │
              ├── DDR4 ECC
              │
              ├── NVMe
              │
              └── PCIe x16
                    │
                    └── Tesla P100 PCIe
```

**X99-BD4 is a particularly clean fit.**

The official manual explicitly documents:

```text
PCIe 3.0 x16
PCIe 3.0 x16
PCIe 3.0 x4
PCIe 2.0 x1
M.2 NVMe PCIe 3.0 x4
```

and 128 GB maximum DDR4. ([Huananzhi][2])

### For 2× P100

This is where I'd favor the **X99-BD4**.

```text
P100 #1  ─── PCIe x16
P100 #2  ─── PCIe x16
             │
             ▼
        Xeon E5 v3/v4
```

The board has two physical x16 slots, which is exactly what you want. ([Huananzhi][1])

However, **physical x16 does not automatically mean x16 electrical bandwidth in every CPU/slot configuration**, so I'd verify the manual/CPU lane mapping before buying specifically for 2× P100.

### One important detail

The Huananzhi listing says **B85 chipset**, despite being marketed as X99-BD4. That's normal for these Chinese LGA2011-3 boards—the important part for your use case is the **Xeon LGA2011-3 + PCIe topology**, rather than the chipset name printed in the marketing material. ([Huananzhi][1])

### My choice for your P100 cluster

I'd rank them by **use case**, not by generic motherboard quality:

```text
1× P100:
    X99-BD4  ≈  Kenao X99-D4

2× P100:
    X99-BD4  >  Kenao X99-D4
    (better documented PCIe configuration)

4× P100:
    Neither would be my first choice.
    Get a real server/workstation board.
```

And there is one thing I particularly like about the **BD4 for your situation**: Huananzhi actually publishes the BIOS, including a **ReBAR-enabled BIOS**, rather than you having to hunt down a random BIOS dump. ([Huananzhi][1])

**If the Kenao is dramatically cheaper**, though—e.g. **¥100–150/board vs ¥300+ for BD4**—the economics change. For a disposable P100 compute node, I'd potentially take the Kenao and spend the savings on GPUs/PSUs.

If you give me the **prices of the Kenao X99-D4 and Huananzhi X99-BD4**, I can calculate the **cost per P100 node** and tell you which one makes more sense economically.

[1]: https://www.huananzhi.com/list_6/40.html?utm_source=chatgpt.com "X99-BD4-华南金牌"
[2]: https://www.huananzhi.com/attach/book/User/%E4%B8%AD%E8%8B%B1%E6%96%87X99-BD4V1.1.pdf?utm_source=chatgpt.com "中英文X99-BD4V1.1"
