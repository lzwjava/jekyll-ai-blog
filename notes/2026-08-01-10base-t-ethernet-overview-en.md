---
audio: false
generated: true
image: false
lang: en
layout: post
title: 10Base-T Ethernet Overview
translated: false
type: note
---

Here’s a detailed breakdown of **10Base-T** and its specifications:

---

### 🔹 **10Base-T Overview**

- **Standard**: IEEE 802.3i (Ethernet over twisted pair).
- **Speed**: **10 Mbit/s** (Megabits per second).
  - The **"10"** in the name directly indicates the **10 Mbps** data rate.
- **Cabling**: Uses **Unshielded Twisted Pair (UTP)** cables, typically **Category 3 (Cat3)** or higher (e.g., Cat5, Cat5e).
- **Topology**: **Star topology** (devices connect to a central hub or switch).
- **Maximum Segment Length**: **100 meters** (per cable run between a device and the hub/switch).
- **Encoding**: Uses **Manchester encoding** for signal transmission.

---

### 🔹 **Why Not the Other Options?**

| Option | Speed       | Explanation                                                                 |
|--------|-------------|-----------------------------------------------------------------------------|
| A      | 100 Mbit/s   | This is **100Base-TX** (Fast Ethernet), not 10Base-T.                      |
| B      | 50 Mbit/s    | No Ethernet standard uses 50 Mbps over twisted pair.                     |
| C      | 20 Mbit/s    | No Ethernet standard uses 20 Mbps.                                         |
| **D**  | **10 Mbit/s**| **Correct**: Matches the **10Base-T** standard.                             |

---

### 🔹 **Key Features of 10Base-T**

1. **Half-Duplex Communication**:
   - Devices can either **transmit** or **receive** at a time (not simultaneously).
   - Uses **CSMA/CD** (Carrier Sense Multiple Access with Collision Detection) to manage collisions.

2. **Connectors**:
   - Uses **RJ-45** connectors (8P8C modular plugs).

3. **Hubs vs. Switches**:
   - Originally designed for **hub-based networks** (shared bandwidth).
   - Later, **switches** replaced hubs to enable full-duplex communication (doubling effective speed to 20 Mbps in full-duplex mode).

4. **Legacy but Foundational**:
   - 10Base-T was widely used in the **1990s** and laid the groundwork for faster Ethernet standards (e.g., 100Base-TX, 1000Base-T).

---

### 🔹 **Comparison with Other Ethernet Standards**

| Standard   | Speed       | Cabling          | Year Introduced | Notes                          |
|------------|-------------|------------------|-----------------|--------------------------------|
| 10Base-T   | 10 Mbps     | Cat3+ UTP        | 1990            | First twisted-pair Ethernet.   |
| 100Base-TX | 100 Mbps    | Cat5+ UTP        | 1995            | Fast Ethernet.                 |
| 1000Base-T | 1 Gbps      | Cat5e+ UTP       | 1999            | Gigabit Ethernet.              |
| 10GBase-T  | 10 Gbps     | Cat6a+ UTP       | 2006            | 10-Gigabit Ethernet.           |

---

### 🔹 **Why 10Base-T Matters**

- **Cost-Effective**: Used existing **telephone-grade** twisted pair wiring (Cat3), reducing infrastructure costs.
- **Scalability**: Star topology made it easy to expand networks.
- **Foundation**: Paved the way for modern Ethernet standards (e.g., 100 Mbps, 1 Gbps, and beyond).

---

### 🔹 **Summary**

10Base-T is **10 Mbps Ethernet over twisted pair**, and its name explicitly reflects its speed. The correct answer is **D: 10Mbit/s**.
