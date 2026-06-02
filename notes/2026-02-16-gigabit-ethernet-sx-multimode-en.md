---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gigabit Ethernet SX Uses Multimode Fiber
translated: false
type: note
---

Question: In Gigabit Ethernet 1000BASE-SX, which uses short-wavelength laser as the signal source, what is the transmission medium?

A. Coaxial cable
B. Single-mode fiber
C. Multimode fiber
D. Category 5 or Category 5e UTP

Answer:

**C. Multimode fiber**

**Detailed explanation:**

1000BASE-SX is one of the IEEE 802.3z Gigabit Ethernet standards introduced in 1998 (part of 802.3-1998). The naming breakdown is:

- **1000** = 1000 Mbps (1 Gbps)
- **BASE** = baseband transmission
- **SX** = Short-wavelength laser (850 nm), Multimode fiber

Key characteristics of 1000BASE-SX:

- **Light source**: 850 nm short-wavelength VCSEL (Vertical-Cavity Surface-Emitting Laser) or LED in early implementations
- **Transmission medium**: **Multimode optical fiber** (MMF)
  - Most common: 62.5/125 µm multimode fiber → maximum distance **275 meters** (full-duplex)
  - 50/125 µm multimode fiber → maximum distance **550 meters** (full-duplex)
- **Connector types**: Typically SC or LC duplex connectors
- Designed for short to medium reach inside buildings (data centers, backbone links, campus networks)

**Why not the other options?**

- **A. Coaxial cable** — Used in older Ethernet standards (10BASE5, 10BASE2), not for Gigabit Ethernet
- **B. Single-mode fiber** — Used in 1000BASE-LX (long-wavelength 1310 nm) and 1000BASE-LX10/ZX standards for much longer distances (up to 5–70 km), not SX
- **D. Category 5 or 5e UTP** — Used in 1000BASE-T (copper twisted-pair standard), which reaches up to 100 meters over four pairs of Cat 5e/Cat 6 cable, not optical SX

**Quick comparison of common 1000BASE variants:**

| Standard      | Medium                  | Wavelength | Max Distance (full-duplex) |
|---------------|-------------------------|------------|----------------------------|
| 1000BASE-SX   | Multimode fiber         | 850 nm     | 275 m (62.5 µm) / 550 m (50 µm) |
| 1000BASE-LX   | Single-mode or multimode| 1310 nm    | 550 m (MMF) / 5–10 km (SMF) |
| 1000BASE-T    | Cat 5e / Cat 6 UTP      | —          | 100 m                      |

Your answer (C) was **correct**.

References:

- None (standard IEEE 802.3 Gigabit Ethernet specification knowledge)
