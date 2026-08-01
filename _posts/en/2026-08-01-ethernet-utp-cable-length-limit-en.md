---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ethernet UTP Cable Length Limit
translated: false
type: note
---

### Explanation: **Maximum Length of UTP Cable in Ethernet Networks**

In **Ethernet networking standards** (IEEE 802.3), the **maximum length for a single segment of UTP (Unshielded Twisted Pair) cable** between a **node (e.g., computer, station)** and a **hub/switch** is **100 meters**. This applies to:

- **10BASE-T** (10 Mbps Ethernet)
- **100BASE-TX** (100 Mbps Fast Ethernet)
- **1000BASE-T** (1 Gbps Gigabit Ethernet, though stricter cable quality is required)

---

#### **Why 100 Meters?**
1. **Signal Attenuation**:
   - Electrical signals weaken over distance due to resistance and interference.
   - Beyond 100 meters, the signal may degrade, causing errors or connection failures.

2. **Collision Domain**:
   - In half-duplex Ethernet (e.g., older hub-based networks), the **collision domain** must be limited to ensure CSMA/CD (Carrier Sense Multiple Access with Collision Detection) works properly.
   - The **100-meter limit** ensures that a device can detect collisions before completing the transmission of a frame.

3. **Standard Compliance**:
   - The **IEEE 802.3** standard specifies 100 meters as the maximum for **horizontal cabling** (from the workstation to the telecommunications closet).
   - This includes **90 meters of solid-core cable** (permanent link) + **10 meters of stranded patch cables** (for flexibility at both ends).

---

#### **Key Points**
- **UTP Cable Types**:
  - **Cat 5e** or higher (e.g., Cat 6, Cat 6a) is typically used for 100 Mbps and 1 Gbps Ethernet.
  - Lower-quality cables (e.g., Cat 3) may not support 100 meters at higher speeds.

- **Exceptions**:
  - **Fiber optic cables** can span much longer distances (e.g., 550 meters for multimode, kilometers for single-mode).
  - **Repeaters or switches** can extend the network beyond 100 meters by regenerating the signal.

- **Modern Networks**:
  - Most modern networks use **switches** (not hubs) and **full-duplex communication**, which eliminates collision domains but retains the 100-meter limit for UTP.

---
#### **Summary**
The **100-meter rule** is a **fundamental Ethernet standard** to ensure reliable communication. For your question:
- **Correct Answer: B (100 meters)**. ✅
