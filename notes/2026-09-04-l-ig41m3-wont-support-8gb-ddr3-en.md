---
audio: false
generated: true
image: false
lang: en
layout: post
title: L-IG41M3 Won't Support 8GB DDR3
translated: false
type: note
---

Question: Will the Lenovo L-IG41M3 motherboard support Kingston DDR3 8GB 1333MHz RAM?Answer: **No, a Kingston DDR3 8GB single stick will very likely NOT work** on the Lenovo L-IG41M3. Here's why:

---

### ❌ The Main Problem — 8GB Single Stick

The L-IG41M3 board has a maximum RAM capacity of **4GB total** — meaning it cannot recognize a single 8GB stick at all. This is a hard limitation of the **Intel G41 chipset**, not just a BIOS issue.

---

### ⚠️ Secondary Problem — High Density Chips

Newer, high-density RAM sticks tend to be incompatible with the G41 chipset. Even if the speed is downclocked, the BIOS on this board can be very picky with high-density modules.

---

### ✅ What RAM Actually Works

| Spec | Recommended |
|---|---|
| Type | DDR3 |
| Speed | 1066 MHz or 1333 MHz |
| **Max per stick** | **2GB or 4GB** |
| Max total | **4GB (2 slots)** |
| Voltage | 1.5V |
| Best config | **2 × 2GB DDR3-1333** |

---

### 💡 Best Safe Option for This Board

> **2 × 2GB DDR3 1333MHz 1.5V** sticks — this gives you **4GB total**, which is the maximum this board can handle, and has the best compatibility.

A single Kingston 8GB stick is simply too large for this old platform — save it for a newer board.

References:
- [Lenovo L-IG41M3 Guide – Alibaba Electronics](https://electronics.alibaba.com/buyingguides/lenovo-l-ig41m3-motherboard-guide)
- [RAM Incompatibility on L-IG41M3 – Tom's Hardware Forum](https://forums.tomshardware.com/threads/possible-ram-incompatibility-l-ig41m3-old-motherboard.3787600/)
