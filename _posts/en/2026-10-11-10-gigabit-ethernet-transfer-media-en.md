---
audio: false
generated: true
image: false
lang: en
layout: post
title: 10 Gigabit Ethernet Transfer Media
translated: false
type: note
---

**Question:** What transfer media/methods does 10 Gigabit Ethernet (万兆位以太网) support?

**Answer:**

10 Gigabit Ethernet (10GbE, IEEE 802.3ae / 802.3an) supports **multiple transfer media**, divided into two main categories:

---

### 🔵 Optical Fiber (光纤)

| Standard | Fiber Type | Max Distance |
| --- | --- | --- |
| **10GBASE-SR** | Multi-mode fiber (MMF) | 26–400 m |
| **10GBASE-LR** | Single-mode fiber (SMF) | 10 km |
| **10GBASE-ER** | Single-mode fiber (SMF) | 40 km |
| **10GBASE-ZR** | Single-mode fiber (SMF) | 80 km |
| **10GBASE-LX4** | Multi/Single-mode fiber | 300 m / 10 km |

---

### 🟡 Copper (铜缆)

| Standard | Medium | Max Distance |
| --- | --- | --- |
| **10GBASE-T** (802.3an) | Cat 6a / Cat 7 UTP | 100 m |
| **10GBASE-CX4** | Twinaxial copper cable | 15 m |
| **10GBASE-CR / DAC** | Direct Attach Copper (SFP+) | 1–7 m |

---

### Key Points

- **10GBASE-T** is the most common copper solution, requiring **Cat 6a or higher** cabling (unlike Gigabit which only needs Cat 5e).
- **Fiber** is preferred for longer distances or data center backbones.
- **DAC (Direct Attach Copper)** cables are popular for short rack-to-rack connections due to low cost and low latency.
- All variants run at **10 Gbps** full-duplex.

---

**References:**

- [10 Gigabit Ethernet – Wikipedia](https://en.wikipedia.org/wiki/10_Gigabit_Ethernet)
- [IEEE 802.3an (10GBASE-T)](https://en.wikipedia.org/wiki/10GBASE-T)
