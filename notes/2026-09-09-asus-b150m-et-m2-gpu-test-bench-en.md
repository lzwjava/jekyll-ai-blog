---
audio: false
generated: true
image: false
lang: en
layout: post
title: ASUS B150M-ET M2 GPU Test Bench
translated: false
type: note
---

## Question: ASUS B150M-ET M2 — what is this board?

ASUS **B150M-ET M2** is a low-end **micro-ATX LGA1151 motherboard from around 2016**, based on Intel's B150 chipset. It is actually a pretty useful cheap-board option for a **GPU test bench**, especially given what you've been building.

![Image](https://images.openai.com/static-rsc-4/7L7FEzdi5OdwPRQXkpl00ho4QRmS0J_k63CnJrKswqRGo5D_o454baW3oj6nKBmElEW8CPeF6xeb8TJ2gusik9bjUh1BXbG_RDT_tPNgAZS1YjHwZU4QTgsd23H07upNetQ79tiuKhMMrmhyQzWAAa5aNG8efPxcq_iZ52b5vpnVJh6p5HWqhHcraLduoZz4?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/UMGwfOeojvLhrTgaswYXks-TDYxCc6ghoqyZtTWOOBO83Y74dSEuhlMAJkX2vu1bQBta4piwawgWLS_QD70q_5Adr__fg2gtGAuLTQitorlbDDlC0XUrbAsgKl8e_XRc6U5PP4dMQ0Z38zPpdJL1gLqtExbqWcl6VOMkXfnQdQulAJ2RkrVhkJozECSGtUKH?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/YzA0aeKbsaa3Bt-_5fT68yVxH37VliuRiAUePMpUs6fdXRD8pG7EyKw1r48j5s_7aGOTfmyO1YSfwmMq3SNqoCRnmxz1xJCsvPh8_ehqP7lsNukJE71si0BkJi2d1YLLEJ5DO1bl1eBphqNMiqSvjatT65hy64QqnCkTwT35O7i4NNJm00iRQ3VgOc94FnuJ?purpose=fullsize)

### Core specs

| Part            | B150M-ET M2                 |
| --------------- | --------------------------- |
| Chipset         | **Intel B150**              |
| CPU socket      | **LGA1151**                 |
| CPU generation  | 6th-gen Skylake officially  |
| RAM             | **2 × DDR4 DIMM**           |
| Max RAM         | **32 GB**                   |
| GPU slot        | **1 × PCIe x16**            |
| PCIe additional | 2 × PCIe x1                 |
| M.2             | **1 × M.2**, 2242/2260/2280 |
| SATA            | **6 × SATA 6 Gb/s**         |
| LAN             | Gigabit Ethernet            |
| Audio           | Realtek ALC887              |
| Form factor     | ~22.6 × 18.5 cm micro-ATX   |

ASUS's manual confirms the LGA1151 socket, two DDR4 slots, PCIe x16, two PCIe x1 slots, six SATA ports, and M.2 socket. ([ASUS Downloads][1])

### CPU compatibility

This is the important part.

Officially, the board supports:

* Core **i3/i5/i7 6th gen**
* Pentium
* Celeron
* LGA1151 Skylake CPUs

For example:

```text
i3-6100
i5-6400
i5-6500
i5-6600
i7-6700
Pentium G4400
Pentium G4500
Celeron G3900
```

The official documentation specifically lists 6th-generation Core/Pentium/Celeron processors. ([ASUS Download Center][2])

There is also a later BIOS history, with ASUS releasing BIOS 3606 in 2018 to update CPU microcode and improve stability/security. ([ASUS Mall][3])

**Important:** don't assume that every 7th-gen Kaby Lake CPU works just because it is physically LGA1151. Check the exact CPU support list/BIOS before buying.

### For your GPU testing use case

This board is actually quite attractive.

The topology is basically:

```text
CPU
 │
 └── PCIe x16
       │
       └── GPU
```

So if your goal is:

```text
cheap CPU
+ cheap DDR4
+ B150 motherboard
+ PSU
+ GPU under test
```

you don't need an expensive X99/X299 platform.

And because it has **PCIe x16**, you can test modern GPUs even though the CPU/platform is old. The GPU will simply operate according to the PCIe generation supported by the platform/device.

For GPU repair/testing, I'd actually prefer this kind of simple LGA1151 board over a complicated multi-GPU platform.

### One major problem: no I/O shield

The seller says:

> **无挡板**

meaning **the rear I/O shield is missing**.

That's not a functional problem. You can run the motherboard perfectly fine without it.

For a bench/test setup:

```text
              GPU
               │
        ┌──────┴──────┐
        │ B150M-ET M2 │
        └─────────────┘
             │
           PSU
```

I'd actually **not care much about the missing shield** for a GPU repair bench.

### M.2 is a nice bonus

The **M.2 slot supports 2242 / 2260 / 2280** drives. ([ASUS Downloads][1])

So you can put a cheap NVMe SSD there and have:

```text
B150M-ET M2
 ├── LGA1151 CPU
 ├── DDR4
 ├── M.2 SSD
 └── PCIe x16 → GPU under test
```

That's a very clean test platform.

### My verdict

For your use:

**GPU testing / repair bench: 8/10**

**Cheap general PC: 7/10**

**Modern gaming PC: 3/10**

**LLM machine: 1/10**

The platform is old, but that's exactly why it can be useful: **cheap, simple, DDR4, LGA1151, PCIe x16, M.2, and no unnecessary complexity.**

The main thing I'd check before buying is **the exact asking price + whether the seller can demonstrate POST/BIOS + whether the CPU socket pins are clean**. Since the listing says "功能都正常", I'd still want a photo of the socket and a powered-on BIOS screen before paying.

If you send me the **actual listing photos**, I can inspect the board condition and tell you whether I'd buy it for your GPU test bench.

References:

* [ASUS B150M-ET M2 official support](https://www.asus.com/us/supportonly/b150m-et%20m2/helpdesk_manual/?utm_source=chatgpt.com)
* [ASUS B150M-ET M2 user manual](https://dlcdnet.asus.com/pub/ASUS/mb/LGA1151/B150M-ET_M2_Series/C11414_B150M-ET_M2_UM_6pages_0309.pdf?utm_source=chatgpt.com)
* [ASUS B150M-ET M2 BIOS history](https://www.asus.com.cn/supportonly/b150m-et%20m2%20series/helpdesk_bios/?utm_source=chatgpt.com)

I can also compare this board directly against your **ASUS B85 GPU test bench** and tell you which one is the better buy.

[1]: https://dlcdnets.asus.com.cn/pub/ASUS/mb/LGA1151/B150M-ET_M2_Series/C11415_B150M-ET_M2_V5_UM_6pages_0309.pdf?model=B150M-ET+M2%2FV5&utm_source=chatgpt.com "C11415 / 第一版 / 2016 年 2 月"
[2]: https://dlcdnet.asus.com/pub/ASUS/mb/LGA1151/B150M-ET_M2_Series/C11415_B150M-ET_M2_V5_UM_6pages_0309.pdf?utm_source=chatgpt.com "C11415 / 第一版 / 2016 年 2 月"
[3]: https://www.asus.com.cn/supportonly/b150m-et%20m2%20series/helpdesk_bios/?utm_source=chatgpt.com "B150M-ET M2 SERIES - 服务支持"
