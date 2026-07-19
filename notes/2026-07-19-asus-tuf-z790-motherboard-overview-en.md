---
audio: false
generated: true
image: false
lang: en
layout: post
title: ASUS TUF Z790 Motherboard Overview
translated: false
type: note
---

**Question: Intro to ASUS TUF GAMING Z790-PLUS WIFI motherboard**

ASUS TUF GAMING Z790-PLUS WIFI is a **high-end consumer ATX motherboard** based on Intel's **Z790 chipset**, mainly designed for **12th/13th/14th generation Intel Core CPUs** (Alder Lake / Raptor Lake / Raptor Lake Refresh).

![Image](https://images.openai.com/static-rsc-4/DFmrk__nwKEbgYNhfdILQU9zhIXgaQLlb1CdCm3cQY-KF_kNjHJt3gSb3IjTlElgRla4BRgfj2GIcLKwRlqIVGSlcgruK3McyD_I6C8tQY383BXsf8miIXEKA8SMaj-5SqDa1Y4TZPQuYJg61RiIuJR4LdFIUHF6pv9s2wdcXUNz6WaGTjSBeqDUb906ZPHX?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/5P6jSxAxYHdsqLUZLlep0vQUwF-Od5rxHNLX6ZjxWG2HJZAiV5fvV7xsIuMkeJqba8AzMK8uByf8GouTbxvzJceNnEI0zOz8sU19rQkmoFyWBU8mdsoQW1x07SmG7Ou7R-rabX784JpO5qnXYAxb2MOvJJRMMrTEQf7LZEUMNwlTrGNqDtmrr1_OiWk0fenb?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/roXiiHcBRiOEbz2JBusvS5IySBkYPXzwqo8PRAe3OPLTPqj0bvdhMUpvqqBGh_AlnoSW4R0VX-oJQGs9Jr_s2ylbIhjsj0Wj--iQZ34JFduGoiOdAzMttnVnCI_FiNaLNiKXJG8WSRB9NK7ZtJAEPPMinwFSpfhInBHB4RiPfoRchrzznKNz0g0TE6k3PuyM?purpose=fullsize)

## Key specs

| Feature         | Details                              |
| --------------- | ------------------------------------ |
| CPU socket      | LGA1700                              |
| CPU support     | Intel 12th / 13th / 14th Gen Core    |
| Chipset         | Intel Z790                           |
| Form factor     | ATX                                  |
| Memory          | 4 × DDR5 DIMM                        |
| Memory capacity | Up to 192GB DDR5 (with 48GB modules) |
| PCIe GPU slot   | PCIe 5.0 x16                         |
| M.2 storage     | Multiple M.2 NVMe slots (PCIe 4.0)   |
| Network         | 2.5Gb Ethernet                       |
| Wireless        | WiFi 6 + Bluetooth                   |
| VRM             | Strong power delivery with heatsinks |
| BIOS            | UEFI, CPU upgrade support            |

---

## Why Z790 matters

Intel motherboard tiers:

```
H610
  |
B660/B760
  |
Z690/Z790  <--- enthusiast
```

The important difference:

* **B760**:

  * no CPU overclocking
  * fewer PCIe lanes
  * cheaper

* **Z790**:

  * CPU multiplier overclocking
  * stronger VRM
  * more expansion
  * better for i7/i9

For a:

* i5-13600K
* i7-13700K
* i9-13900K
* i9-14900K

Z790 makes sense.

---

## VRM / power

The "供电稳" part means the motherboard has a stronger VRM design.

For example:

```
PSU 12V
 |
VRM
 |
CPU voltage ~1V
 |
CPU cores
```

A 13900K can pull:

* normal gaming: ~100-150W
* heavy all-core: 250W+

A weak motherboard may throttle. A TUF Z790 can handle these CPUs much better.

---

## For your RTX 3090 / dual GPU thinking

This board is interesting, but note:

### PCIe layout

Usually:

```
CPU PCIe lanes:

GPU slot 1:
PCIe 5.0 x16

Chipset:
PCIe x4 lanes
 |
M.2
 |
other PCIe slots
```

A second GPU usually runs:

```
GPU1: PCIe 5.0 x16
GPU2: PCIe 4.0 x4
```

because consumer Intel CPUs only have:

```
CPU:
16 PCIe lanes GPU
4 PCIe lanes NVMe

Total:
20 PCIe lanes
```

Not like server platforms:

```
Threadripper:
64+ PCIe lanes

EPYC:
128+ lanes
```

So for:

* single RTX 3090 ✅
* RTX 4090 + NVMe ✅
* RTX 3090 + another GPU ⚠️ limited

---

## Compared with your MSI MAG B760M Mortar WiFi

Your previous board:

MSI MAG B760M Mortar WiFi

is actually already a very good board.

Difference:

|            | MSI B760M Mortar | ASUS TUF Z790   |
| ---------- | ---------------- | --------------- |
| Size       | mATX             | ATX             |
| DDR5       | yes              | yes             |
| CPU OC     | no               | yes             |
| PCIe lanes | fewer            | more            |
| Expansion  | medium           | better          |
| VRM        | good             | stronger        |
| Dual GPU   | limited          | slightly better |

For your use case:

* GPT training
* RTX 3090
* local LLM inference
* PyTorch

the motherboard itself is **not the bottleneck**.

The big constraints are:

1. VRAM
2. PCIe bandwidth
3. power supply
4. cooling

---

## Used-market value

A used TUF Z790-PLUS WIFI is a pretty reasonable choice because:

* DDR5 platform
* supports 13900K/14900K
* ATX gives more room
* good resale

But I would not pay a huge premium over B760.

For AI workstation:

```
B760 + RTX3090
        |
        |
        v
same model training speed

Z790 + RTX3090
```

The GPU does the work.

---

For your case (i9-13900KF + RTX 4070 currently, considering RTX 3090/dual GPU), the **main reason to upgrade to Z790 is not performance; it is physical expansion space and PCIe layout**. If you want 2×3090, even Z790 is not ideal — you start looking at **Threadripper / workstation platforms**.
