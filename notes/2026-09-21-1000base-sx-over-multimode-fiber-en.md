---
audio: false
generated: true
image: false
lang: en
layout: post
title: 1000BASE-SX over Multimode Fiber
translated: false
type: note
---

Question: What does **1000BASE-SX** use with multimode fiber?

Answer:

**1000BASE-SX = Gigabit Ethernet over multimode fiber (MMF), using 850 nm VCSEL lasers.**

Typical setup:

```text
1000BASE-SX
     │
     ├── Wavelength: 850 nm
     ├── Source: VCSEL laser
     ├── Fiber: Multimode fiber (MMF)
     ├── Speed: 1 Gbit/s
     └── Duplex: 2 fibers
             ├── TX
             └── RX
```

Common fiber types:

| Fiber             | 1000BASE-SX typical max |
| ----------------- | ----------------------: |
| OM1 (62.5/125 µm) |                  ~275 m |
| OM2 (50/125 µm)   |                  ~550 m |
| OM3 (50/125 µm)   |                  ~550 m |
| OM4 (50/125 µm)   |                  ~550 m |
| OM5               |                  ~550 m |

The important distinction is:

* **1000BASE-SX** → **850 nm + multimode**
* **1000BASE-LX** → **1310 nm**, primarily single-mode, but can run over MMF with the appropriate mode-conditioning setup
* **1000BASE-T** → copper twisted pair

For an SFP, you'd typically see something like:

```text
1000BASE-SX SFP
LC duplex
850 nm
MMF
```

So if you're looking at an existing **multimode LC fiber run**, I can also map **OM1/OM2/OM3/OM4 → which 1G/10G SFPs you can use and their distances**.