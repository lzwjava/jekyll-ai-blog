---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI MAG B760M MORTAR WIFI Overview
translated: false
type: note
---

![Image](https://images.openai.com/static-rsc-4/i_SjU_1AhCST0vxGq5qFs_w89wnke-MeO5dVy_A_nwqBf2Xo_u0IO77LBldyySUEg9Alcx6y6rKp5lkBWidaiFsTWjcSekQj9Nurj-0ss_9320QAjsp1nKyYrspKdI6BWrlmR5kZF_hvmhHzy5j-EL1MYUMTbsaSb1cgQn71fXpP-OImgz5TbAdMhvuewVTx?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ezsGDKN_q-RXa6QxJaQ5kPmRjTQi84jSJCIolkYHTPkUrOnWnGpCuv52EjHvL9fJTxy1VbKVJBNuWAZghKk4kDRWYjeVEOR4ar2fwOWX7HF02mc0g81AunOU98av9JcMBQi_U8RwODlMih2KKvv0gDTTOgd5Eqaap1GAMzc3IUnuH16pg444kXh1EuQv902M?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ljaCxS9Qh3OUuCZig4mGcQM_fQWKj_-_5jn0ZKuYLWCmdvi_u7UU0py0zcmBCDTNYSjaTzI73qvyLz7ddTWMtcxYVnYC9g-xHB98kh2WZKTaDTFZt_J66vRpcVGq_ITMulV4RX6KJzqmguCATnHxNhtr6kEVXiKJlNjnmhm7EhEyxUdM-e9Z6KrVRSYIgRoi?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/AFHdVs1dhsjsSEHjuA9ezNdqmWYBoYCTFs4SE68Q2U4HUBf6gEA_SURHeJdIZMMy2aNbX73GNnEj1kpKjRGEDfzC3XoMs-B_3VddzkemdSV1-zyXrD72-CW37T2__oMFTgsHFT7MfKngDWhdSmviFox5wAKKdo6O5W3wmhgd70MHwevF96tCMKc4XBruCJF1?purpose=fullsize)

The **MSI MAG B760M MORTAR WIFI** is a fairly high-end **mATX Intel LGA1700 motherboard**. It is particularly interesting for you because it is a much better platform for **GPU testing / multiple PCIe devices / hardware experiments** than cheap H610/B660 boards.

[MSI official specification](https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/Specification?utm_source=chatgpt.com)

### Core specifications

| Part        | Specification                     |
| ----------- | --------------------------------- |
| Form factor | **mATX, 243.84 × 243.84 mm**      |
| Chipset     | **Intel B760**                    |
| CPU socket  | **LGA1700**                       |
| CPU         | 12th / 13th / 14th-gen Intel      |
| RAM         | **4× DDR5**, up to 256 GB         |
| GPU slot 1  | **PCIe 5.0 x16** from CPU         |
| GPU slot 2  | **PCIe 4.0 x4** from chipset      |
| Small slot  | PCIe 3.0 x1                       |
| M.2         | **2× PCIe 4.0 x4**                |
| SATA        | **4× SATA 6 Gb/s**                |
| LAN         | **2.5 GbE**                       |
| Wireless    | **Wi-Fi 6E + Bluetooth 5.3**      |
| USB         | Up to **USB 3.2 Gen 2x2 20 Gb/s** |
| VRM         | **12+1+1** power design           |
| PCB         | **6-layer, 2 oz copper**          |

MSI officially lists 4 DDR5 DIMMs, 256 GB maximum memory, and PCIe x16/x4 expansion configuration. ([MSI USA][1])

---

## 1. The important part for your GPU experiments

This is probably the most interesting characteristic:

```text
CPU
 │
 ├── PCIe 5.0 x16 ─────────── GPU #1
 │
 └── DMI
      │
      └── B760 chipset
           ├── PCIe 4.0 x4 ─── GPU #2
           ├── PCIe 3.0 x1
           ├── M.2 #2
           ├── SATA
           ├── USB
           └── LAN/WiFi
```

The primary slot is **PCIe 5.0 x16**, while the second full-length slot is **PCIe 4.0 x4**. ([MSI USA][1])

So you can physically install something like:

```text
RTX 4070
    ↓
PCIe 5.0 x16 slot

GT 730 / Quadro / test GPU
    ↓
PCIe 4.0 x4 slot
```

This makes it quite useful as a **GPU repair/test bench**.

But there's an important distinction:

**the second slot is physically x16 but electrically only x4.**

That's perfectly reasonable for testing whether a GPU enumerates, driver testing, display output, diagnostics, etc. It isn't equivalent to having two x16 CPU-connected slots.

---

## 2. CPU support

It uses **LGA1700**, so CPUs such as:

```text
i3-12100
i5-12400
i5-12600K
i5-13400
i5-13600K / KF
i7-13700K / KF
i9-13900K / KF
i5-14600K
i7-14700K
i9-14900K
```

are in its compatibility family.

MSI's current specification also lists 14th-gen support, although the original product was launched around 12th/13th-gen. ([MSI USA][1])

For a GPU test bench, I would actually prefer something like:

**i5-12400 / i5-13400**

rather than spending money on an i9.

You don't need a 300 W CPU just to test whether a GPU works.

---

## 3. DDR5

There are **four DIMM slots**:

```text
A1   A2   B1   B2
│    │    │    │
└────┴────┴────┴── DDR5
```

Maximum officially specified capacity is **256 GB**.

It supports DDR5 up to around **7200+ MT/s via overclocking/XMP**, while standard JEDEC speeds are lower. ([MSI USA][1])

For a practical workstation:

```text
2 × 32 GB DDR5
= 64 GB
```

is already very good.

For your AI work:

```text
2 × 32 GB
or
2 × 48 GB
```

would be more useful than chasing 7200 MT/s.

---

## 4. Storage

There are:

```text
M.2 #1 ── PCIe 4.0 x4 ── CPU
M.2 #2 ── PCIe 4.0 x4 ── B760
```

plus:

```text
4 × SATA 6 Gb/s
```

So you can have:

```text
NVMe SSD #1
NVMe SSD #2
SATA SSD/HDD × 4
```

MSI provides M.2 Shield Frozr heatsinks as well. ([MSI Storage][2])

For your model-training machine, two NVMe drives is convenient:

```text
SSD #1 → OS / code / environments
SSD #2 → datasets / checkpoints
```

---

## 5. Network is unusually good for a B760 board

You get:

**Realtek 2.5 GbE**

and:

**Intel Wi-Fi 6E + Bluetooth 5.3**. ([MSI USA][1])

For your workloads, 2.5 GbE is actually useful if you have:

```text
GPU workstation
      │
  2.5 GbE
      │
NAS / server
```

rather than relying on 1 GbE.

---

## 6. Rear I/O

The rear panel gives you roughly:

```text
USB 2.0
DisplayPort
USB 10 Gb/s
2.5G Ethernet
Wi-Fi antenna
audio
HDMI 2.1
USB-C 20 Gb/s
S/PDIF
```

The HDMI/DP outputs are from the **CPU's integrated graphics**, so an `F` CPU such as an i5-12400F cannot use those motherboard video outputs. ([MSI USA][1])

That's worth remembering when building a test bench.

For example:

```text
i5-12400     → motherboard HDMI/DP works
i5-12400F    → motherboard HDMI/DP produces no image
```

---

# VRM / power delivery

This is one reason the MORTAR is considerably nicer than a cheap B760 board.

MSI specifies a **12+1+1 power design**, dual 8-pin CPU power connectors, large heatsinks, and a 6-layer PCB with 2 oz copper. ([MSI][3])

The physical structure is approximately:

```text
             CPU
              │
        ┌─────┴─────┐
        │   VRM     │
        │ 12+1+1    │
        └───────────┘
              │
          DDR5 DIMMs

PCIe GPU ────────────────
```

It's more than enough for an i5/i7-class CPU.

For something like a 13900K/14900K, however, the **CPU itself** becomes the difficult thermal/power problem—not whether this board can merely boot it.

---

# Why the MORTAR is attractive for you

I'd rate it roughly:

| Area                     | Rating |
| ------------------------ | -----: |
| GPU testing              |  ⭐⭐⭐⭐⭐ |
| AI workstation           |  ⭐⭐⭐⭐½ |
| CPU performance platform |  ⭐⭐⭐⭐⭐ |
| Expansion                |   ⭐⭐⭐⭐ |
| Networking               |  ⭐⭐⭐⭐⭐ |
| Storage                  |   ⭐⭐⭐⭐ |
| Cheapness                |    ⭐⭐⭐ |
| mATX compactness         |  ⭐⭐⭐⭐⭐ |

The key combination is:

```text
mATX
+
PCIe 5.0 x16
+
PCIe 4.0 x4
+
4× DDR5
+
2× NVMe
+
2.5GbE
+
Wi-Fi 6E
+
strong VRM
```

That's a **very serious little board**.

---

# But about your ¥1,299 price

This needs a little caution.

The exact **MAG B760M MORTAR WIFI** is an older LGA1700 generation now. MSI's current official site still lists it, but the newer **MORTAR WIFI II** exists as well. ([MSI][3])

Current Chinese listings show the newer **B760M MORTAR WIFI II** around **¥1,199–1,299**, while the original MORTAR WIFI can also appear around this price depending on seller. ([MSI Store][4])

So:

**¥1,299 for the original MORTAR WIFI DDR5 is not particularly attractive today.**

I'd distinguish:

```text
Original B760M MORTAR WIFI
        ↓
    good board
        ↓
   ¥1,299 = expensive


B760M MORTAR WIFI II
        ↓
newer revision / 3× M.2
        ↓
~¥1,199–1,299
        ↓
more interesting
```

The WIFI II has **3 M.2 slots**, for example, versus 2 on the original. ([MSI][5])

### For your particular use

If you're buying this primarily for your **GPU repair/testing bench**, I'd actually look for a **used/open-box MORTAR around ¥500–800** rather than paying ¥1,299.

At ¥1,299, I'd compare it against newer B760/B860/AM5 boards first.

[MSI MAG B760M MORTAR WIFI official page](https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI?utm_source=chatgpt.com)

I can also map out **exactly which PCIe slot, M.2 slot, RAM slot, CPU power connector, F_PANEL and fan headers you should use on this board for a two-GPU repair/test bench**.

[1]: https://us.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/Specification?utm_source=chatgpt.com "MAG B760M MORTAR WIFI"
[2]: https://storage-asset.msi.com/datasheet/mb/cn/MAG-B760M-MORTAR-WIFI.pdf?utm_source=chatgpt.com "主板
MAG B760M MORTAR WIFI
U N I T E  A S  O N E
FEA"
[3]: https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI?utm_source=chatgpt.com "MAG B760M MORTAR WIFI"
[4]: https://store.msi.cn/?utm_source=chatgpt.com "微星商城msi-微星笔记本电脑、主板、显卡，官网直营商城，正品有保障"
[5]: https://www.msi.cn/Motherboard/MAG-B760M-MORTAR-WIFI-II?utm_source=chatgpt.com "MAG B760M MORTAR WIFI II"
