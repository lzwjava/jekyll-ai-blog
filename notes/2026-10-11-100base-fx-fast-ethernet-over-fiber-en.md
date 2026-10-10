---
audio: false
generated: true
image: false
lang: en
layout: post
title: 100BASE-FX Fast Ethernet over Fiber
translated: false
type: note
---

**Question:** What is 100BASE-FX and how does it work in networking?

**Answer:**

## 100BASE-FX Overview

100BASE-FX is a **Fast Ethernet** standard defined under **IEEE 802.3u (1995)** that delivers 100 Mbps data transmission over **fiber optic cable** rather than copper wire.

Breaking down the name:
| Part | Meaning |
|------|---------|
| **100** | 100 Mbps data rate |
| **BASE** | Baseband transmission |
| **FX** | Fiber optic medium (two strands) |

---

## Physical Layer

| Specification | Details |
|--------------|---------|
| **Cable type** | Multimode fiber (MMF), 62.5/125 µm or 50/125 µm |
| **Strands** | 2 (one TX, one RX) |
| **Wavelength** | 1300 nm (infrared) |
| **Light source** | LED or laser |
| **Connectors** | SC (preferred), ST, MIC/FDDI |

---

## Range / Distance

| Duplex Mode | Max Distance |
|-------------|-------------|
| **Half-duplex** | ~412 meters |
| **Full-duplex** | **2 kilometers (2 km)** |

This makes 100BASE-FX a strong choice for **building-to-building or campus backbone** links where copper (100BASE-TX, max 100 m) falls short.

---

## Encoding

- Uses **4B5B** block encoding — every 4 data bits mapped to a 5-bit symbol (improves clock synchronization)
- Combined with **NRZI** (Non-Return-to-Zero Inverted) line coding for the optical signal

---

## Key Advantages over Copper

1. **Longer distance** — up to 2 km vs. 100 m for 100BASE-TX
2. **EMI immunity** — fiber is immune to electromagnetic interference
3. **Better security** — harder to tap than copper
4. **No ground loop issues** — ideal across separate buildings

---

## Comparison: 100BASE-FX vs 100BASE-TX

| Feature | 100BASE-FX | 100BASE-TX |
|---------|-----------|-----------|
| Speed | 100 Mbps | 100 Mbps |
| Medium | Multimode fiber | Cat 5e/6 UTP copper |
| Max distance | 2 km (full-duplex) | 100 m |
| Connector | SC / ST | RJ-45 |
| Cost | Higher | Lower |
| EMI resistance | Excellent | Moderate |

---

## Typical Use Cases

- **Campus backbone** links between buildings
- **Industrial environments** with heavy electrical noise
- **High-security networks** where eavesdropping risk must be minimized
- **Legacy fiber upgrades** in buildings already wired with 62.5 µm MMF (e.g., from older FDDI installations)

---

## Quick Note on Topology

100BASE-FX supports both **point-to-point** connections and connections through **fiber hubs/switches**. In full-duplex mode (the common deployment), CSMA/CD collision detection is disabled, allowing the full 2 km reach.

---

**References:**
- [IEEE 802.3u Standard (Fast Ethernet)](https://standards.ieee.org/ieee/802.3u/1183/)
- [100BASE-FX – Ethernet Physical Layer](https://en.wikipedia.org/wiki/Fast_Ethernet#100BASE-FX)
- [Fiber Optic Cabling in Ethernet – Cisco](https://www.cisco.com/c/en/us/td/docs/internetworking/technology/handbook/Ether.html)