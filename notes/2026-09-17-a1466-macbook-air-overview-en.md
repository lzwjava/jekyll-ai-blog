---
audio: false
generated: true
image: false
lang: en
layout: post
title: A1466 MacBook Air Overview
translated: false
type: note
---

Question: **Introduction to the Mac A1466 laptop**

Answer: **A1466 is Apple's model identifier for the 13-inch MacBook Air**, covering multiple generations from roughly **2010–2017**. The exact CPU, RAM, ports, and year depend on the EMC/model number.

![Image](https://images.openai.com/static-rsc-4/lrg83sQ8LzdFCPh84fC483ikbCRdb8cemdYFqgTZTxTpiadnSG-Sj8r2PdEk1NVKErm1zeCdpghzTaTHizL2ZvCLL8OjJmj1KKFCE2_OGEyzR9mU0h-nFcIctyL-7f1Z0SrQdx0TUM2JRFwpTwJz8p9JIoRTSbWfUjrfT0zxERdfaxbl60oWw-922MK1B8Sc?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/T-OvfEEezCtDrVlv8-MezzNHeWs3LWCuhIJWfkWqvEIGoKOgxPiAetLgpJecqDC4tUIJcS2sMLGBB8HUOJUxiryun5gaNVdHIIVXVmIEaJ8YbS7AZUK1Is7gaKuB36XoH983wYrAN-NADF7WjhrvFBes54oXWawAOoGai7Yn3NcbmPiuS-Ly0JwTNUcJ4XfV?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/u6R3SEDDfpeITA8mZDbeRWBn7wud1mAl0n-G8E7b9mlWhSNJ_X0Gk9SCUSmGxFuZ9-BmZ5FHcopF3IYC7OcLz0200_zcmDSMpxEwW7virr64dVdUMBO-Nfs5iW5vzJWDnzSM9xfq6LDIS4rT97t_8UdPseam7V4XiK7U4tN7O4jBLRpq7wnRvI1am7htxtxA?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Q7twOCu9ild-23IB0Y7SfjbsyQL3NzxbYUxvqvNeePuHvz0d1ny6REs373X9EcnnRbg-o8zu1yboqGvUyXyzrkHGVlTooQFrK5QT0xtd1HLHw6giARxf22ZxZt1iBkN1WFBN3p8LMeppVH9LHFinv8zSfVuQBS-FnUlhXkvn97XE7qgmmLzP0a0kBwZHbfMO?purpose=fullsize)

### Basic specs

| Item           | A1466                               |
| -------------- | ----------------------------------- |
| Product        | 13-inch MacBook Air                 |
| Screen         | 13.3", 1440×900                     |
| CPU            | Intel Core i5/i7, generation varies |
| RAM            | Usually 4–8 GB LPDDR3               |
| Storage        | Apple proprietary SSD               |
| GPU            | Intel integrated graphics           |
| Display output | Thunderbolt / Mini DisplayPort      |
| USB            | 2× USB-A                            |
| Networking     | Wi-Fi + Bluetooth                   |
| Ethernet       | No built-in Ethernet                |
| Battery        | Internal lithium-polymer            |
| Construction   | Aluminum unibody                    |
| Weight         | ~1.35 kg                            |
| Identifier     | **A1466**                           |

### The important part: A1466 is not one machine

For example:

* **2012 A1466** → Ivy Bridge
* **2013–2014** → Haswell
* **2015** → Broadwell
* **2017** → Broadwell refresh, typically i5-5350U

The **2017 A1466** is particularly interesting as a cheap old Mac:

```text
MacBook Air A1466 (2017)
        │
        ├── Intel Core i5-5350U
        │     ├── 2 cores / 4 threads
        │     └── 1.8 GHz base / up to 2.9 GHz
        │
        ├── Intel HD Graphics 6000
        ├── 8 GB LPDDR3
        ├── 13.3" 1440×900
        ├── 128/256 GB SSD
        └── macOS support
```

It is **very different from the newer M1/M2 MacBook Air**. The A1466 is Intel-based and relatively easy to open and repair compared with many newer Macs.

### For repair / hardware experiments

Given your GPU-repair work, the A1466 is actually a nice little machine to understand **Apple laptop hardware**:

```text
                    A1466
                      │
        ┌─────────────┴─────────────┐
        │                           │
     Logic board                 I/O / power
        │                           │
   Intel SoC/CPU              MagSafe charging
   Intel iGPU                 USB
   LPDDR3 RAM                 Thunderbolt
   SPI EFI ROM                Wi-Fi/Bluetooth
        │
        └────── proprietary SSD
```

The major caveat is that **RAM is soldered**, so you generally cannot upgrade 4 GB → 8 GB yourself.

If you're looking at a specific **A1466 listing**, send me its CPU/EMC number or photo of the bottom label. I can identify the **exact year, CPU, RAM, SSD, macOS maximum, repairability, and whether it is worth buying**.
